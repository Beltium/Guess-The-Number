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