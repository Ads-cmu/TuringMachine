from django.shortcuts import render
from app.models import AI, Game, Round
import random
from django.http import JsonResponse
from django.utils import timezone
import requests
import time
from django.views.decorators.http import require_http_methods

def game_home_page(request):
    models = AI.objects.all()
    players = []
    for model in models:
        players.append(model.user)
    context = {'players':players}
    return JsonResponse(context) #placeholder, not sure what to put here

def create_game(request, name="Meghana"):
    try:
        ai_model = AI.objects.get(user=name)
    except AI.DoesNotExist:
        return JsonResponse({'error': 'Model not found'}, status=404)

    a_is_model = random.choice([True, False])
    game = Game.objects.create(a_is_model=a_is_model, model_id=ai_model, create_time=timezone.now())
    game.save()
    return JsonResponse({'game_id': game.id})

def fetch_responses(request, question, game_id):
    game = Game.objects.get(id=game_id)
    model = AI.objects.get(id=game.model_id.id)

    round = Round.objects.create(game_id=game, question=question)
    model_answer = "Placeholder"#requests.get(model.endpoint+'?question='+question)
    print(f"reached {round.id}")
    while round.human_answer is None:
        round = Round.objects.get(id=round.id)
        time.sleep(0.1) #sleep 100ms
    round.model_answer=model_answer
    round.save()
    if game.a_is_model:
        context = {'response_a':round.model_answer,'response_b':round.human_answer, 'game_id':game.id, 'round_id':round.id}
    else:
        context = {'response_b':round.model_answer,'response_a':round.human_answer, 'game_id':game.id, 'round_id':round.id}
    return JsonResponse(context)

def check_guess(request, guess, game_id):
    game = Game.objects.get(id=game_id)
    win = False
    if guess==game.a_is_model:
        win=True
    
    return JsonResponse({'win':win}) 

def save_feedback(request):

    return False

def fetch_question(request):
    game = Game.objects.all().order_by('-create_time')[0]
    all_rounds = Round.objects.filter(game_id=game.id)
    for round in all_rounds:
        if round.human_answer is None:
            return JsonResponse({'round_id':round.id,'is_question':True,'question':round.question}) #add person
    return JsonResponse({'is_question':False,'question':'NA'})

#make get request to receive response 
# def post_human_response(request, round_id, answer):
    