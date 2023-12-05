from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,FormView,CreateView
from social.forms import RegisterationForm
from django.urls import reverse


class SignUpView(CreateView):

    # def get(self,request,*args,**kwargs):
    #     form=RegisterationForm()
    #     return render(request,"register.html",{"form":form})
    
    # FormView=> for form display
# --------------------------------------------
    template_name="register.html"
    form_class=RegisterationForm

    def get_success_url(self):
        return reverse("signup")

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


