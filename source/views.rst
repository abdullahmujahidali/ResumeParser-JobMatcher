Views
=====

AIAssistantViewSet
------------------

This viewset includes actions for parsing resumes and matching job descriptions.

Resume Parser
~~~~~~~~~ ~~~

```python
@action(detail=False, methods=["post"], name="Resume Parser", url_path="resume-parser")
def resume_parser(self, request, pk=None):
    ...
```

Job Matcher
~~~~~~~~~~~

```python
@action(detail=False, methods=["post"], name="Matches Candidate with a Job Description", url_path="job-matcher")
def job_matcher(self, request, pk=None):
    ...
