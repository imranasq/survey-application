from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserLoginForm, SignUpForm
from .models import User

from rest_framework import viewsets
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated


class SignUpView(CreateView):
    template_name   = 'user/user-registration.html'
    form_class      = SignUpForm
    success_url     = reverse_lazy('login')
    success_message = "Your profile was created successfully"


class LoginView(View):
    model         = User
    template_name = "user/user-login.html"

    def post(self, request):
        email    = request.POST['email']
        password = request.POST['password']
        user     = authenticate(email=email, password=password)

        if user is not None:
            if user.is_admin:
                login(request, user)
                return HttpResponseRedirect('/')
            elif user.user_type=="Customer":
                login(request, user)
                return redirect('/customer-panel')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect('/login')

    def get(self, request):
        form    = UserLoginForm(request.POST or None)
        context = {
            'login_form': form,
           }
        return render(request, "user/user-login.html", context)



class AdminPanelView(LoginRequiredMixin,TemplateView):
    login_url     = '/login/'
    model         = User
    template_name = "user/admin-panel.html"

    def get_context_data(self, **kwargs):
        filtered_user = User.objects.filter(email=self.request.user.email)
        if filtered_user.exists():
            users = filtered_user
        context = {
            'users': users
        }
        return context

class CustomerPanelView(LoginRequiredMixin, TemplateView):
    login_url     = '/login/'
    model         = User
    template_name = "user/customer-panel.html"

    def get_context_data(self, **kwargs):
        filtered_user = User.objects.filter(email=self.request.user.email)
        if filtered_user.exists():
            users = filtered_user
        context = {
            'users': users
        }
        return context

class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login")

class UserView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class   = LoginSerializer
    queryset           = User.objects.all()