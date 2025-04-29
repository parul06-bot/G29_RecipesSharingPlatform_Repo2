from django.contrib import admin

# Register your models here.
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    list_filter = ('created_by', 'cuisine')
    search_fields = ('title', 'description')

