import subprocess
import os
import re
from openai import OpenAI
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import JobApplication
from .forms import JobApplicationForm

client = OpenAI(api_key="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")

# Home view for landing page
def home(request):
    return render(request, 'index.html')

# CV upload view
def upload_cv(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save()  # Save the job application to the database
            return process_uploaded_file(request, job_application.id)
    else:
        form = JobApplicationForm()

    return render(request, 'index.html', {'form': form})

# Convert DOCX to HTML using LibreOffice in headless mode
def convert_docx_to_html(docx_file):
    """Converts a DOCX file to HTML using LibreOffice in headless mode."""
    try:
        if not os.path.isfile(docx_file):
            raise FileNotFoundError(f"The file {docx_file} does not exist.")

        output_file = os.path.splitext(docx_file)[0] + '.html'
        command = ['libreoffice', '--headless', '--convert-to', 'html', '--outdir', os.path.dirname(docx_file), docx_file]
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return output_file

    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e.stderr.decode()}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Process the uploaded CV and convert it to HTML
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

# View to convert the CV to ATS format
def convert_to_ats_format(request):
    if request.method == "POST":
        try:
            # Get the CV and job description from the POST request
            cv_content = request.POST.get("cv_content")
            job_description = request.POST.get("job_description")

            # Generate ATS-friendly content using OpenAI
            ats_cv_content = generate_ats_format_and_match_score(cv_content, job_description)

            return JsonResponse({ "ats_cv_content": ats_cv_content})

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)

# Helper function to call OpenAI API for ATS format conversion
def generate_ats_format_and_match_score(cv_content, job_description):
    try:
        # Create a prompt for OpenAI
        prompt = (
            f"Convert the following CV content to an ATS-friendly format."
            f"Please format each job entry as 'Company Name (Position) [Date Range]'. "
            f"Rename the non-standard titles (e.g., PROFILE SUMMARY) for each sections to standard, clear section headings like PROFESSIONAL SUMMARY, WORK EXPERIENCE, SKILLS, EDUCATION, etcetera."
            f"Rearrange the sections in order of priority for ATS systems."
            f"Format the section titles as simple headings."
            f"Format the WORK EXPERIENCE section in reverse-chronological format."
            f"Avoid unnecessary commas and ensure each section is clearly separated.\n\n"
            f"CV Content: {cv_content}\n\n"
            f"Job Description: {job_description}\n\n"
            f"Additionally, provide a match score (out of 100) that indicates how closely the CV matches the job description."
        )

        # Call OpenAI API to generate ATS content
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract ATS content from the response
        ats_content = response.choices[0].message.content

        # Apply formatting changes: replace asterisks with simple headings
        ats_content = apply_custom_formatting(ats_content)

        # Apply basic formatting (e.g., replacing newlines with <br> for HTML display)
        formatted_ats_content = ats_content.replace("\n", "<br>")  # Convert newlines to <br> for HTML display

        return formatted_ats_content

    except Exception as e:
        # Handle any potential errors from OpenAI or the prompt
        print(f"Error generating ATS content and match score: {e}")
        return "Error generating ATS content"

def apply_custom_formatting(content):
    """
    Format the content to remove asterisks, convert them to headings,
    and replace bullet points with dashes.
    """

    # Convert lines like **PROFILE SUMMARY** into PROFILE SUMMARY
    content = re.sub(r'\*\*(.*?)\*\*', r'\n\1\n', content)

    # Replace bullet points (asterisks or other symbols) with dashes
    content = content.replace('•', '-').replace('*', '-')

    # Remove empty line at the top of the text, if it exists
    content = re.sub(r'^\s*\n', '', content)

    # Optionally, remove excess newlines
    content = re.sub(r'\n\s*\n', '\n\n', content)  # Removes extra newlines but keeps paragraph spacing

    return content
