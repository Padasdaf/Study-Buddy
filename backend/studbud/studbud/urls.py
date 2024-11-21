"""
URL configuration for studbud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from homepage.views import HomeView, LoginView, ProfileView, HistoryView, FeedbackView, MatchupView, BuddiesView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('history/', HistoryView.as_view(), name='history'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('matchup/', MatchupView.as_view(), name='matchup'),
    path('matchup/buddies/', BuddiesView.as_view(), name='buddies')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
