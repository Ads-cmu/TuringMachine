from django.shortcuts import render
from app.models import AI, Game, Round
import random
from django.http import JsonResponse
import requests
import time

# Create your views here.
def create_game(request, name):
    try:
        ai_model = AI.objects.get(name=name)
    except AI.DoesNotExist:
        return JsonResponse({'error': 'Model not found'}, status=404)

    a_is_model = random.choice([True, False])
    game = Game.objects.create(A_is_model=a_is_model, model_id=ai_model)

    return JsonResponse({'game_id': game.id})

def fetch_responses(request, question, game_id):
    global question_global, human_response_global
    
    game = Game.objects.get(id=game_id)
    model = AI.objects.get(id=game.model_id)

    round = Round.objects.create(game_id=game.id, question=question)
    model_answer = requests.get(model.endpoint+'?question='+question)
    while round.human_answer is None:
        round = Round.objects.get(id=round.id)
        time.sleep(0.1) #sleep 100ms
    round.model_answer=model_answer
    round.save()
    if game.a_is_model:
        return JsonResponse({'response_a':round.model_answer,'response_b':round.human_answer, 'game_id':game.id})
    return JsonResponse({'response_b':round.model_answer,'response_a':round.human_answer, 'game_id':game.id})



# def fetch_question():

# def post_human_response():
    