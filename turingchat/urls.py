"""
URL configuration for turingchat project.

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
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.game_home_page, name="home_page"),
    path('create_game.html',views.create_game, name="create_game"),
    path('human_response.html',views.fetch_question,name="human_response"),
    path('feedback.html',views.check_guess,name="fetch_question"),
    path('fetch_responses.html/',views.fetch_responses,name="fetch_responses")
]
