import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st


# Chargement le modèle SpaCy
nlp = spacy.load("fr_core_news_md")

# Liste par défaut des mots vides de spaCy
default_stopwords = set(nlp.Defaults.stop_words)

# Liste personnelle des mots vides
custom_stopwords = {'neuf', 'qu', 'quelqu'} 
combined_stopwords = default_stopwords.union(custom_stopwords)

# Génère un nuage de mots à partir du document SpaCy et l'affiche.
# :param doc: Le document SpaCy analysé.
# :param width: La largeur du nuage de mots.
# :param height: La hauteur du nuage de mots.
# :param bg_color: La couleur de fond du nuage de mots.
def generate_wordcloud(doc, width, height, bg_color):
    # Extraction du texte du document SpaCy
    text = " ".join([token.text for token in doc])

    # Génération du nuage de mots
    wordcloud = WordCloud(width=width, height=height, background_color=bg_color, stopwords=combined_stopwords).generate(text)

    # Affichage du nuage de mots
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)