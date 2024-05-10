from django.test import TestCase
from ..forms import *


# Тести для форми Post
class TestPostForm(TestCase):
    def test_post_form_valid_data(self):
        form = PostForm(data={
            'title': 'Test',
            'content': 'Test content',
        })

        self.assertTrue(form.is_valid())

    def test_post_form_no_data(self):
        form = PostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)


# Для форми CommentForm
class TestCommentForm(TestCase):
    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'description': 'Test comment',
        })

        self.assertTrue(form.is_valid())


# Ряд тестів для форми ProfileEditForm
class TestProfileEditForm(TestCase):
    def test_valid_data(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'bio': 'A bio for John Doe',
        }

        form = ProfileEditForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = ProfileEditForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


# Тести для RegisterForm
class TestRegisterForm(TestCase):
    def test_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
        }

        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


# Перевірка для форми LoginForm
class TestLoginForm(TestCase):
    def test_valid_data(self):
        form_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }

        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        
