from django.views import generic
from django.shortcuts import render, get_object_or_404

from .models import Post
from .forms import CommentForm

class PostView(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('create_date')
    template_name = 'blog/index.html'

class PostDetails(generic.DetailView):
    model = Post
    template_name = 'blog/post_details.html'

    def get(self, request, slug):
        template_name = 'blog/post_details.html'
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True)
        new_comment = None
            
        comment_form = CommentForm()

        return render(request, template_name, { 'post': post,
                                                'comments': comments,
                                                'new_comment': new_comment,
                                                'comment_form': comment_form})

    def post(self, request, slug):
        template_name = 'blog/post_details.html'
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True)
        new_comment = None
        # Comment posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

        return render(request, template_name, {'post': post,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form})