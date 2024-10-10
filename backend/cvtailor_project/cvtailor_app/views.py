import subprocess
import os
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
        return render(request, 'preview.html', {'sections': sections})
    
    except FileNotFoundError as e:
        return HttpResponse(f"File not found: {e}", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)
