from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================
# Custom User Model
# =========================
class UserInfoModel(AbstractUser):
    USER_TYPE = [
        ('admin','Admin'),
        ('client', 'Client'),
        ('employee', 'Employee')
    ]
    
    display_name = models.CharField(max_length=255, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='employee')

    def __str__(self):
        return f'{self.username} - {self.user_type}'


# =========================
# User Profile (Employee side)
# =========================
class UserProfileModel(models.Model):
    user_info = models.OneToOneField(
        UserInfoModel, 
        on_delete=models.CASCADE, 
        related_name='user_profile'
    )
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile/', blank=True, null=True)

    def __str__(self):
        return self.user_info.username


# =========================
# Client Profile
# =========================
class ClientProfileModel(models.Model):
    client_info = models.OneToOneField(
        UserInfoModel, 
        on_delete=models.CASCADE, 
        related_name='client_profile'
    )
    company_name = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='client_profile/', blank=True, null=True)

    def __str__(self):
        return f"Client: {self.client_info.username}"


# =========================
# Category
# =========================
class CategoryModel(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


# =========================
# Job Post
# =========================
class JobPostModel(models.Model):
    category = models.ForeignKey(
        CategoryModel, 
        on_delete=models.CASCADE,
        default=1 
    )
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    job_description = models.TextField(blank=True)
    skill_set = models.TextField(null=True)
    salary_range = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(
        ClientProfileModel, 
        on_delete=models.CASCADE, 
        related_name='job_posts'
    )

    def __str__(self):
        return f'{self.job_title} - {self.company_name}'


# =========================
# Job Apply
# =========================
class JobApplyModel(models.Model):
    applied_by = models.ForeignKey(
        UserProfileModel, 
        on_delete=models.CASCADE,
        null=True 
    )
    applied_job = models.ForeignKey(
        JobPostModel,
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    resume = models.FileField(upload_to='resume/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user = self.applied_by.user_info.username if self.applied_by else "Anonymous"
        return f'{user} - {self.applied_job.job_title}'
