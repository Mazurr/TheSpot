from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Post(models.Model):
    title = models.CharField(max_length = 100, unique = True)
    slug = models.SlugField(max_length = 100, unique = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog_posts')
    update_date = models.DateTimeField(auto_now = True)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add = True)
    status = models.IntegerField(choices = STATUS, default = 0)

    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        return self.title

