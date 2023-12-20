from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,FormView,CreateView,UpdateView,DetailView,ListView
from social.forms import RegisterationForm,LoginForm,UserProfileForm,PostForm,CommentForm,StoryForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from social.models import UserProfile,Posts,Stories
from django.utils import timezone

class SignUpView(CreateView):

    # def get(self,request,*args,**kwargs):
    #     form=RegisterationForm()
    #     return render(request,"register.html",{"form":form})
    
    # FormView=> for form display
# --------------------------------------------
    template_name="register.html"
    form_class=RegisterationForm

    def get_success_url(self):
        return reverse("signin")

    # def post(self,request,*args,**kwargs):
    #     form=RegisterationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("signup")
    #     else:
    #         return render(request,"register.html",{"form":form})

# ----------------------------------------


# TemplateView => to render a html page
# class IndexView(TemplateView):
#     template_name="index.html"


class SignInView(FormView):

    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                print("success")
                return redirect("index")
        print("failed")
        return render(request,"login.html",{"form":form})
    
class IndexView(CreateView,ListView):

    template_name="index.html"
    form_class=PostForm
    model=Posts
    context_object_name="data"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("index")
    
    def get_queryset(self):
        blocked_profile=self.request.user.profile.block.all()
        blockedprofile_id=[pr.user.id for pr in blocked_profile]
        qs=Posts.objects.all().exclude(user__id__in=blockedprofile_id).order_by("-create_date")
        return qs
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        current_date=timezone.now()
        context["stories"]=Stories.objects.filter(expiry_date__gte=current_date)
        return context
    


class SignOutView(View):

    def get(self,request,*args,**Kwargs):
        logout(request)
        return redirect("signin")
    

# localhost:8000/profile/<int:pk>/change/
class ProfileUpdateView(UpdateView):

    template_name="profile_add.html"
    form_class=UserProfileForm
    model=UserProfile

    def get_success_url(self):
        return reverse("index")
    

class ProfileDetailView(DetailView):
    template_name="profile_detail.html"
    model=UserProfile
    context_object_name="data"

class ProfileListView(ListView):
    # def get(self,request,*args,**kwargs):
    #     qs=UserProfile.objects.all().exclude(user=request.user)
    #     return render(request,"profile_list.html",{"data":qs})
    template_name="profile_list.html"
    context_object_name="data"
    model=UserProfile
    
    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)
    


class FollowView(View):

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action=="follow":
            request.user.profile.following.add(profile_object)
        elif action=="unfollow":
            request.user.profile.following.remove(profile_object)
        return redirect("index")
    

class PostLikeView(View):

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        action=request.POST.get("action")
        if action=="like":
            post_object.liked_by.add(request.user)
        elif action=="dislike":
            post_object.liked_by.remove(request.user)
        return redirect("index")
    

class CommentView(CreateView):
    template_name="index.html"
    form_class=CommentForm

    def get_success_url(self):
        return reverse("index")
    
    def form_valid(self, form):
        id=self.kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        form.instance.user=self.request.user
        form.instance.post=post_object
        return super().form_valid(form)



class ProfileBlockView(View):

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action=="block":
            request.user.profile.block.add(profile_object)
        elif action=="unblock":
            request.user.profile.block.remove(profile_object)
        return redirect("index")
    

class StoriesCreateView(View):
    
    def post(self,request,*args,**kwargs):
        form=StoryForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        return redirect("index")
    