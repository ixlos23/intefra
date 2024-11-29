# Register your models here.
from django.contrib import admin

from .models import Film, Genre


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date')
    filter_horizontal = ('genre',)


admin.site.register(Genre)
