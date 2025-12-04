import parso
from pymongo import MongoClient
from db_init import initialiser_bd
from random import choice, sample
from util import get_choice
from models import Personnage, Monstre



def afficher_personnages_disponibles(bd):
    print("Personnages disponibles:")
    personnages = bd['personnages'].find({}, {'nom': 1, '_id': 0})
    for personnage in personnages:
        print(f"  - {personnage['nom']}")


def obtenir_noms_personnages(bd):
    return [personnage['nom'] for personnage in bd['personnages'].find({}, {'nom': 1, '_id': 0})]


def obtenir_donnees_personnage(bd, nom):
    noms = obtenir_noms_personnages(bd)
    for nom_db in noms:
        if nom_db.lower() == nom.lower():
            return bd['personnages'].find_one({'nom': nom_db})


def saisir_personnage(numero, bd):
    noms = obtenir_noms_personnages(bd)
    noms_minuscules = [nom.lower() for nom in noms]
    nom_choisi = get_choice(f"Entrez le nom du personnage {numero}: ", noms_minuscules)
    return obtenir_donnees_personnage(bd, nom_choisi)


def choisir_equipe(bd):
    print("Choisissez votre équipe de personnages:")
    afficher_personnages_disponibles(bd)
    
    equipe = []
    for i in range(1, 4):
        donnees = saisir_personnage(f"numéro {i}", bd)
        if donnees:
            equipe.append(Personnage(donnees))
    
    noms_equipe = [personnage.nom for personnage in equipe]
    print(f"Vous avez choisi: {', '.join(noms_equipe)}")
    return equipe


def enregistrer_score(bd, nom_joueur, score):
    bd['scores'].insert_one({
        'nom_joueur': nom_joueur,
        'score': score
    })
    print(f"Score enregistré pour {nom_joueur}: {score} vague(s)")


def calculer_degats(attaque, defense):
    degats = attaque - defense
    if degats < 0:
        degats = 0
    return degats


def afficher_scores(bd):
    scores = list(bd['scores'].find().sort('score', -1).limit(3))
    if scores:
        print("\n--- Meilleurs Scores ---")
        for i, score in enumerate(scores, 1):
            print(f"{i}. {score['nom_joueur']}: {score['score']} vague(s)")
    else:
        print("Aucun score enregistré")

def afficher_etat_combat(equipe, monstre):
    print(f"\nÉtat des personnages:")
    for personnage in equipe:
        print(f"  {personnage.nom} - PV: {personnage.pv}")
    
    print(f"\nMonstre: {monstre.nom} - PV: {monstre.pv}")


def attaque_personnages(equipe, monstre):

    print(f"\nLes personnages attaquent!")
    for personnage in equipe:
        if personnage.est_vivant():
            degats = calculer_degats(personnage.attaque, monstre.defense)
            monstre.prendre_degats(degats)
            print(f"  {personnage.nom} inflige {degats} dégâts!")


def attaque_monstre(monstre, equipe):
    print(f"\n{monstre.nom} attaque!")
    personnage_cible = choice([personnage for personnage in equipe if personnage.est_vivant()])
    degats = calculer_degats(monstre.attaque, personnage_cible.defense)
    personnage_cible.prendre_degats(degats)
    print(f"  {monstre.nom} attaque {personnage_cible.nom} et inflige {degats} dégâts!")


def boucle_combat(equipe, monstre, bd, nom_joueur):
    vague = 1
    
    while True:
        print(f"\n{'='*50}")
        print(f"VAGUE {vague}")
        print(f"{'='*50}")
        
        afficher_etat_combat(equipe, monstre)
                
        attaque_personnages(equipe, monstre)
        
        if not monstre.est_vivant():
            print(f"\nVague {vague} gagnée! Tu as vaincu {monstre.nom}!")
            vague += 1
            monstre = obtenir_monstre_aleatoire(bd)
            continue
        
        attaque_monstre(monstre, equipe)
        
        if not any(personnage.est_vivant() for personnage in equipe):
            print(f"\n Vous avez perdu a la vague {vague} contre {monstre.nom}.")
            return vague



def obtenir_monstre_aleatoire(bd):
    monstres = list(bd['monstres'].find())
    monstre_aleatoire = sample(monstres, 1)[0]
    return Monstre(monstre_aleatoire)


def afficher_equipes(equipe, monstres):
    print("\n--- Équipes du Combat ---")
    noms_equipe = [personnage.nom for personnage in equipe]
    print(f"Votre équipe: {', '.join(noms_equipe)}")
    print(f"Monstre adverse: {', '.join([monstre.nom for monstre in monstres])}\n")


def demarrer_combat(equipe, bd, nom_joueur):
    print("=== Le Combat Commence ===")
    monstre_aleatoire = obtenir_monstre_aleatoire(bd)
    afficher_equipes(equipe, [monstre_aleatoire])
    
    score = boucle_combat(equipe, monstre_aleatoire, bd, nom_joueur)
    
    enregistrer_score(bd, nom_joueur, score)


# menu principal
def afficher_menu():
    print("\n=== Menu Principal ===")
    print("1. Démarrer une nouvelle partie")
    print("2. Afficher les scores")
    print("3. Quitter")
    return get_choice("Sélectionnez une option (1-3): ", ['1', '2', '3'])


def boucle_jeu(bd):
    while True:
        choix = afficher_menu()
        
        if choix == '1':
            nom_joueur = ""
            while not nom_joueur:
                nom_joueur = input("\nEntrez votre nom : ").strip()
                if not nom_joueur:
                    print("Veuillez entrer un pseudo valide")
            equipe = choisir_equipe(bd)
            demarrer_combat(equipe, bd, nom_joueur)

        elif choix == '2':
            afficher_scores(bd)
        elif choix == '3':
            print("vous quittez le jeu")
            break
        else:
            print("Option non reconnue.")


if __name__ == '__main__':
    initialiser_bd()
    client = MongoClient('mongodb://localhost:27017/')
    bd = client['jeu_monstres']
    boucle_jeu(bd)
    client.close()