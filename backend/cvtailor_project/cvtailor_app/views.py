from django.shortcuts import render, HttpResponse, redirect
from .forms import JobApplicationForm

# Create your views here.
def home(request):
    return render(request, 'index.html')

def upload_cv(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the job application to the database
            return HttpResponse("CV uploaded and job description saved successfully!")
    
    # If GET or form is invalid, render the form again
    else:
        form = JobApplicationForm()

    return render(request, 'index.html', {'form': form})


