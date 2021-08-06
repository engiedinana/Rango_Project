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
from datetime import date

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}==================================={os.linesep}TEST FAILURE={os.linesep}=================================={os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

#helper function to populat database
def create_user(username, password):
    user = get_user_model().objects.create_user(username=username)
    user.set_password(password)
    user.save()
    return user

#helper function to populat database
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

#helper function to populat database
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
    
#helper function to populat database
def create_comment(profile, cat):
    comment, __ = Comments.objects.update_or_create(
        defaults= {'profileInfo' : profile,
        'category' : cat}
    )
    return comment

#helper function to populat database
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
    #Create a single entry of a category and a page to get started
    def setUp(self):
        self.user = create_user("testUser", "testPassword")
        self.super = create_super_category('Frameworks')
        self.cat = create_category('python', self.super, self.user,datetime.datetime.now().date())
        self.page= add_page('learn x in y minutes','https://learnxinyminutes.com/docs/python', self.cat,self.user)        
        login = self.client.login(username='testUser', password='testPassword')

    def tearDown(self):
        self.cat.delete()
        self.super.delete()
        
    #This test was just a first test to see this file works. 
    # It tests rango's show_category page is routable    
    def test_save_list_view(self):
        
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.content = self.response.content.decode()
        
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'rango/category.html')
        
    #This test is for testing the corner case of just a single entry of page(done in setup function) 
    # in the show category page
    def test_database_single_entry(self):
        # Test a post request for saving page
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page.id
        })
        self.assertEquals(self.response.status_code, 200)
        #Retrievable from DB after the post request
        self.assertEquals(self.user.pages.first().title, 'learn x in y minutes')
        self.assertEquals(len(self.user.pages.all()), 1)
        
    #This test extends from the above test and tests the removal of a page
    #after a inserting into  favorite list of a single entry 
    def test_database_single_entry_2(self):
        ####### SETUP ########
        # Test a post request for saving page
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page.id
        })
        self.assertEquals(self.response.status_code, 200)
        #Retrievable from DB after the post request
        self.assertEquals(self.user.pages.first().title, 'learn x in y minutes')
        self.assertEquals(len(self.user.pages.all()), 1)
        #Create a post request for removing page from the saved list
        
        ###### UNIT TEST #####
        self.response = self.client.post(reverse('rango:unsave_favorite'),{
            'page_id': self.page.id
        })  
        self.assertEquals(self.response.status_code, 200)
        #Change is reflected in the DB from the old state to the new state
        self.assertNotEquals(len(self.user.pages.all()),1 )
        self.assertEquals(len(self.user.pages.all()),0 )
    
    #This test checks for the saving and unsaving of pages when many pages are present in 
    #a single category
    def test_database_multiple_pages_in_category(self):
        ########## SETUP ###########
        self.page1= add_page('dummies','https://www.dummies.com/computers/', self.cat,self.user)        
        self.page2= add_page('official','https://www.python.org/', self.cat,self.user)
        self.assertIsInstance(self.cat, Category)
        self.assertIsInstance(self.super,SuperCategories)
        
        #First vist the show category page
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.assertEquals(self.response.status_code, 200)
        self.content = self.response.content.decode()
        #Verify appropritae buttons/icons are displayed/hidden on the UI since the
        #user is logged in and there are pages on the page, The feature is supposed to be active
        self.assertTrue('class="hide"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('class="show"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        
        ########## UNIT TEST (SAVE 2 PAGES) #########
        #Save multiple pages in a category
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page1.id
        })
        self.assertEquals(self.response.status_code, 200)
        
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page2.id
        })
        self.assertEquals(self.response.status_code, 200)
        #Now verify 
        #Verify the post request has updated the database
        self.assertEquals(self.user.pages.all()[0].title, 'dummies')
        self.assertEquals(self.user.pages.all()[1].title, 'official')
        #There are two post request so 2 pages should be there in the fav list
        self.assertEquals(len(self.user.pages.all()), 2)
        
    #This test extends from the above test and now tests only the deletion in scenario
    #where multiple pages are saved.
    def test_deleting_when_multiple_pages_are_saved(self):
        ########### SETUP ###########
        self.page1= add_page('dummies','https://www.dummies.com/computers/', self.cat,self.user)        
        self.page2= add_page('official','https://www.python.org/', self.cat,self.user)
        self.assertIsInstance(self.cat, Category)
        self.assertIsInstance(self.super,SuperCategories)
        
        #First vist the show category page
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.assertEquals(self.response.status_code, 200)
        self.content = self.response.content.decode()
        #Verify appropritae buttons/icons are displayed/hidden on the UI since the
        #user is logged in and there are pages on the page, The feature is supposed to be active
        self.assertTrue('class="hide"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('class="show"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        
        #Save multiple pages in a category
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page1.id
        })
        self.assertEquals(self.response.status_code, 200)
        
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page2.id
        })
        self.assertEquals(self.response.status_code, 200)
        #Now verify 
        #Verify the post request has updated the database
        self.assertEquals(self.user.pages.all()[0].title, 'dummies')
        self.assertEquals(self.user.pages.all()[1].title, 'official')
        #There are two post request so 2 pages should be there in the fav list
        self.assertEquals(len(self.user.pages.all()), 2)
        
        ################ UNIT TEST ################ 
        #Create a post request for removing page from the saved list with multiple pages in it
        self.response = self.client.post(reverse('rango:unsave_favorite'),{
            'page_id': self.page1.id
        })  
        self.assertEquals(len(self.user.pages.all()), 1)
    
    #This test case extends from the basic funtionality covered in the above test cases
    #So the scenario is user does some saving then a unsaving operation
    #then routed to another page to be routed back and see the saved changes
    def route_to_another_page_then_route_back_to_the_show_category_page(self):
        ########## SETUP ##############
        self.page1= add_page('dummies','https://www.dummies.com/computers/', self.cat,self.user)        
        self.page2= add_page('official','https://www.python.org/', self.cat,self.user)
        self.assertIsInstance(self.cat, Category)
        self.assertIsInstance(self.super,SuperCategories)
        
        #First vist the show category page
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.assertEquals(self.response.status_code, 200)
        self.content = self.response.content.decode()
        #Verify appropritae buttons/icons are displayed/hidden on the UI since the
        #user is logged in and there are pages on the page, The feature is supposed to be active
        self.assertTrue('class="hide"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('class="show"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        
        #Save multiple pages in a category
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page1.id
        })
        self.assertEquals(self.response.status_code, 200)
        
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page2.id
        })
        self.assertEquals(self.response.status_code, 200)
        #Now verify 
        #Verify the post request has updated the database
        self.assertEquals(self.user.pages.all()[0].title, 'dummies')
        self.assertEquals(self.user.pages.all()[1].title, 'official')
        #There are two post request so 2 pages should be there in the fav list
        self.assertEquals(len(self.user.pages.all()), 2)   
        #Create a post request for removing page from the saved list
        self.response = self.client.post(reverse('rango:unsave_favorite'),{
            'page_id': self.page1.id
        })  
        self.assertEquals(len(self.user.pages.all()), 1)
        
        
        ########## UNIT TEST (with the setup ready, now reroute ) ############
        #Route to another page and come back to the page to see the same fav list with one saved
        #entry and three total entry
        self.response = self.client.get(reverse('rango:index'))
        self.assertEquals(self.response.status_code, 200)
        
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.content = self.response.content.decode()
        self.assertEquals(self.response.status_code, 200)
        
        #DB should be updated and shows one less entry
        self.assertEquals(len(self.user.pages.all()), 1)
        self.assertEquals(len(Page.objects.all(), 3))
    
    def test_save_all_pages_present(self):
        ########## SETUP #############
        self.page1= add_page('dummies','https://www.dummies.com/computers/', self.cat,self.user)        
        self.page2= add_page('official','https://www.python.org/', self.cat,self.user)
        self.assertIsInstance(self.cat, Category)
        self.assertIsInstance(self.super,SuperCategories)
        
        #First vist the show category page
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.assertEquals(self.response.status_code, 200)
        self.content = self.response.content.decode()
        #Verify appropritae buttons/icons are displayed/hidden on the UI since the
        #user is logged in and there are pages on the page, The feature is supposed to be active
        self.assertTrue('class="hide"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('class="show"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        
        ############## UNIT TEST (save all 3 pages ) ############33333
        #Save multiple pages in a category
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page1.id
        })
        self.assertEquals(self.response.status_code, 200)
        
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page2.id
        })
        self.assertEquals(self.response.status_code, 200)
    
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page.id
        })
        self.assertEquals(self.response.status_code, 200)
        self.assertEquals(len(self.user.pages.all()), len(Page.objects.all()))
    
    #this test extends from the above setup and deletes all the saved pages
    def test_unsave_all_pages(self): 
        ####################### SETUP ##########################
        self.page1= add_page('dummies','https://www.dummies.com/computers/', self.cat,self.user)        
        self.page2= add_page('official','https://www.python.org/', self.cat,self.user)
        self.assertIsInstance(self.cat, Category)
        self.assertIsInstance(self.super,SuperCategories)
        
        #First vist the show category page
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.assertEquals(self.response.status_code, 200)
        self.content = self.response.content.decode()
        #Verify appropritae buttons/icons are displayed/hidden on the UI since the
        #user is logged in and there are pages on the page, The feature is supposed to be active
        self.assertTrue('class="hide"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('class="show"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        
        #Save multiple pages in a category
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page1.id
        })
        self.assertEquals(self.response.status_code, 200)
        
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page2.id
        })
        self.assertEquals(self.response.status_code, 200)
    
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page.id
        })
        
        self.assertEquals(self.response.status_code, 200)
        self.assertEquals(len(self.user.pages.all()), 3)
        ############### UNIT TEST : UNSAVE ALL ###################
        #Save multiple pages in a category
        self.response = self.client.post(reverse('rango:unsave_favorite'),{
            'page_id': self.page1.id
        })
        self.assertEquals(self.response.status_code, 200)
        
        self.response = self.client.post(reverse('rango:unsave_favorite'),{
            'page_id': self.page2.id
        })
        self.assertEquals(self.response.status_code, 200)
    
        self.response = self.client.post(reverse('rango:unsave_favorite'),{
            'page_id': self.page.id
        })
        
        self.assertEquals(self.response.status_code, 200)
        self.assertEquals(len(self.user.pages.all()), 0)
        self.assertEquals(len(Page.objects.all()), 3)
        
    #Test for favorites list on the user profile page
    def test_user_profile_page(self):
        ########## SETUP ########
        self.page1= add_page('dummies','https://www.dummies.com/computers/', self.cat,self.user)        
        self.page2= add_page('official','https://www.python.org/', self.cat,self.user)
        self.assertIsInstance(self.cat, Category)
        self.assertIsInstance(self.super,SuperCategories)
        
        #First vist the show category page
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        #Save multiple pages in a category
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page1.id
        })
        self.response = self.client.post(reverse('rango:save_favorite'),{
            'page_id': self.page2.id
        })
        
        ################ UNIT TEST ##############
        #Now vist user profile page to view the changes
        self.response= self.client.get(reverse('rango:profile', kwargs={'username':self.user.username}))
        #The feature for saving and unsaving is supposed to be presented to the user via UI buttons
        #with hide show classes
        self.content = self.response.content.decode()
        self.context = self.response.context
        
        self.assertTrue('class="hide"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertTrue('class="show"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}") 
        self.assertIsNotNone(self.context['pages'] ,f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        
        self.assertEquals(len(self.user.pages.all()), 2)
        self.assertEquals(len(self.context['pages']), len(self.user.pages.all()))
        
    #Now user logs out and visiting show_Category
    def test_user_log_out(self):
        ######## UNIT TEST ###########
        self.client.logout()
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.assertEquals(self.response.status_code, 200)
        self.content = self.response.content.decode()
        self.context = self.response.context
        #user is logged out and there are pages on the page, The feature is supposed to be not active
        self.assertFalse('class="hide"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertFalse('class="show"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        
        #Verify there is no saved pages present to be retrieved
        self.assertIsNone(self.context['fav_list'] ,f"{FAILURE_HEADER}{FAILURE_FOOTER}")
      
    #This test tests for the corner case when there is just the category and no pages in it at all.
    def test_database_no_entry(self):
        ######## SETUP ########
        #After login, logout and delete all pages to test the 'start fresh' scenario
        self.client.logout()
        self.page.delete()
        ########## UNIT TEST ############
        #Query the page when only category is created and exists and there is no data inside it
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.assertEquals(self.response.status_code, 200)
        self.content = self.response.content.decode()
        self.context = self.response.context
        #Verify there is no saved pages present to be retrieved
        self.assertIsNone(self.context['fav_list'] ,f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        #Make sure UI doesn't unnecesarily render the content
        self.assertFalse('class="hide"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertFalse('class="show"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        #Making sure pages container is not displayed either
        self.assertFalse('id="category_pages"' in self.content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        
#These are tests for the contact us feature
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
    
    # This tests the user is routed to the view     
    def test_contact_us_view(self):
        
        self.response = self.client.get(reverse('rango:contact_us'))
        self.content = self.response.content.decode()

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'rango/contact_us.html')
    
    #This tests after rendering of the view , the form has desired fields
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

    #This tests the render on the page has everything expected as per the html code
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
    
    ######## This tests that the form submitted via post is saved and can be actually retrieved from DB ##########
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

#### This Class tests the comments feature on the show category page ###
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
        #self.comment.delete()
        #self.page.delete()
        
    # This tests the user is routed to the view after addition of the feature     
    def test_comments_view(self):
        
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.content = self.response.content.decode()

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'rango/category.html')
    
    #The user has form fields as expected
    def test_comments_form(self):
        comment_form = CommentForm()
        self.assertEqual(type(comment_form.__dict__['instance']), Comments, f"{FAILURE_HEADER}The class comments form could not be found in forms.py module.{FAILURE_FOOTER}")
        
        fields = comment_form.fields
        
        expected_fields = {
            'description': django_fields.CharField
        }
        
        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]
            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in CommentsForm implementation'{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field '{expected_field_name}' in CommentsForm was not of the expected type '{type(fields[expected_field_name])}'{FAILURE_FOOTER}")
    
    #The form is actually rendered if the user is logged in 
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
    
    #The form is saved to DB and can be actually retreived from the DB
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
        #self.assertTrue(comment1.date < date.today())
       
# User is logged in comments form must show and zero comments for a new category with no page      
    def test_category_with_one_page_newly_added(self):
        self.client.login()
        sup = create_super_category("Algorithms")
        cat = create_category('ML', sup, self.user, datetime.datetime.now().date())
        add_page('learn x in y minutes','https://learnxinyminutes.com/docs/python', cat,self.user)
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'ML'}))
        context = response.context
        content = response.content.decode()
        self.assertIsNone(context)
        #comments must render and form must not render
        self.assertFalse('id="comment_container"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
    
# comments on a empty category are not allowed unless pages are added in and user is not logged in      
    def test_empty_category1(self):
        self.client.logout()
        self.comment.delete()
        response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        context = response.context
        content = response.content.decode()
        #comments must not render and form must not render either
        self.assertFalse('id="comment_form"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")
        self.assertFalse('id="comment_container"' in content, f"{FAILURE_HEADER}{FAILURE_FOOTER}")

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