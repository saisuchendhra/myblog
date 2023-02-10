from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import CommentForm
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

def frontpage(request):
    posts = Post.objects.all()
    return render(request, 'frontpage.html', {'posts' : posts})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    
    # hit count logic
    object = get_object_or_404(Post, pk=post.id)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(object)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    #hit count logic end 

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment  = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug = post.slug)
    else:
        form = CommentForm()


    return render(request, 'post_detail.html', {'post':post, 'form':form})