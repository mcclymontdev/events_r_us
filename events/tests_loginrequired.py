# Login required tests
# Based off of TwD unit tests

import os
import re
from populate_events import populate
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}----------------{os.linesep}TEST FAILED{os.linesep}----------------{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

def create_user():
    user = User.objects.get_or_create(username='test',first_name='Eric',last_name='Alexander',email='test@example.com')[0]
    user.set_password('ivorysoap81')
    user.save()
    return user


class loginRequiredTests(TestCase):
    def test_bad_add_event(self):
        populate()
        response = self.client.get(reverse('events:add_event'))
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}User was not redirected{FAILURE_FOOTER}")
    
    def test_good_add_event(self):
        populate()
        user_object = create_user()
        self.client.login(username='test', password='ivorysoap81')
        response = self.client.get(reverse('events:add_event'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Login check failed.{FAILURE_FOOTER}")
        
        content = response.content.decode()
        self.assertTrue('Add event' in content, f"{FAILURE_HEADER}The wrong page was shown to the user.{FAILURE_FOOTER}")

    def test_bad_manage_events(self):
        populate()
        response = self.client.get(reverse('events:manage_events'))
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}User was not redirected{FAILURE_FOOTER}")
    
    def test_good_manage_events(self):
        populate()
        user_object = create_user()
        self.client.login(username='test', password='ivorysoap81')
        response = self.client.get(reverse('events:manage_events'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Login check failed.{FAILURE_FOOTER}")
        
        content = response.content.decode()
        self.assertTrue('Manage events' in content, f"{FAILURE_HEADER}The wrong page was shown to the user.{FAILURE_FOOTER}")

    def test_bad_profile(self):
        populate()
        response = self.client.get(reverse('events:profile'))
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}User was not redirected{FAILURE_FOOTER}")
    
    def test_good_profile(self):
        populate()
        user_object = create_user()
        self.client.login(username='test', password='ivorysoap81')
        response = self.client.get(reverse('events:profile'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Login check failed.{FAILURE_FOOTER}")
        
        content = response.content.decode()
        self.assertTrue('Edit profile' in content, f"{FAILURE_HEADER}The wrong page was shown to the user.{FAILURE_FOOTER}")

    def test_bad_edit_event(self):
        populate()
        response = self.client.get(reverse('events:edit_event', kwargs={'id': 1}))
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}User was not redirected{FAILURE_FOOTER}")
    
    def test_good_edit_event(self):
        populate()
        user_object = create_user()
        self.client.login(username='test', password='ivorysoap81')
        response = self.client.get(reverse('events:edit_event', kwargs={'id': 1}))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Login check failed.{FAILURE_FOOTER}")
        
        content = response.content.decode()
        self.assertTrue('Edit event' in content, f"{FAILURE_HEADER}The wrong page was shown to the user.{FAILURE_FOOTER}")