from django.shortcuts import get_object_or_404
from user.models import Experience, Qualification, Skill, Social, User
from rest_framework import viewsets, status
from rest_framework.response import Response
import time
import openai
import os
from openai import OpenAI
from django.conf import settings
import json
from .utils import bulk_create_objects
from .constants import job_descriptions

from rest_framework.decorators import action


client = OpenAI()
client.api_key = settings.OPENAI_API_KEY
parser_assistant_id = settings.OPENAI_PARSER_ASSISTANT_ID
job_matcher_assistant_id = settings.OPENAI_JOB_MATCHER_ASSISTANT_ID


class AIAssistantViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    @action(
        detail=False, methods=["post"],
        name="Resume Parser", url_path="resume-parser"
    )
    def resumeParser(self, request, pk=None):
        file_path = os.path.join(os.path.dirname(__file__), "Abubakar.pdf")

        try:
            file = client.files.create(
                file=open(file_path, "rb"),
                purpose='assistants'
            )
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Extract the resume details from the file according to the instructions.",
                        "attachments": [
                            {
                                "file_id": file.id,
                                "tools": [{"type": "file_search"}]
                            }
                        ]
                    }
                ]
            )

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=parser_assistant_id,
            )
            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                if run.status in ("queued", "in_progress", "requires_action"):
                    time.sleep(1)
                elif run.status == "failed":
                    return Response({"error": f"Run failed. Last error was: {run.last_error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                elif run.status == "completed":
                    messages = client.beta.threads.messages.list(
                        thread_id=thread.id
                    )

                    assistant_message = messages.data[0].content[0].text.value
                    parsed_data = json.loads(assistant_message)

                    user = User.objects.create(
                        first_name=parsed_data.get('first_name', ''),
                        last_name=parsed_data.get('last_name', ''),
                        email=parsed_data.get('email', ''),
                        phone_number=parsed_data.get('phone_number', ''),
                        location=parsed_data.get('location', ''),
                        raw_response=parsed_data
                    )

                    bulk_create_objects(
                        Qualification, parsed_data.get('qualifications', []), user)
                    bulk_create_objects(
                        Experience, parsed_data.get('experience', []), user)
                    bulk_create_objects(
                        Skill, parsed_data.get('skills', []), user)
                    bulk_create_objects(
                        Social, parsed_data.get('socials', []), user)

                    return Response({"message": "Resume parsed and saved successfully", "user_id": user.id, "content": parsed_data}, status=status.HTTP_201_CREATED)

        except openai.APIConnectionError as e:
            return Response({"error": f"Server connection error: {e.__cause__}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(
        detail=False, methods=["post"],
        name="Matches Candidate with a Job Description", url_path="job-matcher"
    )
    def job_matcher(self, request, pk=None):
        user = get_object_or_404(User, email="abubakarmujahid@live.com")

        try:
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Analyze the provided job description and resume data to determine if the candidate is a good fit for the job. Provide a score (percentage) and a brief description explaining the match."
                    },
                    {
                        "role": "assistant",
                        "content": f"You are an assistant designed to evaluate job applicants based on their skills and experiences against specific job descriptions. Use the provided job description and resume data to make your assessment."
                    },
                    {
                        "role": "user",
                        "content": f"Job Description: {job_descriptions[3]}"
                    },
                    {
                        "role": "user",
                        "content": f"Resume Data: {user.raw_response}"
                    }
                ],
            )

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=job_matcher_assistant_id,
            )
            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                if run.status in ("queued", "in_progress", "requires_action"):
                    time.sleep(1)
                elif run.status == "failed":
                    return Response({"error": f"Run failed. Last error was: {run.last_error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                elif run.status == "completed":
                    messages = client.beta.threads.messages.list(
                        thread_id=thread.id
                    )

                    assistant_message = messages.data[0].content[0].text.value
                    parsed_data = json.loads(assistant_message)
                    return Response({"message": "Resume parsed and saved successfully", "user_id": user.id, "content": parsed_data}, status=status.HTTP_201_CREATED)

        except openai.APIConnectionError as e:
            return Response({"error": f"Server connection error: {e.__cause__}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
