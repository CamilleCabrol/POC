from langdetect import detect
import streamlit as st


# Détecte la langue du texte donné en utilisant une bibliothèque de détection de la langue.
# :param text: Le texte pour lequel la langue doit être détectée.
def detect_language(text):
    try:
        language = detect(text)
        st.write(f"Langue détectée : {language}")
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la détection de la langue : {str(e)}")
