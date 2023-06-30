from DB import BotDB
BotDB = BotDB("tic-tac-toe.db")

TOKEN = YOUR_BOT_API


# символы, которые используются
SYMBOLS = ['⭕','◻','❌']


HELP = 'Бот для игры в крестики-нолики\nСоздатель: @dieyouannoying\n\n' \
            'Используйте команду /start для начала новой игры'

# ошибки
ALERT = 'Нажимать можно только на ' + SYMBOLS[1]
