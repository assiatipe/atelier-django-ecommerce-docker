from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django import forms


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


def home_redirect(request):
    return redirect('/products/')


urlpatterns = [
    path('', home_redirect, name='home'),

    path('admin/', admin.site.urls),

    path('products/', include('products.urls')),

    path('cart/', include('cart.urls')),

    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'signup/',
        CreateView.as_view(
            template_name='registration/signup.html',
            form_class=SignupForm,
            success_url='/login/'
        ),
        name='signup'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
