
# Import des modules
import json, csv
from random import randint

# Paramètre
path_file = "scores" # Chemin du fichier où les scores seront enregistrés

def save_data(data, file_format, path=path_file):
    """Sauvegarde des données dans un fichier JSON ou CSV."""
    path = f"{path}.{file_format}" # Chemin au complet
    try:
        if file_format == "json":
            with open(path, 'w') as file:
                json.dump(data, file, indent=5) # Enregistrement dans le JSON
        elif file_format == "csv":
            with open(path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Pseudo', 'Score']) # En-tête
                for pseudo, data in data.items():
                    for score in data['scores']:
                        writer.writerow([pseudo, score])
        print(f"Données sauvegardées avec succès dans {path}.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")


def load_data(file_format, path=path_file):
    """Charge des données depuis un fichier JSON ou CSV."""
    path = f"{path}.{file_format}" # Chemin au complet
    data = {}
    try:
        if file_format == "json":
            with open(path, 'r') as file:
                data = json.load(file) # Lecture JSON
        elif file_format == "csv":
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Ignore l'en-tête
                for row in reader:
                    pseudo, score = row
                    score = int(score)
                    if pseudo not in data: # Vérifier que le pseudo n'y est pas déjà
                        data[pseudo] = {'scores': [], 'max_score': 0}
                    data[pseudo]['scores'].append(score) # Ajout des scores dans la liste 'score'
                    data[pseudo]['max_score'] = max(data[pseudo]['max_score'], score) # Score max
        print(f"Données chargées avec succès depuis {path}.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return {}


def get_valid_input(prompt, valid_options):
    """Récupère une entrée valide de l'utilisateur."""
    while True:
        try:
            user_input = int(input(prompt))
            if user_input in valid_options:
                return user_input
            else:
                print(f"Veuillez entrer un nombre parmi {', '.join(map(str, valid_options))}.") # Print les options valides séparées par des virgules
        except ValueError:
            print("Veuillez entrer un nombre entier.")


def update_scores(scores, pseudo, score):
    """Met à jour les scores du joueur."""
    if pseudo not in scores:
        scores[pseudo] = {'scores': [], 'max_score': 0} # Si joueur inconnu, mettre score à 0
    scores[pseudo]['scores'].append(score) # Rajouter score à la liste
    scores[pseudo]['max_score'] = max(scores[pseudo]['max_score'], score) # Calculer le score max
    return scores


def rand_nb(difficulty):
    """Nombre aléatoire en fonction de la difficulté"""
    nb_range = {1: 100, 2: 1000, 3: 10000}
    return randint(1, nb_range[difficulty])


def choose_difficulty():
    """Permet au joueur de choisir une difficulté"""
    print("\n=== CHOISISSEZ UNE DIFFICULTÉ ===")
    print("1. Facile (1-100, 30 coups)")
    print("2. Moyen (1-1000, 20 coups)")
    print("3. Difficile (1-10000, 10 coups)")
    choice = get_valid_input("Votre choix : ", [1, 2, 3])
    attempts = {1: 30, 2: 20, 3: 10}
    range = {1: 100, 2: 1000, 3: 10000}
    return (choice, range[choice], attempts[choice])


def game():
    """Fonction principal du jeu"""
    difficulty, range, attemps_max = choose_difficulty() # Choix de difficulté
    guess_nb = rand_nb(difficulty) # Nombre à deviner
    print(guess_nb) # Debug
    nb, attemps, score = 0, 0, 0
    print(f"Vous avez choisit la difficulté {difficulty}.")
    print(f"Vous devez trouver le nombre choisi aléatoirement entre 1 et {range} et {attemps_max} coups maximals.")
    while nb != guess_nb:
        while True:
            try:
                nb = int(input(f"Entrez un nombre ({attemps_max - attemps} coups restants) : "))
            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier.")
                continue
            break
        if nb == guess_nb:
            # Nombre trouvé => gagné
            print("Félicitation, vous avez gagné !")
            score = (attemps_max - attemps) * difficulty**3
            print(f"Votre score est de {score} points.")
            return score

        elif attemps_max == attemps:
            # Plus d'attemps => Perdu (score de 0)
            print("Vous avez perdus par manque de coups.")
            return score

        elif nb > guess_nb:
            print("C'est moins !")
            attemps +=1
            continue

        elif nb < guess_nb:
            print("C'est plus !")
            attemps += 1
            continue


def main():
    """Fonction principale"""
    scores = load_data("json")

    print(r"""      ______                                                ________  __                        __    __                          __                           
     /      \                                              /        |/  |                      /  \  /  |                        /  |                          
    /$$$$$$  | __    __   ______    _______  _______       $$$$$$$$/ $$ |____    ______        $$  \ $$ | __    __  _____  ____  $$ |____    ______    ______  
    $$ | _$$/ /  |  /  | /      \  /       |/       |         $$ |   $$      \  /      \       $$$  \$$ |/  |  /  |/     \/    \ $$      \  /      \  /      \ 
    $$ |/    |$$ |  $$ |/$$$$$$  |/$$$$$$$//$$$$$$$/          $$ |   $$$$$$$  |/$$$$$$  |      $$$$  $$ |$$ |  $$ |$$$$$$ $$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |
    $$ |$$$$ |$$ |  $$ |$$    $$ |$$      \$$      \          $$ |   $$ |  $$ |$$    $$ |      $$ $$ $$ |$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$    $$ |$$ |  $$/ 
    $$ \__$$ |$$ \__$$ |$$$$$$$$/  $$$$$$  |$$$$$$  |         $$ |   $$ |  $$ |$$$$$$$$/       $$ |$$$$ |$$ \__$$ |$$ | $$ | $$ |$$ |__$$ |$$$$$$$$/ $$ |      
    $$    $$/ $$    $$/ $$       |/     $$//     $$/          $$ |   $$ |  $$ |$$       |      $$ | $$$ |$$    $$/ $$ | $$ | $$ |$$    $$/ $$       |$$ |      
     $$$$$$/   $$$$$$/   $$$$$$$/ $$$$$$$/ $$$$$$$/           $$/    $$/   $$/  $$$$$$$/       $$/   $$/  $$$$$$/  $$/  $$/  $$/ $$$$$$$/   $$$$$$$/ $$/       """)
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Jouer")
        print("2. Consulter les scores")
        print("0. Quitter")
        choice = get_valid_input("Votre choix : (1/2/0) ", [1, 2, 0])

        match choice:

            case 1:
                pseudo = input("Entrez votre pseudo : ")
                while True:
                    score = game()  # Le jeu se lance et on récupère le score
                    scores = update_scores(scores, pseudo, score)  # On l'enregistre

                    # Print les scores et "Perdu" si 0
                    print(f"Scores de {pseudo} : {', '.join(str(score) if score != 0 else 'perdu' for score in scores[pseudo]['scores'])}")
                    print(f"Meilleur score de {pseudo} : {scores[pseudo]['max_score']}")
                    save_data(scores, "json")
                    save_data(scores, "csv")

                    # Demande pour rejouer
                    c = get_valid_input("Voulez-vous rejouer, changer de joueur ou arréter ? (1/2/0) ", [1, 2, 0])
                    match c:
                        case 1:
                            # Relance le jeu
                            continue
                        case 2:
                            # Change de pseudo et relance le jeu
                            pseudo = input("Entrez votre pseudo : ")
                            continue
                        case 0:
                            # Quitter
                            break

            case 2:
                print("\n=== TABLEAU DES SCORES ===")
                for pseudo, data in scores.items():  # Afficher les scores de chaque joueur
                    print(f"\n{pseudo} : \nMeilleur score : {data['max_score']} \nTous les scores : {', '.join(str(score) if score != 0 else 'perdu' for score in data['scores'])}")

            case 0:
                print("Merci d'avoir joué. À bientôt !")
                break  # Quitter le programme


# Lancement de la fonction principale
if __name__ == '__main__':
    main()