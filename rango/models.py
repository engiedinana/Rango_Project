from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from rango.maxVal import maxLength128, maxLength150


class UserProfile(models.Model):
    """GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    first_name = models.CharField(max_length=maxLength128)
    last_name = models.CharField(max_length=maxLength128)
    username = models.CharField(max_length=maxLength128, unique=True)
    email = models.EmailField(max_length=maxLength128, unique=True)
    dob = models.DateField()
    facebook = models.BooleanField(blank=True)
    """
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username
"""
class SuperCategories(models.Model):
    title = models.CharField(max_length=maxLength128)
"""
class Category(models.Model):
    #super_cat = models.ForeignKey(SuperCategories, on_delete=models.CASCADE)
    #user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=maxLength128, unique=True)
    #rating = models.FloatField(max_length=maxLength128)
    #image = models.ImageField(upload_to='', blank=True)
    #last_modified = models.DateField()

    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=maxLength128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    #Many users can have many favorite pages
    favorite = models.ManyToManyField(User, related_name='pages')
    def __str__(self):
        return self.title

#Table for storing user requests, suggestions, complaints and handling via admin
class Enquiries(models.Model):
    #Basic user details
    first_name = models.CharField(max_length=maxLength128)
    last_name = models.CharField(max_length=maxLength128)
    email = models.EmailField(max_length=maxLength128)
    #Field to store comments of user for the issue, suggestion etc.
    description = models.CharField(max_length=maxLength150)
   
#Table for storing user comments on a category
class Comments(models.Model):
    #Link comment to the category it is meant for
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #Comment description
    description = models.TextField()
    #date the comment was made
    date = models.DateField()