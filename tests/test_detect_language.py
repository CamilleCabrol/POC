import unittest
from extraction_connaissances.detect_language import detect_language

class TestDetectLanguage(unittest.TestCase):
    def test_detect_language(self):
        text = "Ceci est un texte en français et il faut que mon texte passe s'il vous plaît."
        result = detect_language(text)
        self.assertEqual(result, "fr")

if __name__ == '__main__':
    unittest.main()