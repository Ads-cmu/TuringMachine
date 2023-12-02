from django.db import models

# Create your models here.
class AI(models.Model):
    user = models.CharField(max_length=300)
    endpoint = models.CharField(max_length=300)

class Game(models.Model):
    a_is_model = models.BooleanField(null=True)
    user_guess = models.CharField(max_length=30, blank=True,null=True)
    model_id = models.ForeignKey(AI, on_delete=models.PROTECT)

class Round(models.Model):
    game_id = models.ForeignKey(Game, on_delete=models.PROTECT)
    question = models.CharField(max_length=300)
    model_answer = models.CharField(max_length=300, blank=True,null=True)
    human_answer = models.CharField(max_length=300, blank=True,null=True)

                            