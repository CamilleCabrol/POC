import streamlit as st
import spacy
from spacy import displacy

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Charger le modèle SpaCy
nlp = spacy.load("fr_core_news_sm")

# # Configurez votre clé API OpenAI
# openai.api_key = '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'

def main():
    st.title("Extraction de Connaissances à partir de Textes")
    text = st.text_area("Entrez votre texte ici:", "")
    if st.button("Analyser"):
        analyze_text(text)

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

def analyze_text(text):
    doc = nlp(text)
    display_results(doc)

def extract_entities(doc):
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def display_entities(doc):
    st.subheader("Entités Nommées")
    entities = extract_entities(doc)
    for entity, label in entities:
        full_label = get_entity_label_name(label)
        st.write(f"{entity} - {full_label}")

def display_results(doc):
    st.subheader("Visualisation de la structure du texte")
    displacy.render(doc, style="ent")

    st.subheader("Nuage de mots")
    generate_wordcloud(doc)

    st.subheader("Résumé")
    generate_summary(doc)

    # Ajoutez l'affichage des entités nommées
    display_entities(doc)


def generate_wordcloud(doc):

     # Extraire le texte du document SpaCy
    text = " ".join([token.text for token in doc])

    # Générer le nuage de mots
    wordcloud = WordCloud(width=800, height=400, background_color="white", stopwords=nlp.Defaults.stop_words).generate(text)

    # Afficher le nuage de mots
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# def generate_summary(doc):
#     # Extraire les phrases clés
#     key_phrases = [chunk.text for chunk in doc.noun_chunks]

#     # Afficher le résumé
#     st.write(" ".join(key_phrases))

def generate_summary(doc):
    # Extraire les phrases
    sentences = [sent.text for sent in doc.sents]

    # Utiliser TF-IDF pour attribuer des scores aux phrases
    tfidf_vectorizer = TfidfVectorizer(stop_words=list(nlp.Defaults.stop_words))
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

# #     # Calculer la similarité cosinus entre les phrases
    sentence_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Sélectionner les phrases importantes en fonction des scores
    important_sentences = [sentences[i] for i in sentence_similarity.sum(axis=1).argsort()[:-5:-1]]

# #     # Afficher le résumé
    st.write(" ".join(important_sentences))

# def generate_summary(doc):
#     # Utilisez GPT-3 pour générer un résumé abstrait
#     abstract_summary = generate_abstractive_summary(doc.text)
    
#     # Afficher le résumé abstrait
#     st.write(abstract_summary)

# def generate_abstractive_summary(text):
#     # Utilisez l'API OpenAI pour générer un résumé abstrait
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=text,
#         max_tokens=150  # Ajustez la longueur du résumé selon vos besoins
#     )

#     abstract_summary = response['choices'][0]['text']
#     return abstract_summary

if __name__ == "__main__":
    main()
