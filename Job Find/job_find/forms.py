from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from job_find.models import *

# =========================
# Register Form
# =========================
class RegisterForm(UserCreationForm):
    class Meta:
        model = UserInfoModel
        fields = [
            'username',
            'display_name',
            'email',
            'user_type',
        ] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'user_type' in self.fields:
            filtered_choices = [
                choice for choice in UserInfoModel.USER_TYPE 
                if choice[0] != 'admin'
            ]
            self.fields['user_type'].choices = filtered_choices

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



# =========================
# Login Form
# =========================
class LoginForm(AuthenticationForm):
    
    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# =========================
# Job Post Form (Client)
# =========================
class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPostModel
        fields = [
            'category',
            'job_title',
            'job_description',
            'skill_set',
            'salary_range',
        ]

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)
        
        for fields in self.fields.values():
            fields.widget.attrs.update({'class':'form-control'})


# =========================
# Job Apply Form (Employee)
# =========================
class JobApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplyModel
        fields = ['resume']



    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)
        
        for fields in self.fields.values():
            fields.widget.attrs.update({'class':'form-control'})
 
# =============================
# Employee Profile Update Form
# =============================
class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = '__all__'
        exclude = ['user_info', 'email']
        
    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)
        
        for fields in self.fields.values():
            fields.widget.attrs.update({'class':'form-control'})
            
# =============================
# Client Profile Update Form
# =============================           
class ClientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ClientProfileModel
        fields = '__all__'
        exclude = ['client_info']
        
    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)
        
        for fields in self.fields.values():
            fields.widget.attrs.update({'class':'form-control'}) 