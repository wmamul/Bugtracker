from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.username, ext)
    return os.path.join('profile_pics', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=rename_image)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=30)
    
    def __str__(self):
        return "%s profile" %self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
