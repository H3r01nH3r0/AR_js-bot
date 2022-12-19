from json import load
from db import Database
from maket import Maket_to_HTML

db = Database('database/main.db')

def get_config(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        data: dict = load(file)
        return data

def generation(user_id):
    if db.get_user_ctg(user_id) == 'text':
        maket = Maket_to_HTML('makets/text_maket.html')
        text = db.get_user_text(user_id)
        maket.text(text, user_id)
        link = f'privat-links/{user_id}.html'
        return link
    elif db.get_user_ctg(user_id) == 'picture':
        maket = Maket_to_HTML('makets/picture_maket.html')
        picture = db.get_user_pict(user_id)
        maket.picture(picture, user_id)
        link = f'privat-links/{user_id}.html'
        return link
    elif db.get_user_ctg(user_id) in db.get_ctg():
        category = db.get_user_ctg(user_id)
        poss = db.get_user_poss(user_id)
        maket = Maket_to_HTML('makets/object_maket.html')
        user_obj = db.get_object(category, poss)
        maket.object(user_obj, user_id)
        link = f'privat-links/{user_id}.html'
        return link
