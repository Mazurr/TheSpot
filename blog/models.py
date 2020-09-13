from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

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

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    name = models.CharField(max_length = 50)
    email = models.EmailField(max_length= 100)
    contents = models.TextField(max_length= 500)
    create_date = models.DateTimeField(auto_now_add = True)
    active = models.BooleanField(default = False)

    class Meta:
        ordering = ['create_date']
    
    def __str__(self):
        return 'Comments {} by {}'.format(self.contents, self.name)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    email_confirmed = models.BooleanField(default = False)

@receiver(post_save, sender = User)

def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
        instance.profile.save()