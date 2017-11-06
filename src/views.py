# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from decouple import config
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from wand.image import Image
from django.contrib.auth import logout
import os

@login_required
def home(request):
    return render(request, 'src/index.html')

import facebook
import ipdb
@login_required
def upload_photo(request):
    fi = request.FILES.get('userfile')
    message = request.POST.get('message')
    caption = request.POST.get('caption')
    social = request.user.social_auth.get(provider='facebook')
    access_token = social.extra_data['access_token']
    api = facebook.GraphAPI(access_token)
    user_id = api.get_object('me', fields="id")['id']
    username = api.get_object('me', fields="name")['name']
    profile_link = api.get_object("me", fields="link")['link']
    fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/photography/")
    savedFilename = user_id + "." + fi.name.split('.')[-1]
    filepath = fs.base_location + savedFilename
    if os.path.isfile(filepath):
        os.system("rm " + filepath)
    filename = fs.save(savedFilename, fi)
    savedFilenameURL = request.get_host() + "/media/photography/" + savedFilename
    graph = facebook.GraphAPI(access_token = config('PAGE_ACCESS_TOKEN'))
    msg = "Username: " + username + "(" + profile_link + ")\nCategory: Photography Contest #LuvLdh\n" + "Catpion: " + caption + "\nDescription: " + message
    attachment =  {
        #'name': 'Link name',
        'link': savedFilenameURL, #"http://lab.gdy.club:7777/media/1580271875386906_pic.png", #savedFilenameURL,
        #'caption': 'Check out this example',
        #'description': 'This is a longer description of the attachment',
        'picture': savedFilenameURL #"http://lab.gdy.club:7777/media/1580271875386906_pic.png" #savedFilenameURL
    }
    status = graph.put_wall_post(msg, attachment)
    fbpostURL = URLofSharedPost(status)
    return render(request, 'src/postlink.html', {'output': fbpostURL})

@login_required
def upload_contentwriting(request):
    fi = request.FILES.get('userfile')
    message = request.POST.get('message')
    caption = request.POST.get('caption')
    social = request.user.social_auth.get(provider='facebook')
    access_token = social.extra_data['access_token']
    api = facebook.GraphAPI(access_token)
    user_id = api.get_object('me', fields="id")['id']
    username = api.get_object('me', fields="name")['name']
    profile_link = api.get_object("me", fields="link")['link']
    fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/contentwriting/")
    savedFilename = user_id + "." + fi.name.split('.')[-1]
    filepath = fs.base_location + savedFilename
    if os.path.isfile(filepath):
        os.system("rm " + filepath)
    filename = fs.save(savedFilename, fi)
    #ipdb.set_trace()
    savedFilenameURL = request.get_host() + "/media/contentwriting/" + savedFilename
    imageLocation = settings.MEDIA_ROOT + "/contentwriting/" + user_id + ".jpg"
    imageURL = request.get_host() + "/media/contentwriting/" + user_id + ".jpg"
    pdfLocation = fs.base_location+savedFilename
    pdf_to_image(pdfLocation+"[0]", imageLocation)
    graph = facebook.GraphAPI(access_token = config('PAGE_ACCESS_TOKEN'))
    msg = "Username: " + username + "(" + profile_link + ")\nCategory: Content Writing Contest #LuvLdh\n" + "Caption: " + caption + "\nDescription: " + message + "\nRead more: http://" + savedFilenameURL + "\n"
    attachment =  {
        'link': imageURL, #"https://lab.gdy.club",#imageURL,
        'picture': imageURL, #"https://lab.gdy.club"#imageURL,
    }
    status = graph.put_wall_post(msg, attachment)
    fbpostURL = URLofSharedPost(status)
    return render(request, 'src/postlink.html', {'output': fbpostURL})

@login_required
def upload_souvenir(request):
    fi = request.FILES.get('userfile')
    message = request.POST.get('message')
    caption = request.POST.get('caption')
    social = request.user.social_auth.get(provider='facebook')
    access_token = social.extra_data['access_token']
    api = facebook.GraphAPI(access_token)
    user_id = api.get_object('me', fields="id")['id']
    username = api.get_object('me', fields="name")['name']
    profile_link = api.get_object("me", fields="link")['link']
    fs = FileSystemStorage(location=settings.MEDIA_ROOT+"/souvenir/")
    savedFilename = user_id + "." + fi.name.split('.')[-1]
    filepath = fs.base_location + savedFilename
    if os.path.isfile(filepath):
        os.system("rm " + filepath)
    filename = fs.save(savedFilename, fi)
    #ipdb.set_trace()
    savedFilenameURL = request.get_host() + "/media/souvenir/" + savedFilename
    imageLocation = settings.MEDIA_ROOT + "/souvenir/" + user_id + ".jpg"
    imageURL = request.get_host() + "/media/souvenir/" + user_id + ".jpg"
    pdfLocation = fs.base_location+savedFilename
    pdf_to_image(pdfLocation+"[0]", imageLocation)
    graph = facebook.GraphAPI(access_token = config('PAGE_ACCESS_TOKEN'))
    msg = "Username: " + username + "(" + profile_link + ")\nCategory: Souvenir Contest #LuvLdh\n" + "Caption: "+ caption + "\nDescription: " + message + "\nRead more: http://" + savedFilenameURL + "\n"
    attachment =  {
        'link': imageURL,
        'picture': imageURL,
    }
    status = graph.put_wall_post(msg, attachment)
    fbpostURL = URLofSharedPost(status)
    return render(request, 'src/postlink.html', {'output': fbpostURL})

def URLofSharedPost(status):
    post_id = status['id'].split('_')[-1]
    return "https://www.facebook.com/sscsLdh/posts/"+ post_id

def pdf_to_image(pdf_location, img_location):
    with Image(filename=pdf_location) as img:
        img.save(filename=img_location)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('https://luvldh.gdy.club')
