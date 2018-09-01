
FRUIT_VEGETABLES = 0
DAIRY = 1
MEAT = 2
CEREAL = 3
GROCERY = 4
EXTRAS = 5
FOOD_CATEGORY_CHOICES = (
    (FRUIT_VEGETABLES, 'fruits et légumes'),
    (DAIRY, 'crèmerie'),
    (MEAT,'boucherie / charcuterie / poissons'),
    (CEREAL,'pates / riz / céréales'),
    (GROCERY, 'épicerie'),
    (EXTRAS, 'autre')
)

MAX_FRESH_CATEGORY = MEAT #cette catégorie et toutes les catégories en-dessous sont des catégories d'aliments frais


NOON = 0
NIGHT = 1
MOMENT_CHOICES = (
    (NOON, 'midi'),
    (NIGHT, 'soir')
)

WAIT = 0
PLANNED = 1
BOUGHT = 2
STATUS_CHOICES = (
    (WAIT, 'en attente'),
    (PLANNED, 'prévu dans une liste'),
    (BOUGHT, 'acheté'),
)

PLANNED = 1
BOUGHT = 2
DELETED = 3
LIST_STATUS_CHOICES = (
    (PLANNED, 'prévu'),
    (BOUGHT, 'acheté'),
    (DELETED, 'supprimé')
)
