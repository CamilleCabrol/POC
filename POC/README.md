# Guide d'Utilisation - Extraction de Connaissances à partir de Textes

## Introduction
Bienvenue dans l'application d'extraction de connaissances à partir de textes ! Cette application a été développée dans le cadre d'un projet de master 2 MIAGE pour la matière Systèmes de Gestion des Connaissances.

## Prérequis
Assurez-vous d'avoir les éléments suivants installés sur votre machine avant de commencer :
- [Python](https://www.python.org/) (version recommandée : 3.6 ou supérieure)
- [pip](https://pip.pypa.io/) (gestionnaire de paquets Python)

## Installation du projet et des dépendances
Ouvrez un terminal et clonez le projet depuis GitHub :
```bash
git clone git@github.com:CamilleCabrol/POC.git
cd POC
```

 Exécutez les commandes suivantes pour installer les dépendances nécessaires :

```bash
pip install streamlit
pip install spacy
pip install langdetect
pip install flair
pip install wordcloud
pip install matplotlib
pip install scikit-learn
```

## Téléchargement du modèle SpaCy

Après l'installation de SpaCy, téléchargez le modèle de langue français avec la commande :
```bash
python -m spacy download fr_core_news_md
```

## Exécution de l'application

Lancez l'application en utilisant la commande suivante :

```bash
streamlit run app.py
```

L'application sera accessible dans votre navigateur à l'adresse http://localhost:8501/. Vous pouvez choisir d'entrer du texte manuellement ou d'uploader un fichier texte pour l'analyse.

## Options de personnalisation

L'application propose des options de personnalisation telles que la largeur, la hauteur et la couleur de fond du nuage de mots.

## Note
Pour plus d'informations ou en cas de problèmes, n'hésitez pas à contacter l'auteur de l'application : Camille CABROL.