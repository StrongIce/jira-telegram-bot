import telebot 
from function import ad_user_search, add_user_base, user_fullname_search, chat_id_search,jira_login,create_ticket_jira,my_bot


jira = jira_login()
bot = my_bot
hideBoard = telebot.types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def start(message):
    global chat_id
    chat_id = message.from_user.id
    if  chat_id_search(chat_id) == True:
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('NOX', ' Баланс')
        keyboard.row('Телефония', ' ПК')
        keyboard.row('Интернет', 'Другое') 
        bot.send_message(message.chat.id, f"Что случилось?", reply_markup=keyboard)
        bot.register_next_step_handler(message, problem_read)    
    else: 
        bot.send_message(message.chat.id, f'Нет доступа! \nВведи кодовое слово: ')
        bot.register_next_step_handler(message, access)


def access(message):
    code_access = message.text
    if code_access == 'Доступ21':
        bot.send_message(message.chat.id, f"Введи свое имя: ")
        bot.register_next_step_handler(message, first_names)
    else:
        bot.send_message(message.chat.id, f"Доступ запрещен! Попробуй еще раз!")
        bot.register_next_step_handler(message, access) 

def first_names(message):
    global first_name
    first_name = message.text
    bot.send_message(message.chat.id, f"Введи свою фамилию: ")
    bot.register_next_step_handler(message, last_names)


def last_names(message):
    global last_name
    last_name = message.text 
    fullname = last_name + ' ' + first_name
    if ad_user_search(fullname) == False:
        bot.send_message(message.chat.id, f'Таких нет в наших местах. \nВведи свое имя: ')
        bot.register_next_step_handler(message, first_names) 
    else:
        bot.send_message(message.chat.id, f'Регистрация пройдена!')
        bot.send_message(message.chat.id, f'Если хочешь сообщить о проблеме введи команду /start')
        user = (message.from_user.id, first_name, last_name, ad_user_search(fullname))
        add_user_base(user)
        bot.register_next_step_handler(message, start)


def problem_read(message):
    global problem_summary
    problem_summary = message.text
    if problem_summary == 'Баланс':
        bot.send_message(message.chat.id, 'Укажите имя и телефон сотрудника: ', reply_markup=hideBoard)
        bot.register_next_step_handler(message, create_ticket_balance)
    elif problem_summary == 'Телефония':
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Белая', ' Серая')
        bot.send_message(message.chat.id, "Выбери вид: ", reply_markup=keyboard)
        bot.register_next_step_handler(message, create_ticket_phones)
    else: 
        bot.send_message(message.chat.id, "Введите подробное описание проблемы", reply_markup=hideBoard)
        bot.register_next_step_handler(message, create_discryption)


def create_ticket_phones(message):
    user_fullname = user_fullname_search(chat_id)
    user = ad_user_search(user_fullname)
    descryprtion = 'Не работает серая связь' 
    if message.text == 'Серая':      
        bot.send_message(message.chat.id, "Окей, заявка создается: " + user_fullname_search(chat_id))   
        create_ticket_jira(problem_summary,user_fullname,user,descryprtion)    
        last_issue = jira.search_issues("project=IT")[0].key
        bot.send_message(message.chat.id, "Готово! Заявка зарегистрированна с номером: " +  last_issue, reply_markup=hideBoard)
        bot.register_next_step_handler(message, start)
        my_group_chat = message.from_user.id
        bot.send_message(my_group_chat, "Создана заявка от: " + ' ' \
            + user_fullname + '\n' + 'Тема проблемы: ' + problem_summary + '\n' + 'C номером: ' \
            + last_issue + '\n' + 'Не работает серая связь')
    else: 
        bot.send_message(message.chat.id, "Введите подробное описание проблемы", reply_markup=hideBoard) 
        bot.register_next_step_handler(message, create_discryption)


def create_discryption(message):
    global descryprtion
    descryprtion = message.text
    bot.send_message(message.chat.id, "Введите свой IP или AnyDesk \n(если работаешь дома)")
    bot.register_next_step_handler(message, create_ticket)

def create_ticket_balance(message):         
    description = f'Пополнить баланс: {message.text}'
    fullname = user_fullname_search(chat_id)
    user = ad_user_search(fullname)
    bot.send_message(message.chat.id, "Окей, заявка создается: " + fullname)
    create_ticket_jira(problem_summary,fullname,user,description)     
    last_issue = jira.search_issues("project=IT")[0].key
    bot.send_message(message.chat.id, "Готово! Заявка зарегистрированна с номером: " +  last_issue, reply_markup=hideBoard)
    bot.register_next_step_handler(message, start)
    my_group_chat = message.from_user.id
    bot.send_message(my_group_chat, "Создана заявка от: " + ' ' \
        + user_fullname_search(chat_id) + '\n' + 'Тема проблемы: ' + problem_summary + '\n' + 'C номером: ' \
        + last_issue + '\n' + description)


def create_ticket(message):
    descr = f'{descryprtion},{message.text}'
    fullname = user_fullname_search(chat_id)
    user = ad_user_search(fullname)       
    my_ip = message.text
    bot.send_message(message.chat.id, "Окей, заявка создается: " + fullname)
    create_ticket_jira(problem_summary,fullname,user,descr)
    last_issue = jira.search_issues("project=IT")[0].key
    bot.send_message(message.chat.id, "Готово! Заявка зарегистрированна с номером: " +  last_issue)
    bot.register_next_step_handler(message, start)
    my_group_chat = message.from_user.id
    bot.send_message(my_group_chat, "Создана заявка от: " + ' ' + fullname + \
         '\n' + 'Тема проблемы: ' + problem_summary + '\n' \
         + 'C номером: ' + last_issue + '\n' + 'Описание: ' \
         + descryprtion + '\n' + 'IP: ' + my_ip)


bot.polling(none_stop=True, interval=0)