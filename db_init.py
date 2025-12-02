
from pymongo import MongoClient


def initialiser_bd():

    client = MongoClient('mongodb://localhost:27017/')
    client.admin.command('ping')
    print("Connecte à MongoDB")
  
    bd = client['jeu_monstres']
    
    # si deja des collections les supprimer
    for collection in ['personnages', 'monstres', 'scores']:
        if collection in bd.list_collection_names():
            bd[collection].drop()
    
    # Personnages
    donnees_personnages = [
        {'nom': 'Guerrier', 'attaque': 15, 'defense': 10, 'pv': 100},
        {'nom': 'Mage', 'attaque': 20, 'defense': 5, 'pv': 80},
        {'nom': 'Archer', 'attaque': 18, 'defense': 7, 'pv': 90},
        {'nom': 'Voleur', 'attaque': 22, 'defense': 8, 'pv': 85},
        {'nom': 'Paladin', 'attaque': 14, 'defense': 12, 'pv': 110},
        {'nom': 'Sorcier', 'attaque': 25, 'defense': 3, 'pv': 70},
        {'nom': 'Chevalier', 'attaque': 17, 'defense': 15, 'pv': 120},
        {'nom': 'Moine', 'attaque': 19, 'defense': 9, 'pv': 95},
        {'nom': 'Berserker', 'attaque': 23, 'defense': 6, 'pv': 105},
        {'nom': 'Chasseur', 'attaque': 16, 'defense': 11, 'pv': 100},
    ]
    
    collection_personnages = bd['personnages']
    collection_personnages.insert_many(donnees_personnages)
    print(f" {len(donnees_personnages)} personnages insérés")
    
    # Monstres
    donnees_monstres = [
        {'nom': 'Gobelin', 'attaque': 10, 'defense': 5, 'pv': 50},
        {'nom': 'Orc', 'attaque': 20, 'defense': 8, 'pv': 120},
        {'nom': 'Dragon', 'attaque': 35, 'defense': 20, 'pv': 300},
        {'nom': 'Zombie', 'attaque': 12, 'defense': 6, 'pv': 70},
        {'nom': 'Troll', 'attaque': 25, 'defense': 15, 'pv': 200},
        {'nom': 'Spectre', 'attaque': 18, 'defense': 10, 'pv': 100},
        {'nom': 'Golem', 'attaque': 30, 'defense': 25, 'pv': 250},
        {'nom': 'Vampire', 'attaque': 22, 'defense': 12, 'pv': 150},
        {'nom': 'Loup-garou', 'attaque': 28, 'defense': 18, 'pv': 180},
        {'nom': 'Squelette', 'attaque': 15, 'defense': 7, 'pv': 90},
    ]
    
    collection_monstres = bd['monstres']
    collection_monstres.insert_many(donnees_monstres)
    print(f"✓ {len(donnees_monstres)} monstres ont ete initialisé ")
    
    bd['scores']
    print("scores créé")
    
    client.close()
    print("\n bd initialisée ")
    return True





