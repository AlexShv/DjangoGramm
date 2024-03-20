from django.forms import ModelForm, CharField, Form, PasswordInput, TextInput, ClearableFileInput, FileField, \
    ImageField
from djangogramm.models import User, Comment
from django.contrib.auth.forms import UserCreationForm


# Форма для реєстрації користувачів
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Форма для логіну
class LoginForm(Form):
    email = CharField(
        max_length=65,
        widget=TextInput(attrs={'class': 'form-control custom-input'})
    )
    password = CharField(
        max_length=65,
        label='Password',
        widget=PasswordInput(attrs={'class': 'form-control custom-input'})
    )


# Додаткові налаштування для додавання декількох фото до посту
class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


# Форма для створення постів
class PostForm(Form):
    title = CharField(label='Title')
    content = CharField(label='Content')
    title_image = ImageField(label='Image for post title', required=False)
    images = MultipleFileField(label='Images', required=False)


# Форма для створення коментарів
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['description']


# Форма для редагування профілю
class ProfileEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'avatar']
