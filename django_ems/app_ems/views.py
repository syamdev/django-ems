from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView, RedirectView

from .forms import EmployeeForm
from .models import Employee, Salary, generate_next_emp_no


def my_profile(request, pk):
    profile = get_object_or_404(Employee, pk=pk)
    if request.method.upper() == 'POST':
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


def index(request):
    if request.method.upper() == 'GET':
        return render(request, 'index.html', {})


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {})


class IndexGenericView(TemplateView):
    template_name = 'index.html'


class ProfileView(View):

    form_class = EmployeeForm
    # initial = {'hire_date': 'TODAY_DATE'}
    template_name = 'profile_detail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_context_data().get('profile'))
        return render(request, self.get_template_name(), {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_object())
        if form.is_valid():
            #  <process form cleaned data>
            form.save()
            return HttpResponseRedirect('/success/')
        return render(request, self.template_name, {'form': form})

    def get_template_name(self):
        """Return the name of template we should render"""
        return self.template_name

    def get_context_name(self):
        """Return the data passed to the template"""
        return {
            'profile': self.get_object(),
        }

    def get_object(self):
        """Return the blogpost instance that the view displays"""
        return get_object_or_404(Employee, pk=self.kwargs.get('pk'))


class ProfileListView(ListView):
    model = Employee
    template_name = 'profile_list.html'
    paginate_by = 100

    def get_queryset(self):
        order_by_field = self.request.GET.get('order_by') or '-hire_date'
        queryset = super(ProfileListView, self).get_queryset()
        return queryset.order_by(order_by_field)


class ProfileDetailView(DetailView):
    model = Employee
    template_name = 'profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['employee'] = Employee.objects.filter(pk=self.object.pk)
        return context


class ProfileCreateView(CreateView):
    template_name = 'profile_create.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('profile_list')

    def get_initial(self):
        # Get the initial dictionary from the superclass method and fill it up with additional
        initial = super(ProfileCreateView, self).get_initial()
        initial['emp_no'] = generate_next_emp_no()
        return initial


class ProfileDeleteView(DeleteView):
    template_name = 'profile_delete.html'
    model = Employee
    success_url = reverse_lazy('profile_list')

    def get(self, request, *args, **kwargs):
        """
        Take note this is a hack as we don't want to show confrmation page before deleting.
        By default, Django will try to look for a template called objectname__confirm_delete.html.
        """
        return self.post(request, *args, **kwargs)


class ProfileUpdateView(UpdateView):
    template_name = 'profile_update.html'
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('profile_list')
