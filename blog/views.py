from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect

from .models import Post, Category
from .forms import CommentForm, SignUpForm, PasswordResetForm, PasswordChangeForm, PostForm, EditPostForm, EmailChangeForm, DeleteUserForm

############################################ Posts Managment ########################################################################

# Index Page
 
class PostView(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-create_date')
    template_name = 'blog/index.html'
    paginate_by = 5

class MyPostsView(generic.ListView):
    template_name = 'blog/my_posts.html'
    paginate_by = 5
    queryset = Post.objects
    def get(self, request, *args, **kwargs):
        self.queryset = Post.objects.filter(author=request.user.pk).order_by('-create_date')
        return super(MyPostsView, self).get(request, *args, **kwargs)
    
# Post Details

class PostDetails(generic.DetailView):
    model = Post
    template_name = 'blog/post_details.html'

    def get(self, request, slug):
        template_name = 'blog/post_details.html'
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True)
        new_comment = None
            
        comment_form = CommentForm(request=request, initial={'name': request.user.username})

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
        print(request.user.username)
        comment_form = CommentForm(data=request.POST, request=request, initial={'name': request.user.username})
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

        return render(request, template_name, { 'post': post,
                                                'comments': comments,
                                                'new_comment': new_comment,
                                                'comment_form': comment_form})

class AddPost(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'

    def get(self, request):
        add_post_form = self.form_class(request=request)
        return render(request, self.template_name, {'form': add_post_form})

    def post(self, request):
        add_post_form = self.form_class(request=request, data=request.POST)
        if add_post_form.is_valid():
            add_post_form.save()
            return redirect('blog:home')
        return render(request, self.template_name, {'form': add_post_form})

class EditPost(generic.UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = 'blog/edit_post.html'
    

class DeletePost(generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:home')

def Categories(request, category):
    category_posts = Post.objects.filter(category=category.replace('-', ' '))
    return render(request, 'blog/categories.html', {'category': category.title().replace('-', ' '), 'category_posts':category_posts})

def Like(request, slug):
    post = get_object_or_404(Post, slug=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog:post_details', args=[str(slug)]))

############################################ Users Managment ########################################################################

class SignUp(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        f = self.form_class()
        return render(request, self.template_name, {'form': f})

    def post(self, request, *args, **kwargs):
        f = self.form_class(request.POST)
        if f.is_valid():
            user = f.save()
            current_site = get_current_site(request)
            subject = 'Activate Your The Spot Account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('blog:login')

        return render(request, self.template_name, {'form': f})

class ActivateAccount(generic.View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            return redirect('blog:home')
        else:
            return redirect('blog:home')

# Reset password via e-mail

class ResetPassword(generic.View):
    template_name = 'registration/password_reset.html'
    def post(self, request, *args, **kwargs):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    current_site = get_current_site(request)
                    subject = "Password Reset Requested"
                    message = render_to_string("registration/password_reset_email.html",
		    	    {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http'
                    })
                    user.email_user(subject, message)
        return render(request, self.template_name, {"password_reset_form":password_reset_form})

    def get(self, request):
	    password_reset_form = PasswordResetForm()
	    return render(request, self.template_name, {"password_reset_form":password_reset_form})

# Change password, email and delete user

class AccountSettings(generic.View):
    template_name = 'blog/account.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            pass_change_form = PasswordChangeForm(request)
            email_change_form = EmailChangeForm(request)
            delete_user_form = DeleteUserForm(request)
            return render(request, self.template_name, {'pass_change_form': pass_change_form, 'email_change_form': email_change_form, 'delete_user_form': delete_user_form,})  
        else:
            return redirect('blog:home')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ### Change user password ###
            if 'pass_change' in request.POST:
                user = User.objects.get(username = request.user.username)
                pass_change_form = PasswordChangeForm(request=request, data=request.POST)
                if pass_change_form.is_valid():
                    user.set_password(pass_change_form.cleaned_data['new_pass2'])
                    user.save()
                    return redirect('blog:login')
            else:
                pass_change_form = PasswordChangeForm(request)
            ### Change user email ###
            if 'email_change' in request.POST:
                user = User.objects.get(username = request.user.username)
                email_change_form = EmailChangeForm(request=request, data=request.POST)
                if email_change_form.is_valid():
                    user.email = email_change_form.cleaned_data['new_email']
                    user.save()
            else:
                email_change_form = EmailChangeForm(request)
            ### Delete user ###
            if 'delete_user' in request.POST:
                delete_user_form = DeleteUserForm(request=request, data=request.POST)
                if delete_user_form.is_valid():
                    user = User.objects.get(username=request.user.username)
                    user.delete()
                    return redirect('blog:home')
            else:
                delete_user_form = DeleteUserForm(request)
        else:
            return redirect('blog:home')
        return render(request, self.template_name, {'pass_change_form': pass_change_form, 'email_change_form': email_change_form, 'delete_user_form': delete_user_form,})