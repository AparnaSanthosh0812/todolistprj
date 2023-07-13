from django.shortcuts import render, redirect
'''from django.http import HttpResponse'''

from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
'''from django.contrib.auth.views import LogoutView'''
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from django.contrib import messages
from django.contrib.auth.models import User,auth


class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name='task'

    def get_context_data(self, **kwargs: Any):
        context=super().get_context_data(**kwargs)
        context['task']=context['task'].filter(user=self.request.user)
        context['count']=context['task'].filter(complete=False).count()
        
        search_input=self.request.GET.get('Search-area') or ''
        if search_input:
            context['task']=context['task'].filter(title__startswith=search_input)
            context['search_input']=search_input

        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='tasks'
    template_name= 'todo/task_detail.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('task')

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    success_url=reverse_lazy('task')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('task')

class CustomLoginView(LoginView):
    template_name='todo/login.html'
    fields="__all__"
    redirect_authenticated_user=False

    def get_success_url(self):
        return reverse_lazy('task')
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                
                return redirect(register)
            else:
                user = User.objects.create_user(username=username,password=password)
                user.set_password(password)
                user.save()
                print("success")
                return redirect('login')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        print("no post method")
        return render(request, 'todo/register.html')

'''class RegisterPage(FormView):
    template_name='todo/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('task')

    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task') 
        return super(RegisterPage, self).get(*args, *kwargs)'''
    
    





