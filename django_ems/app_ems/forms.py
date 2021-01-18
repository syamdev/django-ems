from django import forms
from .models import Employee, Salary


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('emp_no', 'birth_date', 'first_name', 'last_name', 'gender', 'hire_date',)


class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        fields = '__all__'
