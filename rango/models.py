from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from rango.maxVal import maxLength128, maxLength150, maxLength256
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# This table extends the User model in django to add some more user fields we need in Rango
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField(blank=True, null=True)
    facebook = models.BooleanField(default = False)
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(default = "", blank = True)
    picture = models.ImageField(upload_to='profile_images', default="", blank = True)
    def __str__(self):
        return self.user.username

# This table contains all super categories in the syste, --> each super category can contains more than one category
class SuperCategories(models.Model):
    # super category title
    title = models.CharField(max_length=maxLength128)
    def __str__(self):
        return self.title

class Category(models.Model):
    # super category to which the category belongs to
    super_cat = models.ForeignKey(SuperCategories, on_delete=models.CASCADE)
    # category title
    name = models.CharField(max_length=maxLength128, unique=True)
    # category ranking and helper columns to calculate an average for the submitted ratings
    rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ])
    rating_sum_val = models.IntegerField(default=0, blank = True)
    rating_count_val = models.IntegerField(default=0, blank=True)
    # category image and last_modified date
    image = models.ImageField(upload_to='', default="", blank = True)
    last_modified = models.DateField(default=datetime.date.today, blank = True)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

class Page(models.Model):
    # category to which the page belongs
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # page basic details: title, url and description for what it talks about
    title = models.CharField(max_length=maxLength128)
    url = models.URLField()
    description = models.CharField(max_length=maxLength128, blank = False, default = "")
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
    profileInfo = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #Link comment to the category it is meant for
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #Comment description/text
    description = models.CharField(max_length=maxLength256)
    #date the comment was made
    date = models.DateField(default=date.today, blank=True, null=True)