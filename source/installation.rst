Installation Guide
===================

Follow these steps to install and set up the Smart Resume Parser and Job Matcher application:

1. Clone the repository:

    .. code-block:: bash

        git clone git@github.com:abdullahmujahidali/ResumeParser-JobMatcher.git
        cd SmartResumeJobMatcher

2. Set up a virtual environment:

    .. code-block:: bash

        python -m venv myenv
        source myenv/bin/activate

3. Install dependencies:

    .. code-block:: bash

        pip install -r requirements.txt

4. Set up environment variables:

    Create a `.env` file in the project root with the following content:

    .. code-block:: env

        OPENAI_API_KEY=your_openai_api_key
        OPENAI_PARSER_ASSISTANT_ID=your_parser_assistant_id
        OPENAI_JOB_MATCHER_ASSISTANT_ID=your_job_matcher_assistant_id

5. Apply migrations and start the server:

    .. code-block:: bash

        python manage.py migrate
        python manage.py runserver
