from django.db import models
from django.utils.text import slugify

# ✅ Les 58 wilayas d’Algérie (id, nom)
WILAYAS = [
    ("01", "Adrar"), ("02", "Chlef"), ("03", "Laghouat"), ("04", "Oum El Bouaghi"),
    ("05", "Batna"), ("06", "Béjaïa"), ("07", "Biskra"), ("08", "Béchar"),
    ("09", "Blida"), ("10", "Bouira"), ("11", "Tamanrasset"), ("12", "Tébessa"),
    ("13", "Tlemcen"), ("14", "Tiaret"), ("15", "Tizi Ouzou"), ("16", "Alger"),
    ("17", "Djelfa"), ("18", "Jijel"), ("19", "Sétif"), ("20", "Saïda"),
    ("21", "Skikda"), ("22", "Sidi Bel Abbès"), ("23", "Annaba"), ("24", "Guelma"),
    ("25", "Constantine"), ("26", "Médéa"), ("27", "Mostaganem"), ("28", "MSila"),
    ("29", "Mascara"), ("30", "Ouargla"), ("31", "Oran"), ("32", "El Bayadh"),
    ("33", "Illizi"), ("34", "Bordj Bou Arreridj"), ("35", "Boumerdès"), ("36", "El Tarf"),
    ("37", "Tindouf"), ("38", "Tissemsilt"), ("39", "El Oued"), ("40", "Khenchela"),
    ("41", "Souk Ahras"), ("42", "Tipaza"), ("43", "Mila"), ("44", "Aïn Defla"),
    ("45", "Naâma"), ("46", "Aïn Témouchent"), ("47", "Ghardaïa"), ("48", "Relizane"),
    ("49", "Timimoun"), ("50", "Bordj Badji Mokhtar"), ("51", "Ouled Djellal"),
    ("52", "Béni Abbès"), ("53", "In Salah"), ("54", "In Guezzam"),
    ("55", "Touggourt"), ("56", "Djanet"), ("57", "El M'Ghair"), ("58", "El Meniaa"),
]

# ✅ Catégories
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class MessageContact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.email}"
  
   
class Commande(models.Model):
    date_commande = models.DateTimeField(auto_now_add=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    # ✅ Wilaya
    wilaya = models.CharField(max_length=2, choices=WILAYAS, default="16")

    TYPE_LIVRAISON_CHOICES = [
        ("domicile", "Livraison à domicile"),
        ("retrait", "Point de retrait"),
    ]
    type_livraison = models.CharField(
        max_length=20,
        choices=TYPE_LIVRAISON_CHOICES,
        default="domicile"
    )

    # ✅ Commune
    commune = models.CharField(max_length=100, blank=True, null=True)

    # ✅ Nouveau champ status
    STATUS_CHOICES = [
        ("Nouveau", "🆕 Nouveau"),
        ("Assuré", "✅ Assuré"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Nouveau"
    )

    def __str__(self):
        return f"Commande #{self.id} - {self.nom}"



class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="lignes")
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    taille = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.quantite} x {self.article.titre}"


class CommandeImage(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='commandes/')

    def __str__(self):
        return f"Image pour {self.commande}"


# ✅ Articles
class Article(models.Model):
    titre = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    couleur = models.CharField(max_length=100, blank=True, null=True)
    publie = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles")

    def __str__(self):
        return self.titre


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='articles/')
    ordre = models.IntegerField(default=0)  # Pour définir l'ordre d'affichage

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"Image pour {self.article.titre}"


# ✅ Orders (ancien modèle, si tu veux le garder séparé)
class Order(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='orders/', blank=True, null=True)

    def __str__(self):
        return self.name
