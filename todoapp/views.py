from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import todo
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .forms import TodoForm

@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()
        return redirect('home-page')
    
    query = request.GET.get('q')
    if query:
        all_todos = todo.objects.filter(user=request.user, todo_name__icontains=query)
    else:
        all_todos = todo.objects.filter(user=request.user)
    
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(password) < 3:
            messages.error(request, 'password must be at least 3 characters long')
            return redirect('register')
        get_all_user = User.objects.filter(username=username)
        if get_all_user:
            messages.error(request, 'User already exist')
            return redirect('register')
        new_User = User.objects.create_user(username=username, email=email, password=password)
        new_User.save()
        messages.success(request, 'User successfully created, login now')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def LogoutView(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')
    return render(request, 'todoapp/login.html', {})

@login_required
def DeleteTask(request, id):
    get_todo = get_object_or_404(todo, id=id, user=request.user)
    get_todo.delete()
    return redirect('home-page')

@login_required
def Update(request, id):
    get_todo = get_object_or_404(todo, id=id, user=request.user)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')
@login_required
def profile(request):
    user = request.user
    todos = todo.objects.filter(user=user)
    total_tasks = todos.count()
    completed_tasks = todos.filter(status=True).count()
    pending_tasks = total_tasks - completed_tasks
    discipline_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    context = {
        'user': user,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'discipline_rate': discipline_rate,
    }
    return render(request, 'todoapp/profile.html', context)

@login_required
def edit_profile(request):
    return render(request, 'todoapp/edit_profile.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        return redirect('profile')
    return redirect('edit_profile')



