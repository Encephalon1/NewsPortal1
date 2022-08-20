from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import Author


@login_required
def upgrade_user(request):
    user = request.user
    authors_group = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='Authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(author=user)
    return redirect('/')
