from collections import Counter
import re
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

#Etape 1 : Fonction pour compter les occurrences des mots dans un texte
def compter_occurrences(texte):
    mots = re.findall(r'\b\w+\b', texte.lower())
    comptage = Counter(mots)
    return dict(sorted(comptage.items(), key=lambda item: item[1], reverse=True))

#Etape 2 : Fonction pour retirer les mots parasites
def retirer_mots_parasites(comptage, mots_parasites):
    return {mot: occ for mot, occ in comptage.items() if mot not in mots_parasites}

#Etape 3 : Fonction pour récupérer les mots parasites d'un fichier
def recuperer_mots_parasites(fichier):
    with open(fichier, mode='r', encoding='utf-8') as file:
        mots_parasites = file.read().splitlines()
    return mots_parasites

#Etape 5 : Fonction pour retirer les balises HTML d'une chaine de caractères
def retirer_balises_html(chaine_html):
    soup = BeautifulSoup(chaine_html, 'html.parser')
    return soup.get_text()

#Etape 6 : Fonction pour récupérer les valeurs d'un attribut spécifique
def recuperer_attributs(chaine_html, balise, attribut):
    soup = BeautifulSoup(chaine_html, 'html.parser')
    return [tag[attribut] for tag in soup.find_all(balise) if tag.has_attr(attribut)]


#Etape 8: Fonction pour extraire le nom de domaine d'une URL
def extraire_nom_domaine(url):
    nom_domaine = re.findall(r'https?://([^/]+)/?', url)
    return nom_domaine[0] if nom_domaine else None

#Etape 9: Fonction pour classer les URLs en fonction du nom de domaine
def classer_urls_par_domaine(nom_domaine, urls):
    urls_du_domaine = []
    urls_hors_domaine = []
    for url in urls:
        if nom_domaine in url:
            urls_du_domaine.append(url)
        else:
            urls_hors_domaine.append(url)
    return urls_du_domaine, urls_hors_domaine

#Etape 10: Fonction pour ouvrir une URL et récupérer le HTML
def recuperer_html(url):
    reponse = requests.get(url)
    return reponse.text if reponse.status_code == 200 else None

# Etape n°11
def audit_page():
    # Étape 1 : Demander l'URL de la page à analyser
    print("\n==> Début de l'analyse...")
    url_page = input("Veuillez entrer l'URL de la page à analyser : ")

    # Étape 2 : Récupérer le texte HTML de la page
    texte_html_page = recuperer_html(url_page)

    if texte_html_page:
        # Étape 3 : Supprimer les balises HTML
        texte_sans_balises = retirer_balises_html(texte_html_page)

        # Étape 4 : Obtenir les occurrences de mots
        occurrences = compter_occurrences(texte_sans_balises)

        # Étape 5 : Lire les mots parasites depuis le fichier CSV
        mots_parasites = recuperer_mots_parasites("parasite.csv")

        # Étape 6 : Supprimer les mots parasites
        mots_filtres = retirer_mots_parasites(occurrences, mots_parasites)

        # Étape 7 : Récupérer les valeurs des attributs alt des balises img
        valeurs_alt_img = recuperer_attributs(texte_html_page, 'img', 'alt')

        # Étape 8 : Extraire le nom de domaine de l'URL
        nom_domaine = extraire_nom_domaine(url_page)

        # Étape 9 : Créer une liste d'URLs de test
        liste_urls_test = [
            "https://www.example.com/page1.html",
            "https://www.example.com/page2.html",
            "https://www.anotherdomain.com/page3.html",
            "https://www.example.com/page4.html",
        ]

        # Étape 10 : Filtrer les URLs par domaine
        urls_domaine, urls_hors_domaine = classer_urls_par_domaine(nom_domaine, liste_urls_test)

        # Affichage des résultats
        print("\n=== Résultats de l'audit ===\n")
        print("Mots clefs les plus importants :", list(mots_filtres.items())[:3])
        print("Nombre de liens entrants :", len(urls_domaine))
        print("Nombre de liens sortants :", len(urls_hors_domaine))
        print("Présence de balises alt pour les images :", valeurs_alt_img)
        print("\n====== Fin de l'audit ======\n")
    else:
        print("ERROR ! Impossible de récupérer le texte HTML de la page.")

# Appel de la fonction pour réaliser l'audit
audit_page()

# ========== Phase de test ==========

#Etape 4 
# Test d'utilisation pour les étapes 1 à 3
texte_test = """
Bien sûr, je serais ravi de vous aider à réaliser ce projet en Python.
Nous allons le diviser en étapes et commencer à implémenter chacune d'elles.
Assurons-nous de comprendre chaque étape avant de passer à la suivante.
Vous pourrez également tester chaque fonction individuellement.
"""

# Étape 1 : Compter les occurrences des mots
occurrences = compter_occurrences(texte_test)
print("\n=== Résultats de l'étape 1 ===")
print("Occurrences des mots triées par fréquence :", occurrences)

# Étape 2 : Lire les mots parasites depuis un fichier
fichier_mots_parasites = "mots_parasites.txt"
mots_parasites = recuperer_mots_parasites(fichier_mots_parasites)

# Étape 3 : Retirer les mots parasites
comptage_sans_parasites = retirer_mots_parasites(occurrences, mots_parasites)
print("\n=== Résultats de l'étape 2 et 3 ===")
print("Mots parasites lus depuis le fichier :", mots_parasites)
print("Occurrences des mots sans les parasites :", comptage_sans_parasites)

#Etape 7 
# Test d'utilisation pour les étapes 5 et 6
html_test = """
    <div>
        <p>Paragraphe 1</p>
        <p>Paragraphe 2</p>
        <a href="lien1.html">Lien 1</a>
        <a href="lien2.html">Lien 2</a>
        <img src="image1.jpg" alt="Description de l'image 1">
        <img src="image2.jpg" alt="Description de l'image 2">
    </div>
"""

# Étape 5 : Retirer les balises HTML
texte_sans_balises = retirer_balises_html(html_test)
print("\n=== Résultats de l'étape 5 ===")
print("Texte sans balises HTML :", texte_sans_balises)

# Étape 6 : Récupérer les valeurs de l'attribut href des balises a
valeurs_href_a = recuperer_attributs(html_test, 'a', 'href')
print("\n=== Résultats de l'étape 6 ===")
print("Valeurs des attributs href des balises a :", valeurs_href_a)