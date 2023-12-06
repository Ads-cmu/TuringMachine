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
    path('fetch_responses.html/',views.fetch_responses,name="fetch_responses")
    path('human_response.html',views.fetch_question,name="human_response"),
    path('feedback.html',views.check_guess,name="fetch_question"),
]

'''
Tests:
game_home_page

create_game name
http://34.228.80.251:8000/create_game.html?name=Meghana

fetch_responses question, game_id
http://34.228.80.251:8000/fetch_responses.html?question=Hi&game_id=1

check_guess guess, game_id

save_feedback difficulty, reason, comment

fetch_question

save_human_response round_id, answer
'''