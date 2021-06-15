# -*- coding: utf-8 -*-
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import Author
from blog.forms import CommentForm, PostForm
from blog.models import Category, Newsletter, Post
# from django.http import HttpRequest
from django.shortcuts import get_object_or_404



class IndexView(View):
    def get(self, request, *args, **kwargs):
        featured_posts = Post.objects.filter(featured=True)[0:3]
        latest_posts = Post.objects.order_by("-timestamp")[0:3]
        context = {"featured_posts": featured_posts, "latest_posts": latest_posts}
        return render(request, "blog/index.html", context=context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        newsletter = Newsletter()
        newsletter.email = email
        newsletter.save()
        messages.info(request, "Successfully subscribed!")
        return redirect("index")


class PostDetailView(DetailView):

    model = Post
    template_name = "blog/post_detail.html"
    _comment_form = CommentForm()



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_posts"] = Post.objects.all().order_by("-timestamp")[0:3]
        context["categories"] = Category.objects.all()
        context["comment_form"] = self._comment_form
        self.object.view_count += 1
        self.object.save()
        # self.view_count + 1
        return context

    def post(self, request, *args, **kwargs):
        _post = self.get_object()
        _comment_form = CommentForm(request.POST)
        if _comment_form.is_valid():
            _comment_form.instance.user = request.user.author
            _comment_form.instance.post = _post
            _comment_form.save()
            return redirect(_post)



class PostListView(ListView):

    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_posts"] = Post.objects.all().order_by("-timestamp")[0:3]
        context["categories"] = Category.objects.all()
        return context



class SearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "")
        search_result = Post.objects.filter(
            Q(title__icontains=q) | Q(overview__icontains=q)
        ).all()
        context = {"search_result": search_result}
        return render(request, "blog/search.html", context=context)


class PostCreateView(CreateView):
    model = Post
    template_name = "blog/post_create.html"
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = Author.objects.filter(user=self.request.user).first()
        # form.instance.author = self.request.user
        # form.instance.author = self.request.user.profile
        form.save()
        
        return redirect(reverse("post_detail", kwargs={"slug": form.instance.slug}))


class PostUpdateView(UpdateView):
    model = Post
    template_name = "blog/post_update.html"
    form_class = PostForm

    def form_valid(self, form):
        if form.instance.author == self.request.user.author:
            form.save()
            return redirect(reverse("post_detail", kwargs={"slug": form.instance.slug}))


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("index")


def CategoryDetails(request, the_slug):
    categ = get_object_or_404(Category, slug=the_slug)
    object_list = categ.post.all().order_by("-title")
    categories = Category.objects.all()
    latest_posts = Post.objects.all().order_by("-timestamp")[0:3]

    paginator = Paginator(object_list, 4)  # 4 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/category_detail.html', {'categ': categ, 'page': page, 'posts': posts, 'categories': categories, 'latest_posts': latest_posts})


# def CategoryDetails(request, pk):
#     categ = get_object_or_404(Category, id=pk)
#     categories = Category.objects.all()
#     latest_posts = Post.objects.all().order_by("-timestamp")[0:3]
#     return render(request, 'blog/category_detail.html', {'categ': categ, 'categories': categories, 'latest_posts': latest_posts})
