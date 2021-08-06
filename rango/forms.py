from django import forms
from rango.models import Comments, Page, Category, Enquiries, SuperCategories
from django.contrib.auth.models import User
from rango.models import UserProfile
from rango.maxVal import maxLength128,maxLength200,maxLength150,maxLength256

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=maxLength128, help_text="Please enter the category name.")
    # the title represents the super category this category will belong to .. the user should choose from a predefined list containing the super categories in the DB
    title = forms.ModelChoiceField(queryset=SuperCategories.objects.all(), empty_label="Select Topic", help_text= "Select a topic that fits the category:")
    # the user will be asked to upload an image to represent the category, if they don't do that, a default image will be used
    image = forms.ImageField(help_text="Please add an image:", required=False)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        # added the new fields: title and image
        fields = ('name', 'title', 'image')

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=maxLength128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=maxLength200, help_text="Please enter the URL of the page.")
    # Users will now be asked to add a description for the page so that users can check when hovering over the page link
    description = forms.CharField(max_length=maxLength128, help_text="Please enter the description of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # suppoerting both http and https links
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
class UserForm(forms.ModelForm):
    # these are the fields that are available in the built in User in django
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    first_name = forms.CharField(max_length=maxLength128, widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=maxLength128, widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    # extra fields we need to extend the User: gender, dob, website and picture --> if a user doesn't upload an image, a default one will be used
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    class Meta:
        model = UserProfile
        fields = ('gender', 'dob', 'website', 'picture',)

class ContactUsForm(forms.ModelForm):
    # this form allows users to submit enquiries/issues by providing their details
    first_name = forms.CharField(max_length=maxLength128, widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=maxLength128, widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    description = forms.CharField(max_length=maxLength150, widget=forms.Textarea(attrs={'placeholder':'Write your enquiry here in 150 words'}))
    email = forms.EmailField(max_length=maxLength128, widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Enquiries
        fields = ('first_name','last_name', 'email', 'description',)
        
class CommentForm(forms.ModelForm):
    # this forms allows users to engage through comments. They need to provide a description.
    description = forms.CharField(max_length=maxLength256, widget=forms.TextInput(attrs={'placeholder': 'Write your comment in 256 words'}))
    class Meta:
        model = Comments
        fields=('description',)