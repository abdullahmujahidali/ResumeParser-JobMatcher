# Django OpenAI Resume Parser and Job Matcher

A Django application that integrates with OpenAI to provide two main features:

1. **Resume Parser**: Extracts details from uploaded resume files and saves them to the database.
2. **Job Matcher**: Analyzes a user's resume data against a job description and returns a matching score and a brief description.

## Features

- **Resume Parsing**: Upload a resume in PDF format, and the application extracts and stores relevant details such as qualifications, experience, skills, and social profiles.
- **Job Matching**: Matches the extracted resume data against a job description and returns a percentage score indicating how well the candidate fits the job, along with a brief explanation.

## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:Carte-Blanche-Innovation-Integrated/SmartResumeJobMatcher.git
    cd SmartResumeJobMatcher
    ```

2. Set up a virtual environment:

    ```bash
    python -m venv myenv
    source myenv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables for OpenAI API key and other settings. Create a `.env` file in the project root with the following content:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    OPENAI_PARSER_ASSISTANT_ID=your_parser_assistant_id
    OPENAI_JOB_MATCHER_ASSISTANT_ID=your_job_matcher_assistant_id
    ```

5. Apply migrations and start the server:

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Usage

### Resume Parser

Endpoint: `/assistant/resume-parser/`

Send a POST request to this endpoint with the resume file to parse and store the extracted details.

### Job Matcher

Endpoint: `/assistant/job-matcher/`

Send a POST request to this endpoint to match the user's resume data against a job description and get the matching score and description.


## Views

### AIAssistantViewSet

This viewset includes actions for parsing resumes and matching job descriptions.

#### Resume Parser

```python
@action(detail=False, methods=["post"], name="Resume Parser", url_path="resume-parser")
def resume_parser(self, request, pk=None):
    ...
```

#### Job Matcher

```python
@action(detail=False, methods=["post"], name="Matches Candidate with a Job Description", url_path="job-matcher")
def job_matcher(self, request, pk=None):
    ...
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

---

Feel free to customize this README with more details as necessary for your project.