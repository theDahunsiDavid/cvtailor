import subprocess
import os
from openai import OpenAI

client = OpenAI(api_key="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")
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from .models import JobApplication
from .forms import JobApplicationForm

# Create your views here.
def home(request):
    return render(request, 'index.html')

def upload_cv(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save()  # Save the job application to the database
            return process_uploaded_file(request, job_application.id)

    # If GET or form is invalid, render the form again
    else:
        form = JobApplicationForm()

    return render(request, 'index.html', {'form': form})

def convert_docx_to_html(docx_file):
    """Converts a DOCX file to HTML using LibreOffice in headless mode."""
    try:
        # Ensure the file exists
        if not os.path.isfile(docx_file):
            raise FileNotFoundError(f"The file {docx_file} does not exist.")

        # Define the output file path in the same directory as the input file
        output_file = os.path.splitext(docx_file)[0] + '.html'

        # Define the command
        command = ['libreoffice', '--headless', '--convert-to', 'html', '--outdir', os.path.dirname(docx_file), docx_file]

        # Run the command and capture the output
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Define the output file path
        return output_file

    except subprocess.CalledProcessError as e:
        # Capture and print error messages from the command
        print(f"Error during conversion: {e.stderr.decode()}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def process_uploaded_file(request, file_id):
    """Processes the uploaded CV and converts to HTML."""
    job_application = JobApplication.objects.get(id=file_id)
    file_path = job_application.uploaded_file.path
    job_description = job_application.job_description # Retrieve job description from model

    try:
        html_file = convert_docx_to_html(file_path)
        if html_file is None or not os.path.isfile(html_file):
            # Handle the case where conversion failed
            return HttpResponse("Error converting the document.", status=500)

        # Read the content of the HTML file
        with open(html_file, 'r') as f:
            html_content = f.read()

        sections = {"CV Content": html_content}

        # Render the HTML content in your preview page
        return render(request, 'preview.html', {
            'sections': sections,
            'job_description': job_description
        })

    except FileNotFoundError as e:
        return HttpResponse(f"File not found: {e}", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

def convert_to_ats_format(request):
    """
    Convert CV content to ATS format using OpenAI API.
    """
    if request.method == "POST":
        # Get the CV content from the request
        cv_content = request.POST.get("cv_content")
        job_description = request.POST.get("job_description")

        # Call OpenAI to process the CV content for ATS format
        ats_cv_content = generate_ats_format(cv_content, job_description)

        return JsonResponse({'ats_cv_content': ats_cv_content})

def generate_ats_format(cv_content, job_description):
    """
    Call OpenAI API to convert CV content to ATS-friendly format.
    """
    # Your OpenAI API key should be set in your environment variables

    # Create a prompt for OpenAI
    prompt = f"Convert the following CV content to an ATS-friendly format:\n\nCV Content: {cv_content}\n\nJob Description: {job_description}"

    # Call OpenAI's API
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ])

    # Extract the ATS content from the response
    ats_content = response.choices[0].message.content

    return ats_content
