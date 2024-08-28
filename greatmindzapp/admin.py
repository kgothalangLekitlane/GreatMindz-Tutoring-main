from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . models import Message, GetTutor, Tutor, LessonMode, Grade, Subject, LessonStart, Syllabus,Blog, JobStatus, Gender, Citizen, University, UnderGrad, CanTutorOnline, Review, Province, Relationship


class TutorAdmin(BaseUserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject_tutored', 'mobile_number', 'is_active','is_approved', 'id', 'pk')
    search_fields = ('first_name','last_name', 'email',)
    readonly_fields = ('date_joined','last_login',)
    ordering = ('first_name',)
    filter_horizontal = ()
    list_filter = ('last_login',)

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name","last_name","gender", "sa_citizen", "id_no", "mobile_number", 
                                      "subject_tutored","can_tutor_online", "street_address",'suburb','town','bio', "profile_pic" ]}),
        ("Permissions", {"fields": ["is_admin", "is_active", "is_superuser", "is_approved", "is_staff"]}),
    ]
    add_fieldsets = (
        ( None, {
            'classes':('wide'),
            'fields':('email','first_name','last_name', 'subject_tutored', 'street_address', 'bio', 'password1', 'password2', 'profile_pic',),
        }),
    )
  

class GetTutorAdmin(admin.ModelAdmin):
    list_display = ('first_name','grade', 'subject','syllabus','mobile','suburb','town', 'lesson_mode', 'created_at','jobstatus',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('fullname','email', 'contactnumber','message',)


admin.site.register(Message, MessageAdmin)
admin.site.register(GetTutor, GetTutorAdmin)
admin.site.register(LessonMode)
admin.site.register(LessonStart)
admin.site.register(Subject)
admin.site.register(Syllabus)
admin.site.register(Grade)
admin.site.register(Blog)
admin.site.register(JobStatus)
admin.site.register(Gender)
admin.site.register(University)
admin.site.register(UnderGrad)
admin.site.register(Citizen)
admin.site.register(CanTutorOnline)
admin.site.register(Tutor, TutorAdmin)
admin.site.register(Review)
admin.site.register(Province)
admin.site.register(Relationship)


