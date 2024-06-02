from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='smart-resume-job-matcher',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    author='Abdullah Mujahid',
    author_email='abdullahmujahidali@gmail.com',
    description='A Django application for parsing resumes and matching job descriptions using OpenAI.',
    url='https://github.com/abdullahmujahidali/ResumeParser-JobMatcher',
    project_urls={
        'Source': 'https://github.com/abdullahmujahidali/ResumeParser-JobMatcher',
        'Documentation': 'https://your-docs-url.com',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
