import spacy


class SpacyDoc():

    nlp = spacy.load('es_core_news_sm')

    def __init__(self, document):
        self.doc = self.nlp(document)
        self._normalize_doc = None

    @property
    def normalize_doc(self):
        """Normalizar texto removiendo signos de puntución y lematizando las palabras"""
        min_len = 3
        words = [t.lemma_.lower()
                 for t in self.doc if not t.is_stop and t.is_alpha]
        lexical_tokens = ' '.join([t for t in words if len(t) > min_len])
        return lexical_tokens

    @property
    def pos(self):
        """Return json array tag pos"""
        def map_POS(token):
            return {
                token.text: {
                    "lemma": token.lemma_,
                    "pos": token.pos_,
                    "tag": token.tag_,
                    "dep_": token.dep_,
                    "shape_": token.shape_,
                    "is_alpha": token.is_alpha,
                    "is_stop": token.is_stop,
                    "sentiment": token.sentiment
                }
            }

        return [map_POS(token) for token in self.doc]

    @property
    def entities(self):
        """Return json array tag pos"""
        def map_entity(token):
            return {
                token.text: {
                    "start_char": token.start_char,
                    "end_char": token.end_char,
                    "label": token.label_
                }
            }

        return [map_entity(token) for token in self.doc.ents]
