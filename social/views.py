from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,FormView,CreateView
from social.forms import RegisterationForm,LoginForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout


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
    
class IndexView(TemplateView):

    template_name="index.html"


class SignOutView(View):

    def get(self,request,*args,**Kwargs):
        logout(request)
        return redirect("signin")