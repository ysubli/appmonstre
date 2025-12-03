def get_choice(prompt, choix_valides):
    while True:
        choix = input(prompt).strip().lower()
        if choix in choix_valides:
            return choix
        else:
            print(f"Choix non valide. Veuillez choisir parmi: {', '.join(choix_valides)}")