from django.urls import path
from job_find.views import *

urlpatterns = [
    path('', home_page, name='home_page'),
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    
    path('profile/', profile_page, name='profile_page'),
    path('profile-update/', profile_update, name='profile_update'),

    path('jobs/', job_list, name='job_list'),
    path('job-post/', job_post, name='job_post'),
    path('edit-job/<int:job_id>/', edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', delete_job, name='delete_job'),

    path('apply-now/<int:job_id>/', apply_now, name='apply_now'),
    path('applied-jobs/', applied_job_list, name='applied_job_list'),
    path('candidates/<int:job_id>/', candidate_list, name='candidate_list'),
]
