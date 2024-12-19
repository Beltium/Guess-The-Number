
from random import randint

def rand_nb(difficulty):
    range = {1: 100, 2: 1000, 3: 10000}
    return randint(1, range[difficulty])

def choose_difficulty():
    """Permet au joueur de choisir une difficulté"""
    print("\n=== CHOISISSEZ UNE DIFFICULTÉ ===")
    print("1. Facile (1-100, 30 coups)")
    print("2. Moyen (1-1000, 20 coups)")
    print("3. Difficile (1-10000, 10 coups)")
    try :
        choice = int(input("Votre choix : "))
    except ValueError:
        print("Veuillez rentrer un nombre.")
    if choice not in [1, 2, 3]:
        print("Veuillez rentrez un nombre entre 1 et 3")
    attempts = {1: 30, 2: 20, 3: 10}
    return choice, attempts[choice]

def game():
    return 0

# Fonction principale
def main():
    print("Hello World!")


if __name__ == '__main__':
    print(choose_difficulty())