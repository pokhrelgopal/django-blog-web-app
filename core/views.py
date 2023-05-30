from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Post
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'core/index.html')


def registeruser(request):
    if request.method == 'POST':
        firstname = request.POST['firstName']
        lastname = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmPassword']
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    first_name=firstname, last_name=lastname, email=email, username=email, password=password)
                user.save()
                profile = Profile(user=user)
                profile.save()
                messages.success(request, 'User created successfully')
                return redirect('index')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')

    return render(request, 'core/index.html')


def loginuser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('index')
            else:
                messages.info(request, 'Invalid credentials')
                return redirect('index')
    return render(request, 'core/index.html')


def logoutuser(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('index')


@login_required(login_url='login')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    print(profile.bio)
    context = {
        'profile': profile
    }
    return render(request, 'core/profile.html', context)


def posts(request):
    q = request.GET.get('q')
    if q:
        posts = Post.objects.filter(title__icontains=q)
    else:
        posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'core/posts.html', context)


@login_required(login_url='login')
def addPost(request):
    if request.method == 'POST':
        title = request.POST['title']
        caption = request.POST['caption']
        image = request.FILES['image']
        post = Post(title=title, caption=caption,
                    image=image, author=request.user.profile)
        post.save()
        messages.success(request, 'Post created successfully')
        return redirect('posts')
    return render(request, 'core/posts.html')


def singlePost(request, pk):

    post = Post.objects.get(id=pk)
    context = {
        'post': post
    }
    return render(request, 'core/single_post.html', context)


@login_required(login_url='login')
def profileBlog(request):
    profile = Profile.objects.get(user=request.user)
    profileBlog = Post.objects.filter(author=profile)
    context = {
        'profile': profile,
        'profileBlog': profileBlog
    }
    return render(request, 'core/profile_blog.html', context)


@login_required(login_url='login')
def deletePost(request):
    hidden_id = request.POST['hidden_id']
    if request.user != Post.objects.get(id=hidden_id).author.user:
        messages.info(request, 'You are not allowed to delete this post')
        return redirect('profile-blog')
    post = Post.objects.get(id=hidden_id)
    post.delete()
    messages.success(request, 'Post deleted successfully')
    return redirect('profile-blog')


def editPost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user != post.author.user:
        messages.info(request, 'You are not allowed to edit this post')
        return redirect('profile-blog')
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.caption = request.POST.get('caption')
        if 'image' in request.FILES:
            post.image = request.FILES['image']
            print(post.image)
        else:
            if post.image:
                post.image = post.image
        post.save()
        messages.success(request, 'Post updated successfully')
        return redirect('profile-blog')
    post = Post.objects.get(id=pk)
    print(post.image)
    context = {
        'post': post
    }
    return render(request, 'core/edit_post.html', context)


def updateProfile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['firstName']
        user.last_name = request.POST['lastName']
        user.email = request.POST['email']
        user.save()
        profile = Profile.objects.get(user=user)
        profile.bio = request.POST['bio']
        if 'profile_picture' in request.FILES:
            profile.profile_pic = request.FILES['profile_picture']
            print(profile.profile_pic)
        else:
            if profile.profile_pic:
                profile.profile_pic = profile.profile_pic
        profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'core/profile.html')
