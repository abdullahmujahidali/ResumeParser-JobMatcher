Usage
=====

To use Smart Resume Parser and Job Matcher, follow these steps:

1. **Resume Parser**:

   - Endpoint: `/assistant/resume-parser/`
   - Send a POST request to this endpoint with the resume file to parse and store the extracted details.
   - Input Data: `resume` (FileField)
   - Output: JSON response containing the parsed resume details.

   Example Input Data:

   ::

      {
          "resume": "<resume_file>"
      }

2. **Job Matcher**:

   - Endpoint: `/assistant/job-matcher/`
   - Send a POST request to this endpoint to match the user's resume data against a job description and get the matching score and description.
   - Input Data: JSON object containing `resume_data` and `job_description`.
   - Output: JSON response containing the matching score and description.

   Example Input Data:

   ::

      {
          "resume_data": {
              "first_name": "Abdullah",
              "last_name": "Mujahid",
              "email": "abdullahmujahidali1@gmail.com",
              ...
          },
          "job_description": "Job brief ..."
      }
