
"""
Programme de Guess The Number (Juste Prix) avec gestion des scores.

Ce programme permet à un ou plusieurs joueurs de jouer au GTN :
- Le joueur choisit une difficulté et tente de deviner un nombre aléatoire.
- Les scores sont sauvegardés et chargés depuis des fichiers JSON et CSV (au choix).
- Les joueurs peuvent consulter leurs meilleurs scores et tous leurs scores enregistrés.

Fonctionnalités :
- Choix de la difficulté avec différents niveaux (facile, moyen, difficile).
- Calcul et sauvegarde des scores dans des fichiers JSON et CSV.
- Consultation des scores enregistrés par pseudo.
- Gestion du menu principal pour jouer ou consulter les scores.

Paramètres :
- `path_file` : Chemin les fichiers où les scores seront enregistréss (par défaut : "scores").
- `default_file_format` : Format pour l'enregistrement ("json" ou "csv")

Modules utilisés :
- json
- csv
- random : pour générer des nombres aléatoires.
"""

# Import des modules
import json, csv
from random import randint

# Paramètres
path_file = "scores"  # Chemin les fichiers où les scores seront enregistrés
load_file_format = "json"  # Format pour l'enregistrement ("json" ou "csv")

def save_data(data, file_format, path=path_file):
    """
    Sauvegarde les données dans un fichier JSON ou CSV.

    Args:
        data (dict): Les données à sauvegarder.
        file_format (str): Le format du fichier ('json' ou 'csv').
        path (str): Le chemin du fichier sans extension (par défaut `path_file`).

    Raises:
        Exception: En cas d'erreur lors de la sauvegarde des données.
    """
    path = f"{path}.{file_format}"  # Chemin complet du fichier
    try:
        if file_format == "json":
            with open(path, 'w') as file:
                json.dump(data, file, indent=5)  # Enregistrement des données dans le fichier JSON
        elif file_format == "csv":
            with open(path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Pseudo', 'Score'])  # En-tête du fichier CSV
                for pseudo, data in data.items():
                    for score in data['scores']:  # Parcours des scores par pseudo
                        writer.writerow([pseudo, score])
        print(f"Données sauvegardées avec succès dans {path}.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")


def load_data(file_format, path=path_file):
    """
    Charge les données depuis un fichier JSON ou CSV.

    Args:
        file_format (str): Le format du fichier à charger ('json' ou 'csv').
        path (str): Le chemin du fichier sans extension (par défaut `path_file`).

    Returns:
        dict: Les données chargées.

    Raises:
        Exception: En cas d'erreur lors du chargement des données.
    """
    path = f"{path}.{file_format}"  # Chemin complet du fichier
    data = {}
    try:
        if file_format == "json":
            with open(path, 'r') as file:
                data = json.load(file)  # Lecture des données depuis le fichier JSON
        elif file_format == "csv":
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Ignore l'en-tête
                for row in reader:
                    pseudo, score = row
                    score = int(score)
                    if pseudo not in data:  # Création d'une entrée pour chaque pseudo non existant
                        data[pseudo] = {'scores': [], 'max_score': 0}
                    data[pseudo]['scores'].append(score)  # Ajout du score dans la liste des scores
                    data[pseudo]['max_score'] = max(data[pseudo]['max_score'], score)  # Mise à jour du score max
        print(f"Données chargées avec succès depuis {path}.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return {}


def get_valid_input(prompt, valid_options):
    """
    Demande une entrée utilisateur valide parmi les options données.
    Cette fonction réessaie tant qu'une entrée valide n'est pas fournie.

    Args:
        prompt (str): Le message affiché à l'utilisateur.
        valid_options (list): Les options valides (nombres entiers).

    Returns:
        int: L'option choisie par l'utilisateur.
    """
    while True:
        try:
            user_input = int(input(prompt))  # Convertir l'entrée utilisateur en entier
            if user_input in valid_options:
                return user_input  # Retourner l'entrée si elle est valide
            else:
                print(f"Veuillez entrer un nombre parmi {', '.join(map(str, valid_options))}.")  # Afficher les options valides
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def update_scores(scores, pseudo, score):
    """
    Met à jour les scores d'un joueur dans le dictionnaire.

    Args:
        scores (dict): Le dictionnaire des scores existants.
        pseudo (str): Le pseudo du joueur.
        score (int): Le score à ajouter.

    Returns:
        dict: Le dictionnaire des scores mis à jour.
    """
    if pseudo not in scores:
        scores[pseudo] = {'scores': [], 'max_score': 0}  # Initialiser l'entrée pour un nouveau joueur
    scores[pseudo]['scores'].append(score)  # Ajouter le score dans la liste des scores
    scores[pseudo]['max_score'] = max(scores[pseudo]['max_score'], score)  # Mettre à jour le score max si nécessaire
    return scores


def rand_nb(difficulty):
    """
    Génère un nombre aléatoire en fonction de la difficulté.

    Args:
        difficulty (int): Le niveau de difficulté (1, 2 ou 3).

    Returns:
        int: Un nombre aléatoire entre 1 et la plage définie par la difficulté.
    """
    nb_range = {1: 100, 2: 1000, 3: 10000}  # Plages de nombres par difficulté
    return randint(1, nb_range[difficulty])  # Générer un nombre aléatoire dans la plage correspondante


def choose_difficulty():
    """
    Permet au joueur de choisir une difficulté.

    Returns:
        tuple: La difficulté choisie (int), la plage de nombres (int), et le nombre maximal d'essais (int).
    """
    print("\n=== CHOISISSEZ UNE DIFFICULTÉ ===")
    print("1. Facile (1-100, 30 coups)")
    print("2. Moyen (1-1000, 20 coups)")
    print("3. Difficile (1-10000, 10 coups)")
    choice = get_valid_input("Votre choix : ", [1, 2, 3])
    attempts = {1: 30, 2: 20, 3: 10}  # Nombre d'essais selon la difficulté
    range = {1: 100, 2: 1000, 3: 10000}  # Plage de nombres selon la difficulté
    return (choice, range[choice], attempts[choice])


def game():
    """
    Lance une partie.

    Returns:
        int: Le score obtenu par le joueur.
    """
    difficulty, range, attemps_max = choose_difficulty()  # Choix de difficulté
    guess_nb = rand_nb(difficulty)  # Nombre à deviner généré aléatoirement
    print(guess_nb)  # Debug (affiche le nombre à deviner)
    nb, attemps, score = 0, 0, 0  # Initialisation des variables de jeu
    print(f"Vous avez choisi la difficulté {difficulty}.")
    print(f"Vous devez trouver le nombre choisi aléatoirement entre 1 et {range} avec {attemps_max} coups maximaux.")
    while nb != guess_nb:
        while True:
            try:
                nb = int(input(f"Entrez un nombre ({attemps_max - attemps} coups restants) : "))  # Entrée utilisateur
            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier.")
                continue
            break
        if nb == guess_nb:
            # Nombre trouvé => gagné
            print("Félicitation, vous avez gagné !")
            score = (attemps_max - attemps) * difficulty**3  # Calcul du score basé sur les essais restants et la difficulté
            print(f"Votre score est de {score} points.")
            return score

        elif attemps_max == attemps:
            # Plus d'essais => perdu (score de 0)
            print("Vous avez perdu par manque de coups.")
            return score

        elif nb > guess_nb:
            print("C'est moins !")  # Le nombre entré est trop grand
            attemps += 1
            continue

        elif nb < guess_nb:
            print("C'est plus !")  # Le nombre entré est trop petit
            attemps += 1
            continue


def main():
    """
    Fonction principale qui gère le menu du jeu et les interactions utilisateur.
    """
    scores = load_data(load_file_format)  # Chargement des scores depuis le fichier défini

    print(r"""      ______                                                ________  __                        __    __                          __
     /      \                                              /        |/  |                      /  \  /  |                        /  |                          
    /$$$$$$  | __    __   ______    _______  _______       $$$$$$$$/ $$ |____    ______        $$  \ $$ | __    __  _____  ____  $$ |____    ______    ______  
    $$ | _$$/ /  |  /  | /      \  /       |/       |         $$ |   $$      \  /      \       $$$  \$$ |/  |  /  |/     \/    \ $$      \  /      \  /      \ 
    $$ |/    |$$ |  $$ |/$$$$$$  |/$$$$$$$//$$$$$$$/          $$ |   $$$$$$$  |/$$$$$$  |      $$$$  $$ |$$ |  $$ |$$$$$$ $$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |
    $$ |$$$$ |$$ |  $$ |$$    $$ |$$      \$$      \          $$ |   $$ |  $$ |$$    $$ |      $$ $$ $$ |$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$    $$ |$$ |  $$/ 
    $$ \__$$ |$$ \__$$ |$$$$$$$$/  $$$$$$  |$$$$$$  |         $$ |   $$ |  $$ |$$$$$$$$/       $$ |$$$$ |$$ \__$$ |$$ | $$ | $$ |$$ |__$$ |$$$$$$$$/ $$ |      
    $$    $$/ $$    $$/ $$       |/     $$//     $$/          $$ |   $$ |  $$ |$$       |      $$ | $$$ |$$    $$/ $$ | $$ | $$ |$$    $$/ $$       |$$ |      
     $$$$$$/   $$$$$$/   $$$$$$$/ $$$$$$$/ $$$$$$$/           $$/    $$/   $$/  $$$$$$$/       $$/   $$/  $$$$$$/  $$/  $$/  $$/ $$$$$$$/   $$$$$$$/ $$/       """)
    # Logo du jeu

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Jouer")
        print("2. Consulter les scores")
        print("0. Quitter")
        choice = get_valid_input("Votre choix : (1/2/0) ", [1, 2, 0])  # Validation du choix utilisateur

        match choice:
            case 1:
                pseudo = input("Entrez votre pseudo : ")  # Demande du pseudo
                while True:
                    score = game()  # Lancement du jeu, récupération du score
                    scores = update_scores(scores, pseudo, score)  # Mise à jour des scores du joueur

                    # Affichage des scores actuels du joueur
                    print(f"Scores de {pseudo} : {', '.join(str(score) if score != 0 else 'perdu' for score in scores[pseudo]['scores'])}")
                    print(f"Meilleur score de {pseudo} : {scores[pseudo]['max_score']}")

                    save_data(scores, "json")  # Sauvegarde des scores en JSON
                    save_data(scores, "csv")  # Sauvegarde des scores en CSV

                    # Proposer de rejouer ou de changer de pseudo
                    c = get_valid_input("Voulez-vous rejouer, changer de joueur ou arrêter ? (1/2/0) ", [1, 2, 0])
                    match c:
                        case 1:
                            # Rejouer avec le même pseudo
                            continue
                        case 2:
                            # Changer de pseudo pour un autre joueur
                            pseudo = input("Entrez votre pseudo : ")
                            continue
                        case 0:
                            # Retourner au menu principal
                            break

            case 2:
                print("\n=== TABLEAU DES SCORES ===")
                for pseudo, data in scores.items():  # Parcourir et afficher les scores de chaque joueur
                    print(f"\n{pseudo} : \nMeilleur score : {data['max_score']} \nTous les scores : {', '.join(str(score) if score != 0 else 'perdu' for score in data['scores'])}")

            case 0:
                print("Merci d'avoir joué. À bientôt !")  # Message de fin
                break  # Quitter le programme


# Lancement de la fonction principale
if __name__ == '__main__':
    main()