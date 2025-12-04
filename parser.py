import spacy

class Parser:
    ambiguous_terms = ["portion", "region", "section", "element", "part", "mechanism", "unit", "module",
                   "assembly", "arrangement", "structure", "interface", "system", "apparatus", "means",
                   "configuration", "component", "entity", "path", "environment", "block", "area",
                   "layer", "subsystem"]  # low weight
    abstract_terms = ["configured to", "adapted to", "arranged to", "operable to", "coupled", "communicate",
                  "transmit", "receive", "process", "control", "determine", "estimate", "optimize", "map",
                  "transition", "activate", "state change", "oriented", "mating direction", "provide power",
                  "provide charging", "substantially parallel", "substantially perpendicular", "interact",
                  "manage", "monitor", "evaluate", "facilitate", "enable"]  # medium weight
    neutral_terms = ["device", "connector", "housing", "circuitry", "controller", "contacts", "antenna",
                 "mobile device", "contactless device", "microusb connector", "apple lightning connector"] # no weight
    specific_terms = ["lightning contacts", "smartcard circuitry", "smartcard controller", "pcb", 
                  "integrated circuit", "antenna coil", "chip", "ic", "circuit board", "transceiver",
                  "sensor", "pin", "terminal", "electrical contact", "signal line", "microcontroller",
                  "processor", "memory chip", "ram", "flash memory", "voltage regulator", "transistor",
                  "capacitor", "resistor", "inductor", "usb-c connector", "hdmi connector", "rf module",
                  "nfc antenna", "bluetooth module", "power bus", "ground line", "data line",
                  "charging circuit", "power supply", "voltage rail", "current sensor"] # high weight

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm") # loading the language model

        self.score = 0 # each instance of a class has a score initialized to 0
        self.total_tokens = 0 # this will be used to compare the score against the total possible score

        self.chunk = []
        self.noun_phrases = []
        self.tokens = []
    
    def get_chunk(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            claim = "".join(lines)

            self.chunk = claim.split("\n")
    
    def get_noun_phrases(self):
        if self.chunk == []:
            print("You need to turn your txt file into chunks first")
        else:
            # you want to create a list of lists where each list contains noun phrases that you can then tokenize
            for i in range(len(self.chunk)): # iterate through each chunk
                temp_chunk_list = []
                temp_string_chunk = "".join(self.chunk[i])
                doc = self.nlp(temp_string_chunk)
                for phrase in doc.noun_chunks: 
                    temp_chunk_list.append(phrase.text) # append the noun chunks to the temp storage and then append to self.noun_phrases
                self.noun_phrases.append(temp_chunk_list)
    
    def get_token(self):
        if self.noun_phrases == []:
            print("You need to turn your chunks into noun phrases first")
        else:
            for i in range(len(self.noun_phrases)):
                temp_token_list = []
                temp_string_token = "".join(self.noun_phrases[i])
                doc = self.nlp(temp_string_token)
                for token in doc:
                    temp_token_list.append(token.text)
                self.tokens.append(temp_token_list)    
    
    def evalutate_claim(self):
        # normalize term lists
        ambiguous = [term.lower() for term in Parser.ambiguous_terms]
        abstract = [term.lower() for term in Parser.abstract_terms]
        neutral = [term.lower() for term in Parser.neutral_terms]
        specific = [term.lower() for term in Parser.specific_terms]

        # this for loop is to check phrases such as surface mount component
        for i in range(len(self.noun_phrases)):
            for phrases in self.noun_phrases[i]:
                # normalize phrases
                cleaned_phrases = phrases.lower()

                if cleaned_phrases in ambiguous:
                    self.total_tokens += 1 
                    self.score -= 1
                elif cleaned_phrases in abstract:
                    self.total_tokens += 1
                    self.score += 1
                elif cleaned_phrases in neutral:
                    self.total_tokens += 1
                elif cleaned_phrases in specific:
                    self.total_tokens += 1
                    self.score += 2

        # this for loop is to check individual tokens such as negotiation or logic
        for i in range(len(self.tokens)):
            for token in self.tokens[i]:
                # normalize tokens
                cleaned_token = token.lower()

                if cleaned_token in ambiguous:
                    self.total_tokens += 1 
                    self.score -= 1
                elif cleaned_token in abstract:
                    self.total_tokens += 1
                    self.score += 1
                elif cleaned_token in neutral:
                    self.total_tokens += 1
                elif cleaned_token in specific:
                    self.total_tokens += 1
                    self.score += 2
                

        max = self.total_tokens * 2
        min = self.total_tokens * -1
        strength = (self.score - min)/ (max - min)

        if strength < 0.33:
            explanation = "This claim contains too many ambiguous terms and lacks precise, technical terms. \nThe interpretation may be too broad."
        elif strength < 0.66:
            explanation = "This claim contains a mix of abstract and specific terms. \nThe interpretation is neither too broad or specific."
        else:
            explanation = "This claim contains a lot of technicalically specific terms. \nThis interpretation is very clear and may be too specific, as a result it could be limiting."

        print("----- CLAIM EVALUATION SUMMARY -----")
        print(f"Total matched tokens : {self.total_tokens}")
        print(f"Raw score            : {self.score} (range: {min} to {max})")
        print(f"Strength (0-1)       : {strength:.2f}")
        print("-----------------------------------")
        print(explanation)
        print("-----------------------------------")