from django import forms
from .models import Document, BookingModel


class UserForm(forms.Form):
    username = forms.CharField(label='User name', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    
class RegisterForm(forms.Form):
    username = forms.CharField(label='User name', max_length=100)
    email_address = forms.CharField(label='Email address', max_length=100)
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        
        fields = ('description', 'document', )
        

class ForgotForm(forms.Form):
    username = forms.CharField(label='Enter your email address or user name: ', max_length=100)
    
SESSION_CHOICES = (
    ('1', "1hr Session"),
    ('2', '2hr Session'),
    ('3', '3hr Session'),
    ('4', '4hr Session')
)

class BookingForm(forms.ModelForm):
    class Meta:
        model = BookingModel
        fields = ['session_length', 'email_address', 'phone_number', 'date_time']