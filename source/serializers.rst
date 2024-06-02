Serializers
===========

QualificationSerializer
------------------------

```python
class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ["university", "degree", "institute", "grade_type",
                  "grade", "start_year", "end_year", "major"]
```

ExperienceSerializer
--------------------

```python
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ["title", "company", "start_year", "end_year", "description"]
```

ProjectSerializer
-----------------

```python
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "description"]
```

SkillSerializer
---------------

```python
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["name"]
```

SocialSerializer
----------------

```python
class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = ["url"]
```

ResumeSerializer
----------------

```python
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['resume', 'email']
```

UserSerializer
--------------

```python
class UserSerializer(serializers.ModelSerializer):
    qualifications = QualificationSerializer(many=True)
    experiences = ExperienceSerializer(many=True)
    projects = ProjectSerializer(many=True)
    skills = SkillSerializer(many=True)
    socials = SocialSerializer(many=True)
    ...
```

AccountCreationSerializer
-------------------------

```python
class AccountCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')
        extra_kwargs = {
            'password': {'write_only': True},
        }
```