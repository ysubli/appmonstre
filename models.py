class Personnage:
    def __init__(self, donnees):
        self.nom = donnees['nom']
        self.attaque = donnees['attaque']
        self.defense = donnees['defense']
        self.pv = donnees['pv']
    
    def est_vivant(self):
        return self.pv > 0
    
    def prendre_degats(self, degats):
        self.pv -= degats
        if self.pv < 0:
            self.pv = 0
    
    def afficher_info(self):
        print(f"  {self.nom} - PV: {self.pv}")


class Monstre:
    def __init__(self, donnees):
        self.nom = donnees['nom']
        self.attaque = donnees['attaque']
        self.defense = donnees['defense']
        self.pv = donnees['pv']
    
    def est_vivant(self):
        return self.pv > 0
    
    def prendre_degats(self, degats):
        self.pv -= degats
        if self.pv < 0:
            self.pv = 0
    
    def afficher_info(self):
        print(f"  {self.nom} - PV: {self.pv}")
