from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
import uuid
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings
import os
from django.contrib import messages
from .models import CourseEnrollment

# Create your views here.

@login_required
def italian_videos(request):
    context = {
        'course_name': 'Italian Masterclass',
        'videos': [
            {
                'title': 'Session 1: Perfect Pasta Dough',
                'url': 'https://www.youtube.com/embed/SeF8OOAsj-A',
                'description': 'Learn the secrets to making authentic Italian pasta dough from scratch.'
            },
            {
                'title': 'Session 2: Classic Tomato Sauce',
                'url': 'https://www.youtube.com/embed/b3RoeV-FQmA',
                'description': 'Master the art of a simple yet flavorful Italian tomato sauce.'
            },
            {
                'title': 'Session 3: Shaping Pasta',
                'url': 'https://www.youtube.com/embed/JcFb51qMpDA',
                'description': 'Explore different pasta shapes and how to create them by hand.'
            },
            {
                'title': 'Session 4: Pizza Perfection',
                'url': 'https://www.youtube.com/embed/NLHT3561roA',
                'description': 'Techniques for creating the perfect pizza crust and toppings.'
            }
        ]
    }
    return render(request, 'courses/italian_videos.html', context)

@login_required
def baking_videos(request):
    return render(request, 'courses/baking_videos.html')

@login_required
def asian_videos(request):
    return render(request, 'courses/asian_videos.html')

@login_required
def generate_certificate(request):
    course_name = request.GET.get('course', 'Online Cooking Course') 
    if request.method == 'POST':
        user_name = request.POST.get('user_name', request.user.get_full_name() or request.user.username)
        certificate_id = uuid.uuid4()
        instructor_name = "Chef CrazyBites"
        completion_date_obj = date.today()

        context = {
            'user_name': user_name,
            'course_name': course_name,
            'completion_date': completion_date_obj,
            'certificate_id': certificate_id, 
            'instructor_name': instructor_name, 
        }
        return render(request, 'courses/certificate_display.html', context)
    
    # If GET request, show the form
    return render(request, 'courses/certificate_form.html', {'course_name': course_name})

@login_required
def download_certificate(request):
    # Get the certificate data
    course_name = request.GET.get('course', 'Online Cooking Course')
    user_name = request.user.get_full_name() or request.user.username
    certificate_id = uuid.uuid4()
    instructor_name = "Chef CrazyBites"
    completion_date = date.today()
    
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    
    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=1  # Center alignment
    )
    
    # Add content
    elements.append(Paragraph("Certificate of Completion", title_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("This certifies that", normal_style))
    elements.append(Paragraph(user_name, ParagraphStyle(
        'NameStyle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=12,
        alignment=1
    )))
    elements.append(Paragraph(f"has successfully completed the<br/><b>{course_name}</b><br/>provided by Crazy Bites", normal_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Date: {completion_date.strftime('%B %d, %Y')}", normal_style))
    elements.append(Paragraph(f"Instructor: {instructor_name}", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(f"Certificate ID: {certificate_id}", normal_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create the HTTP response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{certificate_id}.pdf"'
    
    return response

@login_required
def enroll_view(request):
    """View to display the enrollment form"""
    return render(request, 'courses/enroll.html')

@login_required
def process_enrollment(request):
    """View to process the enrollment form submission"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            course = request.POST.get('course')
            experience = request.POST.get('experience')
            dietary = request.POST.get('dietary', '')
            
            # Create enrollment record
            enrollment = CourseEnrollment.objects.create(
                name=name,
                email=email,
                phone=phone,
                course=course,
                experience=experience,
                dietary_restrictions=dietary
            )
            
            messages.success(request, 'Enrollment successful! You can now access the course videos.')
            
            # Redirect to the appropriate video page based on the course
            if course == 'italian':
                return redirect('courses:italian_videos')
            elif course == 'baking':
                return redirect('courses:baking_videos')
            elif course == 'asian':
                return redirect('courses:asian_videos')
            
        except Exception as e:
            messages.error(request, f'Error processing enrollment: {str(e)}')
            return redirect('courses:enroll')
    
    return redirect('courses:enroll')
