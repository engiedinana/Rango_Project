from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rango.models import Page, Category, SuperCategories
from django.contrib.auth import get_user_model
#from django.test import Client
import json

#helper function to populat database
def create_user(username, password):
    user = get_user_model().objects.create_user(username=username)
    user.set_password(password)
    user.save()
    return user

#helper function to populat database
def create_category(name, super, user):
    category, __ = Category.objects.update_or_create(
        name=name,
        defaults={'super_cat': super}
    )
    return category

def create_super_category(title):
    super = SuperCategories.objects.create(title=title)
    super.save()
    return super

#helper function to populat database
def add_page(title, url, cat , user):
    page, __ = Page.objects.update_or_create(
        title=title,
        url=url,
        defaults={'category': cat}
    )
    #page.favorite.add(user)
    return page

# The following test is for the save and deleting of
# a page from the favorites list
class TestFavoritesFeature(TestCase):
    def setUp(self):
        self.user = create_user("testUser", "testPassword")
        self.super = create_super_category('Frameworks')
        self.cat = create_category('python', self.super, self.user)
        self.page= add_page('learn x in y minutes','https://learnxinyminutes.com/docs/python', self.cat,self.user)        
        
    def tearDown(self):
        self.user.delete()
        self.super.delete()
        self.cat.delete()
        self.page.delete()
        
    def test_save_list_view(self):
        login = self.client.login(username='testUser', password='testPassword')
        
        # Check our user is logged in
        #self.response=self.client.get(reverse('rango:contact_us'))
        #self.response= self.client.get(reverse('rango:profile', kwargs={'username':self.user.username}))
        
        self.response = self.client.get(reverse('rango:show_category', kwargs={'category_name_slug': 'python'}))
        self.content = self.response.content.decode()
        
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'rango/category.html')

    def test_database_single_entry(self):
        self.response = self.client.get(reverse('rango:save_favorite'),{
            'page_id': self.page.id
        })
        self.assertEquals(self.response.status_code, 302)
        self.assertEquals(self.user.pages.first().title, 'learn x in y minutes')
        self.assertEquals(len(self.user.pages.all()), 1)
        
        self.response = self.client.get(reverse('rango:unsave_favorite'),{
            'id': self.page.id
        })
        print(self.response.context)
        self.assertEquals(self.response.status_code, 302)
        #self.assertEquals(self.user.pages.first().title, 'learn x in y minutes')
        self.assertNotEquals(len(self.user.pages.all()),1 )
        self.assertEquals(len(self.user.pages.all()),0 )
    """    
    def test_database_multiple_entries(self):
        response = self.client.post(reverse('rango:save_favorite'),{
    
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.user.pages.first().title, 'learn x in y minutes')
    
    def test_database_no_entry(self):
        pass
    def test_database_get_saved_and_save_unsaved_pages(self):
        pass
"""