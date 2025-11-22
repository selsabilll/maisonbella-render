import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Article, Commande, CommandeImage, LigneCommande, ArticleImage, WILAYAS
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
  

def help(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_content = request.POST.get("message")

        # Préparer le mail HTML avec un peu de style
        html_message = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
            <h2 style="color: #2E86C1;">Nouveau message depuis le formulaire de contact</h2>
            <p><strong>Nom :</strong> {name}<br>
            <strong>Email :</strong> {email}</p>
            <p><strong>Message :</strong></p>
            <div style="padding: 10px; background-color: #F2F3F4; border-radius: 5px;">
                {message_content}
            </div>
            <p style="font-size: 12px; color: #888;">Ce message a été envoyé depuis votre site web.</p>
        </div>
        """

        # Envoi du mail HTML
        try:
            send_mail(
                subject=f"Message de {name} ({email})",
                message=f"Message de {name}: {message_content}",  # texte brut fallback
                from_email='raoufzsjj@gmail.com',
                recipient_list=['selsabilachaima.lounis@gmail.com'],  # ton email pour recevoir
                html_message=html_message,
                fail_silently=False
            )
            messages.success(request, "Votre message a bien été envoyé par email ✅")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi du mail : {e}")

    return render(request, "main/help.html")






# ✅ Page produits
def product(request):
    articles = Article.objects.filter(publie=True).prefetch_related('images')
    return render(request, 'main/product.html', {'articles': articles})

# ✅ Page accueil
def home(request):
    return render(request, 'main/home.html')
# ✅ Marquer une commande comme assurée
def assurer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if commande.status == "Nouveau":  # Vérifie avant de changer
        commande.status = "Assuré"
        commande.save()
        messages.success(request, f"La commande #{commande.id} a été marquée comme assurée ✅")
    else:
        messages.info(request, f"La commande #{commande.id} est déjà assurée.")
    return redirect("ord")  # Redirige vers la liste des 

# ✅ Voir
def voir(request):
    return render(request, "main/voir.html")


# ✅ Filtrer par catégorie
def category(request, category_name):
    articles = Article.objects.filter(category__name=category_name, publie=True).prefetch_related('images')
    return render(request, 'main/category.html', {'articles': articles, 'category_name': category_name})

def commande(request):
    if request.method == "POST":
        # Création de la commande principale
        nouvelle_commande = Commande.objects.create(
            nom=request.POST.get("nom"),
            prenom=request.POST.get("prenom"),
            adresse=request.POST.get("adresse"),
            telephone=request.POST.get("telephone"),
            wilaya=request.POST.get("wilaya"),
            commune=request.POST.get("commune"),
            type_livraison=request.POST.get("type_livraison") or request.POST.get("delivery_type")
        )

        # Récupération des données du panier
        cart_data = request.POST.get("cart_data")
        if cart_data:
            try:
                panier = json.loads(cart_data)
                for item in panier:
                    article_id = item.get("id") or item.get("product_id") or item.get("articleId")
                    if not article_id:
                        continue
                    try:
                        if isinstance(article_id, str):
                            article_id = int(article_id)
                        article = Article.objects.get(id=article_id)
                        quantite = item.get("quantity") or item.get("qty") or item.get("quantite") or 1
                        taille = item.get("size") or item.get("taille") or ""
                        LigneCommande.objects.create(
                            commande=nouvelle_commande,
                            article=article,
                            quantite=quantite,
                            taille=taille
                        )
                    except (Article.DoesNotExist, ValueError, TypeError):
                        continue
            except json.JSONDecodeError:
                pass

        # Construction du contenu HTML pour le mail
        from django.utils.html import escape
        lignes = LigneCommande.objects.filter(commande=nouvelle_commande)
        html_rows = ""
        for ligne in lignes:
            html_rows += f"""
            <tr>
                <td style="border:1px solid #ccc; padding:8px;">{escape(nouvelle_commande.nom)}</td>
                <td style="border:1px solid #ccc; padding:8px;">{escape(nouvelle_commande.prenom)}</td>
                <td style="border:1px solid #ccc; padding:8px;">{escape(nouvelle_commande.telephone)}</td>
                <td style="border:1px solid #ccc; padding:8px;">{escape(nouvelle_commande.adresse)}, {escape(nouvelle_commande.commune)}, {escape(nouvelle_commande.wilaya)}</td>
                <td style="border:1px solid #ccc; padding:8px;">{escape(nouvelle_commande.type_livraison)}</td>
                <td style="border:1px solid #ccc; padding:8px;">{escape(ligne.article.titre)}</td>
                <td style="border:1px solid #ccc; padding:8px;">{escape(ligne.quantite)}</td>
                <td style="border:1px solid #ccc; padding:8px;">{escape(ligne.taille)}</td>
                <td style="border:1px solid #ccc; padding:8px;">{escape(ligne.article.prix)} DA</td>
            </tr>
            """

        html_message = f"""
        <div style="font-family: Arial, sans-serif; line-height:1.5; color:#333;">
            <h2 style="color:#2E86C1;">Nouvelle commande #{nouvelle_commande.id}</h2>
            <table style="border-collapse:collapse; width:100%; max-width:800px;">
                <thead>
                    <tr style="background-color:#2E86C1; color:#fff;">
                        <th style="border:1px solid #ccc; padding:8px;">Nom</th>
                        <th style="border:1px solid #ccc; padding:8px;">Prénom</th>
                        <th style="border:1px solid #ccc; padding:8px;">Téléphone</th>
                        <th style="border:1px solid #ccc; padding:8px;">Adresse</th>
                        <th style="border:1px solid #ccc; padding:8px;">Type de livraison</th>
                        <th style="border:1px solid #ccc; padding:8px;">Article</th>
                        <th style="border:1px solid #ccc; padding:8px;">Quantité</th>
                        <th style="border:1px solid #ccc; padding:8px;">Taille</th>
                        <th style="border:1px solid #ccc; padding:8px;">Prix</th>
                    </tr>
                </thead>
                <tbody>
                    {html_rows}
                </tbody>
            </table>
            <p style="margin-top:10px; font-weight:bold;">Total lignes : {lignes.count()}</p>
            <p style="font-size:12px; color:#888;">Ce message a été envoyé depuis votre site web.</p>
        </div>
        """

        # Envoi du mail
        try:
            send_mail(
                subject=f"Nouvelle commande #{nouvelle_commande.id}",
                message="Nouvelle commande",  # fallback texte brut
                from_email='raoufzsjj@gmail.com',  # ton Gmail
                recipient_list=['selsabilachaima.lounis@gmail.com'],  # email qui reçoit la commande
                html_message=html_message,
                fail_silently=False
            )
        except Exception as e:
            messages.error(request, f"Erreur lors de l'envoi du mail de commande : {e}")

        messages.success(request, "Votre commande a été enregistrée avec succès ✅")
        return redirect("/")

    return render(request, "main/commande.html", {"WILAYAS": WILAYAS})



@user_passes_test(lambda u: u.is_superuser, login_url='/')
def ord(request):
    commandes = Commande.objects.prefetch_related('lignes__article__images').all().order_by('-date_commande')
    return render(request, "main/ord.html", {"commandes": commandes})



# ✅ Page détail article
def orders(request, id):
    article = get_object_or_404(Article.objects.prefetch_related('images'), id=id) 
    return render(request, "main/orders.html", {"article": article})


# ✅ Ajouter un article
def ajouter_article(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        prix = request.POST.get('prix')
        couleur = request.POST.get('couleur')
        publie = bool(request.POST.get('publie'))

        # Créer l'article sans image
        article = Article.objects.create(
            titre=titre,
            prix=prix,
            couleur=couleur,
            publie=publie
        )

        # Ajouter les images si elles existent
        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            ArticleImage.objects.create(
                article=article,
                image=image,
                ordre=i  # Pour définir l'ordre d'affichage
            )

        return redirect('home')

    return render(request, 'main/ajouter_article.html')


# ✅ Supprimer un article
def delete_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()  # Les images liées seront supprimées automatiquement (CASCADE)
    return redirect('home')


# ✅ Ajouter des images à une commande
def ajouter_images_commande(request, id):
    commande = get_object_or_404(Commande, id=id)
    if request.method == 'POST':
        for fichier in request.FILES.getlist('images'):
            CommandeImage.objects.create(commande=commande, image=fichier)
        return redirect('orders', id=commande.id)
    return render(request, 'main/ajouter_images_commande.html', {'commande': commande})


# ✅ Ajouter des images à un article existant
def ajouter_images_article(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        ordre_max = ArticleImage.objects.filter(article=article).count()
        
        for i, image in enumerate(images):
            ArticleImage.objects.create(
                article=article,
                image=image,
                ordre=ordre_max + i
            )
        messages.success(request, f"{len(images)} image(s) ajoutée(s) à l'article.")
        return redirect('orders', id=article.id)
    
    return render(request, 'main/ajouter_images_article.html', {'article': article})
