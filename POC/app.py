"""
Application Streamlit pour mon POC dont le sujet est l'extraction de connaissances à partir de textes.
Projet dans le cadre de mon master MIAGE.

SGC - Camille CABROL
"""

##Rajouter sur mon ordi
# pip install langdetect
# pip install flair

import streamlit as st
import spacy
from spacy import displacy
from langdetect import detect

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from extraction_connaissances.analyze_text import analyze_text

from extraction_connaissances.detect_language import detect_language
from extraction_connaissances.extract_entities import extract_entities


# Chargement le modèle SpaCy
nlp = spacy.load("fr_core_news_md")


# # clé API OpenAI
# openai.api_key = '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'


# Fonction principale de l'application. Elle gère l'interface utilisateur et l'analyse du texte.
def main():

    st.title("Extraction de Connaissances à partir de Textes")

    # Option pour choisir entre l'entrée de texte manuelle ou l'upload de fichier
    input_option = st.radio("Choisissez une option d'entrée :", ["Texte manuel", "Uploader un fichier"])

    if input_option == "Texte manuel":
        text = st.text_area("Entrez votre texte ici:", "")
    else:
        uploaded_file = st.file_uploader("Uploader un fichier texte", type=["txt"])
        if uploaded_file is not None:
            text = uploaded_file.read().decode("utf-8")
        else:
            text = ""

    # Utilisation de st.expander pour créer un menu dépliant
    with st.expander("Options de personnalisation"):
        # Ajout des options pour le nuage de mots
        wordcloud_width = st.slider("Largeur du nuage de mots :", min_value=400, max_value=1200, value=800)
        wordcloud_height = st.slider("Hauteur du nuage de mots :", min_value=200, max_value=800, value=400)
        wordcloud_bg_color = st.color_picker("Couleur de fond du nuage de mots :", "#ffffff")

    # Ajout d'un conteneur pour afficher la langue détectée
    lang_result_container = st.empty()

    if st.button("Analyser"):
        if not text:
            st.warning("Veuillez entrer du texte ou uploader un fichier avant d'analyser.")
        else:
            # Permet la détection de la langue
            with st.spinner("Analyse en cours..."):
                detected_language = detect_language(text)

            # Affiche la langue détectée dans le conteneur, mais seulement si la langue est détectée
            if detected_language:
                # Affiche la langue détectée dans le conteneur
                lang_result_container.text(detected_language)

            with st.spinner("Analyse du texte en cours..."):
                analyze_text(text, wordcloud_width, wordcloud_height, wordcloud_bg_color)
    

if __name__ == "__main__":
    main()
