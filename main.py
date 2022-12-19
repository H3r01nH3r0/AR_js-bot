import urllib
from aiogram import Bot, Dispatcher, types, executor
import utils
from utils import get_config
from keyboards import Keyboards
from db import Database
from urllib import request

config = get_config('config.json')
keyboards = Keyboards(texts=config["texts"])
bot = Bot(token=config["TOKEN"], parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
db = Database('database/main.db')
domein_name = 'arbot.su'

def check_leng(text, alphabet=set('qwertyuiopasdfghjklzxcvbnm')):
    return not alphabet.isdisjoint(text.lower())

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message) -> None:
    if db.check_user(message.from_user.id):
        await bot.send_message(message.from_user.id,
                               text=config["texts"]["choose"],
                               reply_markup=keyboards.main())
    else:
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id,
                               text=config["texts"]["choose"],
                               reply_markup=keyboards.main())

@dp.callback_query_handler(state="*")
async def callback_query_handler(callback_query: types.CallbackQuery) -> None:
    if callback_query.data == '3d_object':
        categories = db.get_category()
        if categories:
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id,
                                   text=config["texts"]["whatpict"],
                                   reply_markup=keyboards.choose_partition(categories))
        else:
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
            await bot.send_message(callback_query.from_user.id,
                                   text=config["texts"]["noctg"],
                                   reply_markup=keyboards.main())
    elif callback_query.data == 'picture':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id,
                               text=config["texts"]["sendpict"])
    elif callback_query.data == 'text':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id,
                               text=config["texts"]["sendtext"])
    elif callback_query.data == 'yes':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_photo(callback_query.from_user.id,
                             open('files/pattern-marker.png', 'rb'),
                             caption=config["texts"]["marker"])
        await bot.send_message(callback_query.from_user.id,
                               text=config["texts"]["marker2"].format(link=f'https://{domein_name}/files/pattern-marker.png'),
                               reply_markup=keyboards.ready())
    elif callback_query.data == 'no':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id,
                               text=config["texts"]["choose"],
                               reply_markup=keyboards.main())
    elif callback_query.data == 'monitor':
        db.add_pos(callback_query.from_user.id, 'vert')
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_photo(callback_query.from_user.id,
                             open('files/pattern-marker.png', 'rb'),
                             caption=config["texts"]["marker"])
        await bot.send_message(callback_query.from_user.id,
                               text=config["texts"]["marker2"].format(link=f'https://{domein_name}/files/pattern-marker.png'),
                               reply_markup=keyboards.ready())
    elif callback_query.data == 'table':
        db.add_pos(callback_query.from_user.id, 'horis')
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_photo(callback_query.from_user.id,
                             open('files/pattern-marker.png', 'rb'),
                             caption=config["texts"]["marker"])
        await bot.send_message(callback_query.from_user.id,
                               text=config["texts"]["marker2"].format(link=f'https://{domein_name}/files/pattern-marker.png'),
                               reply_markup=keyboards.ready())
    elif callback_query.data == 'ready':
        link = utils.generation(callback_query.from_user.id)
        #бот отправляет команду на заполнение html документа и генирацию ссылки, после чего отправляет ссылку пользователю
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id,
                               text=config["texts"]["browser"].format(link=f'https://{domein_name}/{link}'),
                               reply_markup=keyboards.again())
    elif callback_query.data == 'again':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id,
                               text=config["texts"]["choose"],
                               reply_markup=keyboards.main()
                               )
    elif callback_query.data.startswith('ctg'):
        category = callback_query.data.split('_')[1]
        db.add_ctg(callback_query.from_user.id, category)
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id,
                               text=config["texts"]["object"],
                               reply_markup=keyboards.choose_obj())

@dp.message_handler(content_types = ['text'])
async def bot_message(message: types.Message):
    new_text = message.text
    if check_leng(new_text):
        db.add_ctg(message.from_user.id, 'text')
        if db.check_user_text(message.from_user.id):
            db.change_user_text(message.from_user.id, new_text)
        else:
            db.add_user_text(message.from_user.id, new_text)
        await bot.send_message(message.from_user.id,
                               text=f'Вы хотите использовать этот текст:\n\n<b>{new_text}</b>',
                               reply_markup=keyboards.yes(), parse_mode='HTML')
    else:
        await bot.send_message(message.from_user.id,
                               text=f'К сожалению, пока что я поддерживаю только кирилицу\n\n'
                                    f'Попробуй отправить текст еще раз')

@dp.message_handler(content_types = ['document'])
async def handle_docs_photo(message: types.Message):
    db.add_ctg(message.from_user.id, 'picture')
    doc_id = message.document.file_id
    file_info = await bot.get_file(doc_id)
    fi = file_info.file_path
    name = message.document.file_name
    file_format = name.split('.')[1]
    file_name = str(message.from_user.id) + '.' + str(file_format)
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{config["TOKEN"]}/{fi}', f'files/{file_name}')
    if db.check_user_pict(message.from_user.id):
        db.change_user_pict(message.from_user.id, f'files/{file_name}')
    else:
        db.add_user_pict(message.from_user.id, f'files/{file_name}')
    await bot.send_message(message.from_user.id, 'Файл успешно сохранён')
    await bot.send_photo(message.from_user.id,
                         open('files/pattern-marker.png', 'rb'),
                         caption=config["texts"]["marker"])
    await bot.send_message(message.from_user.id,
                           text=config["texts"]["marker2"].format(link=f'https://{domein_name}/files/pattern-marker.png'),
                           reply_markup=keyboards.ready())

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=False)