import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix , classification_report , accuracy_score , ConfusionMatrixDisplay
from itemCart.models import orderedItems , order1
from .models import food , Review
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter , defaultdict
import json
from django.db.models.query import QuerySet

def dict_to_vector(ingre_dict , all_ingre):
    return np.array([ingre_dict.get(ing , 0) for ing in all_ingre])

def get_all_ingre():
    all_ingre = set()
    for item in food.objects.all():
        if isinstance(item.ingredients , str):
            item.ingredients = json.loads(item.ingredients)        
        all_ingre.update(item.ingredients.keys())
    return list(all_ingre)

def get_similarity_score(item1 , item2 , all_ingre):

    score = 0 
    if item1.course == item2.course:
        score += 1
    
    if item1.type == item2.type:
        score += 1
    
    vect1 = dict_to_vector(item1.ingredients , all_ingre)
    vect2 = dict_to_vector(item2.ingredients , all_ingre)

    ingre_similar = cosine_similarity([vect1] , [vect2])[0][0]
    score += ingre_similar * 3
    return score

def recommended_freq():
    top_n = 5

    order_Item = orderedItems.objects.all()
    f_counter = Counter()

    for item in order_Item:
        f_counter[item.item] += item.quantity
    
    freq_items = []

    for item in f_counter.most_common(top_n):
        freq_items.append(item)
    freq_items = [food.name for food , _ in freq_items]
    return freq_items

def recommend_content_based(req):
    if(orderedItems.objects.filter(order__user = req.user).exists()):
        top_n = 5
        ordered_item = orderedItems.objects.filter(order__user = req.user).values_list('item',flat=True).distinct()
        user_items = food.objects.filter(id__in = ordered_item)
        
        all_items = food.objects.exclude(id__in = ordered_item)
        scores = defaultdict(float)

        all_ingre = get_all_ingre()

        for user_item in user_items:
            for other_item in all_items:
                scores[other_item] += get_similarity_score(user_item , other_item , all_ingre)

        sorted_items = sorted(scores.items() , key=lambda x : x[1] , reverse=True)
        count = 0
        arr = []
        for item in sorted_items[:top_n]:
            count += 1
            arr.append(item[0])

        if count == 0:
            return recommended_freq()
        else:
            return arr

    else:
        return recommended_freq()


def seggestions(req):

    l = []

    if req.user.is_authenticated:
        name_list = recommend_content_based(req)
    else:
        name_list = recommended_freq()
        
    for i in name_list:
        food_item = food.objects.get(name = i)
        l.append(food_item)

    return l