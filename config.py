from DB import BotDB
BotDB = BotDB("tic-tac-toe.db")

TOKEN = YOUR_BOT_API


# символы, которые используются
SYMBOLS = ['⭕','◻','❌']

# ответы бота
YOUR_TURN = 'Ваш ход'
YOU_WIN = 'Вы победили'
YOU_FAIL = 'Вы проиграли'
DRAW = 'Ничья'
HELP = 'Бот для игры в крестики-нолики\nСоздатель: @dieyouannoying\n\n' \
            'Используйте команду /start для начала новой игры'

# ошибки
ALERT = 'Нажимать можно только на ' + SYMBOL_1
