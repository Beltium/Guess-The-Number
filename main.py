
from random import randint
import json

# Paramètre
path_file = "scores.json"

def save_dict_to_json(data, path = path_file):
    """Sauvegarde un dictionnaire dans un fichier JSON"""
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=5)
        print(f"Données sauvegardées avec succès dans {path}.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def load_dict_from_json(path = path_file):
    """Charge un dictionnaire depuis un fichier JSON"""
    try:
        with open(path, 'r') as file:
            data = json.load(file)
        print(f"Données chargées avec succès depuis {path}.")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return {}

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
    while True:
        try:
            choice = int(input("Votre choix : "))
            if choice not in [1, 2, 3]:
                print("Veuillez rentrez un nombre entre 1 et 3")
        except ValueError:
            print("Veuillez rentrer un nombre.")
            continue
        break
    attempts = {1: 30, 2: 20, 3: 10}
    range = {1: 100, 2: 1000, 3: 10000}
    return (choice, range[choice], attempts[choice])

def game():
    difficulty, range, attemps_max = choose_difficulty()
    gnb = rand_nb(difficulty)
    print(gnb)
    nb, attemps, score = 0, 0, 0
    print(f"Vous avez choisit la difficulté {difficulty}.")
    print(f"Vous devez trouver le nombre choisi aléatoirement entre 1 et {range} et {attemps_max} coups maximals.")
    while nb != gnb:
        while True:
            try:
                nb = int(input(f"Entrez un nombre ({attemps_max - attemps} coups restants) : "))
            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier.")
                continue
            break
        if nb == gnb:
            print("Félicitation, vous avez gagné !")
            score = (attemps_max - attemps) * difficulty**3
            print(f"Votre score est de {score} points.")
            return score
            break
        elif attemps_max == attemps:
            print("Vous avez perdus par manque de coups.")
            return score
            break
        elif nb > gnb:
            print("C'est moins !")
            attemps +=1
            continue
        elif nb < gnb:
            print("C'est plus !")
            attemps += 1
            continue

# Fonction principale
def main():
    scores = load_dict_from_json()
    print("Bienvenue sur Guess The Number !")
    pseudo = str(input("Entrez votre pseudo : "))
    score = game()
    # Vérification si le pseudo existe déjà dans le dictionnaire des scores
    if pseudo not in scores:
        scores[pseudo] = {'scores': [], 'max_score': 0}
    else:
        print(f"Scores de {pseudo} : {scores[pseudo]['scores']}")
        print(f"Meilleur score de {pseudo} : {scores[pseudo]['max_score']}")

    scores[pseudo]['scores'].append(score)
    scores[pseudo]['max_score'] = max(scores[pseudo]['max_score'], score)

    print(scores)
    save_dict_to_json(scores)


if __name__ == '__main__':
    main()