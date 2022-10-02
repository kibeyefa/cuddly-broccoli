from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from chat.models import Thread

@login_required(login_url='accounts:login')
def home_view(request):
    return redirect('chat:home')