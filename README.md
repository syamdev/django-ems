# Building Django App - Employee Management System (EMS)
Build Django web app for Employee Management System (EMS)


## PostgreSQL

- Access via pgAdmin
- Create db
- Restore db


## Start Django Project

`pip install django`

`django-admin startproject django_ems`

```
cd ~/my-project-dir
echo "DB_NAME=somethingelse" > .env
echo "DB_USER=somethingelse" > .env
echo "DB_PASSWORD=somethingelse" > .env
echo "DB_HOST=somethingelse" > .env
echo "DB_PORT=somethingelse" > .env
```
```
export DB_NAME=somethingelse
export SECRET_KEY=somethingelse
etc
```
`pip install python-dotenv`

`pip install psycopg2`

`pip freeze > requirements.txt`


## Configure Django

### Settings Config

```
settings/
   ├── __init__.py
   ├── base.py
   ├── ci.py
   ├── local.py
   ├── staging.py
   ├── production.py
   └── qa.py
```
```
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
...
```
### Database PostgreSQL Setting

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'employees',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {'options': '-c search_path=public'},
    }
}
```

`python manage.py startapp app_ems`

`python manage.py runserver --settings=django_ems.settings.local`

`python manage.py migrate --settings=django_ems.settings.local`

`python manage.py createsuperuser --settings=django_ems.settings.local`


## Models Approach

### Create Models First

- Create models then makemigrations

`python manage.py makemigrations app_ems --settings=django_ems.settings.local`

### Create PostgreSQL DB from Models

`python manage.py sqlmigrate app_ems 0001_initial --settings=django_ems.settings.local`

`python manage.py migrate --settings=django_ems.settings.local`

### Delete Table

- You can delete via pgAdmin directly

- You can go to table:
    - <b>django_migrations</b>: delete migration rows
    - <b>auth_permission</b>: delete model rows
    
- You can delete app <b>migrations</b> directory

### Create Models Based on An Existing Database

- Create app Feedback

`python manage.py makemigrations app_feedback --settings=django_ems.settings.local`

`python manage.py inspectdb --settings=django_ems.settings.local`

`python manage.py inspectdb > app_ems/models.py --settings=django_ems.settings.local`

- Clean up: models.py
    - Delete: django stuffs, models.DO_NOTHING, managed = False, id on class DeptManager, DeptEmp, Salaries, Titles
    - Rename model employess to employee, 'employees' to employee
    - add:
    ```
      GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
      )
    ```

    `gender = ... ,choices=GENDER_CHOICES)`

    - on class saries: add attr foreignkey: related_name='employeeSalaries'
    - on class title: add attr foreignkey: related_name='employeeTitles'
    - foreignkey: add on_delete=models.CASCADE
- makemigration app_ems

### Fake Migration

`migrate --fake app_ems 0001_initial`


## Querysets

`python manage.py shell`


```
from app_ems.models import Employee


queryset = Employee.objects.all()
print(queryset)
```

```
def __str__(self):
    return "first_name=%s, last_name=%s" % (self.first_name, self.last_name)
```


## Django Admin

### Register Models for DB

#### On admin.py:
```
from .models import Feedback

admin.site.register(Feedback)
```

### Add Form Field to Django Admin Form

#### On admin.py:
```
from django import forms


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = '__all__'


class FeedbackAdmin(admin.ModelAdmin):
    form = FeedbackForm
    search_fields = ('name', 'category', 'email', 'subject',)
    list_display = ('name', 'category', 'email', 'subject', 'is_read',)
    list_editable = ('is_read',)


admin.site.register(Feedback, FeedbackAdmin)
```

### Customize Django Admin Form

#### On admin.py
- Add textarea
`comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 50, 'style': 'resize:none;'}))`

- Edit form to read only
```
class FeedbackAdmin(admin.ModelAdmin):
    [...]
    readonly_fields = ('created_on',)
```

- Edit Add form
```
class FeedbackAddForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 50, 'style': 'resize:none;'}))

    class Meta:
        model = Feedback
        fields = fields = ('name', 'subject', 'category', 'email', 'comment', 'is_read',)
```
```
class FeedbackAdmin(admin.ModelAdmin):
    [...]

    def get_form(self, request, obj=None, change=False, **kwargs):
        if obj is None:
            return FeedbackAddForm
        else:
            return super(FeedbackAdmin, self).get_form(request, obj, **kwargs)
```

- Customize button & action position
```
    # readonly_fields = ('created_on',)
    save_on_top = True
    actions_on_bottom = False
```

- Add action text
`actions = [mark_feedback_as_read]`
  
- Ordering from last update
`ordering = ('-created_on',)`

#### On models.py
- Add choices

```
    CATEGORY_CHOICES = (
        ('1', 'General'),
        ('2', 'Management'),
        ('3', 'Compensation'),
        ('4', 'Suggestions'),
        ('5', 'Complaint'),
    )
    
    category = models.CharField(max_length=10, default='1', choices=CATEGORY_CHOICES)
    [...]
    
    def __str__(self):
        return self.email
```

### Add Custom Actions

### On admin.py
- add action
```
def mark_feedback_as_read(modeladmin, request, queryset):
    for employeeFeedback in queryset:
        employeeFeedback.is_read = True
        employeeFeedback.save()


class FeedbackAdmin(admin.ModelAdmin):
    [...]
    actions = [mark_feedback_as_read]
```

- add action description
```
mark_feedback_as_read.short_description = 'Mark selected feedback as read'
```

- add action message
```
def mark_feedback_as_read
    [...]
    modeladmin.message_user(request, "%s successfully marked as read" % len(queryset))
```

### Move forms from admin.py to forms.py

### Move `def mark_feedback_as_read` from admin.py to forms.py

### Validations prevent SQL Injection

- Allowed character checks
- Cardinality checks
- Consistency checks
- File existence checks
- Spelling & grammar checks
- Solutions:
  - Use parameterized queries (do string parsing to remove special characters or SQL keywords)
  
### Django Validation

#### Validation on form level, forms.py
- Create an object of email validator

```
from django.core.validators import EmailValidator, MinLengthValidator, MaxLengthValidator


class FeedbackAddForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'size': 20}), validators=[EmailValidator(), MinLengthValidator(6), MaxLengthValidator(100)])
```

#### Validation on model level, models.py

- It's more preferred. Because it can be used for different modules/application, example: REST API, without duplicate validation. 
```
from django.core.validators import EmailValidator, MinLengthValidator, MaxLengthValidator


class Feedback(models.Model):
    [...]
    email = models.CharField(max_length=150, validators=[EmailValidator(), MinLengthValidator(6), MaxLengthValidator(100)])
```

#### Remember this after edit models.py
```
python manage.py makemigrations --settings=django_ems.settings.local
python manage.py migrate --settings=django_ems.settings.local
python manage.py runserver --settings=django_ems.settings.local
```

### Django custom model function validation
```
from django.core.exceptions import ValidationError


def validate_allowed_domains(value):
    allowed_domains = ["sy4m.com", "webitu.com"]
    user_part, domain_part = value.rsplit('@', 1)
    if domain_part not in allowed_domains:
        raise ValidationError("Invalid employee email address")


class Feedback(models.Model):
    [...]
    email = models.CharField(max_length=150,
                             validators=[EmailValidator(),
                                         MinLengthValidator(6),
                                         MaxLengthValidator(100),
                                         validate_allowed_domains]
                             )
```

###  Django custom form validation

#### On models.py
```
class Feedback(models.Model):
    [...]
    emp_no = models.IntegerField()
```

- Add a field 'emp_no' on admin.py & forms.py

#### On forms.py
- Add function validation
```
class FeedbackAddForm(forms.ModelForm):
    [...]
    def clean_emp_no(self):
        print(self.cleaned_data)
        return self.cleaned_data.get('emp_no')
```
```
    def clean_emp_no(self):
        print(self.cleaned_data)
        emp_no = self.cleaned_data.get('emp_no')
        if emp_no and not Employee.objects.filter(pk=emp_no).exists():
            raise forms.ValidationError('Invalid employee number')

    def clean(self):
        formdata = super(FeedbackAddForm, self).clean()
        category = formdata.get('category')
        comment = formdata.get('comment')
        if category == '5' and comment:
            if 'reference_no=' not in comment:
                raise forms.ValidationError('Your complaint should have tag "reference_no="')
            return formdata
```

- Create form on <b>forms.py</b> for "app_ems"
- Register form to django admin on <b>admin.py</b> for "app_ems"

### Add Custom Filters

#### On admin.py

- Add filter by gender
```
class GenderFilter(admin.SimpleListFilter):
    title = 'Gender'
    parameter_name = 'gender'

    def lookups(self, request, model_admin):
        return (
            ('M', 'Male'),
            ('F', 'Female'),
        )

    def queryset(self, request, queryset):
        return queryset.filter(gender__exact=self.value()) if self.value() else queryset


class EmployeeAdmin(admin.ModelAdmin):
    [...]
    list_filter = ('hire_date', GenderFilter)
```

- Add filter by deparment
```
class DepartmentFilter(admin.SimpleListFilter):
    title = 'Department'
    parameter_name = 'deparment'

    def lookups(self, request, model_admin):
        departments = set([d for d in Department.objects.all()])
        return [(d.dept_no, d.dept_name) for d in departments]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(departments__dept_no__exact=self.value()) if self.value() else queryset


class EmployeeAdmin(admin.ModelAdmin):
    [...]
    list_filter = ('hire_date', GenderFilter, DepartmentFilter)
```

- Add inline table
```
from django.contrib import admin
from .models import Employee, Department, DeptEmp, DeptManager, Salary, Titles
from .forms import EmployeeForm, SalaryForm


class SalaryTableInline(admin.TabularInline):
    form = SalaryForm
    model = Salary
    fk_name = 'emp_no'
    extra = 1


class EmployeeAdmin(admin.ModelAdmin):
    [...]
    inlines = [SalaryTableInline]
```
#### On models.py
```
class Employee(models.Model):
    [...]
    departments = models.ManyToManyField(Department, related_name='departments', through='DeptEmp')
```

- Change model name
```
class Salary(models.Model):
    [...]
    salary_amount = models.IntegerField()
```

### User View Permission

- Add user
- Select permission for user

### Change Django Admin Header

#### On project/urls.py
```
admin.site.site_header = 'My Admin Panel'
admin.site.site_title = 'My Administration Site'
admin.site.index_title = 'My Administration'
```

### Change Django Admin Section Title

#### On app/apps.py
```
class AppEmsConfig(AppConfig):
    name = 'app_ems'
    verbose_name = 'EMS Section'
```

#### On settings (settings/base.py)
```
INSTALLED_APPS = [
    [...]
    'app_ems.apps.AppEmsConfig',
    'app_feedback.apps.AppFeedbackConfig',
]
```

### Renama Table on Django Admin

#### On models.py
```
    class Meta:
        verbose_name = 'My Salary'
        verbose_name_plural = "My Salaries"
```


## URL Configurations & Response Views

### Django URLs Views

### Function Based Views
- Manual from your own
- No standard template for CRUD

#### On app/urls.py
```
from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^employees/(?P<pk>[0-9]+)/profile/$', views.my_profile, name='app_ems'),
    re_path(r'^$', views.index),
]
```
#### On project/urls.py
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_ems.urls')),
]
```
#### On app/views.py
```
from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>EMS Home Page</h1>')


def my_profile(request, pk):
    return HttpResponse('<h1>This is my first function based view %s</h1>' % pk)
```

### FBV Form Templates
#### On views.py
- Render index.html template
```
def index(request):
    return render(request, 'index.html', {})
```

- Create Profile View function
```
from django.shortcuts import render, get_object_or_404, redirect
[...]
def my_profile(request, pk):
    profile = get_object_or_404(Employee, pk=pk)
    if request.method.Upper() == 'POST':
        form = EmployeeForm(request.POST, instance=profile)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return redirect('my_profile', pk=pk)

    form = EmployeeForm(instance=profile)
    context = {
        'form': form,
    }
    return render(request, 'profile.html', context=context)
```
- Create form on profile.html
```
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit">
</form>
```

#### On app/urls.py
- Add view function name
```
urlpatterns = [
    re_path(r'^employees/(?P<pk>[0-9]+)/profile/$', views.my_profile, name='my_profile'),
    [...]
```
### Class Based Views
- Standar template for CRUD

#### On views.py
- Create class IndexViews (get, post)

#### On app/urls.py
- Edit view to IndexView.as_view()

### Generic View Template
- Abstract common patterns for CRUD
- DRY principle CRUD
```
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView, RedirectView
```
- Create view for CRUD:
    - ProfileListView
    - ProfileDetailView
    - ProfileCreateView
    - ProfileUpdateView
    - ProfileDeleteView
    
- Create HTML templates for each view

### Until here, django app with **simple CRUD** is ready with minimal template. 

#### Urls
- siteurl/ : index page
- employees/profile/list/ : profile list
- employees/<emp_no>/profile/ : profile detail
- employees/profile/create/ : create profile
- employees/<emp_no>/profile/update/ : update profile
- employees/<emp_no>/profile/delete/ : delete profile


## Django Templates

- Using parallax template: https://materializecss.com/getting-started.html#templates
- Implement template to each view
- Install: ` pip install  django-materializecss-form ` 