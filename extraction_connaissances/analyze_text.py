import spacy
import streamlit as st

from extraction_connaissances.display_results import display_results

# Chargement le modèle SpaCy
nlp = spacy.load("fr_core_news_md")

# Analyse le texte fourni et affiche les résultats.
# :param text: Le texte à analyser.
# :param wordcloud_width: La largeur du nuage de mots.
# :param wordcloud_height: La hauteur du nuage de mots.
# :param wordcloud_bg_color: La couleur de fond du nuage de mots.
def analyze_text(text, wordcloud_width, wordcloud_height, wordcloud_bg_color):
    try:
        doc = nlp(text)
        with st.spinner("Affichage des résultats..."):
            display_results(doc, wordcloud_width, wordcloud_height, wordcloud_bg_color)
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de l'analyse du texte : {str(e)}")
