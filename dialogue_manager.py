import os
from sklearn.metrics.pairwise import pairwise_distances_argmin

from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from utils import *    

class DialogueManager(object):
    def __init__(self, location_table=None, value_table=None):
        print("Loading resources...")

        # Intent recognition:
        self.intent_recognizer = unpickle_file('intent_rf.pkl') #unpickle_file(paths['INTENT_RECOGNIZER'])
        self.tfidf_vectorizer = unpickle_file('tfidf_trans.pkl') #unpickle_file(paths['TFIDF_VECTORIZER'])
        
        # template answers
        self.ANSWER_TEMPLATE_size_yes = "Wa you buying %s ah. That one upsize better!"
        self.ANSWER_TEMPLATE_size_no = "Wa you buying %s ah. That one better dont upsize!"
        self.ANSWER_TEMPLATE_nav = "Ok the nearest %s is at %s. Only %s minutes away if you take PMD!"

        # BBT Variables
        self.current_location = None
        self.bubble_tea_shop = None
        
        # Data Tables
        self.bbt_location_table = pd.read_csv('bbt_locations.csv',  engine='python')
        self.bbt_value_table = None
         
        # Bubble Tea store names:
        # Get bubble tea store names
        bbt_store_list_file = open('bbt_store_list.txt','r')
        bbt_store_list = []
        for l in bbt_store_list_file.readlines():
            bbt_store_list.append(l.strip())
            
        bbt_store_list = [x.split('.') for x in bbt_store_list][:-2]
        bbt_store_dict = {}
        for el in bbt_store_list:
            bbt_store_dict[el[0]] = el

        all_store_names = []
        for el in bbt_store_list:
            all_store_names += el
            
        self.bbt_store_dict = bbt_store_dict
        self.all_store_names = all_store_names
        
        # Create chitchat bot
        self.generic_chatbot = ChatBot('Generic Responder loler')
        self.generic_chatbot.set_trainer(ChatterBotCorpusTrainer)
        self.generic_chatbot.train("chatterbot.corpus.english")
        
    
    def generate_answer(self, question):

        # Recognize intent of the question using `intent_recognizer`.

        features = self.tfidf_vectorizer.transform([question])
        
        # Check if postal:
        postal = get_location(question)
        
        if postal == None:
            intent = self.intent_recognizer.predict(features)
        else:
            intent = 1  # navigation
      
    
        # Chit-chat part:   
        if intent == 0:  # diaglouge
            # Pass question to chitchat_bot to generate a response.       
            response = self.generic_chatbot.get_response(question)
            return response
        
        # Goal-oriented part:
        elif intent == 2:  # size     
            # Pass features to tag_classifier to get predictions.
            self.bubble_tea_shop = store_recognizer(question, self.all_store_names, self.bbt_store_dict)
            
            if self.bubble_tea_shop != None:
                # Check if worth it to upsize
                #upsize = # query table
                upsize = False
                if upsize == True:
                    return self.ANSWER_TEMPLATE_size_yes % (self.bubble_tea_shop)
                else:
                    return self.ANSWER_TEMPLATE_size_no % (self.bubble_tea_shop)
            
            else:  # if None
                return "Can ask again with the store name anot? Unless your bubble tea not famous."

        else:  # intent is navi
            
            # Fill in bubble tea slot
            if self.bubble_tea_shop is None:  # First time
                self.bubble_tea_shop = store_recognizer(question, self.all_store_names, self.bbt_store_dict)
            
            re_request_loc = False
            store_name = store_recognizer(question, self.all_store_names, self.bbt_store_dict)
            if (store_name != None) and (store_name != self.bubble_tea_shop): 
                self.bubble_tea_shop = store_name
                re_request_loc = True
            
            # Fill in current_location
            test_loc = get_location(question)
            if (self.current_location == None):
                self.current_location = get_location(question)
            
            elif (self.current_location != test_loc) and (test_loc != None):
                self.current_location = test_loc
            
            else:
                self.current_location = self.current_location
            
            if (self.current_location == None) or (re_request_loc==True):
                return "Wait i need your current location. Just give me your postal code will do!"
            
            else:  # Have postal code info
                
                nearest_time, best_add = calc_fastest_time(self.current_location, self.bubble_tea_shop, self.bbt_location_table)

                # Once return this info make sure to reset state variables
                
                return self.ANSWER_TEMPLATE_nav % (self.bubble_tea_shop, best_add, str(nearest_time)[:2])
            
            
            