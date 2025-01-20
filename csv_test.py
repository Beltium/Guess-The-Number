import csv

def save_scores_to_csv(scores, path='scores.csv'):
    try:
        with open(path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Pseudo', 'Score', 'Statut'])
            for pseudo, data in scores.items():
                for i, score in enumerate(data['scores']):
                    statut = 'Gagné' if score > 0 else 'Perdu'
                    writer.writerow([pseudo, score, statut])
        print(f"Données sauvegardées avec succès dans {path}.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde en CSV : {e}")


scores = {'Beltium': {'scores': [270, 29, 30], 'max_score': 270}, 'Notch': {'scores': [30, 29, 0, 270], 'max_score': 270}}
save_scores_to_csv(scores)

def load_scores_from_csv(path='scores.csv'):
    """
    Charge les scores depuis un fichier CSV et reconstruit le dictionnaire d'origine.

    Args:
        path (str): Chemin du fichier CSV à lire (par défaut 'scores.csv').

    Returns:
        dict: Dictionnaire contenant les scores et le score maximum pour chaque joueur.
    """
    scores = {}
    try:
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Ignore l'en-tête

            for row in reader:
                pseudo, score, statut = row
                score = int(score)  # Convertir le score en entier

                # Ajouter le pseudo dans le dictionnaire si nécessaire
                if pseudo not in scores:
                    scores[pseudo] = {'scores': [], 'max_score': 0}

                # Ajouter le score au joueur
                scores[pseudo]['scores'].append(score)

                # Mettre à jour le score maximum
                scores[pseudo]['max_score'] = max(scores[pseudo]['max_score'], score)

        print(f"Données chargées avec succès depuis {path}.")
    except Exception as e:
        print(f"Erreur lors du chargement en CSV : {e}")

    return scores

print(load_scores_from_csv())