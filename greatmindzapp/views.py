from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm, GetTutorForm, BecomeTutorForm, LoginForm, TutorUpdateForm
from . models import Tutor, GetTutor, Blog, JobStatus, Review
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def home(request):
    maths_tutors = Tutor.objects.filter(subject_tutored = "Mathematics")
    return render(request, "home.html", {'maths_tutors':maths_tutors})

def becomeatutor(request):
    return render(request, "becomeatutor.html")

class BlogListView(ListView):
    model = Blog   
    template_name = "blog.html"

class BlogDetailView(DetailView):
    model = Blog   
    template_name = "viewblogpost.html"

def post_single(request, blog):  
    blog = get_object_or_404(Blog, slug=blog) 
    return render(request, "viewblogpost.html", {'blog':blog})

def contact(request):
    submitted = False
    if request.method == 'POST':
      form = MessageForm(request.POST)
      if form.is_valid:         
          form.save()
          name = form.cleaned_data['fullname']
          email = form.cleaned_data['email']
          contactnumber = form.cleaned_data['contactnumber']
          message = form.cleaned_data['message']
                 
          return HttpResponseRedirect('/contact?submitted=True')
      else:
          messages.error(request, f'Na na na')
          return redirect('contact')

    else:
        form = MessageForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, "contact.html", {'form':form, 'submitted':submitted})

def about(request):
    return render(request, "about.html")

def getatutor(request):
    submitted = False
    if request.method == 'POST':
        form = GetTutorForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, f'We will get back to you homie')
            return redirect('getatutor')
        else:
            messages.error(request)    
    else:
        form = GetTutorForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, "getatutor.html", {'form':form, 'submitted':submitted})

#def activate(request, uidb64, to_email):
 #   return redirect('home')


#def activateEmail(request, user, to_email):
    #mail_subject = "Activate your user account."
   # message = render_to_string("template_activate_account.html", {
      # 'user': user.username,
      # 'domain': get_current_site(request).domain,
      # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
      # 'token': account_activation_token.make_token(user),
      # 'protocol': 'https' if request.is_secure() else 'http'
  #  })
  #  email = EmailMessage(mail_subject, message, to = [to_email])
  #  if email.send():
      #  messages.success(request, f'Dear {user}, please go to your email inbox and click on \
                    # received activation link to confirm and complete registration' )
   # else:
       # messages.error(request, f'Problem sending email to your email. Check if typed correctly')


def tutorapplication(request):
    context = {}
    if request.method == 'POST':
        form = BecomeTutorForm(request.POST, request.FILES)
        if form.is_valid():
             form.save()           
             return redirect('home')
        context['tutor_form'] = form
    else:
        form = BecomeTutorForm()
        context['tutor_form'] = form

    return render(request, "tutorapplication.html", context)

def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')   
        else:
            context['login_form'] = form        
        
    else:
        form = LoginForm()
        context['login_form'] = form
    return render(request, "login.html", context)

def alltutors(request):
    tutors = Tutor.objects.filter(is_approved=True).filter(is_active=True)   
    online_tutors = Tutor.objects.filter(can_tutor_online='1')
    return render(request, "alltutors.html", {'tutors': tutors, 'online_tutors':online_tutors})


def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):      
    validcolor = JobStatus.objects.first()
    validjobs = validcolor.gettutor_set.all()

    number_of_jobs = validjobs.count()  
    
    return render(request, "tutordashboard.html", {'valid_jobs':validjobs, 'number_of_jobs':number_of_jobs})

def available_jobs(request):
    validcolor = JobStatus.objects.first()
    validjobs = validcolor.gettutor_set.all()
    number_of_jobs = validjobs.count()   

    return render(request, "availablejobs.html", {'valid_jobs':validjobs, 'number_of_jobs':number_of_jobs})

def myjobs(request):       
        tutor_name = Tutor.objects.filter(request.user == request.user)
        tutor_jobs = tutor_name.gettutor_set.all()
        return render(request, "myjobs.html", {'tutor_jobs':tutor_jobs})

def terms(request):      
    return render(request, "terms.html")

def client_terms(request):      
    return render(request, "client_terms.html")

def tutor_terms(request):      
    return render(request, "tutor_terms.html")

def privacy(request):      
    return render(request, "privacy_policy.html")

def apply_job(request, pk):
    applications = []
    if request.method == 'POST':
        job = GetTutor.objects.get(id = pk)
        form = GetTutorForm(request.POST, instance = job)   
        if form.is_valid():
            instance = form.save(commit=False)
            instance.applicant = request.user
            instance.save()
            number = applications.append(instance)
            
            return render(request, 'apply_job.html', {'applications':number})
    else:
        job = GetTutor.objects.get(id = pk) 
        form = GetTutorForm(instance = job)       
        return render(request, "apply_job.html", {'job':job, 'form':form})
##################
# Start of profile
##################

def update_profile(request):
    if request.method == 'POST':      
      form = TutorUpdateForm(request.POST, request.FILES, instance = request.user)
      if form.is_valid():
          form.save()
          messages.success(request, f'Your profile has been updated successfully')
          return redirect('dashboard')
    else:        
        form = TutorUpdateForm(instance = request.user)
    return render(request, "update_profile.html", {'form':form})

def view_profile(request, id):
    reviews = Review.objects.all()
    tutor = Tutor.objects.get(pk = id)
    return render(request, "view_profile.html", {'tutor':tutor, 'reviews':reviews})

################
# End of profile
###############

def current_applications(request):    
    applications = GetTutor.objects.filter(applicant = request.user)  
    return render(request, "current_applications.html", {'applications':applications})

######################################
# Start of filtering tutors by subject
######################################

def maths_tutors(request):
    maths_tutors = Tutor.objects.filter(subject_tutored = "Mathematics")
    return render(request, "subject_filtering/maths_tutors.html", {'maths_tutors':maths_tutors})

def life_sciences_tutors(request):
    life_sciences_tutors = Tutor.objects.filter(subject_tutored = "Life Sciences")
    return render(request, "subject_filtering/life_sciences_tutors.html", {'life_sciences_tutors': life_sciences_tutors})