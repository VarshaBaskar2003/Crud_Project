from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentForm

@login_required
def student_list(request):
    students = Student.objects.all().order_by('id')
    paginator = Paginator(students, 5)  # 5 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'student_list.html', {'page_obj': page_obj})



@login_required
def add_student(request):
    if not request.user.is_staff:
        messages.error(request, "Only staff can delete students.")
        return redirect('student_list')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'student_form.html', {'form': form, 'is_edit': False})



@login_required
def edit_student(request, id):
    if not request.user.is_staff:
        messages.error(request, "Only staff can add student details.")
        return redirect('student_list')

    student=get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'student_form.html', {'form': form, 'is_edit': True})


@login_required
def delete_student(request, id):
    if not request.user.is_staff:
        messages.error(request, "Only staff can delete students.")
        return redirect('student_list')
    student=get_object_or_404(Student, id=id)
    if request.method=='POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'confirm_delete.html', {'student':student})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Account not found. Please signup.")
            return redirect('signup')

        user= authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created successfully")
            return redirect('login')

    return render(request, 'signup.html')
