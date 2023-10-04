from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment
from django.urls import reverse


@login_required(login_url='signin')
def index(request):
    user_profile = Profile.objects.get(user=request.user.id)
    posts = Post.objects.all().order_by('created_at').reverse()
    for post in posts:
        post.user_img = Profile.objects.get(user=post.user.id).profileimg.url
        comments = post.comments.all()
        for comment in comments:
            comment.user_img = Profile.objects.get(
                user=comment.user.id).profileimg.url
        post.commentss = comments
        top_3_likes = []
        for i in range(min(3, post.likes.count())):
            top_3_likes.append(Profile.objects.get(
                user=post.likes.all()[i]).profileimg.url)
        posts.top_3_likes = top_3_likes

    
    return render(request, 'index.html', {'user_profile': user_profile, 'posts': posts})


def signup(request):
    logout(request)
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            passwordcheck = request.POST.get('passwordcheck')
            last_name = request.POST.get('last_name')
            first_name = request.POST.get('first_name')

            if password != passwordcheck:
                messages.info(request, 'Password does not match')
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')

            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            user_login = authenticate(username=username, password=password)
            login(request, user_login)

            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(
                user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('settings')

    except Exception as e:
        print(e)
        return redirect('signup')

    return render(request, 'signup.html')


def signin(request):
    logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if (not (username or password)):
            messages.info(request, 'Please fill all the fields')
            return redirect('signin')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, 'PLease Register First')
            return redirect('signin')

        login(request, user)
        return redirect('index')

    return render(request, 'signin.html')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def settings(request):

    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        profileimg = user_profile.profileimg

        if request.FILES.get('image'):
            profileimg = request.FILES.get('image')

        user_profile.bio = bio
        user_profile.location = location
        user_profile.profileimg = profileimg
        user_profile.save()
        index_url = reverse('index')
        return redirect(index_url)

    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        image = request.FILES.get('image_upload')
        user = User.objects.get(id=request.user.id)

        if not (caption and image):
            messages.info(request, 'Please fill all the fields')
            return redirect('index')

        new_post = Post.objects.create(
            user=user, caption=caption, image=image)
        new_post.save()
        return redirect('index')
    pass


@login_required(login_url='signin')
def like(request):
    try:
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            user = request.user
            post = Post.objects.get(id=post_id)
            if post.likes.filter(id=user.id).exists():
                post.likes.remove(user)
            else:
                post.likes.add(user)
            post.save()
            # return posts with updated likes
            posts = Post.objects.all().order_by('created_at').reverse()
            for post in posts:
                post.user_img = Profile.objects.get(
                    user=post.user.id).profileimg.url
            return render(request, 'posts.html', {'posts': posts})

    except Exception as e:
        print(e)
        return redirect('index')


@login_required(login_url='signin')
def comment(request):
    try:
        if request.method == 'POST':
            comment = request.POST['comment']
            if not comment:
                pass
            post_id = request.POST.get('post_id')
            user = request.user
            post = Post.objects.get(id=post_id)
            new_comment = Comment.objects.create(
                comment=comment, user=user, post=post)
            new_comment.save()
            return redirect('index')

    except Exception as e:
        print(e)
        return redirect('index')


@login_required(login_url='signin')
def delete_comment(request):
    try:
        if request.method == 'POST':
            comment_id = request.POST.get('comment_id_to_delete')
            user_id = int(request.POST.get('user_who_is_deleting'))
            comment = Comment.objects.get(id=comment_id)
            if user_id == comment.user.id:
                comment.delete()
            return redirect('index')

    except Exception as e:
        print(e)
        return redirect('index')


@login_required(login_url='signin')
def delete_post(request):
    try:
        if request.method == 'POST':
            post_id = request.POST['post_id_to_delete']
            user_id = int(request.POST['user_who_is_deleting'])
            post = Post.objects.get(id=post_id)
            print(user_id, post.user.id)
            if user_id == post.user.id:
                post.delete()
            return redirect('index')

    except Exception as e:
        print(e)
        return redirect('index')


@login_required(login_url='signin')
def add_remove_friend(request):
    try:
        if request.method == 'POST':
            user_id = request.POST['user_id']
            if not user_id:
                pass
            user = User.objects.get(id=user_id)
            user_profile = Profile.objects.get(user=user).friends
            if user_profile.filter(id=request.user.id).exists():
                user_profile.remove(Profile.objects.get(user=request.user))
            else:
                user_profile.add(Profile.objects.get(user=request.user))
            user_profile.save()
            return redirect('index')

    except Exception as e:
        print(e)
        return redirect('index')
