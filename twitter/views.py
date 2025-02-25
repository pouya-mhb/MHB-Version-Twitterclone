from django.shortcuts import render, redirect
from .models import Profile, Post, Relationship
from .forms import UserRegisterForm, PostForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

@login_required
def home(request):
	posts = Post.objects.all()
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('home')
	else:
		form = PostForm()

	context = {'posts':posts, 'form' : form }
	return render(request, 'twitter/newsfeed.html', context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		# p_form = ProfileUpdateForm(request.user, request.FILES, instance=request.user.profile)
		# if form.is_valid() and p_form.is_valid():
		if form.is_valid() :
			user = form.save()
			Profile.objects.create(user=user)
			login(request, user)
			# p_form.save()
			return redirect('home')
	else:
		form = UserRegisterForm()

	context = {'form' : form}
	return render(request, 'twitter/register.html', context)


def delete(request, post_id):
	post = Post.objects.get(id=post_id)
	post.delete()
	return redirect('home')


def profile(request, username):
	user = User.objects.get(username=username)
	posts = user.posts.all()
	context = {'user':user, 'posts':posts}
	return render(request, 'twitter/profile.html', context)

@login_required
def profile_setting(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('home')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm()

	context = {'u_form' : u_form, 'p_form' : p_form}
	return render(request, 'twitter/profile_setting.html', context)

@login_required
def follow(request, username):
    try:
        current_user = request.user
        to_user = User.objects.get(username=username)
        # Check if the relationship already exists
        if not Relationship.objects.filter(from_user=current_user, to_user=to_user).exists():
            Relationship.objects.create(from_user=current_user, to_user=to_user)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        return redirect('home')
    return redirect('home')

@login_required
def unfollow(request, username):
    try:
        current_user = request.user
        to_user = User.objects.get(username=username)
        # Check if the relationship exists
        rel = Relationship.objects.get(from_user=current_user, to_user=to_user)
        rel.delete()
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        return redirect('home')
    except Relationship.DoesNotExist:
        # Handle the case where the relationship does not exist
        return redirect('home')
    return redirect('home')
