from django.shortcuts import  get_object_or_404
from registration.models import Profile
from django.views.generic import DetailView, ListView

# Create your views here.

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 10

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])
