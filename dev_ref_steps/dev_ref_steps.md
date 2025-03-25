# Django Task Management System - Step-by-Step Guide

## Project Overview

This guide will walk you through building a Task Management System with Django. The application will include user authentication, CRUD operations for tasks, task filtering, and a REST API.

## Tech Stack

- Django (Backend Framework)
- MySQL (Database)
- Bootstrap (Frontend Styling)
- Django REST Framework (API)

## Prerequisites

- Python (3.8+)
- pip (Python package manager)
- MySQL installed on your system
- Basic understanding of Python, HTML, CSS

## Project Timeline (Estimated)

- Setup & Configuration: 1 day
- User Authentication: 1 day
- Task CRUD Operations: 2 days
- Task Filtering: 1 day
- REST API: 1 day
- Testing & Refinement: 1 day
- **Total**: ~7 days (part-time work)

## Step 1: Environment Setup & Project Configuration

### 1.1 Create a virtual environment

```bash
# Create a project directory
mkdir task_management_system
cd task_management_system

# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 1.2 Install required packages

```bash
pip install django djangorestframework mysqlclient django-crispy-forms
```

### 1.3 Create a new Django project

```bash
django-admin startproject task_management .
```

### 1.4 Configure MySQL database

Open `task_management/settings.py` and update the database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'task_management_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 1.5 Create the MySQL database

```bash
mysql -u your_mysql_username -p
```

```sql
CREATE DATABASE task_management_db;
EXIT;
```

### 1.6 Create a new Django app

```bash
python manage.py startapp tasks
```

### 1.7 Register the app in settings.py

Add 'tasks', 'rest_framework', and 'crispy_forms' to INSTALLED_APPS in `task_management/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',
    'rest_framework',
    'crispy_forms',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
```

### 1.8 Run initial migrations

```bash
python manage.py migrate
```

## Step 2: Create Task Model

### 2.1 Define Task model in tasks/models.py

```python
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
```

### 2.2 Create and apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Implement User Authentication

### 3.1 Create authentication templates

Create directory structure:

```bash
mkdir -p tasks/templates/tasks
mkdir -p tasks/templates/registration
```

### 3.2 Create Base Template (tasks/templates/tasks/base.html)

The `base.html` template serves as the foundation for all other templates in the Django Task Management System. It includes a Bootstrap-powered navigation bar, a message display section, and a content block for child templates to override.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}Task Management System{% endblock %}</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <style>
      body {
        padding-top: 70px;
        padding-bottom: 30px;
      }
    </style>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div class="container">
        <a class="navbar-brand" href="{% url 'tasks:dashboard' %}"
          >Task Manager</a
        >
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            {% if user.is_authenticated %}
            <li class="nav-item">
              <a class="nav-link" href="{% url 'tasks:dashboard' %}"
                >Dashboard</a
              >
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'tasks:task_create' %}"
                >Add Task</a
              >
            </li>
            {% endif %}
          </ul>
          <ul class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
            <li class="nav-item">
              <span class="nav-link">Hello, {{ user.username }}</span>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'logout' %}">Logout</a>
            </li>
            {% else %}
            <li class="nav-item">
              <a class="nav-link" href="{% url 'login' %}">Login</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'register' %}">Register</a>
            </li>
            {% endif %}
          </ul>
        </div>
      </div>
    </nav>

    <div class="container">
      {% if messages %} {% for message in messages %}
      <div class="alert alert-{{ message.tags }}">{{ message }}</div>
      {% endfor %} {% endif %} {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
```

### 3.3 Create Login Template (tasks/templates/registration/login.html)

```html
{% extends 'tasks/base.html' %} {% load crispy_forms_tags %} {% block title
%}Login{% endblock %} {% block content %}
<div class="row justify-content-center mt-5">
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h3 class="text-center">Login</h3>
      </div>
      <div class="card-body">
        <form method="post">
          {% csrf_token %} {{ form|crispy }}
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary">Login</button>
          </div>
        </form>
        <hr />
        <p class="text-center">
          Don't have an account?
          <a href="{% url 'register' %}">Register here</a>
        </p>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

### 3.4 Create Register Template (tasks/templates/registration/register.html)

```html
{% extends 'tasks/base.html' %} {% load crispy_forms_tags %} {% block title
%}Register{% endblock %} {% block content %}
<div class="row justify-content-center mt-5">
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h3 class="text-center">Register</h3>
      </div>
      <div class="card-body">
        <form method="post">
          {% csrf_token %} {{ form|crispy }}
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary">Register</button>
          </div>
        </form>
        <hr />
        <p class="text-center">
          Already have an account? <a href="{% url 'login' %}">Login here</a>
        </p>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

### 3.5 Create Authentication Views (tasks/views.py)

```python
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
```

### 3.6 Configure Authentication URLs (task_management/urls.py)

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tasks.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
]
```

### 3.7 Create App URLs File (tasks/urls.py)

```python
from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/update/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
]
```

### 3.8 Update Settings.py with Login URLs

```python
LOGIN_REDIRECT_URL = 'tasks:dashboard'
LOGIN_URL = 'login'
```

## Step 4: Implement Task CRUD Operations

### 4.1 Create Task Form (tasks/forms.py)

```python
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date']
```

### 4.2 Create Task Views (tasks/views.py)

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    status_filter = request.GET.get('status', '')

    if status_filter:
        tasks = Task.objects.filter(user=request.user, status=status_filter)
    else:
        tasks = Task.objects.filter(user=request.user)

    context = {
        'tasks': tasks,
        'status_filter': status_filter
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('tasks:dashboard')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Update Task'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('tasks:dashboard')

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
```

### 4.3 Create Task Templates

#### Dashboard (tasks/templates/tasks/dashboard.html)

```html
{% extends 'tasks/base.html' %} {% block title %}Dashboard - Task Management
System{% endblock %} {% block content %}
<div class="row mb-4">
  <div class="col-md-8">
    <h2>My Tasks</h2>
  </div>
  <div class="col-md-4 text-end">
    <a href="{% url 'tasks:task_create' %}" class="btn btn-primary">
      <i class="bi bi-plus"></i> Add New Task
    </a>
  </div>
</div>

<div class="row mb-4">
  <div class="col-md-12">
    <div class="card">
      <div class="card-header">
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item">
            <a
              class="nav-link {% if status_filter == '' %}active{% endif %}"
              href="{% url 'tasks:dashboard' %}"
              >All</a
            >
          </li>
          <li class="nav-item">
            <a
              class="nav-link {% if status_filter == 'pending' %}active{% endif %}"
              href="{% url 'tasks:dashboard' %}?status=pending"
              >Pending</a
            >
          </li>
          <li class="nav-item">
            <a
              class="nav-link {% if status_filter == 'in_progress' %}active{% endif %}"
              href="{% url 'tasks:dashboard' %}?status=in_progress"
              >In Progress</a
            >
          </li>
          <li class="nav-item">
            <a
              class="nav-link {% if status_filter == 'completed' %}active{% endif %}"
              href="{% url 'tasks:dashboard' %}?status=completed"
              >Completed</a
            >
          </li>
        </ul>
      </div>
      <div class="card-body">
        {% if tasks %}
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Title</th>
                <th>Status</th>
                <th>Due Date</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {% for task in tasks %}
              <tr>
                <td>
                  <a href="{% url 'tasks:task_detail' task.id %}"
                    >{{ task.title }}</a
                  >
                </td>
                <td>
                  {% if task.status == 'pending' %}
                  <span class="badge bg-warning">Pending</span>
                  {% elif task.status == 'in_progress' %}
                  <span class="badge bg-info">In Progress</span>
                  {% else %}
                  <span class="badge bg-success">Completed</span>
                  {% endif %}
                </td>
                <td>{{ task.due_date|default:"-" }}</td>
                <td>{{ task.created_at|date:"M d, Y" }}</td>
                <td>
                  <a
                    href="{% url 'tasks:task_update' task.id %}"
                    class="btn btn-sm btn-outline-primary"
                    >Edit</a
                  >
                  <a
                    href="{% url 'tasks:task_delete' task.id %}"
                    class="btn btn-sm btn-outline-danger"
                    >Delete</a
                  >
                </td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <div class="text-center py-4">
          <p class="lead text-muted">No tasks found</p>
          <a href="{% url 'tasks:task_create' %}" class="btn btn-primary"
            >Add your first task</a
          >
        </div>
        {% endif %}
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

#### Task Form (tasks/templates/tasks/task_form.html)

```html
{% extends 'tasks/base.html' %} {% load crispy_forms_tags %} {% block title %}{{
title }} - Task Management System{% endblock %} {% block content %}
<div class="row justify-content-center mt-4">
  <div class="col-md-8">
    <div class="card">
      <div class="card-header">
        <h3>{{ title }}</h3>
      </div>
      <div class="card-body">
        <form method="post">
          {% csrf_token %} {{ form|crispy }}
          <div class="mt-4">
            <button type="submit" class="btn btn-primary">Save</button>
            <a
              href="{% url 'tasks:dashboard' %}"
              class="btn btn-outline-secondary"
              >Cancel</a
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

#### Task Detail (tasks/templates/tasks/task_detail.html)

```html
{% extends 'tasks/base.html' %} {% block title %}{{ task.title }} - Task
Management System{% endblock %} {% block content %}
<div class="row justify-content-center mt-4">
  <div class="col-md-8">
    <div class="card">
      <div
        class="card-header d-flex justify-content-between align-items-center"
      >
        <h3>Task Details</h3>
        <div>
          <a
            href="{% url 'tasks:task_update' task.id %}"
            class="btn btn-primary"
            >Edit</a
          >
          <a href="{% url 'tasks:task_delete' task.id %}" class="btn btn-danger"
            >Delete</a
          >
        </div>
      </div>
      <div class="card-body">
        <h4>{{ task.title }}</h4>

        <div class="mb-3">
          <span
            class="badge
                        {% if task.status == 'pending' %}bg-warning
                        {% elif task.status == 'in_progress' %}bg-info
                        {% else %}bg-success{% endif %}"
          >
            {{ task.get_status_display }}
          </span>
        </div>

        {% if task.description %}
        <div class="mb-4">
          <h5>Description</h5>
          <p>{{ task.description|linebreaks }}</p>
        </div>
        {% endif %}

        <div class="row g-3">
          {% if task.due_date %}
          <div class="col-md-4">
            <strong>Due Date:</strong>
            <p>{{ task.due_date }}</p>
          </div>
          {% endif %}
          <div class="col-md-4">
            <strong>Created:</strong>
            <p>{{ task.created_at }}</p>
          </div>
          <div class="col-md-4">
            <strong>Last Updated:</strong>
            <p>{{ task.updated_at }}</p>
          </div>
        </div>

        <div class="mt-4">
          <a
            href="{% url 'tasks:dashboard' %}"
            class="btn btn-outline-secondary"
            >Back to Dashboard</a
          >
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

#### Task Delete Confirmation (tasks/templates/tasks/task_confirm_delete.html)

```html
{% extends 'tasks/base.html' %} {% block title %}Delete Task - Task Management
System{% endblock %} {% block content %}
<div class="row justify-content-center mt-4">
  <div class="col-md-6">
    <div class="card border-danger">
      <div class="card-header bg-danger text-white">
        <h3>Delete Task</h3>
      </div>
      <div class="card-body">
        <p class="lead">
          Are you sure you want to delete the task "{{ task.title }}"?
        </p>
        <p>This action cannot be undone.</p>

        <form method="post">
          {% csrf_token %}
          <div class="mt-4 d-flex gap-2">
            <button type="submit" class="btn btn-danger">Yes, Delete</button>
            <a
              href="{% url 'tasks:task_detail' task.id %}"
              class="btn btn-outline-secondary"
              >Cancel</a
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

## Step 5: Implement REST API using Django REST Framework

### 5.1 Create Serializers (tasks/serializers.py)

```python
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### 5.2 Create API Views (tasks/api.py)

```python
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

### 5.3 Create API URLs (tasks/urls.py)

Update your existing urls.py:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api

app_name = 'tasks'

router = DefaultRouter()
router.register(r'tasks', api.TaskViewSet, basename='task-api')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/update/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),

    # API URLs
    path('api/', include(router.urls)),
]
```

### 5.4 Configure REST Framework in settings.py

Add the following to the bottom of `task_management/settings.py`:

```python
# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

## Step 6: Final Testing and Running the Application

### 6.1 Create a superuser for admin access

```bash
python manage.py createsuperuser
```

### 6.2 Run the development server

```bash
python manage.py runserver
```

### 6.3 Test the application

- Go to http://127.0.0.1:8000/ to access the application
- Register a new user
- Create, view, update, and delete tasks
- Test the API endpoints at http://127.0.0.1:8000/api/tasks/

## Step 7: Deploying to a Live Server (Optional)

### 7.1 Prepare for deployment

- Update settings.py with production settings
- Set DEBUG=False
- Configure ALLOWED_HOSTS
- Set up a proper SECRET_KEY

### 7.2 Choose a deployment platform

- Options include: Heroku, PythonAnywhere, DigitalOcean, AWS, etc.
- Follow platform-specific deployment instructions

## Project Expansion Ideas (For Your Resume)

1. **User Profiles**: Add user profiles with avatars and personal task statistics
2. **Task Categories/Tags**: Allow users to categorize tasks and filter by categories
3. **Task Priorities**: Add priority levels (High, Medium, Low)
4. **Due Date Notifications**: Send email reminders for upcoming tasks
5. **Task Sharing**: Allow users to share tasks with other users
6. **Task Comments**: Add a comment system for tasks
7. **Advanced Analytics**: Add task completion metrics and visualizations
8. **Export Feature**: Allow users to export tasks to CSV/PDF
9. **Mobile Responsiveness**: Ensure the UI works well on mobile devices
10. **JWT Authentication**: Add JWT for the API for better security

## Conclusion

You've now built a complete Task Management System with Django that includes user authentication, CRUD operations, task filtering, and a REST API. This project demonstrates your ability to:

1. Work with Django's MVC architecture
2. Implement user authentication and authorization
3. Design and create database models
4. Build CRUD operations with proper validation
5. Create a RESTful API
6. Implement a responsive UI using Bootstrap
7. Deploy a web application
