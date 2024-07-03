import telebot
import os
import random
import time
import asyncio
import aiohttp

from colorama import Fore, Back, Style, init
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot import asyncio_filters

API_TOKEN = '2129941134:AAH_UEQqtxOHuM3Ils2gxnILtum3xvjwbck'
bot = AsyncTeleBot(API_TOKEN, state_storage=StateMemoryStorage())

class MyStates(StatesGroup):
    phone = State()
    city = State()
    adress = State()
    descript = State()
    application = State()
    end = State()

# colors for cmd
FRED    	= "\033[31m"
FGREEN  	= "\033[32m"
FYELLOW 	= "\033[33m"
FBLUE   	= "\033[34m"
RESET_ALL   = "\033[0m"

# user's id
cid_admin = 1163738962
admin_name = "O6server0"

print(f"{FGREEN}[BOT START WORKING]{RESET_ALL}")
print("-" * 20)
print()

# Стандартная клавиатура
def set_main_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Оборудование", callback_data="equip"),
        InlineKeyboardButton("Интернет", callback_data="internet")
        )
    markup.add(InlineKeyboardButton("Тариф", callback_data="tariff"))
    markup.add(InlineKeyboardButton("Добавить описание к проблеме", callback_data="other"))
    markup.add(InlineKeyboardButton("Показать и составить мою заявку", callback_data="application"))
    return markup

# Кнопка Назад к роутерам
def set_back_routers():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Назад", callback_data="routers"))
    return markup

# Составление заявки
def set_application_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Составить", callback_data="set_application"))
    markup.add(InlineKeyboardButton("Назад", callback_data="back"))
    return markup

# Добавление описания в разделе кабелей
def set_add_discription_cabels():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Добавить описание", callback_data="other"))
    markup.add(InlineKeyboardButton("Показать и составить мою заявку", callback_data="application"))
    markup.add(InlineKeyboardButton("Назад", callback_data="cables"))
    return markup

def set_add_discription_tariff():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Добавить описание", callback_data="other"))
    markup.add(InlineKeyboardButton("Показать и составить мою заявку", callback_data="application"))
    markup.add(InlineKeyboardButton("Назад", callback_data="tariff"))
    return markup

# Добавление описания в разделе роутеров
def set_add_discription_routers():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Добавить описание", callback_data="other"))
    markup.add(InlineKeyboardButton("Показать и составить мою заявку", callback_data="application"))
    markup.add(InlineKeyboardButton("Назад", callback_data="routers"))
    return markup

# Добавление описания в разделе интернета
def set_add_discription_internet():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Добавить описание", callback_data="other"))
    markup.add(InlineKeyboardButton("Показать и составить мою заявку", callback_data="application"))
    markup.add(InlineKeyboardButton("Назад", callback_data="internet"))
    return markup

# Оборудование
def set_equip_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Повреждение кабеля", callback_data="cables"))
    markup.add(InlineKeyboardButton("Повреждение роутера", callback_data="routers"))
    markup.add(InlineKeyboardButton("Назад", callback_data="back"))
    return markup

# Кабеля
def set_cabels_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Оптоволоконный кабель", callback_data="optika"))
    markup.add(InlineKeyboardButton("LAN-кабель", callback_data="lan"))
    markup.add(InlineKeyboardButton("Кабель питания", callback_data="power"))
    markup.add(InlineKeyboardButton("Назад", callback_data="equip"))
    return markup

# Оптоволокно
def set_optic_cabel():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Повреждение кабеля", callback_data="off_optic_cabel"))
    markup.add(InlineKeyboardButton("Повреждение разъёма (коннектора)", callback_data="off_optic_connector"))
    markup.add(InlineKeyboardButton("Назад", callback_data="cables"))
    return markup

# LAN
def set_lan_cabel():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Повреждение кабеля", callback_data="off_lan_cabel"))
    markup.add(InlineKeyboardButton("Повреждение разъёма (коннектора)", callback_data="off_lan_connector"))
    markup.add(InlineKeyboardButton("Назад", callback_data="cables"))
    return markup

# Кабель питания
def set_power_cabel():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Повреждение кабеля", callback_data="off_power_cabel"))
    markup.add(InlineKeyboardButton("Повреждение разъёма (коннектора)", callback_data="off_power_connector"))
    markup.add(InlineKeyboardButton("Повреждение блока питания", callback_data="off_power_block"))
    markup.add(InlineKeyboardButton("Назад", callback_data="cables"))
    return markup

# Роутер
def set_router_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Не горят индикаторы", callback_data="off_indicators"))
    markup.add(InlineKeyboardButton("Индикаторы красные", callback_data="red_indicators"))
    markup.add(InlineKeyboardButton("Попадание влаги", callback_data="water_in_router"))
    markup.add(InlineKeyboardButton("Физическое повреждение", callback_data="physical_damage"))
    markup.add(InlineKeyboardButton("Отсутсвие явных повреждений", callback_data="something_strange"))
    markup.add(InlineKeyboardButton("Назад", callback_data="equip"))
    return markup

# Интернет
def set_internet_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Нет соединения с сетью по LAN", callback_data="off_lan_connection_internet"))
    markup.add(InlineKeyboardButton("Медленная скорость интернета", callback_data="slow_connection_internet"))
    markup.add(InlineKeyboardButton("Отсутствие WIFI соединения", callback_data="off_wifi_connection_internet"))
    markup.add(InlineKeyboardButton("Временная потеря соединения / Плохая связь", callback_data="off_internet_sometimes"))
    markup.add(InlineKeyboardButton("Назад", callback_data="back"))
    return markup

# Тариф
def set_tariff_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Непонятные списания", callback_data="some_offs"))
    markup.add(InlineKeyboardButton("Ошибки с выставлением счетов", callback_data="account_error"))
    markup.add(InlineKeyboardButton("Мой тариф", callback_data="my_tariff"))
    markup.add(InlineKeyboardButton("Смена тарифа", callback_data="change_tariff"))
    markup.add(InlineKeyboardButton("Назад", callback_data="back"))
    return markup

# Назад
def set_back_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Назад", callback_data="back"))
    return markup

"""
    await bot.delete_my_commands(scope=None, language_code=None)
    await bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("start", "Составить заявку")
        ], )
"""

# Старт с регистрацией
@bot.message_handler(commands=['start'])
async def starting(message):
    await bot.delete_my_commands(scope=None, language_code=None)
    await bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("start", "Составить заявку с регистрацией"),
            telebot.types.BotCommand("set", "Составить заявку без регистрации")
        ], )
    await bot.set_state(message.from_user.id, MyStates.phone, message.chat.id)
    await bot.send_message(message.chat.id, "Введите нормер телефона для связи с вами:")

# Старт без регистрации
@bot.message_handler(commands=['set'])
async def starting(message):
    await bot.send_message(message.chat.id, "В чем заключается Ваша проблема?", reply_markup=set_main_keyboard())
    await bot.set_state(message.from_user.id, MyStates.application, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['descript'] = ""
        data['application'] = ""

# Получение номера телефона
@bot.message_handler(state=MyStates.phone)
async def get_phone(message):
    await bot.send_message(message.chat.id, "Введите ваш город:")
    await bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['phone'] = message.text
        data['application'] = ""
        data['descript'] = ""

# Получение города
@bot.message_handler(state=MyStates.city)
async def get_phone(message):
    await bot.send_message(message.chat.id, "Введите ваш адрес для составления заявки:")
    await bot.set_state(message.from_user.id, MyStates.adress, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text

# Получение адреса
@bot.message_handler(state=MyStates.adress)
async def get_phone(message):
    await bot.send_message(message.chat.id, "В чем заключается Ваша проблема?", reply_markup=set_main_keyboard())
    await bot.set_state(message.from_user.id, MyStates.application, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['adress'] = message.text

# Действия бота
@bot.callback_query_handler(func=lambda call: True)
async def editing_keyboard(call):
    cid = call.message.chat.id

    # Возврат к главной форме
    if call.data == "back":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id, text="В чем заключается Ваша проблема?")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_main_keyboard())

    # Оборудование
    elif call.data == "equip":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id, text="В чем заключается Ваша проблема?")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_equip_keyboard())

    # Интернет
    elif call.data == "internet":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id, text="В чем заключается Ваша проблема?")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_internet_keyboard())

    # Тариф
    elif call.data == "tariff":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id, text="В чем заключается Ваша проблема?")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_tariff_keyboard())

    # Вывод заявки
    elif call.data == "application":
        async with bot.retrieve_data(cid, cid) as data:
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                            text="Заявка\n"
                                                 "-------------------------------\n"
                                                 f"| Телефон: {data['phone']}\n"
                                                 f"| Город: {data['city']}\n"
                                                 f"| Адрес: {data['adress']}\n"
                                                 f"| Проблема: {data['application']}\n"
                                                 "-------------------------------\n"
                                                 f"| Описание: {data['descript']}"
                                        )
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_application_keyboard())

    # Отправка заявки
    elif call.data == "set_application":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id, text="Ваша заявка успешно отправлена специалисту!")
        async with bot.retrieve_data(cid, cid) as data:
            await bot.send_message(chat_id=cid_admin,
                                        text="Заявка\n"
                                             "-------------------------------\n"
                                             f"| Телефон: {data['phone']}\n"
                                             f"| Город: {data['city']}\n"
                                             f"| Адрес: {data['adress']}\n"
                                             f"| Проблема: {data['application']}\n"
                                             "-------------------------------\n"
                                             f"| Описание: {data['descript']}"
                                        )
            data['application'] = ""
            data['descript'] = ""
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_back_keyboard())

    # Описание проблемы
    elif call.data == "other":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id, text="Опишите вашу проблему:")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_back_keyboard())

        # Получение описания
        @bot.message_handler(state=MyStates.application)
        async def get_descript(message):
            await bot.set_state(message.from_user.id, MyStates.end, message.chat.id)
            async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['descript'] = message.text
                await bot.send_message(message.chat.id, "Если желаете уточнить заявку, воспользуйтесь кнопками ниже",
                                       reply_markup=set_main_keyboard())

    #
    # КАБЕЛЯ
    #

    elif call.data == "cables":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                    text="| **Оптоволоконный кабель** - тонкий кабель для квадратного разъема\n\n"
                                         "| **LAN-кабель** - толстый кабель, подключенный в один из нескольких одинаковых разъемов\n\n"
                                         "| **Кабель питания** - кабель идущий от разетки\n")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_cabels_keyboard())

    #
    # Оптоволокно
    #

    elif call.data == "optika":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                    text="| **Оптоволоконный кабель** - тонкий провод идущий из подъезда и имеющий квадратный разъём")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_optic_cabel())

    # Повреждение кабеля
    elif call.data == "off_optic_cabel":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Повреждение оптоволоконного кабеля"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Добавьте описание или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_cabels())

    # Повреждение коннектора
    elif call.data == "off_optic_connector":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Повреждение коннектора оптоволоконного кабеля"

            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Добавьте описание или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_cabels())

    #
    # LAN
    #

    elif call.data == "lan":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                    text="| **LAN-кабель** - толстый кабель идущий от роутера к вашему устройству (ПК, ноутбук)."
                                         "\nКабель подключен к одному из нескольких одинаковых разъёмов")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_lan_cabel())

    # Повреждение кабеля
    elif call.data == "off_lan_cabel":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Повреждение LAN-кабеля"

            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Добавьте описание или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_cabels())

    # Повреждение коннектора
    elif call.data == "off_lan_connector":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Повреждение коннектора LAN-кабеля"

            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Добавьте описание или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_cabels())

    #
    # Кабель питания
    #

    elif call.data == "power":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                    text="| **LAN-кабель** - кабель идущий от блока питания подключенного к разетке")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_power_cabel())

    # Повреждение кабеля
    elif call.data == "off_power_cabel":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Повреждение кабеля блока питания"

            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Добавьте описание или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_cabels())

    # Повреждение коннектора
    elif call.data == "off_power_connector":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Повреждение коннектора блока питания"

            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Добавьте описание или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_cabels())

    # Повреждение блока питания
    elif call.data == "off_power_block":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Повреждение самого блока питания"

            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Добавьте описание или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_cabels())

    #
    # РОУТЕР
    #

    elif call.data == "routers":
        await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
            text="Если индикаторы не горят, или же просто не работает что-то - попытайтесь сперва перезагрузить роутер.")
        await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_router_keyboard())

    # Не горят индикаторы
    elif call.data == "off_indicators":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "На роутере не горят индикаторы"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Опишите какие именно индикаторы не горят:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id, reply_markup=set_back_routers())

            # Получение описания
            @bot.message_handler(state=MyStates.application)
            async def get_descript(message):
                async with bot.retrieve_data(cid, cid) as data:
                    data['descript'] = message.text
                    await bot.send_message(message.chat.id,
                                           "Если желаете уточнить заявку, воспользуйтесь кнопками ниже",
                                           reply_markup=set_main_keyboard())

    # Индикаторы красные
    elif call.data == "red_indicators":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "На роутере красные индикаторы"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Опишите какие именно индикаторы красные:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_back_routers())

            # Получение описания
            @bot.message_handler(state=MyStates.application)
            async def get_descript(message):
                async with bot.retrieve_data(cid, cid) as data:
                    data['descript'] = message.text
                    await bot.send_message(message.chat.id,
                                           "Если желаете уточнить заявку, воспользуйтесь кнопками ниже",
                                           reply_markup=set_main_keyboard())

    # Попадание влаги на роутер
    elif call.data == "water_in_router":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "В роутер попала влага, после чего произошла поломка"

            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Добавьте описание или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_routers())

    # Физическое повреждение роутера
    elif call.data == "physical_damage":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Роутер сломался после физического воздействия"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Опишите что именно произошло:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_back_routers())

            # Получение описания
            @bot.message_handler(state=MyStates.application)
            async def get_descript(message):
                async with bot.retrieve_data(cid, cid) as data:
                    data['descript'] = message.text
                    await bot.send_message(message.chat.id,
                                           "Если желаете уточнить заявку, воспользуйтесь кнопками ниже",
                                           reply_markup=set_main_keyboard())

    # Отсутсвие явных повреждений роутера
    elif call.data == "something_strange":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Роутер не работает, но явные повреждения отсутствуют"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Добавьте описание или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_routers())

    #
    # ИНТЕРНЕТ
    #

    # Нет LAN соединения
    elif call.data == "off_lan_connection_internet":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Отсутствует интернет при LAN соединении"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="  Советы:\n\n"
                                             "|  Проверьте подключение кабеля Ethernet между компьютером и роутером.\n\n"
                                             "|  Проверьте индикаторы на роутере. Зелёный, оранжевый - хорошо, красный - плохо.\n\n"
                                             "|  Перезагрузите компьютер и маршрутизатор.\n\n"
                                             "Если советы не помогли - опишите проблему ниже или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_internet())

    # Медленная скорость интернета
    elif call.data == "slow_connection_internet":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Медленная скорость интернета"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="  Советы:\n\n"
                                             "| Проверьте скорость интернета на соответствие с вашим тарифом:\n\n"
                                             "    https://msk.rt.ru/checkup\n\n"
                                             "| Проверьте индикаторы на роутере. Зелёный, оранжевый - хорошо, красный - плохо.\n\n"
                                             "| Попробуйте перезагрузить маршрутизатор.\n\n"
                                             "Если советы не помогли - опишите проблему ниже или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_internet())

    # Отсутсвие WIFI соединения
    elif call.data == "off_wifi_connection_internet":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Отсутсвие WIFI соединения"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="  Советы:\n\n"
                                             "| Перезагрузите маршрутизатор и устройство.\n\n"
                                             "| Проверьте индикатор WIFI на роутере. Зелёный, оранжевый - хорошо, красный - плохо.\n\n"
                                             "| Проверьте другие индикаторы.\n\n"
                                             "Если советы не помогли - опишите проблему ниже или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_internet())

    # Временная потеря соединения / Плохая связь
    elif call.data == "off_internet_sometimes":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Временная потеря соединения / Плохая связь"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="  Советы:\n\n"
                                             "| Переместите устройство или роутер ближе друг к другу.\n\n"
                                             "| Установите усилитель Wi-Fi для расширения зоны покрытия.\n\n"
                                             "| Измените частотный канал Wi-Fi на маршрутизаторе для избежания интерференции с другими устройствами.\n\n"
                                             "| Проверьте наличие обновлений для драйверов Wi-Fi на вашем устройстве.\n\n"
                                             "Если советы не помогли - опишите проблему ниже или составьте заявку:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_internet())

    #
    # ТАРИФ
    #

    # Непонятные списания
    elif call.data == "some_offs":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Производятся непонятные списания"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Опишите возникшую проблему подробнее:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_tariff())

            # Получение описания
            @bot.message_handler(state=MyStates.application)
            async def get_descript(message):
                async with bot.retrieve_data(cid, cid) as data:
                    data['descript'] = message.text
                    await bot.send_message(message.chat.id,
                                           "Если желаете уточнить заявку, воспользуйтесь кнопками ниже",
                                           reply_markup=set_main_keyboard())

    # Ошибки с выставлением счетов
    elif call.data == "account_error":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Ошибка с выставлением счета"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Опишите возникшую ошибку подробнее:")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_tariff())

            # Получение описания
            @bot.message_handler(state=MyStates.application)
            async def get_descript(message):
                async with bot.retrieve_data(cid, cid) as data:
                    data['descript'] = message.text
                    await bot.send_message(message.chat.id,
                                           "Если желаете уточнить заявку, воспользуйтесь кнопками ниже",
                                           reply_markup=set_main_keyboard())

    # Мой тариф
    elif call.data == "my_tariff":
        pass

    # Смена тарифа
    elif call.data == "change_tariff":
        async with bot.retrieve_data(cid, cid) as data:
            data['application'] = "Смена тарифа"
            await bot.edit_message_text(chat_id=cid, message_id=call.message.id,
                                        text="Опишите ваше требование подробнее и ожидайте звонка специалиста.")
            await bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.id,
                                                reply_markup=set_add_discription_tariff())

            # Получение описания
            @bot.message_handler(state=MyStates.application)
            async def get_descript(message):
                async with bot.retrieve_data(cid, cid) as data:
                    data['descript'] = message.text
                    await bot.send_message(message.chat.id,
                                           "Если желаете уточнить заявку, воспользуйтесь кнопками ниже",
                                           reply_markup=set_main_keyboard())

"""
@bot.message_handler(commands=['sendLongText'])
async def command_long_text(m):
    cid = m.chat.id
    await bot.send_message(cid, "If you think so...")
    await bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    await bot.send_message(cid, ".")
"""

bot.add_custom_filter(asyncio_filters.StateFilter(bot))

if __name__ == '__main__':
    asyncio.run(bot.polling(non_stop=True, request_timeout=90))