from django import forms
from django.forms import ModelForm
from . models import Message, GetTutor, Tutor
from django.contrib.auth import authenticate
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class GetTutorForm(ModelForm):
    class Meta:
        model = GetTutor
        fields = ('syllabus', 'grade', 'subject', 'first_name', 'last_name','email',  'mobile', 'relationship', 'street_address','suburb','town', 'province', 'lesson_mode', 'start', 'additional_details',)
        widgets = {
            'syllabus':forms.Select(attrs={'class':'form-control'}),
            'grade': forms.Select(attrs={'class':'form-control'}),
            'subject': forms.Select(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'mobile': forms.TextInput(attrs={'class':'form-control'}),
            'relationship': forms.Select(attrs={'class':'form-control'}),
            'street_address': forms.TextInput(attrs={'class':'form-control'}),
            'suburb': forms.TextInput(attrs={'class':'form-control'}),
            'town': forms.TextInput(attrs={'class':'form-control'}),
            'province': forms.Select(attrs={'class':'form-control'}),
            'lesson_mode': forms.Select(attrs={'class':'form-control'}),
            'start': forms.Select(attrs={'class':'form-control'}),
            'additional_details': forms.Textarea(attrs={'class':'form-control'}),
            
        }
        labels = {
            'grade': 'Grade',
            'subject': 'Subject',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email address',
            'mobile': 'Contact Number',
            'relationship': ' Relationship to learner',
            'lesson_mode': 'Lesson Mode',
            'start': 'When would you like to start?',
            'additional_details': 'Any additional details?',
            'tutor_application': 'Why would you be perfect for this job?'
        }

class MessageForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Message
        fields = "__all__"
        widgets = {
            'fullname': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'contactnumber': forms.TextInput(attrs={'class':'form-control'}),
            'message': forms.Textarea(attrs={'class':'form-control'}),
            'captcha': ReCaptchaV2Checkbox(attrs={'class':'form-control'})
        }
        labels = {
            'fullname': 'Full Name',
            'email':'Email address',
            'contactnumber': 'Contact Number',
            'message': 'Your message'
        }

class BecomeTutorForm(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Tutor
        fields = ('first_name','last_name', 'email', 'gender', 'age', 'sa_citizen', 'id_no', 
                  'mobile_number', 'subject_tutored','can_tutor_online','street_address',
                  'suburb','town','province', 'undergrad_finished', 'highest_qualification', 'bio','profile_pic', 'password',)
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email':'Email Address',
            'gender':'Gender',
            'age': 'Age',
            'sa_citizen':'Are you a South African citizen?',
            'id_no': 'Identity Number',
            'mobile_number':'Contact Number',
            'subject_tutored': 'Subject Tutored',
            'can_tutor_online': 'Can you tutor online?',
            'street_address': 'Street Address',
            'suburb':'Suburb',
            'town':'City/Town',
            'province': 'Province',
            'undergrad_finished': 'Are you still an undergraduate student?',
            'highest_qualification': 'What is your highest qualification?',
            'bio': 'Biography',
            'profile_pic': 'Profile Picture',
            
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),
            'age': forms.TextInput(attrs={'class':'form-control'}),
            'sa_citizen': forms.Select(attrs={'class':'form-control'}),
            'id_no':forms.TextInput(attrs={'class':'form-control'}),
            'mobile_number':forms.TextInput(attrs={'class':'form-control'}),
            'subject_tutored': forms.TextInput(attrs={'class':'form-control'}),
            'can_tutor_online': forms.Select(attrs={'class':'form-control'}),
            'street_address': forms.TextInput(attrs={'class':'form-control'}),
            'suburb': forms.TextInput(attrs={'class':'form-control'}),
            'town': forms.TextInput(attrs={'class':'form-control'}),
            'bio': forms.Textarea(attrs={'class':'form-control'}), 
            'province':forms.Select(attrs={'class':'form-control'}),   
            'undergrad_finished':forms.Select(attrs={'class':'form-control'}),     
            'highest_qualification': forms.TextInput(attrs={'class':'form-control'}),  
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'captcha': ReCaptchaV2Checkbox(attrs={'class':'form-control'})
        }

class TutorUpdateForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['first_name','last_name', 'mobile_number', 'subject_tutored', 'street_address','suburb','town','bio', 'profile_pic']


class LoginForm(ModelForm):
    class Meta:
        model = Tutor
        fields = ('email', 'password',)
        labels = { 
            'email': 'Email address',
            'password':'Password'
        }
        widgets = {        
        'email':forms.EmailInput(attrs={'class':'form-control'}),
        'password': forms.PasswordInput(attrs={'class':'form-control'}),
        }
        
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password = password):
                raise forms.ValidationError("Invalid Credentials")
