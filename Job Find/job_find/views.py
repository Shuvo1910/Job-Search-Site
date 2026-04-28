from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from job_find.models import *
from job_find.forms import *
from django.db.models import Q
from django.contrib import messages

# =========================
# Public Views
# =========================
def home_page(request):
    return render(request, 'home.html')

def register_page(request):
    if request.method == 'POST':
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, "Account created successfully!")
            return redirect('login_page')
    else:
        form_data = RegisterForm()
        
    context = {
        'form_data': form_data,
        'form_title': 'Create Account',
        'btn_name': 'Register',
    }
    return render(request, 'base_auth.html', context)

def login_page(request):
    if request.method == 'POST':
        form_data = LoginForm(request, data=request.POST)
        if form_data.is_valid():
            user = form_data.get_user()
            login(request, user)
            return redirect('home_page')
    else:
        form_data = LoginForm()
        
    context = {
        'form_data': form_data,
        'form_title': 'Login Account',
        'btn_name': 'Login',
    }
    return render(request, 'base_auth.html', context)

def job_list(request):
    user = request.user
    job_data = JobPostModel.objects.all()

    if user.is_authenticated and user.user_type == 'client':
        if hasattr(user, 'client_profile'):
            job_data = JobPostModel.objects.filter(posted_by=user.client_profile)
        else:
            job_data = JobPostModel.objects.none() 

    category_id = request.GET.get('category_id')
    if category_id:
        job_data = job_data.filter(category_id=category_id)

    context = {
        'job_data': job_data,
        'category': CategoryModel.objects.all()
    }
    return render(request, 'jobs.html', context)


# =========================
# Auth & Profile Views
# =========================
@login_required
def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def profile_page(request):
    return render(request, 'profile.html')

@login_required
def profile_update(request):
    user = request.user
    if user.user_type == 'client':
        profile_info, created = ClientProfileModel.objects.get_or_create(client_info=user)
        if request.method == "POST":
            form_data = ClientProfileUpdateForm(request.POST, request.FILES, instance=profile_info)
            if form_data.is_valid():
                form_data.save()
                return redirect('profile_page')
        else:
            form_data = ClientProfileUpdateForm(instance=profile_info)
    else: 
        profile_info, created = UserProfileModel.objects.get_or_create(user_info=user)
        if request.method == "POST":
            form_data = UserProfileUpdateForm(request.POST, request.FILES, instance=profile_info)
            if form_data.is_valid():
                form_data.save()
                return redirect('profile_page')
        else:
            form_data = UserProfileUpdateForm(instance=profile_info)
    
    context = {
        'form_data': form_data,
        'title_name': 'Update Profile',
        'btn_name': 'Update'
    }
    return render(request, 'master/base-form.html', context)

# =========================
# Job Management (For Clients)
# =========================
@login_required
def job_post(request):
    if request.user.user_type != 'client':
        messages.error(request, "Only clients can post jobs.")
        return redirect('job_list')

    if request.method == "POST":
        form_data = JobPostForm(request.POST)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.posted_by = request.user.client_profile
            data.save()
            return redirect('job_list')
    else:
        form_data = JobPostForm()
        
    context = {
        'form_data': form_data,
        'title_name': 'Add Job Post Info',
        'btn_name': 'Post Job'
    }
    return render(request, 'master/base-form.html', context)

@login_required
def edit_job(request, job_id):
    job_data = get_object_or_404(JobPostModel, id=job_id)
    
    if job_data.posted_by != request.user.client_profile:
        return redirect('job_list')

    if request.method == "POST":
        form_data = JobPostForm(request.POST, instance=job_data)
        if form_data.is_valid():
            form_data.save()
            return redirect('job_list')
    else:
        form_data = JobPostForm(instance=job_data)

    context = {
        'form_data': form_data,
        'title_name': 'Update Job Info',
        'btn_name': 'Update Job'
    }
    return render(request, 'master/base-form.html', context)

@login_required
def delete_job(request, job_id):
    job_data = get_object_or_404(JobPostModel, id=job_id)
    if job_data.posted_by == request.user.client_profile:
        job_data.delete()
    return redirect('job_list')

# =========================
# Job Application (For Employees)
# =========================
@login_required
def apply_now(request, job_id):
    if request.user.user_type != 'employee':
        messages.error(request, "Only employees can apply for jobs.")
        return redirect('job_list')

    job_data = get_object_or_404(JobPostModel, id=job_id)
    
    if request.method == "POST":
        form_data = JobApplyForm(request.POST, request.FILES)
        if form_data.is_valid():
            data = form_data.save(commit=False)
            data.applied_by = request.user.user_profile
            data.applied_job = job_data
            data.save()
            messages.success(request, "Application submitted!")
            return redirect('job_list')
    else:
        form_data = JobApplyForm()
        
    context = {
        'form_data': form_data,
        'title_name': f'Apply for {job_data.job_title}',
        'btn_name': 'Apply Now'
    }
    return render(request, 'master/base-form.html', context)

@login_required
def applied_job_list(request):
    job_data = JobApplyModel.objects.filter(applied_by=request.user.user_profile)
    context = {'job_data': job_data}
    return render(request, 'applied_job_list.html', context)

@login_required
def candidate_list(request, job_id):
    job_data = get_object_or_404(JobPostModel, id=job_id)
    if job_data.posted_by != request.user.client_profile:
        return redirect('job_list')
        
    candidate_data = JobApplyModel.objects.filter(applied_job=job_data)
    context = {
        'job': job_data,
        'candidate_data': candidate_data
    }
    return render(request, 'candidate_list.html', context)
