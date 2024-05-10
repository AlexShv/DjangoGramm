from django.test import TestCase
from ..models import *


# Тести для моделі Post
class PostModelTest(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title='Test post', content='Testing')

    def test_labels(self):
        title_label = self.post._meta.get_field('title').verbose_name
        content_label = self.post._meta.get_field('content').verbose_name

        self.assertEquals(title_label, 'title')
        self.assertEquals(content_label, 'content')

    def test_title_label_max_length(self):
        max_length = self.post._meta.get_field('title').max_length
        self.assertEquals(max_length, 70)

    def test_expected_display(self):
        expected_object_name = f'{self.post.id}, {self.post.title}'
        self.assertEquals(expected_object_name, '1, Test post')

    def test_get_absolute_url(self):
        self.assertEquals(self.post.get_absolute_url(), '/post/1/')


# Тестую модель користувача(User)
class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='User', last_name='Test', username='usertest')

    def test_labels(self):
        first_name_label = self.user._meta.get_field('first_name').verbose_name
        last_name_label = self.user._meta.get_field('last_name').verbose_name
        username_label = self.user._meta.get_field('username').verbose_name

        self.assertEquals(first_name_label, 'first name')
        self.assertEquals(last_name_label, 'last name')
        self.assertEquals(username_label, 'username')

    def test_max_length(self):
        name_length = self.user._meta.get_field('first_name').max_length
        surname_length = self.user._meta.get_field('last_name').max_length
        username_length = self.user._meta.get_field('username').max_length

        self.assertEquals(name_length, 150)
        self.assertEquals(surname_length, 150)
        self.assertEquals(username_length, 150)

    def test_expected_username(self):
        expected_object_name = f'{self.user.username}: {self.user.first_name} {self.user.last_name}'
        self.assertEquals(expected_object_name, 'usertest: User Test')


# Тести для моделі Comment
class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Test Post', content='Testing')

    def test_create_comment(self):
        comment = Comment.objects.create(description='Test Comment', author=self.user, post_id=self.post)
        self.assertEquals(comment.description, 'Test Comment')
        self.assertEquals(comment.author, self.user)
        self.assertEquals(comment.post_id, self.post)


# Тести для моделі Reaction
class ReactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.post = Post.objects.create(title='Test Post', content='Testing')

    def test_create_reaction(self):
        reaction = Reaction.objects.create(type_of_reaction='like', user_id=self.user, post_id=self.post)
        self.assertEquals(reaction.type_of_reaction, 'like')
        self.assertEquals(reaction.user_id, self.user)
        self.assertEquals(reaction.post_id, self.post)
