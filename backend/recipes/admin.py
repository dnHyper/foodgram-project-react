from django.contrib import admin

from .models import Ingredient, Recipes, Tag


class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'display_tag',
        'pub_date',
        'is_favorite'
    )
    list_editable = ('name', 'author')
    list_display_links = ('pk',)
    search_fields = ('text', 'name')
    list_filter = ('pub_date', 'author', 'tags')
    fields = ('name', 'text', 'tags', 'author')

    def is_favorite(self, obj):
        return obj.favorite.count()
    is_favorite.short_description = 'В избранном'


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
