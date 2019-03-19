from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, Http404

from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.core import serializers

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import ensure_csrf_cookie

from django.utils import timezone

from socialnetwork.forms import *
from socialnetwork.models import *

def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    new_profile=Profile(user=new_user)
    new_profile.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    login(request, new_user)
    return redirect(reverse('home'))

@ensure_csrf_cookie
@login_required
def globalstream_action(request):
    posts = Post.objects.all().order_by('-post_time')
    context={'posts': posts}
    return render(request, 'socialnetwork/globalstream.html', context)

@login_required
def profile_action(request, id):
    if id == request.user.id:
        context={}
        profile=Profile.objects.filter(id=id).last()
        context['form'] = ProfileForm()
        context['profile'] = profile
        if len(str(profile.user_bio).strip())==0 or profile.user_bio is None:
            context['user_bio'] = 'Default blah blah blah.'
        else:
            context['user_bio'] = '{0}'.format(profile.user_bio)
        context['followlist']=profile.followlist.all()
        return render(request, 'socialnetwork/profile.html', context)
    else:
        context={}
        other_user=User.objects.get(id=id)
        profile=Profile.objects.filter(id=id).last()
        context['form'] = ProfileForm()
        context['profile'] = profile
        if len(str(profile.user_bio).strip())==0 or profile.user_bio is None:
            context['user_bio'] = 'Default blah blah blah.'
        else:
            context['user_bio'] = '{0}'.format(profile.user_bio)
        myProfile = Profile.objects.filter(id=request.user.id).last()
        if other_user in myProfile.followlist.all():
            context['follow'] = 'unfollow'
        else:
            context['follow'] = 'follow'
        return render(request, 'socialnetwork/other_profile.html', context) 

@login_required
def follow_action(request, id):
    context = {}
    other_profile = User.objects.get(id=id)
    profile = Profile.objects.filter(id=id).last()
    context['form'] = ProfileForm()
    context['profile'] = profile
    if len(str(profile.user_bio).strip())==0 or profile.user_bio is None:
        context['user_bio'] = 'Default blah blah blah.'
    else:
        context['user_bio'] = '{0}'.format(profile.user_bio)
    myProfile = Profile.objects.filter(id=request.user.id).last()
    if other_profile in myProfile.followlist.all():
        myProfile.followlist.remove(other_profile)
        context['follow'] = 'follow'
    else:
        myProfile.followlist.add(other_profile)
        context['follow'] = 'unfollow'
    myProfile.save()
    return render(request, 'socialnetwork/other_profile.html', context)


@login_required
def add_post(request):
    if request.method=='GET':
        posts = Post.objects.all().order_by('-post_time')
        context={'posts': posts}
        return render(request, 'socialnetwork/globalstream.html',context)
    elif request.method =='POST':
        context = {}
        error=[]

        if request.POST.get('post_text') =="":
            error.append("you must enter something")
        else:
            new_post = Post(content=request.POST.get('post_text'),
                            post_creator=request.user,
                            post_time = timezone.now())
            new_post.save()

        posts = Post.objects.all().order_by('-post_time')

        context={'posts': posts,'errors':error}
        return render(request, 'socialnetwork/globalstream.html',context)


@login_required
def followerstream(request):
    myProfile = Profile.objects.filter(id=request.user.id).last()
    posts = Post.objects.filter(post_creator__in = myProfile.followlist.all()).order_by('-post_time')
    context={'posts': posts}
    return render(request, 'socialnetwork/followerstream.html',context)

@login_required
def update_profile(request):
    context = {}
    profile=Profile.objects.filter(id=request.user.id).last()
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if not form.is_valid():
        context['form'] = form
    else:
        pic = form.cleaned_data['picture']
        print('Uploaded picture: {} (type={})'.format(pic, type(pic)))
        profile.user_bio = request.POST.get('user_bio')
        profile.content_type = form.cleaned_data['picture'].content_type
        profile.pic_saved=profile.picture
        profile.save()
        profile.picture=None
        profile.save()
        form.save()
        context['form'] = ProfileForm()
    context['profile'] = profile
    if len(str(profile.user_bio).strip())==0 or profile.user_bio is None:
        context['user_bio'] = 'Default blah blah blah.'
    else:
        context['user_bio'] = '{0}'.format(profile.user_bio)

    context['followlist'] = profile.followlist.all()
    return render(request, 'socialnetwork/profile.html', context)

@login_required
def get_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not profile.pic_saved:
        raise Http404

    return HttpResponse(profile.pic_saved, content_type=profile.content_type)

@login_required
def add_comment(request):
    if request.method != 'POST':
        raise Http404

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        message = 'You must enter an comment to add.'
        json_error = '{ "error": "'+message+'" }'
        return HttpResponse(json_error, content_type='application/json')
    new_comment = Comment(content=request.POST['comment_text'],
                    comment_creator = request.user,
                    comment_time = timezone.now(),
                    creator_id=request.user.id,
                    post_id = request.POST['id'])
    new_comment.save()
    response_text = serializers.serialize('json', [Comment.objects.last()])
    return HttpResponse(response_text, content_type='application/json')


def refresh_global(request):
    last_refresh = parse_datetime(request.GET['last_refresh'])
    print(last_refresh)
    print(request.user.username)
    response_text1=serializers.serialize('json',Post.objects.filter(post_time__gt=last_refresh))
    response_text2 = serializers.serialize('json',Comment.objects.filter(comment_time__gt=last_refresh))
    print(Post.objects.filter(post_time__gt=last_refresh).count())
    print(Comment.objects.filter(comment_time__gt=last_refresh).count())
    if Post.objects.filter(post_time__gte=last_refresh).count()==Post.objects.all().count():
        response_text= response_text2
    elif Post.objects.filter(post_time__gte=last_refresh).count()>0 and Comment.objects.filter(comment_time__gte=last_refresh).count()==0:
        response_text= response_text1
    elif Post.objects.filter(post_time__gte=last_refresh).count()>0:
        response_text=response_text1[:len(response_text1)-1]+','+response_text2[1:]
    else:
        response_text= response_text2
    print(response_text)
    return HttpResponse(response_text, content_type='application/json')

def refresh_follower(request):
    myProfile = Profile.objects.filter(id=request.user.id).last()
    last_refresh = parse_datetime(request.GET['last_refresh'])
    print(last_refresh)
    posts = Post.objects.filter(post_creator__in = myProfile.followlist.all()).order_by('-post_time')
    response_text1=serializers.serialize('json',posts.filter(post_time__gte=last_refresh))
    response_text2 = serializers.serialize('json',Comment.objects.filter(comment_time__gte=last_refresh))
    if Post.objects.filter(post_time__gte=last_refresh).count()==Post.objects.all().count():
        response_text= response_text2
    elif Post.objects.filter(post_time__gte=last_refresh).count()>0 & Comment.objects.filter(comment_time__gte=last_refresh).count()==0:
        response_text= response_text1
    elif Post.objects.filter(post_time__gte=last_refresh).count()>0:
        response_text=response_text1[:len(response_text1)-1]+','+response_text2[1:]
    else:
        response_text= response_text2
    return HttpResponse(response_text, content_type='application/json')

