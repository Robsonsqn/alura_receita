from django.contrib import admin
from .models import Pessoa

# Register your models here.
class ListandoPessoas(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email')
    list_display_links = ('id', 'nome', 'email')
    list_per_page = 10
    search_fields = ('nome', 'email')

admin.site.register(Pessoa,ListandoPessoas)
