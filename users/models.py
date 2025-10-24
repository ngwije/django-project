from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        return super().save()
    
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    

class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        user = super().create_user(username, email, password, **extra_fields)
        # Automatically create profile
        from users.models import Profile
        Profile.objects.get_or_create(user=user)
        return user
    

def get_user_profile(user):
    from .models import Profile
    profile, created = Profile.objects.get_or_create(user=user)
    return profile

# Add as a property to User model
User.add_to_class('get_profile', get_user_profile)