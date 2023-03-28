from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel
from langchain.llms import OpenAI
from langchain import PromptTemplate 
import numpy as np
import re

class CustomFashionClassifier:
    def __init__(self,dataset):
        self.dataset = dataset
        self.model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
        self.processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")
    
    def classify(self,image):
        # image = Image.open(img_path)
        # image.resize((224, 224))
        inputs = self.processor(text=self.dataset,
                   images=image, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
        probs = logits_per_image.softmax(dim=1)  
        # print(probs)
        return self.dataset[np.argmax(probs.detach().numpy())]
    

class CustomFashionRecommender:
    def __init__(self,openai_key):
        self.openai_key = openai_key
        try:
            self.model = OpenAI(openai_api_key=self.openai_key,model="text-davinci-003")
        except:
            raise Exception("Incorrect APIKey")
        self.template = "You are a fashion expert that takes input in the format (clothing_or_occasion_type, gender_ that represents either a type of clothing or an occasion, along with the gender. Based on the input, offer six outfit ideas that cater to diverse styles, trends, and looks, focusing solely on clothing items (not any types of shoes or accessories) If the input represents a type of clothing, suggest different variations of the item to explore. For instance, if the input is 'red dress', suggest different types of red dresses such as wrap dresses, maxi dresses, and shift dresses, along with outfit ideas for each. If the input represents an event or occasion, share outfit ideas suitable for that event, incorporating multiple clothing items. For instance, if the input is 'summer picnic', suggest outfit ideas that include dresses, rompers, shorts, and tops that would be suitable for a casual summer picnic. Use vivid and concise descriptions (1-3 words) that can be easily converted into search queries for our fashion product database. The search terms should not include the gender, only the relevant clothing terms. Ensure that each recommendation has at least 2-3 search terms. Provide six separate dictionaries, each representing a unique recommendation. For the 'copy' field, include 2-3 sentences describing the clothing-only recommendation. Always provide the output in JSON format] for example tell me what is the output of  ({clothing_or_occasion_type},{gender}), give 6 ideas of what this can be styled with"

    def recommend(self,cloth_type,gender):
        out = self.template.format(clothing_or_occasion_type=cloth_type,gender="Male")
        return self.model(out) 