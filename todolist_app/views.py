from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todolist(request):
    # return HttpResponse ("welcome to welfare")
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
     #       form.save()
        messages.success(request,("new task added successfully!!"))
        return redirect('todolist')
    else: 
      #  all_tasks = TaskList.objects.all()
        all_tasks = TaskList.objects.filter(manage = request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)

        return render(request,'todolist.html',{'all_tasks': all_tasks})
        
@login_required
def delete_task(request,task_id):
        task = TaskList.objects.get(pk=task_id)
        task.delete()

        return  redirect('todolist')

def edit_task(request,task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
            form.save()
    
        messages.success(request,("task updated successfully!!"))
        return redirect('todolist')
    else: 
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj': task_obj})

def complete_task(request,task_id):
        task = TaskList.objects.get(pk=task_id)
        task.done = True
        task.save()

        return redirect('todolist')

def pending_task(request,task_id):
        task = TaskList.objects.get(pk=task_id)
        task.done = False
        task.save()

        return redirect('todolist')

def index(request):
    context = {
        'index_text' : "welcome to index page"
    }
    return render(request,'index.html',context)

@login_required
def contact(request):
    context = {
        'contact_text' : "welcome to contact page"
    }
    return render(request,'contact.html',context)

def about(request):
    context = {
        'about_text' : "welcome to about page"
    }
    return render(request,'about.html',context)
