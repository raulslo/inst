from django.contrib import admin
from user.models import User, UserProfile, Follower


admin.site.register(Follower)
admin.site.register(User)
admin.site.register(UserProfile)