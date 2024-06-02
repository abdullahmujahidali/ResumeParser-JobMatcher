from rest_framework import serializers
from user.models import User, Qualification, Experience, Project, Skill, Social


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ["university", "degree", "institute", "grade_type",
                  "grade", "start_year", "end_year", "major"]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ["title", "company", "start_year", "end_year", "description"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "description"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name"]


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ["url"]


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['resume', 'email']

    def create(self, validated_data):
        resume = validated_data.pop('resume', None)
        resume_path = validated_data.pop('resume_path', None)

        user = User.objects.create(
            resume=resume, resume_path=resume_path, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    qualifications = QualificationSerializer(many=True)
    experiences = ExperienceSerializer(many=True)
    projects = ProjectSerializer(many=True)
    skills = SkillSerializer(many=True)
    socials = SocialSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "location",
            "resume",
            "is_active",
            "qualifications",
            "experiences",
            "projects",
            "skills",
            "socials",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
        }
        read_only_fields = ["id"]

    def to_internal_value(self, data):
        if data.get("email"):
            data["email"] = data["email"].lower()
        return super().to_internal_value(data)

    def create(self, validated_data):
        qualifications_data = validated_data.pop('qualifications', [])
        experiences_data = validated_data.pop('experiences', [])
        projects_data = validated_data.pop('projects', [])
        skills_data = validated_data.pop('skills', [])
        socials_data = validated_data.pop('socials', [])

        user = User.objects.create(**validated_data)
        self._create_or_update_related(
            qualifications_data, user, Qualification)
        self._create_or_update_related(experiences_data, user, Experience)
        self._create_or_update_related(projects_data, user, Project)
        self._create_or_update_related(skills_data, user, Skill)
        self._create_or_update_related(socials_data, user, Social)

        return user

    def update(self, instance, validated_data):
        qualifications_data = validated_data.pop('qualifications', [])
        experiences_data = validated_data.pop('experiences', [])
        projects_data = validated_data.pop('projects', [])
        skills_data = validated_data.pop('skills', [])
        socials_data = validated_data.pop('socials', [])

        self._create_or_update_related(
            qualifications_data, instance, Qualification)
        self._create_or_update_related(experiences_data, instance, Experience)
        self._create_or_update_related(projects_data, instance, Project)
        self._create_or_update_related(skills_data, instance, Skill)
        self._create_or_update_related(socials_data, instance, Social)

        return super().update(instance, validated_data)

    def _create_or_update_related(self, related_data, user, model):
        for data in related_data:
            model.objects.update_or_create(user=user, **data)


class AccountCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_account(**validated_data)
