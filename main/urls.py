from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('voir', views.voir, name="voir"),
        path('help', views.help, name="help"),

    path('product/', views.product, name="product"),
    path('category/<str:category_name>/', views.category, name='category'),
    path('ajouter-article/', views.ajouter_article, name="ajouter_article"),
    path('delete_article/<int:id>/', views.delete_article, name="delete_article"),
    path('commande/', views.commande, name="commande"),
    path('orders/<int:id>/', views.orders, name="orders"),
    path('ord/', views.ord, name="ord"),
        path("commande/<int:commande_id>/assurer/", views.assurer_commande, name="assurer_commande"),

    # Nouvelle route pour ajouter des images aux articles existants
    path('article/<int:id>/ajouter-images/', views.ajouter_images_article, name='ajouter_images_article'),
    
    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name="main/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]