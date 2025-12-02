import spacy

class Parser:
    ambiguous_terms = ["module", "unit", "component", "mechanism", "element", "entity", "system", "interface", "structure", "device",
                        "apparatus", "arrangement", "construct", "object", "handler", "tool", "processor", "engine", "manager", "container",
                        "resource", "signal", "framework", "platform", "layer", "operation", "configuration", "routine", "functionality", "gateway",
                        "node", "port", "channel", "service", "controller", "block", "section", "portion", "area", "region",
                        "adapter", "connector", "sub-system", "environment", "protocol", "workflow", "pathway", "space"] # low weight
    abstract_terms = ["means", "logic", "circuitry configured to", "engine configured to",
                      "program code", "instructions", "functionality", "process", "method step",
                      "computing environment", "executable", "abstraction", "virtual object",
                      "cloud resource", "metadata", "pointer", "reference", "operation code",
                      "rule", "policy", "transformation", "mapping", "allocation", "determination",
                      "estimation", "optimization", "evaluation", "generation", "synchronization",
                      "negotiation", "transition", "state change", "activation", "integration",
                      "aggregation", "prediction", "classification", "inference", "thread",
                      "session", "context", "token", "selector", "validator", "renderer",
                      "resolver", "coordinator", "dispatcher", "orchestrator", "intermediary"] # medium weight
    specific_terms = ["NVIDIA GPU", "Intel CPU", "AMD Ryzen processor", "Snapdragon chipset",
                      "ARM Cortex-A76", "USB-C port", "HDMI interface", "SATA connector",
                      "PCIe bus", "UEFI firmware", "BIOS chip", "NVMe SSD", "DDR5 memory",
                      "LPDDR4 RAM", "Samsung OLED display", "Retina display", "Li-Ion battery pack",
                      "Bluetooth 5.0 module", "Wi-Fi 6 antenna", "MIMO radio", "FPGA logic block",
                      "ASIC core", "Xilinx fabric", "Raspberry Pi board", "Arduino microcontroller",
                      "TPM 2.0 module", "AES-256 hardware engine", "TPM-backed key store",
                      "CUDA kernel", "Tensor core", "Vulkan renderer", "DirectX 12 API",
                      "Metal shader", "OpenGL driver", "Java Virtual Machine", "Python interpreter",
                      "Apache Kafka broker", "PostgreSQL server", "MySQL database",
                      "AWS Lambda function", "Azure VM instance", "Google TPU", "Docker container",
                      "Kubernetes node", "Linux kernel module", "Ubuntu operating system",
                      "Windows 11 API", "macOS kernel extension", "iOS framework",
                      "Android SDK component"] # high weight

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm") # loading the language model

        self.score = 0 # each instance of a class has a score initialized to 0
        self.total_tokens = 0 # this will be used to compare the score against the total possible score

        self.chunk = []
        self.noun_phrases = []
        self.tokens = []
    
    def get_chunk(self, file):
        with open(file, 'r') as file:
            lines = file.readlines()
            claim = "".join(lines)

            self.chunk = claim.split("\n")
    
    def get_noun_phrases(self):
        if self.chunk == []:
            print("You need to turn your txt file into chunks first")
            return 
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
        for i in range(len(self.tokens)):
            for token in self.tokens[i]:
                if token in Parser.ambiguous_terms:
                    self.total_tokens += 1 
                    self.score -= 1
                elif token in Parser.abstract_terms:
                    self.total_tokens += 1
                    self.score += 1
                elif token in Parser.specific_terms:
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