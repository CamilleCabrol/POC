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


# Chargement le modèle SpaCy
nlp = spacy.load("fr_core_news_md")


# # clé API OpenAI
# openai.api_key = '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'


# Fonction principale de l'application. Elle gère l'interface utilisateur et l'analyse du texte.
def main():

    st.title("Extraction de Connaissances à partir de Textes")
    text = st.text_area("Entrez votre texte ici:", "")

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
            st.warning("Veuillez entrer du texte avant d'analyser.")
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
    
# Liste par défaut des mots vides de spaCy
default_stopwords = set(nlp.Defaults.stop_words)

# Liste personnelle des mots vides
custom_stopwords = {'neuf', 'qu', 'quelqu'} 
combined_stopwords = default_stopwords.union(custom_stopwords)

# Détecte la langue du texte donné en utilisant une bibliothèque de détection de la langue.

# :param text: Le texte pour lequel la langue doit être détectée.
def detect_language(text):
    try:
        language = detect(text)
        st.write(f"Langue détectée : {language}")
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la détection de la langue : {str(e)}")


# Convertit le label brut d'une entité nommée en un libellé plus convivial.

# :param label: Le label brut de l'entité nommée
# :return: Le libellé correspondant au label ou le label brut s'il n'est pas trouvé.
def get_entity_label_name(label):
    label_names = {
        'PER': 'Personne',
        'ORG': 'Organisation',
        'LOC': 'Lieu géographique',
        'MISC': 'Autre',
        'MONEY': 'Unité monétaire',
        'QUANTITY': 'Quantité',
        'DATE': 'Date',
        'TIME': 'Heure',
        'PERCENT': 'Pourcentage'
    }

    return label_names.get(label, label)


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


# Extrait les entités nommées d'un document SpaCy.

# :param doc: Le document SpaCy analysé.
# :return: Une liste de tuples contenant le texte de l'entité et son label.
def extract_entities(doc):
    entities = {(ent.text, ent.label_) for ent in doc.ents}
    return entities


# Affiche les entités nommées extraites du document SpaCy.

# :param doc: Le document SpaCy analysé.
def display_entities(doc):
    st.subheader("Entités Nommées")
    entities = extract_entities(doc)
    for entity, label in entities:
        full_label = get_entity_label_name(label)
        st.write(f"{entity} - {full_label}")


# Affiche les résultats de l'analyse, y compris la visualisation de la structure du texte,
# le nuage de mots, et le résumé.

# :param doc: Le document SpaCy analysé.
# :param wordcloud_width: La largeur du nuage de mots.
# :param wordcloud_height: La hauteur du nuage de mots.
# :param wordcloud_bg_color: La couleur de fond du nuage de mots.
def display_results(doc, wordcloud_width, wordcloud_height, wordcloud_bg_color):
    st.subheader("Visualisation de la structure du texte")
    displacy.render(doc, style="ent")

    st.subheader("Nuage de mots")
    generate_wordcloud(doc, width=wordcloud_width, height=wordcloud_height, bg_color=wordcloud_bg_color)

    st.subheader("Résumé")
    generate_summary(doc)

    # Ajoutez l'affichage des entités nommées
    display_entities(doc)


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


# Génère un résumé à partir du document SpaCy et l'affiche.

# :param doc: Le document SpaCy analysé.
def generate_summary(doc):
    # Extraction des phrases
    sentences = [sent.text for sent in doc.sents]

    # Utilisation de TF-IDF pour attribuer des scores aux phrases
    tfidf_vectorizer = TfidfVectorizer(stop_words=list(combined_stopwords))
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    # Calcul de la similarité cosinus entre les phrases
    sentence_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Sélection des phrases importantes en fonction des scores
    important_sentences = [sentences[i] for i in sentence_similarity.sum(axis=1).argsort()[:-5:-1]]

    # Affichage du résumé
    st.write(" ".join(important_sentences))

if __name__ == "__main__":
    main()
