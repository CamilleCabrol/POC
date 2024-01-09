# Extrait les entités nommées d'un document SpaCy.
# :param doc: Le document SpaCy analysé.
# :return: Une liste de tuples contenant le texte de l'entité et son label.
def extract_entities(doc):
    entities = {(ent.text, ent.label_) for ent in doc.ents}
    return entities