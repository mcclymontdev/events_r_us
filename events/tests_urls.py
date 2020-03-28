# Basic url setup tests
# Based off of TwD unit tests

import os
import re
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}----------------{os.linesep}TEST FAILED{os.linesep}----------------{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class basicTests(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.events_templates_dir = os.path.join(self.templates_dir, 'events')
    
    """
    Tests if template directory is setup.
    """
    def test_templates_directory_exists(self):
        directory_exists = os.path.isdir(self.templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Events templates directory does not exist.{FAILURE_FOOTER}")
    
    """
    Checks that our app's (events) templates directory exists.
    """
    def test_events_templates_directory_exists(self):

        directory_exists = os.path.isdir(self.events_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The events template directory does not exist.{FAILURE_FOOTER}")
    
    """
    Checks that TEMPLATE_DIR exists and that it points to the correct directory.
    """
    def test_template_dir_setting(self):
        TEMPLATE_DIR_exists = 'TEMPLATE_DIR' in dir(settings)
        self.assertTrue(TEMPLATE_DIR_exists, f"{FAILURE_HEADER}settings.py does not contain TEMPLATE_DIR.{FAILURE_FOOTER}")
        
        TEMPLATE_DIR_value = os.path.normpath(settings.TEMPLATE_DIR)
        TEMPLATE_DIR_computed = os.path.normpath(self.templates_dir)
        self.assertEqual(TEMPLATE_DIR_value, TEMPLATE_DIR_computed, f"{FAILURE_HEADER}TEMPLATE_DIR does not point to the proper template path.{FAILURE_FOOTER}")

    """
    Checks that our TEMPLATE_DIR value appears within the lookup for templates.
    """
    def test_template_lookup_path(self):
        lookup_list = settings.TEMPLATES[0]['DIRS']
        found_path = False
        
        for entry in lookup_list:
            entry_normalised = os.path.normpath(entry)
            
            if entry_normalised == os.path.normpath(settings.TEMPLATE_DIR):
                found_path = True
        
        self.assertTrue(found_path, f"{FAILURE_HEADER}Templates directory is not listed in the TEMPLATES>DIRS lookup list.{FAILURE_FOOTER}")
    
    """
    Does the index.html template exist in the correct place?
    """
    def test_templates_exist(self):
        index_path = os.path.join(self.events_templates_dir, 'index.html')
        
        self.assertTrue(os.path.isfile(index_path), f"{FAILURE_HEADER}Your index.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")


class urlTests(TestCase):
    def setUp(self):
        self.responseIndex = self.client.get(reverse('events:index'))
        self.responseLogin = self.client.get(reverse('events:login'))
        self.responseLogout = self.client.get(reverse('events:logout'))
        self.responseAddEvent = self.client.get(reverse('events:add_event'))
        self.responseSearch = self.client.get(reverse('events:search'))
        self.responseManageEvents = self.client.get(reverse('events:manage_events'))

    
    """
    Tests that the index page uses the index template.
    """
    def test_index_uses_template(self):
        self.assertTemplateUsed(self.responseIndex, 'events/index.html', f"{FAILURE_HEADER}index view does not use the index.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.responseLogin, 'events/login.html', f"{FAILURE_HEADER}login view does not use the login.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.responseAddEvent, 'events/add_event.html', f"{FAILURE_HEADER}add_event view does not use the add_event.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.responseSearch, 'events/search.html', f"{FAILURE_HEADER}search view does not use the search.html template.{FAILURE_FOOTER}")
        self.assertTemplateUsed(self.responseManageEvents, 'events/manage_events.html', f"{FAILURE_HEADER}manage_events view does not use the manage_events.html template.{FAILURE_FOOTER}")
       
    """
    Tests that <!DOCTYPE html> declaration is present in template.
    """
    def test_index_starts_with_doctype(self):
        self.assertTrue(self.responseIndex.content.decode().startswith('<!DOCTYPE html>'), f"{FAILURE_HEADER}Index template does not contain doctype declaration.{FAILURE_FOOTER}")

class staticAndMediaSetupTests(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')
    
    """
    Tests that the static directory exists.
    """
    def test_does_static_directory_exist(self):

        does_static_dir_exist = os.path.isdir(self.static_dir)
        
        self.assertTrue(does_static_dir_exist, f"{FAILURE_HEADER}The static directory was not found.{FAILURE_FOOTER}")  

    """
    Tests that the media directory exists.
    """
    def test_does_media_directory_exist(self):
        does_media_dir_exist = os.path.isdir(self.media_dir)
        
        self.assertTrue(does_media_dir_exist, f"{FAILURE_HEADER}Couldn't find the /media/ directory.{FAILURE_FOOTER}")
   
    """
    Test to check that static and media configs are setup correctly
    """
    def test_static_and_media_configuration(self):
        static_dir_exists = 'STATIC_DIR' in dir(settings)
        self.assertTrue(static_dir_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable STATIC_DIR defined.{FAILURE_FOOTER}")
        
        expected_path = os.path.normpath(self.static_dir)
        static_path = os.path.normpath(settings.STATIC_DIR)
        self.assertEqual(expected_path, static_path, f"{FAILURE_HEADER}STATIC_DIR does not exist in settings.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATICFILES_DIRS' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}STATICFILES_DIRS does not exist in settings.{FAILURE_FOOTER}")
        self.assertEqual([static_path], settings.STATICFILES_DIRS, f"{FAILURE_HEADER}STATICFILES_DIRS does not match the static directory path.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATIC_URL' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}STATIC_URL does not exist in settings.{FAILURE_FOOTER}")
        self.assertEqual('/static/', settings.STATIC_URL, f"{FAILURE_HEADER}STATIC_URL does not match the proper static url.{FAILURE_FOOTER}")
        
        media_dir_exists = 'MEDIA_DIR' in dir(settings)
        self.assertTrue(media_dir_exists, f"{FAILURE_HEADER}MEDIA_DIR does not exist in settings.{FAILURE_FOOTER}")
        
        expected_path = os.path.normpath(self.media_dir)
        media_path = os.path.normpath(settings.MEDIA_DIR)
        self.assertEqual(expected_path, media_path, f"{FAILURE_HEADER}MEDIA_DIR does not point to the correct path.{FAILURE_FOOTER}")
        
        media_root_exists = 'MEDIA_ROOT' in dir(settings)
        self.assertTrue(media_root_exists, f"{FAILURE_HEADER}MEDIA_ROOT does not exist in settings.{FAILURE_FOOTER}")
        
        media_root_path = os.path.normpath(settings.MEDIA_ROOT)
        self.assertEqual(media_path, media_root_path, f"{FAILURE_HEADER}MEDIA_ROOT does not equal the value of MEDIA_DIR.{FAILURE_FOOTER}")
        
        media_url_exists = 'MEDIA_URL' in dir(settings)
        self.assertTrue(media_url_exists, f"{FAILURE_HEADER}MEDIA_URL does not exist in settings.{FAILURE_FOOTER}")
        
        media_url_value = settings.MEDIA_URL
        self.assertEqual('/media/', media_url_value, f"{FAILURE_HEADER}MEDIA_URL does not equal /media/{FAILURE_FOOTER}")
