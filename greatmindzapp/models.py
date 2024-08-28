from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class University(models.Model):
    level = models.CharField(max_length=30)

    def __str__(self):
       return self.level

class UnderGrad(models.Model):
    undergrad_finished = models.CharField(max_length=20)

    def __str__(self):
       return self.undergrad_finished

class Gender(models.Model):
    gender = models.CharField(max_length=10)

    def __str__(self):
       return self.gender
    
class Citizen(models.Model):
    citizen = models.CharField(max_length=10)

    def __str__(self):
       return self.citizen

class Subject(models.Model):
    subject_tutored = models.CharField(max_length=25)

    def __str__(self):
       return self.subject_tutored
    
class Grade(models.Model):
    learner_grade = models.CharField(max_length=25)

    def __str__(self):
       return self.learner_grade

class LessonMode(models.Model):
    lesson_mode = models.CharField(max_length=25)

    def __str__(self):
       return self.lesson_mode 
    
class Syllabus(models.Model):
    learner_syllabus = models.CharField(max_length=25)

    def __str__(self):
       return self.learner_syllabus 

class LessonStart(models.Model):
    lesson_start = models.CharField(max_length=25)

    def __str__(self):
       return self.lesson_start   
   
class JobStatus(models.Model):
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.status

class Province(models.Model):
    province = models.CharField(max_length=100)

    def __str__(self):
        return self.province

class CanTutorOnline(models.Model):
    online = models.CharField(max_length=20)

    def __str__(self):
        return self.online
    
class Message(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    contactnumber = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    
    def __str__(self):
        return self.fullname

class Relationship(models.Model):
    relationship = models.CharField(max_length=20)

    def __str__(self):
        return self.relationship


class TutorManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, mobile_number, subject_tutored, street_address,
                    suburb, town, bio, profile_pic, password=None):

        if not email:
            raise ValueError('You must provide email address')
        if not first_name:
            raise ValueError('You must provide full name')  
        if not last_name:
            raise ValueError('You must provide last name')        
        if not mobile_number:
            raise ValueError('You must provide mobile number')
        if not subject_tutored:
            raise ValueError('You must provide subject tutored')
        if not street_address:
            raise ValueError('You must provide full physical address')
        if not bio:
            raise ValueError('You must provide a biography')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, mobile_number=mobile_number, 
                          subject_tutored=subject_tutored, profile_pic=profile_pic,
                         street_address=street_address, suburb=suburb, town=town,  bio=bio)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name,last_name, mobile_number, subject_tutored, street_address,
                          suburb, town, bio, profile_pic, password=None, **extra_fields):
        user = self.create_user(email=email, first_name=first_name, last_name=last_name, mobile_number=mobile_number, 
                                subject_tutored=subject_tutored, street_address=street_address, 
                                suburb=suburb, town=town,bio=bio, profile_pic=profile_pic, password=password, **extra_fields )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

class Tutor(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address", max_length = 50, unique = True)
    first_name = models.CharField(verbose_name="first name",max_length=100) 
    last_name = models.CharField(verbose_name="last name",max_length=100) 
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    age = models.CharField(verbose_name="last name",max_length=100) 
    sa_citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True)
    id_no = models.CharField(verbose_name="id number",max_length=20, null=True) 
    mobile_number = models.CharField(verbose_name="mobile number", max_length=15)
    subject_tutored = models.CharField(verbose_name="subject tutored", max_length=30)
    can_tutor_online = models.ForeignKey(CanTutorOnline, on_delete=models.CASCADE, null=True)
    
    street_address = models.CharField(max_length=100) 
    suburb = models.CharField(max_length=100, blank=True) 
    town = models.CharField(max_length=100, blank = True)   
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)

    bio = models.TextField(verbose_name="biography", max_length=500)
    highest_qualification = models.CharField(max_length=50, null=True)    
    undergrad_finished = models.ForeignKey(UnderGrad, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(null = True, blank = True, upload_to='images/')
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default= True)
    is_superuser = models.BooleanField(default=True)
     

    objects = TutorManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_number', 'bio', 
                       'subject_tutored', 'street_address','suburb','town', 'profile_pic']

    def __str__(self):
        return self.first_name + self.last_name
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label ):
        return True


class GetTutor(models.Model):
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)   
    last_name = models.CharField(max_length=50)      
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=12)
    relationship = models.ForeignKey(Relationship, on_delete = models.CASCADE)

    street_address = models.CharField(max_length=100) 
    suburb = models.CharField(max_length=100, blank=True) 
    town = models.CharField(max_length=100, blank = True)   
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True)
     
         
    lesson_mode = models.ForeignKey(LessonMode, on_delete=models.CASCADE)
    start = models.ForeignKey(LessonStart, on_delete=models.CASCADE)
    additional_details= models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    pay_rate = models.CharField(max_length=7)
    job_number = models.CharField(max_length=5, unique=True, null=True)
    jobstatus = models.ForeignKey(JobStatus, on_delete=models.CASCADE, null=True)    
    applicant = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True) 
        

    def __str__(self):
        return self.first_name + self.last_name


class Blog(models.Model):
    title= models.CharField(max_length=50)    
    slug = models.SlugField(max_length=250, unique = True)
    body = models.TextField(max_length=1500)
    author = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable = False)

    def get_absolute_url(self):
        return reverse("blog_single", kwargs = {"slug": self.slug})

    def snippet(self):
        return self.body[0:50] + '...'

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
class Review(models.Model):
    review = models.TextField(max_length = 300)
    parent_name = models.CharField(max_length=50)
    learner_name = models.CharField(max_length=50)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tutor.first_name + ' ' + self.tutor.last_name
        
    
