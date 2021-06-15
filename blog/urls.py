# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.urls import re_path
from blog import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("post/", views.PostListView.as_view(), name="post_list"),
    path("post/<slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path(
        "posts/create/",
        login_required(views.PostCreateView.as_view()),
        name="post_create",
    ),
    path(
        "posts/update/<slug>/",
        login_required(views.PostUpdateView.as_view()),
        name="post_update",
    ),
    path(
        "posts/delete/<slug>/",
        login_required(views.PostDeleteView.as_view()),
        name="post_delete",
    ),
    path("category/<slug:the_slug>/", views.CategoryDetails, name='CategoryDetails'),
    # re_path(r'^category/(?P<pk>\d+)$',
            # views.CategoryDetails, name= "CategoryDetails"),
]
