from django.apps import AppConfig


class MealsConfig(AppConfig):
    name = 'meals'
    verbose_name = 'Les Repas' 
    #çverbose_name ça marche pas, peut-être ajouter un truc dans init.py mais j'ai peur que ça mette tout par terre
