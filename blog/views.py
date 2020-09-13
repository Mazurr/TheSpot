from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
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

from .models import Post
from .forms import CommentForm, SignUpForm, PasswordResetForm, PasswordChangeForm

class PostView(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-create_date')
    template_name = 'blog/index.html'
    paginate_by = 5

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
    template_name = 'blog/add_post.html'
    fields = ('title', 'slug', 'author','content', 'status')

class EditPost(generic.UpdateView):
    model = Post
    template_name = 'blog/edit_post.html'
    fields = ('title', 'slug','content', 'status')

class DeletePost(generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:home')

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
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('blog:home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('blog:home')

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

class PasswordChange(generic.View):
    template_name = 'blog/account.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            pass_change_form = PasswordChangeForm(request)
            return render(request, self.template_name, {'pass_change_form': pass_change_form})  
        else:
            return redirect('blog:home')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(username = request.user.username)
            pass_change_form = PasswordChangeForm(request=request, data=request.POST)
            if pass_change_form.is_valid():
                user.set_password(pass_change_form.cleaned_data['new_pass2'])
                user.save()
        else:
            return redirect('blog:home')
        return render(request, self.template_name, {'pass_change_form': pass_change_form})  