from setuptools import setup, find_packages


setup(
    name='smart-resume-job-matcher',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django==5.0.6',
        'openai==1.30.3',
        'djangorestframework==3.15.2',
        'python-dotenv==1.0.1',
        'sphinx==7.3.7'
    ],
    author='Abdullah Mujahid',
    author_email='abdullahmujahidali@gmail.com',
    description='A Django application for parsing resumes and matching job descriptions using OpenAI.',
    url='https://github.com/abdullahmujahidali/ResumeParser-JobMatcher',
    project_urls={
        'Source': 'https://github.com/abdullahmujahidali/ResumeParser-JobMatcher',
        'Documentation': 'https://smart-resume-parser-and-job-matcher.readthedocs.io/en/latest/',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
