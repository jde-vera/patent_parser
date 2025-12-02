import spacy

class Parser:
    ambiguous_terms = [] # low weight
    abstract_terms = [] # medium weight
    specific_terms = [] # high weight

    def __init__(self):
        nlp = spacy.load("en_core_web_sm") # loading the language model

        self.score = 0 # each instance of a class has a score initialized to 0
    
    def get_chunk(file):
        return
    
    def get_noun_phrases(chunk):
        return
    
    def get_token(phrase):
        return
    
    def evalutate_claim():
        return
