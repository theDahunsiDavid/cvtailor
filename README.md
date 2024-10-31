# CV Tailor

CV Tailor is a web application designed to help users create and customize their CVs. This guide will walk you through the installation and usage of the application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
4. [File Structure](#file-structure)
5. [Contributing](#contributing)
6. [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Django 3.x or above
- pip (Python package installer)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/cvtailor.git
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
