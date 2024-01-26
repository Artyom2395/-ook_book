from django.contrib import admin
from .models import Product, Recipe, RecipeProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'times_used']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(RecipeProduct)
class RecipeProductAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'product', 'weight']