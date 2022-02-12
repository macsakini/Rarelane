from django.db import models

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    
    document = models.FileField(upload_to='documents/')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
SESSION_CHOICES = (
    ('1', "1hr Session"),
    ('2', '2hr Session'),
    ('3', '3hr Session'),
    ('4', '4hr Session')
)

class BookingModel(models.Model):
    session_length = models.CharField(choices = SESSION_CHOICES, max_length=255, blank=True)
    email_address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=255, blank=True)
    date_time = models.DateTimeField(max_length=255, blank=True)