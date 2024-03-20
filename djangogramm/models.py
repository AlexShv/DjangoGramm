from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from cloudinary.models import CloudinaryField


# Створив моделі Post, Comment, Reaction, Follow, Photo та розширив стандартну модель User
# за допомогою AbsrtactUser для подальшого користування
class User(AbstractUser):
    bio = models.TextField(
        max_length=400,
        help_text='Tell something about yourself')
    avatar = CloudinaryField('avatar', blank=True)
    email = models.EmailField(max_length=200, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.username)


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(max_length=70,
                             help_text='Create a title to your post')
    content = models.TextField(blank=True,
                               help_text='Add some information about post')
    title_image = CloudinaryField('title_image', blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Photo(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = CloudinaryField('image')


class Comment(BaseModel):
    description = models.TextField(blank=True, help_text='Submit comment')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_id = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.description


class Reaction(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)

    REACTION_CHOICES = (
        ('like', '👍'),
        ('dislike', '👎'),
    )

    type_of_reaction = models.CharField(max_length=10, choices=REACTION_CHOICES, help_text='Reaction for the post')

    def get_type_of_reaction_display(self):
        for choice in self.REACTION_CHOICES:
            if choice[0] == self.type_of_reaction:
                return choice[1]
        return 'Unknown Reaction'

    def __str__(self):
        return f'{self.user_id} reacted to {self.post_id} with {self.get_type_of_reaction_display()}'


class Follow(BaseModel):
    follower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='following_set')
    followed = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='followed_set')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} follows {self.followed}'
