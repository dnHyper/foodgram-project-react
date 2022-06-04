from django.contrib import admin

from .models import Ingredient, Recipes, Tag


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'pub_date', 'cooking_time', 'author')
    search_fields = ('text', 'name')
    list_filter = ('pub_date',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
