from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import streamlit as st


# Chargement le modèle SpaCy
nlp = spacy.load("fr_core_news_md")

# Liste par défaut des mots vides de spaCy
default_stopwords = set(nlp.Defaults.stop_words)

# Liste personnelle des mots vides
custom_stopwords = {'neuf', 'qu', 'quelqu'} 
combined_stopwords = default_stopwords.union(custom_stopwords)

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