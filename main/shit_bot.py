import telebot

token = '6261335234:AAGKSM2l-Sc_WX22YQLzMN6fCsW_3UDr3jQ'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Здравствуйте! \n'
                          f'Чтобы получать уведомления о проблемах на сайтах,'
                          f'укажите свой ID в личном кабинете\n'
                          f'Ваш ID: {message.from_user.id}')


bot.infinity_polling()
