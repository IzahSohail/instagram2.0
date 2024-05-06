from django.shortcuts import render

from album.models import Album, Photo
from .models import Tag, PhotoTagMapping
from user.models import User

from comments.forms import CommentForm
from comments.models import Comment

import base64
from PIL import Image
from io import BytesIO

def my_tags(request):
    
    return