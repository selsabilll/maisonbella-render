from django.contrib import admin
from .models import Article, Commande, Category, ArticleImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 3  # Nombre de champs image vides affichés

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix', 'category', 'publie')
    list_filter = ('category', 'publie')
    search_fields = ('titre', 'category__name')
    inlines = [ArticleImageInline]

@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ['article', 'ordre']

# Enregistrer Commande simplement
admin.site.register(Commande)