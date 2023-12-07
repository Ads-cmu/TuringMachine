from django.shortcuts import render
from app.models import AI, Game, Round, Feedback
import random
from django.http import JsonResponse
from django.utils import timezone
import requests
import time
from django.views.decorators.http import require_http_methods
from app.impersonate import get_model_response

def game_home_page(request):
    players = [model.user for model in AI.objects.all()]
    context = {'players':players}
    return JsonResponse(context) 

def create_game(request):
    name = request.GET.get('name')
    if name is None:
        name="Meghana"
    try:
        ai_model = AI.objects.get(user=name)
    except AI.DoesNotExist:
        return JsonResponse({'error': 'Model not found'}, status=404)

    a_is_model = random.choice([True, False])
    game = Game.objects.create(a_is_model=a_is_model, model_id=ai_model, create_time=timezone.now())
    return JsonResponse({'game_id': game.id})

def fetch_responses(request):
    question = request.GET.get('question')
    game_id = request.GET.get('game_id')
    game = Game.objects.get(id=game_id)
    round = Round.objects.create(game_id=game, question=question)
    model = game.model_id
    model_answer = get_model_response(question, model)
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

def check_guess(request):
    guess = request.GET.get('guess')
    game_id = request.GET.get('game_id')
    num_questions = int(request.GET.get('num_questions'))
    game = Game.objects.get(id=game_id)
    guess = guess == 'True'
    win = guess==game.a_is_model
    game.correct_guess=win
    game.num_questions = num_questions
    game.save()
    return JsonResponse({'win':win}) 

def save_feedback(request):
    difficulty = request.GET.get('difficulty')
    reason = request.GET.get('reason')
    comment = request.GET.get('comment')
    feedback = Feedback.objects.create(difficulty=difficulty, reason=reason, comment=comment)
    return JsonResponse({'saved_feedback':True}) #we should give the user feedback that their feedback has been saved

def fetch_question(request):
    game = Game.objects.last()
    model = game.model_id
    all_rounds = Round.objects.filter(game_id=game.id)
    for round in all_rounds:
        if round.human_answer is None:
            return JsonResponse({'human':model.user,'round_id':round.id,'is_question':True,'question':round.question})
    return JsonResponse({'is_question':False,'question':'NA'})

#make get request to receive response 
def save_human_response(request):
    round_id = request.GET.get('round_id')
    answer = request.GET.get('answer')
    round = Round.objects.get(id=round_id)
    round.human_answer=answer
    round.save()
    return JsonResponse({'saved_response':True})
    
