from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def index(request):
    posts = Post.objects.filter(is_published=True).select_related('category')[:8]
    latest_posts = posts[1:5]
    context = {
        'posts': posts,
        'hero_post': posts[0] if posts else None,
        'latest_posts': latest_posts,
    }
    return render(request, 'journal/index.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = (
        Post.objects.filter(is_published=True, category=category)
        .select_related('category')
    )
    return render(
        request,
        'journal/category_detail.html',
        {
            'category': category,
            'posts': posts,
        },
    )


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related('category'), slug=slug, is_published=True)
    return render(request, 'journal/detail.html', {'post': post})
