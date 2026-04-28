from django.contrib import admin
from job_find.models import *

admin.site.register(UserInfoModel)
admin.site.register(UserProfileModel)
admin.site.register(ClientProfileModel)
admin.site.register(JobPostModel)
admin.site.register(JobApplyModel)
admin.site.register(CategoryModel)