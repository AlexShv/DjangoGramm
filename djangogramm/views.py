from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from .models import User, Post, Comment, Reaction, Follow, Photo
from .forms import RegisterForm, LoginForm, CommentForm, ProfileEditForm, PostForm
from django.contrib import messages
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.http import JsonResponse


# Представлення sign_in відображає сторінку логіна
def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form, 'title': 'Login'})
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')

        return render(request, 'registration/login.html', {'form': form, 'title': 'Login'})


# Вихід із теперішнього аккаунту
def sign_out(request):
    logout(request)
    return render(request, 'registration/logout_page.html', {'title': 'Logout'})


def activateEmail(request, user, email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('djangogramm/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    if email.send():
        messages.success(
            request, f'Dear {user}, please go to you email, click on \
               received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(
            request,
            f'Problem sending confirmation email to {email}, check if you typed it correctly.')


# Представлення щодо реєстрація користувача
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form, 'title': 'Register'})


# Представлення activate відповідає за активацію акаунта для подальшого
# користування
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            'Thank you for your email confirmation. Now you can use your account.')
        return redirect('login_page')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')


# Відображення головної сторінки (Home)
@method_decorator(login_required, name='dispatch')
class MainPage(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'djangogramm/main.html'
    context_object_name = 'posts'
    ordering = '-created_at'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        current_user = self.request.user
        subscriptions = Follow.objects.filter(follower=current_user)
        subscribed_user_ids = subscriptions.values_list('followed_id', flat=True)
        not_subscribed_users = User.objects.exclude(id__in=subscribed_user_ids).exclude(id=current_user.id)
        context['recommended_users'] = not_subscribed_users.order_by('?')[:5]
        return context


# Відображення профілю користувача
@method_decorator(login_required, name='dispatch')
class Profile(DetailView):
    model = User
    template_name = 'djangogramm/profile.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return User.objects.get(username=username)

    def is_user_following(self, user):
        return not self.request.user.following_set.filter(followed=user).exists()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.username + '\'s profile'
        context['all_posts'] = Post.objects.filter(user_id=self.object.id)
        context['count_posts'] = Post.objects.filter(user_id=self.object.id).count()
        context['is_user_following'] = self.is_user_following(self.object)
        context['followers'] = Follow.objects.filter(followed=self.object.id).count()
        context['followed'] = Follow.objects.filter(follower=self.object.id).count()
        return context


# Детальна інформація щодо окремого посту
@method_decorator(login_required, name='dispatch')
class ShowPost(DetailView):
    model = Post
    template_name = 'djangogramm/post_detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['comments'] = Comment.objects.filter(post_id=self.object.id)
        return context


# Редагування профілю користувача
@method_decorator(login_required, name='dispatch')
class EditProfile(UpdateView):
    form_class = ProfileEditForm
    template_name = 'djangogramm/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit profile'
        return context


# Функція для створення постів
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            post = Post.objects.create(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                title_image=form.cleaned_data['title_image'],
                user_id=user
            )

            for data in request.FILES.getlist('images'):
                photo = Photo(post=post)
                photo.image = data
                photo.save()

            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'djangogramm/post_form.html', {'form': form, 'title': 'Create Post'})


# Редагування посту
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.title_image = form.cleaned_data['title_image']
            post.save()
            return redirect('home')
    else:
        form = PostForm(initial={
            'title': post.title,
            'content': post.content,
            'title_image': post.title_image,
        })

    return render(request, 'djangogramm/post_form.html', {'form': form, 'title': 'Edit Post'})


# Видалення посту
@method_decorator(login_required, name='dispatch')
class DeletePost(DeleteView):
    model = Post
    template_name = 'djangogramm/post_confirm_delete.html'

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])


# Додавання коментарів
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = post
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()

    return render(request, 'djangogramm/comment_form.html', {'form': form, 'title': 'Add Comment'})


# Функція для виставлення реакцій для посту
@login_required
def react_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        reaction_type = request.POST.get('reaction_type')

        reaction, created = Reaction.objects.get_or_create(
            user_id=request.user,
            post_id=post,
        )
        reaction.type_of_reaction = reaction_type
        reaction.save()

        likes_count = Reaction.objects.filter(post_id=post.id, type_of_reaction='like').count()
        dislikes_count = Reaction.objects.filter(post_id=post.id, type_of_reaction='dislike').count()

        data = {
            'likes_count': likes_count,
            'dislikes_count': dislikes_count,
        }

        return JsonResponse(data)


# Функція представлення для підписки\відписки користувачів
@login_required
def follow_or_unfollow(request, user_id):
    user_to_act = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        if action_type == 'follow':
            if not Follow.objects.filter(follower=request.user, followed=user_to_act).exists():
                Follow.objects.create(follower=request.user, followed=user_to_act)
        elif action_type == 'unfollow':
            follow_exists = Follow.objects.filter(follower=request.user, followed=user_to_act).exists()
            if follow_exists:
                Follow.objects.filter(follower=request.user, followed=user_to_act).delete()

        followers_count = Follow.objects.filter(followed=user_to_act).count()
        followings_count = Follow.objects.filter(follower=user_to_act).count()

        response_data = {
            'followers_count': followers_count,
            'followings_count': followings_count,
        }

        return JsonResponse(response_data)


# page_not_found обробляє помилку 404 і повертає повідомлення про
# відсутність сторінки.
def page_not_found(request, exception):
    return HttpResponseNotFound('Page does not exist')
