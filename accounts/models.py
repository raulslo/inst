from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



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
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE, related_name="profile")
    age = models.IntegerField(blank=True, null=True)
    photo = models.ImageField( upload_to="profile_image")
    follows = models.ManyToManyField("UserProfile", related_name="followed_by")
    description = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return f'{self.user} Profile'



    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            UserProfile.objects.create(user=instance)
