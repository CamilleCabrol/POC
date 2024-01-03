from spacy import displacy
import streamlit as st
from extraction_connaissances.extract_entities import extract_entities
from extraction_connaissances.summary_generator import generate_summary
from extraction_connaissances.wordcloud_generator import generate_wordcloud


# Affiche les résultats de l'analyse, y compris la visualisation de la structure du texte, le nuage de mots, et le résumé.
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


# Affiche les entités nommées extraites du document SpaCy.
# :param doc: Le document SpaCy analysé.
def display_entities(doc):
    st.subheader("Entités Nommées")
    entities = extract_entities(doc)
    for entity, label in entities:
        full_label = get_entity_label_name(label)
        st.write(f"{entity} - {full_label}")


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