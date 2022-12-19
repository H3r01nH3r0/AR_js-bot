from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from db import Database
db = Database('database/main.db')

class Keyboards:
    def __init__(self, texts: dict) -> None:
        self._texts = texts

    def main(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=self._texts["3d_object"], callback_data='3d_object'))
        markup.add(InlineKeyboardButton(text=self._texts["picture"], callback_data='picture'))
        markup.add(InlineKeyboardButton(text=self._texts["text"], callback_data='text'))
        return markup

    def choose_partition(self, categories) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for i in categories:
            ctg = db.get_link(i[0])
            markup.add(InlineKeyboardButton(text=str(i[0]), callback_data='ctg_' + ctg))
        return markup

    def choose_obj(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=self._texts["monitor"], callback_data='monitor'))
        markup.add(InlineKeyboardButton(text=self._texts["table"], callback_data='table'))
        return markup

    def ready(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=self._texts["ready"], callback_data='ready'))
        return markup

    def again(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=self._texts["again"], callback_data='again'))
        return markup

    def yes(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Да!', callback_data='yes'))
        markup.add(InlineKeyboardButton(text='Нет!', callback_data='no'))
        return markup
