from django.contrib import admin
from .models import Filme, Rating

class FilmeAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class RatingAdmin(admin.ModelAdmin):
    search_fields = ()


admin.site.register(Filme, FilmeAdmin)
admin.site.register(Rating, RatingAdmin)