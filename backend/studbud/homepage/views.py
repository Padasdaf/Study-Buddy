from django.shortcuts import render
from django.views.generic.base import TemplateView
from homepage.models import User

class HomeView(TemplateView):
    template_name = 'studbud/homepage.html'

    def UserList(request):
        user_list = User.objects.all()
        return render(request, 'homepage/user_list.html', {'Top Users': user_list})

