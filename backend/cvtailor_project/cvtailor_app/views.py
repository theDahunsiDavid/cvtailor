import os
import docx
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

def process_uploaded_file(request, file_id):
    """Processes the uploaded CV & extracts sections."""
    job_application = JobApplication.objects.get(id=file_id)
    file_path = job_application.uploaded_file.path

    text = ""
    if job_application.uploaded_file.name.endswith('.docx'):
        doc = docx.Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    elif job_application.uploaded_file.name.endswith('.pdf'):
        pass

    sections = extract_sections(text)

    return render(request, 'preview.html', {'sections': sections})

def extract_sections(text):
    """Extracts sectopms from the CV text."""
    sections = {}
    current_section = 'Summary'
    for line in text.split('\n'):
        if line.strip():
            if line.isupper():
                current_section = line.strip()
                sections[current_section] = []
            else:
                sections[current_section].append(line.strip())

    for section in sections:
        sections[section] = '.<br>'.join(sections[section])

    return sections
