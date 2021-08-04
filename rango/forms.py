from datetime import datetime
from django import forms
from rango.models import Comments, Page, Category, Enquiries, SuperCategories
from django.contrib.auth.models import User
from rango.models import UserProfile
from rango.maxVal import maxLength128,maxLength200,maxLength150,maxLength256
import datetime

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=maxLength128, help_text="Please enter the category name.")
    #views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    title = forms.ModelChoiceField(queryset=SuperCategories.objects.all().order_by('title'), empty_label="Select Topic")
    #last_modified = forms.DateField(initial=datetime.date.today)
    #rating = forms.FloatField()
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name', 'title')

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=maxLength128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=maxLength200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = f'https://{url}'
            cleaned_data['url'] = url
        return cleaned_data
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values; we may not want to include them.
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category','favorite', 'UserProfile')
        # or specify the fields to include (don't include the category field).
        #fields = ('title', 'url', 'views')
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    first_name = forms.CharField(max_length=maxLength128, widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=maxLength128, widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    # website = forms.URLField(widget=forms.URLInput(), required=True, initial='http://')
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    class Meta:
        model = UserProfile
        fields = ('gender', 'dob', 'website', 'picture',)

class ContactUsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=maxLength128, widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=maxLength128, widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    description = forms.CharField(max_length=maxLength150, widget=forms.Textarea(attrs={'placeholder':'Write your enquiry here in 150 words'}))
    email = forms.EmailField(max_length=maxLength128, widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Enquiries
        fields = ('first_name','last_name', 'email', 'description',)
        
class CommentForm(forms.ModelForm):
    #description in comment
    description = forms.CharField(max_length=maxLength256, widget=forms.TextInput(attrs={'placeholder': 'Write your comment in 256 words'}))
    class Meta:
        model = Comments
        fields=('description',)