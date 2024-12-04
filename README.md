# CV Tailor

CV Tailor is a web application built to help job applicants tailor their resumes to various job descriptions with ease.

This guide will walk you through the installation and usage of the application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
4. [File Structure](#file-structure)
5. [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Django 3.x or above
- pip (Python package installer)
- A PostgreSQL database
- An OpenAI API key

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/dahunsi-dami/cvtailor.git
    cd cvtailor
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser (optional, for admin access):

    ```bash
    python manage.py createsuperuser
    ```

6. Run the server:

    ```bash
    python manage.py runserver
    ```

7. Access the application in your browser at `http://127.0.0.1:8000/`.

## Usage

- Upload Your CV and the Job Description: Once you access the application, you'll be directed to the home page where you can attach your CV and paste the job description. Then click on, "Tailor My CV."

- Tailor Your CV: Your CV and the job description will be loaded on the preview page. Click the button below the sidebar once and wait for the tailored text.

- Implement suggestions: A match score will rate how well your resume matches the job description. You will also receive suggestions on how to improve the match score. Suggestions will soon be auto-implementable with a click.

## File Structure

```plaintext
cvtailor/
├── cvtailor_app/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── ... (your HTML templates)
├── cvtailor_project/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── static/
    └── ... (your static files like CSS, JS)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```typescript
Feel free to reach out to me at `gbemigadare@gmail.com`! Let me know if you need any changes.
```
