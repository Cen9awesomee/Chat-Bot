import telebot
from telebot import types

TOKEN = '6068769328:AAEJMF4g30HiPi3pxsKfj1dwHHtYAZJAc1M'
bot = telebot.TeleBot(TOKEN)

# словарь для хранения информации о ПО
software = {}

# команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я бот для учета лицензионного ПО! Чтобы узнать, что я могу, напиши /help")

# команда /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "Я могу выполнить следующие команды:\n" \
                "/add_software - добавить новое ПО в учетную базу\n" \
                "/delete_software - удалить ПО из учетной базы\n" \
                "/list_software - просмотреть список всех ПО\n" \
                "/view_software - просмотреть информацию о конкретном ПО\n" \
                "/update_software - обновить информацию о ПО\n" \
                "/check_license - проверить наличие лицензии на конкретное ПО\n"
    bot.reply_to(message, help_text)

# команда /add_software
@bot.message_handler(commands=['add_software'])
def add_software(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Да', 'Нет')
    bot.reply_to(message, "Хотите добавить новое ПО в базу данных? (Да/Нет)", reply_markup=markup)
    bot.register_next_step_handler(message, add_software_step1)

def add_software_step1(message):
    if message.text == 'Да':
        bot.reply_to(message, "Введите название ПО:")
        bot.register_next_step_handler(message, add_software_step2)
    elif message.text == 'Нет':
        bot.reply_to(message, "Операция отменена.")
    else:
        bot.reply_to(message, "Некорректный ввод. Попробуйте еще раз.")
        add_software(message)

def add_software_step2(message):
    software_name = message.text
    if software_name in software:
        bot.reply_to(message, f"ПО с названием {software_name} уже есть в базе данных.")
    else:
        software[software_name] = {}
        bot.reply_to(message, "Введите количество лицензий:")
        bot.register_next_step_handler(message, add_software_step3)

def add_software_step3(message):
    try:
        software_license_count = int(message.text)
        if software_license_count > 0:
            software[list(software.keys())[-1]]['licenses'] = software_license_count
            bot.reply_to(message, "ПО успешно добавлено в базу данных.")
        else:
            bot.reply_to(message, "Количество лицензий должно быть положительным числом. Попробуйте еще раз.")
            add_software_step2(message)
    except ValueError:
        bot.reply_to(message, "Некорректный ввод. Попробуйте еще раз.")

# команда /list_software
@bot.message_handler(commands=['list_software'])
def list_software(message):
    if software:
        software_list = "Список всех ПО:\n"
        for software_name, software_data in software.items():
            software_list += f"- {software_name} (лицензий: {software_data['licenses']})\n"
        bot.reply_to(message, software_list)
    else:
        bot.reply_to(message, "В базе данных нет ни одного ПО.")

# команда /delete_software
@bot.message_handler(commands=['delete_software'])
def delete_software(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    software_list = list(software.keys())
    markup.add(*software_list)
    bot.reply_to(message, "Выберите ПО, которое нужно удалить:", reply_markup=markup)
    bot.register_next_step_handler(message, delete_software_step1)

def delete_software_step1(message):
    software_name = message.text
    if software_name in software:
        del software[software_name]
        bot.reply_to(message, f"ПО с названием {software_name} удалено из базы данных.")
    else:
        bot.reply_to(message, f"ПО с названием {software_name} не найдено в базе данных.")

def add_help_button():
    markup = types.ReplyKeyboardMarkup()
    help_button = types.KeyboardButton('/help')
    markup.add(help_button)
    return markup
          
bot.polling()