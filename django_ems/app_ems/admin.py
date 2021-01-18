from django.contrib import admin
from .models import Employee, Department, DeptEmp, DeptManager, Salary, Title
from .forms import EmployeeForm, SalaryForm


class SalaryTableInline(admin.TabularInline):
    form = SalaryForm
    model = Salary
    fk_name = 'emp_no'
    extra = 1


class DepartmentFilter(admin.SimpleListFilter):
    title = 'Department'
    parameter_name = 'deparment'

    def lookups(self, request, model_admin):
        departments = set([d for d in Department.objects.all()])
        return [(d.dept_no, d.dept_name) for d in departments]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(departments__dept_no__exact=self.value()) if self.value() else queryset


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
    form = EmployeeForm
    search_fields = ('emp_no', 'first_name', 'last_name', 'gender', 'hire_date')
    list_display = ('emp_no', 'first_name', 'last_name', 'gender', 'hire_date')
    list_display_links = ('emp_no',)
    list_filter = ('hire_date', GenderFilter, DepartmentFilter)
    save_on_top = True
    inlines = [SalaryTableInline]
    actions_on_bottom = False
    ordering = ('-hire_date',)


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(DeptEmp)
admin.site.register(DeptManager)
admin.site.register(Salary)
admin.site.register(Title)
