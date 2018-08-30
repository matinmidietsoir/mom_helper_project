from django.db import models


# Create your models here.

# ------------------  Food - Aliment  --------------------

class Food(models.Model):
	name = models.CharField('nom', max_length=100, unique=True)
	shelf_life = models.DurationField('durée de conservation')
	fresh = models.BooleanField('frais', default=True) 
		# pas frais = dans les placards à l'avance, et la plupart du temps 
		# pas besoin de mesurer dans les recettes ni date limite de conservation
		# par exemple huile, sel, poivre
	secable = models.BooleanField('sécable', default=True) #non utilisé pour l'instant

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
#	quantity = models.DecimalField('quantité par personne', decimal_places=3, max_digits=10)
	quantity = models.IntegerField('quantité par personne en grammes') #todo : ou si non sécable, en qté
	recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
	food = models.ForeignKey(Food, on_delete=models.CASCADE)

# ------------------Meal - Repas  --------------------

NOON = 0
NIGHT = 1
MOMENT_CHOICES = (
    (NOON, 'midi'),
    (NIGHT, 'soir')
)


class Meal(models.Model):
	date = models.DateField()
	moment = models.IntegerField(choices=MOMENT_CHOICES)
	nb_of_guests = models.IntegerField()
	foods = models.ManyToManyField(Food, through='Provision')
	recipes = models.ManyToManyField(Recipe)

	def __str__(self):
		return str(self.date)+" "+str(MOMENT_CHOICES[self.moment][1])+" ("+str(self.nb_of_guests)+" invité(s))"

	class Meta:
		verbose_name = "repas"
		verbose_name_plural = "repas"

# ------------------Provision  --------------------

WAIT = 0
PLANNED = 1
BOUGHT = 2
STATUS_CHOICES = (
    (WAIT, 'en attente'),
    (PLANNED, 'prévu dans une liste'),
    (BOUGHT, 'acheté'),
)

class Provision(models.Model):
	status = models.IntegerField(choices = STATUS_CHOICES, default=0)
	quantity = models.IntegerField()
	meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
	food = models.ForeignKey(Food, on_delete=models.CASCADE)