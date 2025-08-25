from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Thread, Message
from django.http import Http404, JsonResponse
from django.db.models import Max

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ThreadList(TemplateView):
    template_name = "messenger/thread_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['threads'] = Thread.objects.filter(users=self.request.user).annotate(
            last_msg=Max('messages__created')
        ).order_by('-last_msg')
        return context

@method_decorator(login_required, name='dispatch')
class ThreadDetail(DetailView):
    model = Thread

    def get_object(self):
        obj = super(ThreadDetail, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404
        return obj

def add_message(request, pk):
    json_response = {'created':False,}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404(Thread, pk=pk)
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            thread.save()
            json_response['created'] = True
            if len(thread.messages.all()) == 1:
                json_response['first'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(json_response)

@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))

