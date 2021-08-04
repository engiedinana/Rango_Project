from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from rango.maxVal import maxLength128, maxLength150
from django.core.validators import MaxValueValidator, MinValueValidator


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
    title = models.CharField(max_length=maxLength128, unique=True)
    rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ])
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
    #UserProfile = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=maxLength128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    #Many users can have many favorite pages
    favorite = models.ManyToManyField(User, related_name='pages')
    def __str__(self):
        return self.title
"""
class SavedPages(models.Model):
    UserProfile = models.ForeignKey(User, on_delete=models.CASCADE)
    Page = models.ForeignKey(Page, on_delete=models.CASCADE)
"""

class Enquiries(models.Model):
    first_name = models.CharField(max_length=maxLength128)
    last_name = models.CharField(max_length=maxLength128)
    description = models.CharField(max_length=maxLength150)
    email = models.EmailField(max_length=maxLength128)

class Comments(models.Model):
    UserProfile = models.ForeignKey(User, on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date = models.DateField()