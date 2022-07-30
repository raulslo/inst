from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models




class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    objects = UserManager()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField('admin', default=False)

    USERNAME_FIELD = 'email'

    ordering = ('created',)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to="", null=True, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)



    def __str__(self):
        return str(self.user)


class Follower(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owner'
    )
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )

