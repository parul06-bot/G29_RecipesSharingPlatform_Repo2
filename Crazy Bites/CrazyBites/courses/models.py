from django.db import models

# Create your models here.

class CourseEnrollment(models.Model):
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    COURSE_CHOICES = [
        ('italian', 'Italian Masterclass'),
        ('asian', 'Asian Fusion'),
        ('baking', 'Baking Basics'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course = models.CharField(max_length=20, choices=COURSE_CHOICES)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    dietary_restrictions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_course_display()}"
    
    class Meta:
        ordering = ['-created_at']
