import parso
from pymongo import MongoClient
from db_init import initialiser_bd
from random import choice, randint, sample
from util import get_choice



def afficher_personnages_disponibles(bd):
    print("Personnages disponibles:")
    personnages = bd['personnages'].find({}, {'nom': 1, '_id': 1})
    for personnage in personnages:
        print(f"  - {personnage['nom']}")


def obtenir_noms_personnages(bd):
    return [personnage['nom'] for personnage in bd['personnages'].find({}, {'nom': 1, '_id': 1})]


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
        personnage = saisir_personnage(f"numéro {i}", bd)
        if personnage:
            equipe.append(personnage)
    
    noms_equipe = [personnage['nom'] for personnage in equipe]
    print(f"Vous avez choisi: {', '.join(noms_equipe)}")
    return equipe


# scores
def afficher_scores(bd):
    scores = list(bd['scores'].find().sort('score', -1).limit(10))
    if scores:
        print("\n--- Meilleurs Scores ---")
        print(scores[bd])
    else:
        print("Aucun score enregistré")


def calculer_degats(attaque, defense):
    degats = attaque - defense
    return max(1, degats)

def monstre_isalive(monstre):
    if monstre['pv'] > 0:
        return True
    return False
def personnage_isalive(personnage):
    if personnage['pv'] > 0:
        return True
    return False

def boucle_combat(equipe, monstre):
    print("le combat a commencé" )
    while any(personnage_isalive(personnage) for personnage in equipe) and monstre_isalive(monstre):
        print ("ca tourne")



def obtenir_monstre_aleatoire(bd, nombre=1):
    monstres = list(bd['monstres'].find())
    return sample(monstres, min(nombre, len(monstres)))


def afficher_equipes(equipe, monstres):
    print("\n--- Équipes du Combat ---")
    noms_equipe = [personnage['nom'] for personnage in equipe]
    print(f"Votre équipe: {', '.join(noms_equipe)}")
    print(f"Monstre adverse: {', '.join([monstre['nom'] for monstre in monstres])}\n")


def demarrer_combat(equipe, bd):
    print("=== Le Combat Commence ===")
    monstre_aleatoire = obtenir_monstre_aleatoire(bd, 1)[0]
    afficher_equipes(equipe, [monstre_aleatoire])
    boucle_combat(equipe, monstre_aleatoire)


def demarrer_nouvelle_partie(equipe, bd):
    print("\n=== Nouvelle Partie Démarrée ===")
    demarrer_combat(equipe, bd)


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
            equipe = choisir_equipe(bd)
            demarrer_nouvelle_partie(equipe, bd)

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