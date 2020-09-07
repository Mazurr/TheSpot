from django.views import generic
from .models import Post

class PostView(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('create_date')
    template_name = 'blog/index.html'

class PostDetails(generic.DetailView):
    model = Post
    template_name = 'blog/post_details.html'