import uuid
import random
import logging
import typing

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from aiogram import Bot, Dispatcher, executor, md, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified, Throttled

from config import bot_token, access_tokens
#from utils import States
from messages import MESSAGES

from bot_functions import *
from db.bd_managment import *
from modules_installer import *

from cookies import *

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    mode = HelperMode.snake_case
    AUTH_0 = State()
    AUTH = State()
    packagename_input = State()
    apkname_input = State()
    file_with_cookies_input = State()

class StatesAddRK(StatesGroup):
    pack_state = State()
    file_with_cookies_input = State()
    password_fb = State()
    apk_id = State()
    rk_ids = State()
    finishing = State()

class addUsers(StatesGroup):
    package_input = State()
    userids_input = State()


create_bdx()
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


#todo
#userside
#set the web part on requests
#delete apks from bd
#staraight editing of apks in the post of apk segment
#OPTIMIZATION !!!1!1
#todo end


### ADMIN ADMIN ADMIN ADMIN
### ADMIN ADMIN ADMIN ADMIN
### ADMIN ADMIN ADMIN ADMIN
### ADMIN ADMIN ADMIN ADMIN
def create_output_of_bd(user_id):
    POSTS = {
        str(uuid.uuid4()): {
            'title': f'{index[1]}',
            'body': f'\npackage name: {index[0]}\n'
                    f'display name: {index[1]}\n'
                    f'current state: {index[2]}\n'
                    f'url to playstore: \nhttps://play.google.com/store/apps/details?id={index[0]}',
            'votes': random.randint(-2, 5),
        } for index in get_all_apks_for_admin()
    }
    return POSTS

posts_cb = CallbackData('post', 'id', 'action')  # post:<id>:<action>


def get_keyboard(uid) -> types.InlineKeyboardMarkup:
    """
    Generate keyboard with list of posts
    """
    get_keyboard.POSTS = create_output_of_bd(uid)
    markup = types.InlineKeyboardMarkup().add(InlineKeyboardButton('добавить приложение', callback_data='addapk')).add(InlineKeyboardButton('добавить доступ для юзера', callback_data='adduser'))
    for post_id, post in get_keyboard.POSTS.items():
        markup.add(
            types.InlineKeyboardButton(
                post['title'],
                callback_data=posts_cb.new(id=post_id, action='view')),
        )
    return markup


@dp.callback_query_handler(text='adduser', state=States.AUTH)
async def get_auth_passwords(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'дайте пакет приложения к которому надо дать доступ')
    await addUsers.package_input.set()

@dp.message_handler(state = addUsers.package_input)
async def process_start_command(message: types.Message, state=addUsers.package_input):
    if check_if_apk_already_there(message.text) != 0:
        async with state.proxy() as data:
            data['package_2'] = message.text
        await bot.send_message(message.from_user.id, 'чтобы дать доступ вебам к приложению надо дать боту их ид, закидывать пачкой, делить энтером, скидывать сюда в формате \n \nid\nid\nid\nid')
        await addUsers.userids_input.set()

    else:
        await bot.send_message(message.from_user.id, 'you have to add the apk to use this, get to the menu /admin_home')
        await States.AUTH.set()

@dp.message_handler(state = addUsers.userids_input)
async def process_start_command(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        pckg = data['package_2']
        return_data = update_data_bd(pckg, message.text)
        if return_data == 0:
            await bot.send_message(message.from_user.id, 'sorry, there is a bug in the bd, probably there are 2 or more rows of data for one apk /admin_home')
            await States.AUTH.set()
        await bot.send_message(message.from_user.id, 'bd updated, go to the menu /admin_home')
        await States.AUTH.set()


def format_post(post_id: str, post: dict) -> (str, types.InlineKeyboardMarkup):
    text = md.text(\
        md.hbold(post['title']),
        md.quote_html(post['body']),
        '')

    markup = types.InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('назад', callback_data='goback')).add(InlineKeyboardButton('дать вебам доступ', callback_data='adduser'))
    return text, markup


#start command
@dp.message_handler(commands='admin', state = "*")
async def process_start_command(message: types.Message, state=FSMContext):

    await message.reply(MESSAGES['start'])
    await States.AUTH_0.set()

inline_kb_full = InlineKeyboardMarkup()
inline_btn_3 = InlineKeyboardButton('добавить приложение', callback_data='addapk')
inline_kb_full.add(inline_btn_3)

inline_back_button = InlineKeyboardMarkup().add(InlineKeyboardButton('back', callback_data='goback'))

@dp.message_handler(state=States.AUTH_0)
async def get_auth_passwords(message: types.Message, state=FSMContext):
    if message.text in access_tokens:
        print(message.from_user.id)
        await message.reply('список приложений, нажмите на прилу для большей информации.', reply_markup=get_keyboard(message.from_user.id))
        await States.AUTH.set()

    else:
        await message.reply('токен доступа неверный')


@dp.callback_query_handler(text='goback', state=States.AUTH)
async def get_auth_passwords(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'список приложений, нажмите на прилу для большей информации.', reply_markup=get_keyboard(callback_query.from_user.id))


@dp.message_handler(commands='admin_home', state = "*")
async def get_auth_passwords(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'список приложений, нажмите на прилу для большей информации.', reply_markup=get_keyboard(message.from_user.id))
    await States.AUTH.set()


@dp.callback_query_handler(text='adddeveloper', state=States.AUTH)
async def get_auth_passwords(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'дайте пакет прилы к которой будут даваться данные \n\ngo back /admin_home')
    await StatesAddRK.pack_state.set()


@dp.callback_query_handler(text='addrk', state=States.AUTH)
async def get_apk_package(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'для того чтобы добавить аккаунт разработчика в бот нужны куки от аккаунта, пароль от аккаунта, а также ИД приложения в фб. \n \nчтобы продолжить отправьте в бота сообщение с куки, покачто только один поддерживаемый формат, json, чтобы перевести куки, используйте \nhttps://coockie.pro/pages/netscapetojson/ \n\ngo back /admin_home')
    await StatesAddRK.file_with_cookies_input.set()

@dp.message_handler(state=StatesAddRK.file_with_cookies_input)
async def get_apk_package(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['file_with_cookies_input'] = message.text
    print(message.text)
    facebook_cookies = message.text
    await bot.send_message(chat_id = message.from_user.id, text = f'{facebook_cookies} \nдалее скиньте в бота пароль от аккаунта фб')
    await StatesAddRK.password_fb.set()

@dp.message_handler(state=StatesAddRK.password_fb)
async def get_apk_package(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password_fb'] = message.text
    facebook_password = message.text
    await bot.send_message(chat_id = message.from_user.id, text = f'{facebook_password} \nдалее скиньте в бота id of prila')
    await StatesAddRK.apk_id.set()

@dp.message_handler(state=StatesAddRK.apk_id)
async def get_apk_package(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        facebook_cookies = data['file_with_cookies_input']
        facebook_password = data['password_fb']
        facebook_appid = message.text
        package = data['package']
        disname = data['disname']
        status = "ACTIVE"
        metka = 'volos'
        users = '0'
    facebook_apk = message.text
    await bot.send_message(chat_id = message.from_user.id, text = f'{facebook_cookies} \n{facebook_password} \n{facebook_appid} \n{package} \n{disname} \n\n inserted into bd, menu : /admin_home')
    add_apk(package, disname, status, metka, facebook_cookies, facebook_password, facebook_appid, users)
    print(get_all_apks_for_admin())
    for i in get_all_apks_for_admin():
        await bot.send_message(chat_id = message.from_user.id, text = i)
    await States.AUTH.set()


@dp.message_handler(commands=['asdfasdfasdfasdfasdfasdfasdf'], state = "*")
async def process_start_command(message: types.Message, state=FSMContext, callback= types.CallbackQuery):
    try:
        test_bd_test()
    except Exception as e:
        print('something went wrong')
        await bot.send_message(chat_id = message.from_user.id, text = f'tested unsuccesfully))')
    await bot.send_message(chat_id = message.from_user.id, text = f'tested succesfully))')



@dp.message_handler(state=StatesAddRK.finishing)
async def get_apk_package(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        facebook_cookies = data['file_with_cookies_input']
        facebook_password = data['password_fb']
        facebook_appid = message.text
    await bot.send_message(chat_id = message.from_user.id, text = f'{facebook_cookies} \n{facebook_password} \n{facebook_appid} \n\ninserted into bd')
    #login_into_rk(facebook_cookies, facebook_password, facebook_appid, facebook_rks)
    await States.AUTH_0.set()

@dp.callback_query_handler(text='addapk', state=States.AUTH)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'введите пожалуйста package с которым зарегестрированна прила.')
    await States.next()


@dp.callback_query_handler(posts_cb.filter(action='view'), state= States.AUTH)
async def query_view(query: types.CallbackQuery, callback_data: typing.Dict[str, str], message = types.Message):
    post_id = callback_data['id']

    post = get_keyboard.POSTS.get(str(post_id))
    print(post)
    if not post:
        return await query.answer('Unknown apk!')

    text, markup = format_post(post_id, post)
    await query.message.edit_text(text, reply_markup=markup)


data_for_bd = []
@dp.message_handler(state=States.packagename_input)
async def get_apk_package(message: types.Message, state: States.packagename_input):
    if check_for_active_apk(message.text)=='000':
        if check_if_apk_already_there(message.text) == 0:
            await message.reply('this package is available at the store and also isn`t in the bd')
            async with state.proxy() as data:
                data['package'] = message.text

            await message.reply('now give me the display name for the apk')
            await States.next()
        else:
            await message.reply('sorry, this apk is already available in the bot, send me another one or /admin_home')

    else:
        await message.reply('sorry this apk is not available in the store right now')

@dp.message_handler(state=States.apkname_input)
async def get_apk_package(message: types.Message, state: States.apkname_input):
    async with state.proxy() as data:
            data['disname'] = message.text
    await message.reply('send ok to continue, to discard changes click back', reply_markup=inline_back_button.add(InlineKeyboardButton('continue', callback_data='addrk')))
    await States.AUTH.set()

### ADMIN ADMIN ADMIN ADMIN
### ADMIN ADMIN ADMIN ADMIN
### ADMIN ADMIN ADMIN ADMIN
### ADMIN ADMIN ADMIN ADMIN
### ADMIN ADMIN ADMIN ADMIN

### USER USER USER USER
### USER USER USER USER
### USER USER USER USER
### USER USER USER USER

class UserStates(StatesGroup):
    main_menu = State()
    package = State()
    rk_ids = State()


start_kb = types.InlineKeyboardMarkup().add(InlineKeyboardButton('Далее', callback_data='continue'))


@dp.message_handler(commands=['start'], state = "*")
async def process_start_command(message: types.Message, state=FSMContext, callback= types.CallbackQuery):

    await message.reply('Привет! Я бот по расшару приложений, осмотреть мою документацию можно вот тут: каналнейм', reply_markup=start_kb)
    await UserStates.main_menu.set()

@dp.message_handler(commands=['main_menu'], state = "*")
@dp.callback_query_handler(text = ['continue', 'main_menu'], state = '*')
async def process_start_command(message: types.Message, state: FSMContext, callback = types.CallbackQuery):
    print(message.from_user.id)
    APPS = {
        str(uuid.uuid4()): {
            'title': f'{index[1]}',
            'body': f'\npackage name: {index[0]}\n'
                    f'display name: {index[1]}\n'
                    f'current state: {index[2]}\n'
                    f'url to playstore: \nhttps://play.google.com/store/apps/details?id={index[0]}',
            'votes': random.randint(-2, 5),
        } for index in get_active_apks_of_users(str(message.from_user.id))
    }

    print(get_active_apks_of_users(str(message.from_user.id)))
    print('works')
    posts_cb = CallbackData('post', 'id', 'action')
    print('works')
    markup = types.InlineKeyboardMarkup()
    for post_id, post in APPS.items():
        markup.add(
            types.InlineKeyboardButton(
                post['title'],
                callback_data=posts_cb.new(id=post_id, action='view')),
        )

    async with state.proxy() as data:
        data['APPS'] = APPS


    await bot.send_message(message.from_user.id, 'Вот список приложений которые доступны тебе:', reply_markup=markup)

    await UserStates.main_menu.set()

@dp.callback_query_handler(posts_cb.filter(action='view'), state= UserStates.main_menu)
async def query_view(query: types.CallbackQuery, callback_data: typing.Dict[str, str], message = types.Message, state = FSMContext):

    def format_post(post_id: str, post: dict) -> (str, types.InlineKeyboardMarkup):
        text = md.text(
            post['title'],
            post['body'],
            '')

        markup = types.InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('назад', callback_data='main_menu')).add(InlineKeyboardButton('Расшар', callback_data='share'))
        return text, markup

    async with state.proxy() as data:
        APPS = data['APPS']

    post_id = callback_data['id']

    post = APPS.get(str(post_id))

    if not post:
        return await query.answer('Unknown apk!')

    text, markup = format_post(post_id, post)
    await query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(text = ['share'], state = '*')
async def process_start_command(message: types.Message, state: FSMContext, callback = types.CallbackQuery):

    await bot.send_message(message.from_user.id, 'Введите пожалуйста пакет приложения под расшар, вернуться в меню, /main_menu')
    await UserStates.package.set()

@dp.message_handler(state=UserStates.package)
async def get_apk_package(message: types.Message, state: UserStates.package):
    try:
        if str(message.from_user.id) in get_special_package(message.text)[-1]:
            async with state.proxy() as data:
                data['package'] = message.text
            await bot.send_message(message.from_user.id, 'введите пожалуйста id рк на которые требуется расшарить прилу. Mеню, /main_menu . формат: \n\nid\nid\nid\nid\nid')
            await UserStates.rk_ids.set()
        else:
            await bot.send_message(message.from_user.id, 'ошалел? ты шо хаккер, иди у админа доступ проси блин, самый умный чтоли....)) Mеню, /main_menu', reply_markup = InlineKeyboardButton('Хорошо, повинуюсь', callback_data='main_menu'))
            await UserStates.main_menu.set()
    except Exception as e:
        print(e)
        await bot.send_message(message.from_user.id, 'ОШИБКА, скорее всего пакет приложения был неправелен. Попробуйте повторно. Mеню, /main_menu')


@dp.message_handler(state=UserStates.rk_ids)
async def get_apk_package(message: types.Message, state: UserStates.rk_ids):
    async with state.proxy() as data:
        package = data['package']

    apk_data = get_special_package(package)

    rk = message.text.split('\n')
    cookies = apk_data[4]
    passw = apk_data[5]
    appid = apk_data[6]

    r = login_into_rk(cookies, passw, appid, rk)

    if r[0] == 1:
        await bot.send_message(message.from_user.id, 'Поздравляю, рк были добавленны. Mеню, /main_menu', reply_markup = types.InlineKeyboardMarkup(InlineKeyboardButton('Готово', callback_data='main_menu')))
        await UserStates.main_menu.set()
    else:
        await bot.send_message(message.from_user.id, f'скрипт выдал вот эту ошибку\n\n{r[0]} ', reply_markup = types.InlineKeyboardMarkup(InlineKeyboardButton('Ладно...', callback_data='main_menu')))
        await UserStates.main_menu.set()



async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()



if __name__ == '__main__':

    #add_apk(953941448, 'boookofrathisisfine.androidappi', 'фывафыва', 'ACTIVE', 'metka123')
    executor.start_polling(dp, on_shutdown=shutdown)
