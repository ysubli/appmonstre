from pymongo import MongoClient
from db_init import initialiser_bd

# menu 
def afficher_menu(bd):
    """Affiche le menu principal"""
    while True:
        print("=== Menu Principal ===")
        print("1. Démarrer une nouvelle partie")
        print("2. Afficher les scores")
        print("3. Quitter")
        choix = input("Sélectionnez une option (1-3): ")
        if choix == '1':
            demarrer_nouvelle_partie(bd)
        elif choix == '2':
            print("Scores à implémenter")
        elif choix == '3':
            break
        else:
            print("Option non reconnue.")


def afficher_personnages_disponibles(bd):
    """Affiche que les noms des personnages"""
    print("Personnages disponibles:")
    personnages = bd['personnages'].find({}, {'nom': 1, '_id': 1})
    for personnage in personnages:
        print(f"  - {personnage['nom']}")


def choisir_equipe(bd):
    print("Choisissez votre équipe de personnages:")
    equipe=[]
    afficher_personnages_disponibles(bd)
    choix1=input("Entrez le nom du premier personnage: ")
    if choix1 not in [p['nom'] for p in bd['personnages'].find({}, {'nom': 1, '_id': 1})]:
        print("Personnage non reconnu. Veuillez réessayer.")
    else:    
        equipe.append(choix1)
    choix2=input("Entrez le nom du deuxième personnage: ")
    if choix2 not in [p['nom'] for p in bd['personnages'].find({}, {'nom': 1, '_id': 1})]:
        print("Personnage non reconnu. Veuillez réessayer.")
    else:
        equipe.append(choix2)
    choix3=input("Entrez le nom du troisième personnage: ")
    if choix3 not in [p['nom'] for p in bd['personnages'].find({}, {'nom': 1, '_id': 1})]:
        print("Personnage non reconnu. Veuillez réessayer.")
    else:
        equipe.append(choix3)
    print(f"Vous avez choisi: {choix1}, {choix2} et {choix3}")
  

 

def demarrer_nouvelle_partie(bd):
    print("Nouvelle partie démarrée")
    choisir_equipe(bd)


if __name__ == '__main__':
    initialiser_bd()
    client = MongoClient('mongodb://localhost:27017/')
    bd = client['jeu_monstres']
    afficher_menu(bd)
    client.close()