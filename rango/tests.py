import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rango.models import Enquiries, Page, Category, SuperCategories, UserProfile, Comments
from django.contrib.auth import get_user_model
from rango.forms import CommentForm, ContactUsForm, CategoryForm
from django.forms import fields as django_fields
from django.forms import ModelChoiceField
import datetime

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}==================================={os.linesep}TEST FAILURE={os.linesep}=================================={os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

#helper function to populat database
def create_user(username, password):
    user = get_user_model().objects.create_user(username=username)
    user.set_password(password)
    user.save()
    return user

def create_user_profile(user):
    profile,__ = UserProfile.objects.update_or_create(gender = 'F',
                                                   defaults={
                                                   'user': user})
    return profile
#helper function to populat database
def create_category(name, super, user,date,sum=0,count=0):
    category, __ = Category.objects.update_or_create(
        name=name,
        defaults={'super_cat': super},
        last_modified = date,
        rating_sum_val = sum,
        rating_count_val = count
    )
    return category

def create_super_category(title):
    super = SuperCategories.objects.create(title=title)
    super.save()
    return super

#helper function to populat database
def add_page(title, url, cat , user):
    page , __ = Page.objects.update_or_create(
        title=title,
        url = url,
        defaults={'category':cat}
    )
    return page
    #page.favorite.add(user)

def create_comment(profile, cat):
    comment, __ = Comments.objects.update_or_create(
        defaults= {'profileInfo' : profile,
        'category' : cat}
    )
    return comment

def create_enquiry(fname, lname, email):
    enquiry, __ = Enquiries.objects.update_or_create(
    first_name = fname,
    last_name = lname,
    email = email,
    defaults={
    #Field to store comments of user for the issue, suggestion etc.
    'description': "This is first enquiry"})
    return enquiry
    
# The following test is for the save and deleting of
# a page from the favorites list
class TestFavoritesFeature(TestCase):
    def setUp(self):
        self.user = create_user("testUser", "testPassword")
        self.super = create_super_category('Frameworks')
        self.cat = create_category('python', self.super, self.user,datetime.datetime.now().date())
        self.page= add_page('learn x in y minutes','https://learnxinyminutes.com/docs/python', self.cat,self.user)        
        login = self.client.login(username='testUser', password='testPassword')
        
    def tearDown(self):
        self.user.delete()
        self.super.delete()
        self.cat.delete()
        self.page.delete()
        
    def test_save_list_view(self):
        #self.response= self.client.get(reverse('rango:profile', kwargs={'username':self.user.username}))
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.content = self.response.content.decode()
        
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'rango/category.html')

    def test_database_single_entry(self):
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page.id
        })
        self.assertEquals(self.response.status_code, 200)
        self.assertEquals(self.user.pages.first().title, 'learn x in y minutes')
        self.assertEquals(len(self.user.pages.all()), 1)
        
        self.response = self.client.post(reverse('rango:unsave_favorite'),{
            'page_id': self.page.id
        })
        #print(self.response.context)
        self.assertEquals(self.response.status_code, 200)
        self.assertNotEquals(len(self.user.pages.all()),1 )
        self.assertEquals(len(self.user.pages.all()),0 )
    def test_database_no_entry(self):
        pass
    def test_database_get_saved_and_save_unsaved_pages(self):
        pass
    
class ContactUsFeature(TestCase):
    def setUp(self):
        self.user = create_user("testUser", "testPassword")
        self.super = create_super_category('Frameworks')
        self.cat = create_category('python', self.super, self.user, datetime.datetime.now().date()) 
        self.enquiry = create_enquiry("John", "Doe", "test@test.com")
        login = self.client.login(username='testUser', password='testPassword')
        
    def tearDown(self):
        self.user.delete()
        self.super.delete()
        self.cat.delete()
        self.enquiry.delete()
        
    def test_contact_us_view(self):
        
        self.response = self.client.get(reverse('rango:contact_us'))
        self.content = self.response.content.decode()

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'rango/contact_us.html')
    
    def test_contact_us_form(self):
        comment_form = ContactUsForm()
        self.assertEqual(type(comment_form.__dict__['instance']), Enquiries, f"{FAILURE_HEADER}The class contact us form could not be found in forms.py module.{FAILURE_FOOTER}")
        
        fields = comment_form.fields
        
        expected_fields = {
            'first_name': django_fields.CharField,
            'last_name': django_fields.CharField,
            'description': django_fields.CharField,
            'email':django_fields.EmailField
        }
        
        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]
            # f"{FAILURE_HEADER}{FAILURE_FOOTER}"
            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in ContactUsForm implementation'{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field '{expected_field_name}' in ContactUsForm was not of the expected type '{type(fields[expected_field_name])}'{FAILURE_FOOTER}")

    def test_response(self):
        response = self.client.get(reverse('rango:contact_us'))
        context = response.context
        content = response.content.decode()
        
        self.assertTrue('form' in context)
        self.assertTrue('<h6>Contact Us</h6>' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('<h1>Tell us your enquiry, we will get back to you in 3 to 5 working days</h1>' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('name="first_name"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('name="last_name"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('name="email"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('name="description"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('<input type="submit" name="submit" value="Submit" />' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('action="/rango/contactus/"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
    
    def test_functionality(self):
        self.client.post(reverse('rango:contact_us'),
                         {'first_name':'Erlang','last_name':'Gartner', 'email':'test@test.com', 'description':'This is test enquiry, can be a maximum of 150 words'})
        
        enquiry = Enquiries.objects.filter(first_name='Erlang')
        enquiry1 = enquiry[0]
        self.assertEqual(len(enquiry), 1, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertEqual(enquiry1.first_name, 'Erlang',  f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertEqual(enquiry1.last_name, 'Gartner', f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertEqual(enquiry1.email, 'test@test.com', f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertEqual(enquiry1.description, 'This is test enquiry, can be a maximum of 150 words', f"{FAILURE_HEADER}{FAILURE_FOOTER}")


class CommentsFeature(TestCase):
    def setUp(self):
        self.user = create_user("testUser", "testPassword")
        login = self.client.login(username='testUser', password='testPassword')
        
        self.super = create_super_category('Frameworks')
        self.cat = create_category('python', self.super, self.user, datetime.datetime.now().date())
        self.profile = create_user_profile(self.user) 
        self.page= add_page('learn x in y minutes','https://learnxinyminutes.com/docs/python', self.cat,self.user)
        self.comment = create_comment(self.profile, self.cat)
        
    def tearDown(self):
        self.user.delete()
        self.super.delete()
        self.cat.delete()
        self.profile.delete()
        self.comment.delete()
        self.page.delete()
        
    def test_comments_view(self):
        
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.content = self.response.content.decode()

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'rango/category.html')
    
    def test_comments_form(self):
        comment_form = CommentForm()
        self.assertEqual(type(comment_form.__dict__['instance']), Comments, f"{FAILURE_HEADER}The class comments form could not be found in forms.py module.{FAILURE_FOOTER}")
        
        fields = comment_form.fields
        
        expected_fields = {
            'description': django_fields.CharField
        }
        
        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]
            # f"{FAILURE_HEADER}{FAILURE_FOOTER}"
            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in CommentsForm implementation'{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field '{expected_field_name}' in CommentsForm was not of the expected type '{type(fields[expected_field_name])}'{FAILURE_FOOTER}")

    def test_response(self):
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        context = response.context
        content = response.content.decode()
        
        self.assertTrue('form' in context)
        self.assertTrue('comments' in context)
        self.assertTrue('<h1>Comments</h1>' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        #if context.comments != None
        self.assertTrue('id="comment_container"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('name="description"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('<input type="submit" name="submit" value="Post" />' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('action="/rango/category/python/"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
    
    def test_functionality(self):
        self.client.post(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}),
                         {  'profileInfo': self.profile,
                             'description':'This is test enquiry, can be a maximum of 256 words'})
        
        comment = Comments.objects.filter(description='This is test enquiry, can be a maximum of 256 words')
        comment1 = comment[0]
        self.assertEqual(len(comment), 1, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertEqual(comment1.profileInfo, self.profile,  f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertEqual(comment1.category.name, 'python', f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertEqual(comment1.description, 'This is test enquiry, can be a maximum of 256 words', f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        #Date not in future


#testinf the rating functionality in both home page and category page
class Rating_Feature_In_Home_and_Category_Pages(TestCase):
    #creating some records to test with
    @classmethod
    def setUpTestData(self):
        self.user = create_user("testUser", "testPassword")
        self.super = create_super_category('Frameworks')
        self.cat1 = create_category('python', self.super, self.user, datetime.datetime.now().date(),110,16)
        self.page= add_page('learn x in y minutes','https://learnxinyminutes.com/docs/python', self.cat1,self.user)
        self.cat2 = create_category('algorithms', self.super, self.user, datetime.datetime.now().date())

    #testing that all urls work fine
    def test_getcategories_and_index_view_url_exists_at_desired_location(self):
        response = self.client.get('/rango/get_cat/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/rango/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/rango/category/python/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/rango/rate_category/python/0')
        self.assertEqual(response.status_code, 200)

    #testing all views working by name
    def test_getcategories_and_index_view_url_accessible_by_name(self):
        response = self.client.get(reverse('rango:get_cat', kwargs={}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rango:index', kwargs={}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.assertEqual(response.status_code, 200)
        response = self.response = self.client.get(reverse('rango:rate_category', kwargs={'category_name_slug': 'python','star':'0'}))
        self.assertEqual(response.status_code, 200)

    #testing that index view uses the correct template index.html
    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rango/index.html')

    #testing json response of get categories  api
    def test_getcategories_view_json_response(self):
        response = self.client.get('/rango/get_cat/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"categories": [{"title": "python", "slug": "python", "rating": 0, "image": "", "last_modified":datetime.datetime.now().date().strftime('%Y-%m-%d'), "pages": [{"title": "learn x in y minutes", "url":"https://learnxinyminutes.com/docs/python", "description": ""}]},{"title": "algorithms", "slug": "algorithms", "rating": 0, "image": "", "last_modified":datetime.datetime.now().date().strftime('%Y-%m-%d'), "pages": []}]})
    
    #testing http response of rateCategory api based on different rating inputs
    def test_rateCategory_view_response(self):
        response = self.response = self.client.get(reverse('rango:rate_category', kwargs={'category_name_slug': 'python','star':'5'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rating cannot exceed 5')
        response = self.response = self.client.get(reverse('rango:rate_category', kwargs={'category_name_slug': 'algorithms','star':'0'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Success')

    #testind database record update (rating) after calling rate_category api
    def test_database_rating_update_entry(self):
        response = self.response = self.client.get(reverse('rango:rate_category', kwargs={'category_name_slug': 'algorithms','star':'5'}))
        category = Category.objects.get(name='algorithms')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(category.rating, 5)
    
        #testing html response includes rating part
    def test_show_category_response_html(self):
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        content = response.content.decode()

        self.assertTrue('<div class="rate">' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('<input type="radio" id="star5" name="rate" value="5" />' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('<input type="radio" id="star4" name="rate" value="4" />' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('<input type="radio" id="star3" name="rate" value="3" />' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('<input type="radio" id="star2" name="rate" value="2" />' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('<input type="radio" id="star1" name="rate" value="1" />' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")