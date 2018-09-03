from django.contrib import admin
from django import forms
from django.forms import ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Food, Recipe, Ingredient, Meal, Provision, Supplier, Shopping, ListElement
from .static.meals.constants import *
#from django.core.exceptions import DoesNotExist #pas besoin
from datetime import date

#test https://www.apidev.fr/blog/2010/07/13/5-astuces-pour-ameliorer-le-site-d-admin-de-django/
from django.forms.models import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

from admin_extend.extend import extend_registered, add_bidirectional_m2m, registered_form


# admin.py

# ------------------  Food - Aliment  --------------------

class ListElementsForFoodInline(admin.TabularInline):
    model = ListElement
    

class ProvisionsForFoodInline(admin.TabularInline):
    model = Provision
    # attention il faudrait filtrer seulement les repas autour de la date d'aujourd'hui
    # ou ceux pour lesquels il y a eu des courses de faites qui étaient des courses pour au moins un repas de la date d'aujourd'hui.
    # et les afficher de façon plus sexy pour qu'on sachent au moins si le repas est passé au non. 

class FoodAdmin(admin.ModelAdmin):
	#affichage de la liste
	list_display = ('name', 'shelf_life', 'category')
	list_editable = ("shelf_life", "category")
	ordering       = ('category', 'name',"-shelf_life" )
	search_fields  = ('name',)
	list_filter    = ('category',) #'shelf_life',) ça fait planter avec shelf_life..

	#affichage du détail
#	filter_horizontal = ('provision',) 
	inlines = [ProvisionsForFoodInline, ListElementsForFoodInline] # list of aliments


admin.site.register(Food, FoodAdmin)

@extend_registered
class ExtendedFoodAdminForm(add_bidirectional_m2m(registered_form(Food))):

    suppliers = ModelMultipleChoiceField(
        queryset=Supplier.objects.all(),
        widget=FilteredSelectMultiple('fournisseurs',False)
    )

    def _get_bidirectional_m2m_fields(self):
        return super(ExtendedFoodAdminForm, self).\
            _get_bidirectional_m2m_fields() + [('suppliers', 'suppliers')]


# ------------------  Recipe - recette --------------------


class IngredientsInline(admin.TabularInline):
    model = Ingredient
    fieldsets = [
        (None, {'fields': ['food','quantity',]})
        ] # list columns
    extra=1
    verbose_name='ingrédients'


class RecipeAdmin(admin.ModelAdmin):
	
	#affichage de la liste
	def list_of_ingredients(self, queryset):
		#rechercher les ingredients et les merger
		aliments = Food.objects.filter(ingredient__recipe=queryset.id, category__lte = MAX_FRESH_CATEGORY).order_by('-ingredient__quantity')
		message = ', '.join(str(x) for x in aliments)
		return message

	list_of_ingredients.short_description = 'ingrédients frais'
	ordering = ('name',)
	search_fields  = ('name',)
	list_display = ('name','list_of_ingredients')

	# affichage du détail
	inlines = [IngredientsInline,] # list of ingredients

admin.site.register(Recipe, RecipeAdmin)

# ------------------ Meal - Repas---------
class ProvisionsInline(admin.TabularInline):
    model = Provision
    fieldsets = [
        (None, {'fields': ['food','quantity','status',]})
        ] # list columns
    extra=1
# c'est là qu'on voudrait afficher les quantités qui ont été achetées, pour toutes les courses 
# qui contiennent cet aliment et des repas à la même date que celui-ci ou après


class MealAdmin(admin.ModelAdmin):
	
	def list_of_recipes(self, queryset):
		#rechercher les recettes et les merger
		recettes = Recipe.objects.filter(meal__id=queryset.id) #.order_by('-ingredient__quantity') (# todo dans l'ordre du repas entrée plat accom dessert)
		#je reste stupéfaite de meal__id alors que ça devrait être meals__id
		message = ', '.join(str(x) for x in recettes)
		return message

	def weekdayname(self, queryset):
		return queryset.date.strftime('%A')

	ordering = ('date','moment')
	actions = ['compute_provisions']
	date_hierarchy = 'date'

	list_of_recipes.short_description = 'menu'
	weekdayname.short_description = 'jour'
	list_display = ('date','weekdayname','moment','nb_of_guests','list_of_recipes')


# ------------- calcul des provisions à prévoir pour un repas ----------
	def compute_provisions(self, request, queryset):
#	    queryset.update(status='p')
		
		# --- pour chaque recette des repas de queryset --
		# --- pour chaque aliment frais
		# --- mettre à jour quantity dans la table Provisions en fonction du nb_of_guest 
		# de quantity dans la recette (qui est la quantité par personne)

# todo : si statut "prévu dans une liste" PLANNED il va falloir mettre à jour la liste !
# si une liste course est modifiée / effacée, il faut aussi remettre le statut à WAIT

#	c'est pas du tout optimisé mais ça marche et c'est déjà ça
		message_bit = ""
		for repas in queryset:
			recettes = Recipe.objects.filter(meal=repas)
			

			for recette in recettes:
				my_ingredients = Ingredient.objects.filter(recipe=recette, food__category__lte=MAX_FRESH_CATEGORY)
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

					

		self.message_user(request, message_bit)

	compute_provisions.short_description = "calculer les provisions nécessaires pour les repas" #ça serait à faire lorsqu'on sauve un Shopping

	#affichage du détail
	inlines = [ProvisionsInline,] # list of ingredients
	filter_horizontal = ('recipes',)

admin.site.register(Meal, MealAdmin)



# ------------------ Supplier - Fournisseur  --------------------
admin.site.register(Supplier)
	
# ------------------ Shopping - Courses  --------------------

class ListElementsInline(admin.TabularInline):
    model = ListElement


#definir un formulaire #pas utile ici c'est pour garder en mémoire cette possibilité
class MyModelForm(ModelForm):
    #on definit les formats de date acceptes 
    my_date = DateField(input_formats=['%d/%m/%Y','%Y-%m-%d'],                        
                        # et on affecte le widget de date du site d'administration 
                        widget=AdminDateWidget(format='%d/%m/%Y'))
    class Meta:
        model = Shopping
        fields = ['my_date','date','supplier','meals']
	 
class ShoppingAdmin(admin.ModelAdmin):
	

	ordering = ('date',)
	date_hierarchy = 'date'
	actions = ['compute_listelement']

	#calculer la liste
	#seulement les aliments "frais", les autres feront l'objet d'un traitement sans calcul (affichage d'une liste sans quantité)
# ------------- calcul des provisions à prévoir pour un repas ----------
	def compute_listelement(self, request, queryset):
		
		# queryset = les courses (= une date, un fournisseur, des repas)

		# --- pour chaque provision fraiche des meals de queryset --
		# --- mettre à jour quantity dans la table listelement en ajoutant les quantités prévues dans "provisions" 
		
		# chercher les provisions fraiches (table food) nécessaires pour ces courses (en passant par la table meal), et qui ont le bon fournisseur (table supplier)
		# et qui sont en attente (WAIT)

		message_bit='ajout dans la liste de '
		# lister les repas prévus dans ces courses
		for course in queryset:
			repass = Meal.objects.filter(shopping = course)

			for repas in repass:
				# trouver les provisions fraiches pour chaque repas
				my_provisions = Provision.objects.filter(status = WAIT, food__category__lte = MAX_FRESH_CATEGORY, meal=repas)
				message_bit +=' repas '+ str(repas) + str(len(my_provisions))
				# il faut aussi que le fournisseur soit le bon 
					
				for my_provision in my_provisions:
					fournisseurs = Supplier.objects.filter(foods__id = my_provision.food.id) 

					if course.supplier in fournisseurs:
					#on verra pour la date plus tard : la date des courses soit < date du repas - durée de conservation
						try:
							ligne = ListElement.objects.get(shopping = course, food = my_provision.food) 
							#même aliment, mais pas même provision (la provision dépend du repas, donc on ne peut pas faire provision=my_provision)
						except :  #DoesNotExist ne veut pas décidément
							ligne = ListElement.objects.create(shopping = course, food=my_provision.food, quantity= my_provision.quantity)
							message_bit += str(my_provision.quantity)+" créé pour aliment "+str(my_provision.food)+", "
						else:		
							new_quantity = ligne.quantity + my_provision.quantity
							ligne.quantity = new_quantity
							ligne.save()
							message_bit += str(my_provision.quantity)+" ajouté pour aliment "+str(my_provision.food)+", "
						my_provision.status = PLANNED
						my_provision.save()
						
		self.message_user(request, message_bit)
#	c'est pas du tout optimisé mais ça marche et c'est déjà ça
	compute_listelement.short_description = "calculer les listes de courses"


	
	#le site d'admin utilisera notre formulaire
	form = MyModelForm 

	#affichage du détail
	inlines = [ListElementsInline] # list of aliments
	#attention il ne faudrait afficher que les repas après la date des courses !
	#comment surcharger la recherche de tous les repas ?

# il faut pouvoir dire que les courses ont été faites, et éventuellement modifier les quantité, et renseigner les aliments qui n'ont pas été trouvés 
# + d'autres choses achetées en plus pourquoi pas. Ca doit faire passer les "provisions" de "prévu" PLANNED à "acheté" BOUGHT

	filter_horizontal = ('meals',)

#	raw_id_fields = ("meals",) # autre façon de sélectionner les repas

admin.site.register(Shopping, ShoppingAdmin)