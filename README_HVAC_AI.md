# HVAC AI Advisor — Portfolio Edition

**Conçu et développé par Noël Moukoko**

Application Streamlit de démonstration pour explorer les consommations énergétiques, comparer des scénarios de rénovation, étudier des solutions CVC, estimer des émissions à partir de facteurs renseignés et générer un rapport PDF.

## Lancer l'application en local

1. Installe Python 3.11 ou 3.12.
2. Ouvre un terminal dans ce dossier.
3. Installe les dépendances :
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Lance l'application :
   ```bash
   python -m streamlit run app.py
   ```
5. Ouvre l'adresse locale affichée dans le terminal, généralement `http://localhost:8501`.

## Héberger gratuitement avec Streamlit Community Cloud

1. Crée un compte GitHub et un dépôt pour le projet.
2. Ajoute `app.py` et `requirements.txt` au dépôt.
3. Ouvre https://share.streamlit.io/ et connecte ton compte GitHub.
4. Sélectionne le dépôt, la branche et le fichier principal `app.py`.
5. Clique sur **Deploy**. Streamlit installe les dépendances indiquées dans `requirements.txt` et fournit une URL publique.

Tu peux aussi utiliser GitHub Desktop pour envoyer les fichiers au dépôt sans utiliser les commandes Git.

## Important avant publication

- Cette application est un démonstrateur, pas un logiciel d'audit certifié.
- Les gains et investissements de rénovation sont des hypothèses illustratives.
- Les facteurs carbone doivent être vérifiés, documentés et adaptés au périmètre.
- Le parc multi-bâtiments est actuellement conservé dans la session de l'application : exporte le CSV pour garder une copie. Une base de données serait nécessaire pour une conservation durable.
- Ne publie pas de factures réelles ou de données sensibles d'un bâtiment dans une démonstration publique.

## Fichiers

- `app.py` : application principale (renommer `HVAC_AI_Advisor_V10.py` en `app.py`)
- `requirements.txt` : dépendances nécessaires
- `README.md` : instructions de lancement et d'hébergement
