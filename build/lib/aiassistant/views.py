from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from rest_framework.permissions import AllowAny
import time
import openai
import json
import os

from rest_framework import serializers
from .utils import bulk_create_objects
from user.models import User, Experience, Qualification, Skill, Social

# Initialize OpenAI client
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


class JobMatcherSerializer(serializers.Serializer):
    resume_data = serializers.DictField()
    job_description = serializers.CharField()


class AIAssistantViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create_file(self, file_path):
        return client.files.create(file=open(file_path, "rb"), purpose='assistants')

    def create_thread(self, file):
        return client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Extract the resume details from the file according to the instructions.",
                    "attachments": [{"file_id": file.id, "tools": [{"type": "file_search"}]}]
                }
            ]
        )

    def create_run(self, thread_id, assistant_id):
        return client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    def retrieve_run(self, thread_id, run_id):
        return client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    def retrieve_messages(self, thread_id):
        return client.beta.threads.messages.list(thread_id=thread_id)

    def process_resume_data(self, parsed_data):
        user = User.objects.create(
            first_name=parsed_data.get('first_name', ''),

            last_name=parsed_data.get('last_name', ''),
            email=parsed_data.get('email', ''),
            phone_number=parsed_data.get('phone_number', ''),
            location=parsed_data.get('location', ''),
            raw_response=parsed_data
        )

        bulk_create_objects(Qualification, parsed_data.get(
            'qualifications', []), user)
        bulk_create_objects(
            Experience, parsed_data.get('experience', []), user)
        bulk_create_objects(Skill, parsed_data.get('skills', []), user)
        bulk_create_objects(Social, parsed_data.get('socials', []), user)

        return user

    def handle_run_status(self, run, thread_id, user=None):
        while True:
            run = self.retrieve_run(thread_id, run.id)
            if run.status in ("queued", "in_progress", "requires_action"):
                time.sleep(1)
            elif run.status == "failed":
                return Response({"error": f"Run failed. Last error was: {run.last_error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            elif run.status == "completed":
                messages = self.retrieve_messages(thread_id)
                assistant_message = messages.data[0].content[0].text.value
                parsed_data = json.loads(assistant_message)
                if user:
                    return Response({"message": "Job match evaluation completed", "user_id": user.id, "content": parsed_data}, status=status.HTTP_201_CREATED)
                return parsed_data

    @action(detail=False, methods=["post"], name="Resume Parser", url_path="resume-parser")
    def resume_parser(self, request, pk=None):
        resume_file = request.FILES.get('file')
        if not resume_file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_name = default_storage.save(
            f'resumes/{resume_file.name}', ContentFile(resume_file.read()))
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        try:
            file = self.create_file(file_path)
            thread = self.create_thread(file)
            run = self.create_run(
                thread.id, settings.OPENAI_PARSER_ASSISTANT_ID)

            parsed_data = self.handle_run_status(run, thread.id)
            user = self.process_resume_data(parsed_data)

            return Response({"message": "Resume parsed and saved successfully", "user_id": user.id, "content": parsed_data}, status=status.HTTP_201_CREATED)

        except openai.APIConnectionError as e:
            return Response({"error": f"Server connection error: {e.__cause__}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["post"], name="Matches Candidate with a Job Description", url_path="job-matcher")
    def job_matcher(self, request, pk=None):
        serializer = JobMatcherSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        resume_data = serializer.validated_data['resume_data']
        job_description = serializer.validated_data['job_description']

        try:
            thread = client.beta.threads.create(
                messages=[
                    {"role": "user",
                        "content": "Analyze the provided job description and resume data to determine if the candidate is a good fit for the job. Provide a score (percentage) and a brief description explaining the match."},
                    {"role": "assistant", "content": "You are an assistant designed to evaluate job applicants based on their skills and experiences against specific job descriptions. Use the provided job description and resume data to make your assessment."},
                    {"role": "user", "content": f"Job Description: {job_description}"},
                    {"role": "user", "content": f"Resume Data: {resume_data}"}
                ]
            )
            run = self.create_run(
                thread.id, settings.OPENAI_JOB_MATCHER_ASSISTANT_ID)
            response_data = self.handle_run_status(run, thread.id)

            # Check if the response_data is a dictionary
            if isinstance(response_data, dict):
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                # If it's not a dictionary, create a dictionary response
                return Response({"message": "Job match evaluation completed", "content": response_data}, status=status.HTTP_201_CREATED)

        except openai.APIConnectionError as e:
            return Response({"error": f"Server connection error: {e.__cause__}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
