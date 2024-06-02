Usage Instructions
=================

Resume Parser
-------------

Endpoint: `/assistant/resume-parser/`

Send a POST request to this endpoint with the resume file to parse and store the extracted details.

Input Data:
    - `resume` (FileField)

Output:

```json
{
    "message": "Resume parsed and saved successfully",
    "user_id": "e6cf8c90-6685-4843-8ea2-97ab728ec5e6",
    "content": {
        "first_name": "Abdullah",
        "last_name": "Mujahid",
        "email": "myemail@gmail.com",
        "phone_number": "+92322xxxxxx",
        "location": "Lahore, Pakistan",
        "socials": ["Linkedin", "Github", "Google Scholar", "Portfolio"],
        "qualifications": [
            {
                "university": "University of Management & Technology",
                "degree": "Bachelor",
                "institute": "Lahore Pakistan",
                "grade_type": "4.0",
                "grade": 3.57,
                "start": "August 2017",
                "end": "May 2021",
                "major": "Computer Science"
            }
        ],
        "experience": [...],
        "skills": [...],
        "projects": [...]
    }
}
```

Job Matcher
-----------

Endpoint: `/assistant/job-matcher/`

Send a POST request to this endpoint to match the user's resume data against a job description and get the matching score and description.

Input Data:

```json
{
    "resume_data": { ... },
    "job_description": "Job brief ..."
}
```

Output:

```json
{
    "score": 90,
    "description": "Abdullah Mujahid is an excellent fit for the Web Developer position based on the provided job description. His experience as a Senior Full Stack Software Engineer and Development Lead aligns well with the responsibilities of building websites from concept to completion. Abdullah's proficiency in Django, React.js, and Agile methodologies, as well as his strong background in HTML/CSS and familiarity with JavaScript, reinforces his coding and design capabilities. His involvement in web development projects like 'Gladiator Finance - NFT Marketplace' and 'BigBrains - E-learning Platform' highlights his ability to integrate data from back-end services and develop robust web applications. Additionally, his solid understanding of programming languages, network diagnostics, and SEO further supports his suitability for the role."
}
```
