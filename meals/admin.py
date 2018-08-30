from django.contrib import admin

from .models import Food, Recipe, Ingredient, Meal, Provision

# ------------------  Food - Aliment  --------------------
class FoodAdmin(admin.ModelAdmin):
	list_display = ('name', 'shelf_life', 'fresh')
	ordering       = ('-fresh','name', )
	search_fields  = ('name',)
	list_filter    = ('fresh',) #'shelf_life',) ça fait planter avec shelf_life..

admin.site.register(Food, FoodAdmin)

# ------------------  Recipe - recette --------------------


class IngredientsInline(admin.TabularInline):
    model = Ingredient
    fieldsets = [
        (None, {'fields': ['food','quantity',]})
        ] # list columns
    extra=1

class RecipeAdmin(admin.ModelAdmin):
#	list_display = ('name',)
#	fields = ['name']	
	inlines = [IngredientsInline,] # list of ingredients
	ordering = ('name',)

admin.site.register(Recipe, RecipeAdmin)



# ------------------ Meal - Repas---------
class ProvisionsInline(admin.TabularInline):
    model = Provision
    fieldsets = [
        (None, {'fields': ['food','quantity','status',]})
        ] # list columns
    extra=1



class MealAdmin(admin.ModelAdmin):
	inlines = [ProvisionsInline,] # list of ingredients
	ordering = ('date',)
	actions = ['compute_provisions']

# ------------- calcul des provisions à prévoir pour un repas ----------
	def compute_provisions(self, request, queryset):
#	    queryset.update(status='p')
		
		# --- pour chaque recette des repas de queryset --
		# --- pour chaque aliment frais
		# --- mettre à jour quantity dans la table Provisions en fonction du nb_of_guest 
		# de quantity dans la recette (qui est la quantité par personne)

#	c'est pas du tout optimisé mais ça marche et c'est déjà ça
		message_bit = ""
		for repas in queryset:
			recettes = Recipe.objects.filter(meal=repas)
			

			for recette in recettes:
				my_ingredients = Ingredient.objects.filter(recipe=recette,food__fresh=True)
				message_bit += "/"+recette.name+" : "
				print (recette.name)

				for my_ingredient in my_ingredients:
					
					aliment = Food.objects.filter(ingredient=my_ingredient).first()

					my_quantite = my_ingredient.quantity * repas.nb_of_guests

					my_provision=Provision.objects.filter(meal=repas,food=aliment)
					if my_provision.exists():
						# todo : à ne faire que si l'ingrédient n'est pas encore acheté (status BOUGHT)
						my_provision.quantity = my_quantite
						message_bit += aliment.name + " mise à jour, "
					else:
						my_provision=Provision(meal=repas,food=aliment, quantity=my_quantite)
						my_provision.save()
						message_bit += aliment.name + " créé,  "

					# calcul
#					my_ingredient = Ingredient.objects.filter(food=aliment,recipe=recette)
#					if my_ingredient.exists():
#						message_bit += my_ingredient.quantity+", "
#					else:
#						message_bit += ' prout, '
					


		self.message_user(request, message_bit)

	compute_provisions.short_description = "calculer les provisions nécessaires pour les repas"


admin.site.register(Meal, MealAdmin)