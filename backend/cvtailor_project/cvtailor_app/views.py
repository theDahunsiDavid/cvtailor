import subprocess
import os
import re
from openai import OpenAI
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
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
            ats_cv_content, match_score, suggestions = generate_ats_format_and_match_score(cv_content, job_description)

            return JsonResponse({
                "ats_cv_content": ats_cv_content,
                "match_score": match_score,
                "suggestions": suggestions
                })

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)

# Helper function to call OpenAI API for ATS format conversion
def generate_ats_format_and_match_score(cv_content, job_description):
    try:
        # Create a prompt for OpenAI
        prompt = (
            f"Convert the following CV content to an ATS-friendly format as possible without removing personal data like name, address, email, contact info, and other identifying details that would normally not be in an ATS-friendly CV. Let there be no omissions or missing parts, meaning do not remove any sections containing personal information or contact information.\n"
            f"Section titles/headings in the CV content are in all-caps. Separate all sections with an empty line only, not with commas or separators. All sections in CV content must be present in the ATS-friendly format, including all responsibilities under each work experience entry. Ensure no sections or responsibilities are missing in the ATS-friendly format.\n"
            f"Do NOT remove a section because its title/heading is a non-standard title. However, where you can, rename the non-standard titles (e.g., PROFILE SUMMARY) for each section to standard, clear section headings like PROFESSIONAL SUMMARY, WORK EXPERIENCE, SKILLS, EDUCATION, etc.\n"
            f"Do not separate sections with '---' or the likes."
            f"Do not end your response with '---' or the likes."
            f"Format each job entry as 'Company Name (Position) [Date Range]' and include a bullet point list of responsibilities under each position.\n"
            f"Format the WORK EXPERIENCE section in reverse-chronological order.\n"
            f"Use simple headings for section titles, and ensure all sections are clearly separated without unnecessary commas or separators.\n"
            f"Format the WORK EXPERIENCE section in reverse-chronological format."
            f"Include a Match Score (out of 100) that indicates how closely the CV matches the job description as exactly 'Match Score: X/100' where X is the Match Score. Include suggestions to improve the Match Score as 'Suggestions to improve Match Score: X'.\n"
            f"Make sure to check your response or the ATS-friendly content for typos and fix the typos.\n"
            f"Double-check that all sections and responsibilities from the original CV are included in your response.\n\n"
            f"CV Content: {cv_content}\n\n"
            f"Job Description: {job_description}\n\n"
)


        # Call OpenAI API to generate ATS content
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Print the raw response for debugging
        # print("OpenAI Response:", response)

        # Extract ATS content from the response
        ats_content = response.choices[0].message.content
        suggestions = extract_suggestions(ats_content)  # Function to extract suggestions from the response

        # Assuming the match score is provided as a number at the end of the content
        match_score_match = re.search(r'Match Score:\s*(\d+)\s*/\s*100', ats_content, re.IGNORECASE)
        if match_score_match:
            match_score = match_score_match.group(1)  # Extract the match score
            ats_content = ats_content[:match_score_match.start()].strip()  # Remove the score from the content
        else:
            match_score = "N/A"  # Fallback if no score is found

        # Apply formatting changes: replace asterisks with simple headings
        ats_content = apply_custom_formatting(ats_content)

        # Apply basic formatting (e.g., replacing newlines with <br> for HTML display)
        formatted_ats_content = ats_content.replace("\n", "<br>")  # Convert newlines to <br> for HTML display

        return formatted_ats_content, match_score, suggestions

    except Exception as e:
        # Handle any potential errors from OpenAI or the prompt
        print(f"Error generating ATS content and match score: {e}")
        return "Error generating ATS content", "N/A"

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

def extract_suggestions(ats_response):
    # Example: Assuming the response contains a section with suggestions
    suggestions_section = re.search(r'Suggestions to improve Match Score:(.*?)(?:\n\n|\Z)', ats_response, re.DOTALL | re.IGNORECASE)
    if suggestions_section:
        suggestions_text = suggestions_section.group(1).strip()
        return suggestions_text.split("\n")  # Split suggestions into a list
    return []

@csrf_exempt  # Add CSRF exemption if needed
def apply_suggestion(request):
    """View to apply a suggestion to the current CV content."""
    if request.method == "POST":
        try:
            # Extract current CV content and the suggestion from the request
            cv_content = request.POST.get("cv_content")
            suggestion = request.POST.get("suggestion")

            # Apply the suggestion to the CV content
            updated_cv_content = apply_suggestion_to_cv(cv_content, suggestion)

            return JsonResponse({"updated_cv_content": updated_cv_content})

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

def apply_suggestion_to_cv(cv_content, suggestion):
    """
    Applies a specific suggestion to the CV content.

    Args:
        cv_content (str): The current CV content.
        suggestion (str): The suggestion to be applied.

    Returns:
        str: The updated CV content after applying the suggestion.
    """
    try:
        # Here, implement the logic to modify the CV based on the suggestion.
        # You might want to use different rules based on the suggestion text.
        # For example, replacing certain phrases, reformatting sections, etc.

        # Placeholder logic for now:
        if "add experience" in suggestion.lower():
            # Example: Adding an experience section suggestion
            cv_content += "<br><br><strong>Additional Experience:</strong> Suggested addition goes here."
        elif "remove redundancy" in suggestion.lower():
            # Example: Removing redundancy as a suggestion
            cv_content = cv_content.replace("redundant phrase", "")

        # Add more conditions based on the type of suggestions you receive
        # ...

        return cv_content

    except Exception as e:
        print(f"Error applying suggestion: {e}")
        return cv_content  # Return unmodified content if there's an error

