
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Profile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages

# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cuenta creada correctamente, puedes iniciar sesión')
        return response

    def get_success_url(self):
        return reverse_lazy('login')

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificamos en tiempo real
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder':'Username: '})
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'E-mail'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Password'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder':'Repeat password'})

        return form



@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificamos en tiempo real
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Email: '})
        return form

