#coding: utf-8

from django.contrib import admin
from .models import Publicacao, Credito

class CreditoInline(admin.TabularInline):
    model = Credito

#class CreditoInline(admin.StackedInline):
#    model = Credito

class PublicacaoAdmin(admin.ModelAdmin):
    inlines = [ CreditoInline, ]

admin.site.register(Publicacao, PublicacaoAdmin)
#admin.site.register(Credito) gracas ao codigo Inline acima, não faz mais sentido que o usuario acesse diretamente o cadastro de creditos.
