from django.db import models
from .static.meals.constants import *
from datetime import date

# Create your models here.

# ------------------  Food - Aliment  --------------------




class Food(models.Model):
	name = models.CharField('nom', max_length=100, unique=True)
	shelf_life = models.DurationField('durée de conservation')
	category = models.IntegerField(choices = FOOD_CATEGORY_CHOICES)
#	fresh = models.BooleanField('frais', default=True) 
		# pas frais = dans les placards à l'avance, et la plupart du temps 
		# pas besoin de mesurer dans les recettes ni date limite de conservation
		# par exemple huile, sel, poivre
		# to do : catégories au lieu de fresh : fruit/légume, viande, crémerie, épicerie... plus facile pour rechercher 
	secable = models.BooleanField('sécable', default=True) 
		#non utilisé pour l'instant, pour ce qui ne s'achète pas au poids (les oeufs)
		#peut-être il vaudrait mieux aller directement dans POIDS_ET_NB (carottes), NB (oeufs), VOLUME (crème) suivant les aliments. 
		#avec une table de conversion poids / nb pour ceux de cette catégorie (fruits et légumes)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "aliment"

# ------------------  Recipe - recette --------------------

# todo : type de recette (salade, gratin, fricassée, ...) 
# et catégorie (entrée, plat, accompagnement, dessert)
class Recipe(models.Model):
	name = models.CharField('nom', max_length=400, unique=True)
	foods = models.ManyToManyField(Food, through='Ingredient')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "recette"

# ------------------  Ingredient  --------------------

#todo : traduire quantité en g en quantité pour nonsécables (les oeufs par exemple.)
class Ingredient(models.Model):
	quantity = models.DecimalField('quantité par personne en grammes (ou en nb pour les oeufs)', decimal_places=1, max_digits=5)
#	quantity = models.IntegerField('quantité par personne en grammes') #todo : ou si non sécable, en qté
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	food = models.ForeignKey(Food, on_delete=models.CASCADE)

# ------------------Meal - Repas  --------------------


class Meal(models.Model):
	date = models.DateField("date du repas")
	moment = models.IntegerField("midi ou soir", choices=MOMENT_CHOICES)
	nb_of_guests = models.IntegerField("nombre de convives")
	foods = models.ManyToManyField(Food, through='Provision')
	recipes = models.ManyToManyField(Recipe)

	def __str__(self):
		return str(self.date.strftime('%A %d %b'))+" "+str(MOMENT_CHOICES[self.moment][1])+" ("+str(self.nb_of_guests)+" invité(s))"

	class Meta:
		verbose_name = "repas"
		verbose_name_plural = "repas"

# ------------------Provision  --------------------



class Provision(models.Model):
	status = models.IntegerField("état", choices = STATUS_CHOICES, default=0)
	quantity = models.IntegerField("quantité")
	meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
	food = models.ForeignKey(Food, on_delete=models.CASCADE)

	def __str__(self):
		return self.food.name
	class Meta:
		verbose_name = "aliment pour un repas"
		verbose_name_plural = "aliments pour un repas"


# ------------------ Supplier - Fournisseur  --------------------

class Supplier(models.Model):
	name = models.CharField('nom', max_length=100, unique=True)
	foods = models.ManyToManyField(Food, related_name='suppliers')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "fournisseur"
	

# ------------------ Shopping - Courses  --------------------

class Shopping(models.Model):
	date = models.DateField("date des achats")
	supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
	meals = models.ManyToManyField(Meal)
	foods = models.ManyToManyField(Food, through='ListElement') 

	def __str__(self):
		return str(self.date.strftime('%A %d %b'))+" chez '"+str(self.supplier)+"'"

	class Meta:
		verbose_name = "course"

# ------------------ ListElement - Elément d'une Liste de course  --------------------

class ListElement(models.Model):
	status = models.IntegerField("état",choices = LIST_STATUS_CHOICES, default=1)
	quantity = models.IntegerField("quantité")
	shopping = models.ForeignKey(Shopping, on_delete=models.CASCADE)
	food = models.ForeignKey(Food, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural ="liste de courses"