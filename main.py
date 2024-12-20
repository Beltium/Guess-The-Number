
from random import randint, choice


def rand_nb(difficulty):
    range = {1: 100, 2: 1000, 3: 10000}
    return randint(1, range[difficulty])

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
    difficulty, range, attemps = choose_difficulty()
    gnb = rand_nb(difficulty)
    nb = 0
    print(f"Vous avez choisit la difficulté {difficulty}.")
    print(f"Vous devez trouver le nombre choisi aléatoirement entre 1 et {range} et {attemps} coups maximals.")
    while nb != gnb:
        nb = int(input("Entrez un nombre : "))
        if nb == gnb:
            print("Félicitation, vous avez gagné !")
            break
        elif nb > gnb:
            print("C'est moins !")
            continue
        elif nb < gnb:
            print("C'est plus !")
            continue

# Fonction principale
def main():
    print("Hello World!")


if __name__ == '__main__':
    game()