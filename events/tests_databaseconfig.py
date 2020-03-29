# Database setup tests and gitignore
# Based off of TwD unit tests

import os
import warnings
import importlib
from events.models import Category, User
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}----------------{os.linesep}TEST FAILED{os.linesep}----------------{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class basicDatabaseConfig(TestCase):
    """
    Is your database configured as the book states?
    These tests should pass if you haven't tinkered with the database configuration.
    N.B. Some of the configuration values we could check are overridden by the testing framework -- so we leave them.
    """
    def setUp(self):
        pass
    
    """
    Checks .gitignore for database file.
    """
    def does_gitignore_include_database(self, path):
        f = open(path, 'r')
        
        for line in f:
            line = line.strip()
            
            if line.startswith('db.sqlite3'):
                return True
        
        f.close()
        return False
    
    """
    Tests whether the DATABASES settings variable exist and it has the default config
    """
    def test_databases_variable_exists(self):
        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}DATABASES variable not included in settings.py.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}No 'default' database configuration specified by DATABASES variable.{FAILURE_FOOTER}")
    
    """
    Tests git repo is using gitignore and includes the database files.
    """
    def test_gitignore_for_database(self):
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()
        
        if git_base_dir.startswith('fatal'):
            warnings.warn("Git repo doesn't appear to be present?")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')
            
            if os.path.exists(gitignore_path):
                self.assertTrue(self.does_gitignore_include_database(gitignore_path), f"{FAILURE_HEADER}.gitignore file does not include 'db.sqlite3'{FAILURE_FOOTER}")
            else:
                warnings.warn(".gitignore does not appear in repo.")


class databaseUserCatTests(TestCase):
    """
    Check that models are setup correctly.
    """
    def setUp(self):
        category = Category.objects.get_or_create(Name='Test Category')
        Category.objects.get_or_create(Name='Category Test 2')
        
        user = User.objects.create_user(username='Eric1337_Dance', email='Eric1337_Dance@example.com', password='ivorysoap81', first_name='Eric', last_name='Alexander')
    
    def test_UserCat_model(self):
        category = Category.objects.get(Name='Test Category')
        self.assertEqual(category.Name, 'Test Category', f"{FAILURE_HEADER}Name field check on the Category model failed.{FAILURE_FOOTER}")
        
        user = User.objects.get(username='Eric1337_Dance')
        self.assertEqual(user.email, "Eric1337_Dance@example.com", f"{FAILURE_HEADER}Cannot get email from user model.{FAILURE_FOOTER}")
        self.assertEqual(user.first_name, "Eric", f"{FAILURE_HEADER}Cannot get first name from user model.{FAILURE_FOOTER}")


class adminTests(TestCase):
    """
    Create a superuser account.
    Log the superuser in.
    Create a category as well.
    """
    def setUp(self):
        User.objects.create_superuser('root', 'root@example.com', 'toor123')
        self.client.login(username='root', password='toor123')
        
        category = Category.objects.get_or_create(Name='Test Category')
    
    def test_admin_interface_accessible(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}The admin interface is not accessible.{FAILURE_FOOTER}")
    
    def test_models_present(self):
        response = self.client.get('/admin/')
        response_body = response.content.decode()
        
        # Checks that the events app is present
        self.assertTrue('Events' in response_body, f"{FAILURE_HEADER}event app is not present within the admin interface.{FAILURE_FOOTER}")
        
        # Check that categories is present
        self.assertTrue('Categories' in response_body, f"{FAILURE_HEADER}category model was not found in the admin interface.{FAILURE_FOOTER}")