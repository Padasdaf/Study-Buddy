from django.shortcuts import render
from django.views.generic.base import TemplateView
from homepage.models import User  # Use this if you have a custom User model
# from django.contrib.auth.models import User  # Use this if you're using Django's built-in User model

class HomeView(TemplateView):
    template_name = 'studbud/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_users'] = User.objects.all()
        return context

class LoginView(TemplateView):
    template_name = 'studbud/login.html'

class ProfileView(TemplateView):
    template_name = 'studbud/profile.html'

class HistoryView(TemplateView):
    template_name = 'studbud/history.html'

class FeedbackView(TemplateView):
    template_name = 'studbud/feedback.html'

class MatchupView(TemplateView):
    template_name = 'studbud/matchup.html'