import os
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rango.models import Enquiries, Page, Category, SuperCategories, UserProfile, Comments
from django.contrib.auth import get_user_model
from rango.forms import CommentForm, ContactUsForm
from django.forms import fields as django_fields
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
    profile = UserProfile.objects.update_or_create(gender = 'F',
                                                   user = user)
#helper function to populat database
def create_category(name, super, user,date):
    category, __ = Category.objects.update_or_create(
        name=name,
        defaults={'super_cat': super},
        last_modified = date
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
        profile_info = profile,
        category = cat,
        description = "This is a comment"
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
        self.response = self.client.get(reverse('rango:save_favorite'),{
            'page_id': self.page.id
        })
        self.assertEquals(self.response.status_code, 200)
        self.assertEquals(self.user.pages.first().title, 'learn x in y minutes')
        self.assertEquals(len(self.user.pages.all()), 1)
        
        self.response = self.client.get(reverse('rango:unsave_favorite'),{
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
   
"""
class TestRatingFeature(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = create_user("testUser", "testPassword")
        self.super = create_super_category('Frameworks')
        self.cat = create_category('python', self.super, self.user, datetime.datetime.now().date())
        self.page= add_page('learn x in y minutes','https://learnxinyminutes.com/docs/python', self.cat,self.user) 
    # def test_rating_view(self):
    #     self.response = self.client.get(reverse('rango:get', kwargs={'category_name_slug': 'python'}))
    #     self.content = self.response.content.decode()
    #-ve rating boundries super categories
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('rango:get_cat', kwargs={}))
        self.assertEqual(response.status_code, 200)
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/rango/')
        self.assertEqual(response.status_code, 200)
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('rango:index', kwargs={}))
        self.assertEqual(response.status_code, 200)
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rango/index.html')
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/rango/get_cat/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"categories": [{"title": "python", "slug": "python", "rating": 0, "image": "", "last_modified":datetime.datetime.now().date().strftime('%Y-%m-%d'), "pages": [{"title": "learn x in y minutes", "url":"https://learnxinyminutes.com/docs/python", "description": ""}]}]})
    # self.assertJSONEqual(
    #     str(response.content, encoding='utf8'),
    #     {'status': 'success'}
    # )
    # def test_lists_all_authors(self):
    #     # Get second page and confirm it has (exactly) remaining 3 items
    #     response = self.client.get(reverse('index'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertEqual(len(response.context['author_list']), 3)
    """