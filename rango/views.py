from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, SuperCategories, Page, UserProfile, Comments, User
from rango.forms import CategoryForm, ContactUsForm, CommentForm
from django.shortcuts import redirect
from rango.forms import PageForm
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user
from datetime import datetime
from urllib.parse import urlencode
from django.conf import settings
from django.contrib import messages
import requests 
import json
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from datetime import date
import urllib
import math

"""
Description: This function connects to the FB API utilizing the API and Secret Key obtained from FB development webpage.
Params: request, request type (whether it is a login or a register)
Return: condition (to indicate the executed path), email/url, user_data (if any)
"""
def connect_to_facebook(request, request_type):
    # uri needed to switch to FB for authorization
    redirect_uri = "%s://%s%s" % (
        request.scheme, request.get_host(), reverse(request_type)
    )
    if('code' in request.GET):
        code = request.GET.get('code')
        url = 'https://graph.facebook.com/v2.10/oauth/access_token'
        params = {
            'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
            'client_secret': settings.SOCIAL_AUTH_FACEBOOK_SECRET,
            'code': code,
            'redirect_uri': redirect_uri,
        }
        response = requests.get(url, params=params)
        params = response.json()
        params.update({
            'fields': 'id,last_name,first_name,picture,birthday,email,gender'
        })
        url = 'https://graph.facebook.com/me'
        
        user_data = requests.get(url, params=params).json() #containes lastname, firstname, email, birthday, profile picture
        email = user_data.get('email')
        return True, email, user_data
    else:
        # send request to FB to get the resources 
        url = "https://graph.facebook.com/oauth/authorize"
        params = {
            'client_id': settings.SOCIAL_AUTH_FACEBOOK_KEY,
            'redirect_uri': redirect_uri,
            'scope': 'email,public_profile,user_birthday'
        }
        url += '?' + urlencode(params)
        return False, url, ""

"""
Description: This function creates a new user upon registration if the email does not already exist
Params: request, email, user_data
"""
def create_facebook_user(request, email, user_data):
    user_auth, _ = User.objects.get_or_create(email=email, username=email)
    #extract all needed data to create a new user in the DB
    gender = user_data.get('gender', '').lower()
    data_of_birth = user_data.get('birthday')
    dob = datetime.strptime(data_of_birth, "%m/%d/%Y") if data_of_birth else None
    gender = 'M' if gender == 'male' else 'F'
    user_profile_picture = user_data.get('picture', {}).get('data', {}).get('url')
    
    data = {
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
    }
    user_auth.__dict__.update(data)
    #Save the user to DB
    user_auth.save()
    user_auth.backend = settings.AUTHENTICATION_BACKENDS[0]
    #save metadata
    user_metadata = UserProfile(gender = gender, dob = dob, facebook = 1, user = user_auth, picture = user_profile_picture)
    user_metadata.save()
    #Login to view the homepage
    login(request, user_auth)

"""
Description: This function allows users to login using Facebook
Params: request
Return: redirect(...)
"""
def facebook_login(request):
    condition, return_string, _ = connect_to_facebook(request, 'rango:facebook_login')
    if condition:
        email = return_string
        if email:
            try:
                #user exists in the DB, so they can login
                user = User.objects.get(email=email, username=email)
                login(request, user)
                return redirect('/')
            except:
                #user doesn't existin the DB, they need to register first
                messages.error(request, 'Sign up first')
                return redirect('/rango/login/')
        else:
            print('Unable to login with Facebook Please try again') #need UI!
        
    else:
        url = return_string
        return redirect(url)

"""
Description: This function allows users to register using Facebook
Params: request
Return: redirect(...)
"""
def facebook_register(request):
    condition, return_string, user_data = connect_to_facebook(request, 'rango:facebook_register')
    if condition:
        email = return_string
        if email:
            try:
                #user already exists in the DB, they can't register to the system multiple times
                user = User.objects.get(email=email, username = email)
                messages.error(request, 'Account already exists')
                return redirect('/rango/register/')
            except:
                #user doesn't exist in the DB, so create a new user with appropriate data
                create_facebook_user(request, email, user_data)
                return redirect('/')
        else:
            print('Unable to login with Facebook Please try again')
    else:
        url = return_string
        return redirect(url)
#-----------------------------------------------------

User = get_user_model()

def add_cat_supcat_pages_context():
    context_dict = {}
    category_list = Category.objects.all()#.order_by('-likes')[:5]
    super_categories_list = SuperCategories.objects.all()[:4] #only taking first 4 to appear in the nav-bar
    page_list = Page.objects.all()
    context_dict['categories'] = category_list
    #superCategories
    context_dict['super_categories'] = super_categories_list
    context_dict['pages'] = page_list
    return context_dict

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits



def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5.
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    context_dict = add_cat_supcat_pages_context()
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    # Render the response and send it back!
    visitor_cookie_handler(request)
    response = render(request, 'rango/index.html', context=context_dict)
    return response

def get_cat(request):
    context_dict = {}
    category_list = Category.objects.all().order_by('-rating')
    listOfCat = []
    for category in category_list:
        page_list = Page.objects.all().filter(category_id=category.id)[:3]
        cat = {}
        cat["title"]=category.name
        cat["slug"]=category.slug
        cat["rating"]=category.rating
        cat["image"]=str(category.image)
        cat["last_modified"]=str(category.last_modified)
        listOfPag = []
        for page in page_list:
            pag = {}
            pag["title"]= page.title
            pag["url"]= page.url
            pag["description"]= page.description
            listOfPag.append(pag)
        cat["pages"] = listOfPag
        listOfCat.append(cat)
        context_dict["categories"]=listOfCat
    return HttpResponse(json.dumps(context_dict))
     
def about(request):
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    context_dict = add_cat_supcat_pages_context()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/about.html', context=context_dict)
    return response

def terms_of_use(request):
    context_dict = add_cat_supcat_pages_context()
    response = render(request, 'rango/terms_of_use.html', context_dict)
    return response

# Create your views here.
def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = add_cat_supcat_pages_context()
    current_user = get_user(request)
    
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    if category == None:
        return redirect(reverse('rango:index'))
    
    try:
        if (not current_user.is_anonymous) and (current_user is not None):
            profile = UserProfile.objects.get(user=current_user)
    except UserProfile.DoesNotExist:
        profile = None
        
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        # Adds our results list to the template context under name pages.
        #Fetch all the comments
        comment_list = Comments.objects.filter(category=category)
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        context_dict['comments'] = comment_list
         #Get user instance
        user = current_user
        if (not user.is_anonymous) and (user is not None):
            #Get all the favorite pages of the user and send to render on page
            context_dict['fav_list'] = user.pages.all()
        else:
            context_dict['fav_list'] = None
        if (not user.is_anonymous) and (user is not None):    
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    if category and profile:
                        comment = form.save(commit=False)
                        comment.category = category
                        comment.date = date.today()
                        comment.profileInfo = profile
                        comment.save()
                    return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
                else:
                    print(form.errors)        
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
        context_dict['comments'] = None
        context_dict['forms'] = None 
    form = CommentForm()
    context_dict['form'] = form 
        #It is not a post request, it is a get request and render the comment form to the user
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request, username):
    context_dict = add_cat_supcat_pages_context()
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        mytitle = request.POST.get('title')
        try:
            super_category = SuperCategories.objects.get(pk = mytitle)
        except SuperCategories.DoesNotExist:
            super_category = None

        try:
            user = User.objects.get(username = username)
        except SuperCategories.DoesNotExist:
            user = None

         # You cannot add a page to a Category that does not exist...
        if super_category is None:
            return redirect('/rango/')
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            category = form.save(commit=False)
            if 'image' in request.FILES:
                category.image = request.FILES.get('image')
            category.super_cat = super_category
            # category.user = user
            category.save()
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
            # Will handle the bad form, new form, or no form supplied cases.
            # Render the form with error messages (if any).
    context_dict['form'] = form
    return render(request, 'rango/add_category.html', context_dict)

def rate_category(request, category_name_slug,star):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        return HttpResponse("Failed to get") 
    # You cannot add a page to a Category that does not exist...
    sum = category.rating_sum_val
    count = category.rating_sum_val 
    if request.method == 'GET':
        category.rating_sum_val = sum + int(star)
        category.rating_count_val = count + 1
        try:
            category.rating = math.ceil(category.rating_sum_val / category.rating_count_val) #divide by zero!
        except:
            category.rating = category.rating_sum_val
        category.save()
    return HttpResponse("success")   
    

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    context_dict = add_cat_supcat_pages_context()
    context_dict['form'] = form
    context_dict['category'] = category
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model

            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = add_cat_supcat_pages_context()
    context_dict['user_form']= user_form
    context_dict['profile_form']= profile_form
    context_dict['registered'] =  registered
    # Render the template depending on the context.
    return render(request,'rango/register.html',context = context_dict)

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    context_dict = add_cat_supcat_pages_context()
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
            # The request is not a HTTP POST, so display the login form.
        
            # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', context_dict)

#Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))

#View for saving a favorite page
class SaveFavoriteView(View):
    #only authenticated users can add a favorite page
    @method_decorator(login_required)
    #handle ajax get request
    def get(self, request):
        #Fetch id of page to save
        page_id = request.GET['page_id']
        #exception handling for fetching the page from DB
        try:
            page = Page.objects.get(id=int(page_id))
        except Page.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        #Link user to the saved page and save the association in database
        page.favorite.add(get_user(request))
        page.save()
        #return response 
        return HttpResponse("success")
        
#View for removing a page from favorites
class UnsaveFavoriteView(View):
    #only authenticated users can add a favorite page
    @method_decorator(login_required)
    #handle ajax get request
    def get(self, request):
        #Fetch id of page to save
        page_id = request.GET['page_id']
        #exception handling for fetching the page from DB
        try:
            page= Page.objects.get(id=int(page_id))
        except Page.DoesNotExist:
                return HttpResponse(-1)
        except ValueError:
                return HttpResponse(-1)
        #Delete saved page from the fav list
        user = get_user(request)
        to_remove = user.pages.all().filter(id=page_id)
        user.pages.remove(to_remove[0])
        user.save()
        #return response
        return HttpResponse("success")

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
            print(user)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website, 'picture':user_profile.picture})
        return (user, user_profile, form)
    @method_decorator(login_required)
    def get(self, request, username):
        #Render saved list 
        fav_list = get_user(request).pages.all()
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        context_dict = add_cat_supcat_pages_context()
        context_dict['user_profile'] = user_profile
        context_dict['selected_user']= user
        context_dict['form'] = form 
        context_dict['pages']=fav_list
        return render(request, 'rango/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        context_dict = add_cat_supcat_pages_context()
        try:
            (user, user_profile, form) = self. get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
        context_dict['user_profile'] = user_profile
        context_dict['selected_user']= user, 
        context_dict['form']=form
        return render(request, 'rango/profile.html', context_dict)

#View for the cantact us form
class ContactUsView(View):
    #get request to show user the empty form
    def get(self,request):
        context_dict = add_cat_supcat_pages_context()
        form = ContactUsForm()
        context_dict['form'] = form
        return render(request, 'rango/contact_us.html', context_dict) 
    
    #post request to take input from user in a form and store it in the database
    def post(self, request):
        context_dict = add_cat_supcat_pages_context()
        form = ContactUsForm(request.POST)
        #verify form is valid
        if form.is_valid():
            #save the valid form in the database
            form.save(commit=True)
            #redirect user upon successful posting of the comment
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        #If the user reaches here there was some error in the form so re render the form
        context_dict['form'] = form
        return render(request, 'rango/contact_us.html', context_dict)
 