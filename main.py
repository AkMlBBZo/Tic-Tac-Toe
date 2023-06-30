from distutils.cmd import Command
from mailbox import Message
import config
from config import BotDB
import os
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
import contextlib

bot = Bot(token=config.TOKEN)
dp  = Dispatcher(bot=Bot(token=config.TOKEN))
callback_numbers = CallbackData("fabnum", "action")


def get_keyboard(user_id):
    
    field=BotDB.get_game_field(user_id)

    buttons = [
        types.InlineKeyboardButton(text=config.SYMBOLS[field[0]], callback_data=callback_numbers.new(action="b0")),
        types.InlineKeyboardButton(text=config.SYMBOLS[field[1]], callback_data=callback_numbers.new(action="b1")),
        types.InlineKeyboardButton(text=config.SYMBOLS[field[2]], callback_data=callback_numbers.new(action="b2")),
        types.InlineKeyboardButton(text=config.SYMBOLS[field[3]], callback_data=callback_numbers.new(action="b3")),
        types.InlineKeyboardButton(text=config.SYMBOLS[field[4]], callback_data=callback_numbers.new(action="b4")),
        types.InlineKeyboardButton(text=config.SYMBOLS[field[5]], callback_data=callback_numbers.new(action="b5")),
        types.InlineKeyboardButton(text=config.SYMBOLS[field[6]], callback_data=callback_numbers.new(action="b6")),
        types.InlineKeyboardButton(text=config.SYMBOLS[field[7]], callback_data=callback_numbers.new(action="b7")),
        types.InlineKeyboardButton(text=config.SYMBOLS[field[8]], callback_data=callback_numbers.new(action="b8")),
        types.InlineKeyboardButton(text="Сдаться", callback_data=callback_numbers.new(action="b9"))
    ]
    # row_width - nums of buttons in one line
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard

async def end_of_game(message:types.Message,chat_id,message_id):
    await bot.edit_message_text(text="Вы победили",chat_id=chat_id, message_id=message_id)
    await bot.edit_message_text(text="Вы проиграли",chat_id=int(str(BotDB.get_enemy_id(chat_id)[0])[1:][:-2]), message_id=int(str(BotDB.get_enemy_message_id(chat_id)[0])[1:][:-2]))
    BotDB.game_field(chat_id,111111111)
    BotDB.game_field(int(str(BotDB.get_enemy_id(chat_id)[0])[1:][:-2]),111111111)


async def draw(message:types.Message,chat_id,message_id):
    await bot.edit_message_text(text="У вас ничья",chat_id=chat_id, message_id=message_id)
    await bot.edit_message_text(text="У вас ничья",chat_id=int(str(BotDB.get_enemy_id(chat_id)[0])[1:][:-2]), message_id=int(str(BotDB.get_enemy_message_id(chat_id)[0])[1:][:-2]))
    BotDB.game_field(chat_id,111111111)
    BotDB.game_field(int(str(BotDB.get_enemy_id(chat_id)[0])[1:][:-2]),111111111)



async def update_num_text_fab(message: types.Message, n, chat_id, message_id):
    field=BotDB.get_game_field(chat_id)
    if(field[n]!=1):
        await bot.edit_message_text(text="Вы можете нажимать только на "+config.SYMBOLS[1],chat_id=chat_id, message_id=message_id, reply_markup=get_keyboard(chat_id))
        return 0
    field[n]=int(str(BotDB.get_figure(chat_id)[0])[1:][:-2])
    k=0
    for kkk in range(9):
        k*=10
        k+=field[kkk]
    BotDB.game_field(chat_id,int(k))
    BotDB.game_field(int(str(BotDB.get_enemy_id(chat_id)[0])[1:][:-2]),int(k))
    await bot.edit_message_text(text="Ход соперника ",chat_id=chat_id, message_id=message_id, reply_markup=get_keyboard(chat_id))
    await bot.edit_message_text(text="Ваш ход",chat_id=int(str(BotDB.get_enemy_id(chat_id)[0])[1:][:-2]), message_id=int(str(BotDB.get_enemy_message_id(chat_id)[0])[1:][:-2]), reply_markup=get_keyboard(int(str(BotDB.get_enemy_id(chat_id)[0])[1:][:-2])))
    BotDB.turn(0,chat_id)
    BotDB.turn(1,int(str(BotDB.get_enemy_id(chat_id)[0])[1:][:-2]))
    if field[0]==field[1]==field[2]!=1 or field[0]==field[3]==field[6]!=1 or field[0]==field[4]==field[8]!=1 or field[2]==field[4]==field[6]!=1 or field[2]==field[5]==field[8]!=1 or field[6]==field[7]==field[8]!=1 or field[1]==field[2]==field[7]!=1 or field[3]==field[4]==field[5]!=1:
        await end_of_game(message,chat_id,message_id)
    elif field.count(1)==0:
        await draw(message,chat_id,message_id)







@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if(BotDB.user_exists(message.from_user.id)):
        if message.chat.type == 'private':
            BotDB.enemy_search(1,message.from_user.id)
            await message.reply("Поиск соперника")
            for i in range(1,BotDB.num_of_users()+1):
                if int(str(BotDB.get_enemy_search(i)[0])[1:][:-2])==1 and int(str(BotDB.get_user_id(i)[0])[1:][:-2])!=message.from_user.id:
                    BotDB.enemy_search(0,message.from_user.id)
                    BotDB.enemy_search(0,int(str(BotDB.get_user_id(i)[0])[1:][:-2]))
                    BotDB.enemy_id(int(str(BotDB.get_user_id(i)[0])[1:][:-2]),message.from_user.id)
                    BotDB.enemy_id(message.from_user.id,int(str(BotDB.get_user_id(i)[0])[1:][:-2]))
                    msg = await message.reply('Соперник найден, удачной игры, вы играете за '+config.SYMBOLS[0]+'\nСейчас ваш ход', reply_markup=get_keyboard(message.from_user.id))
                    BotDB.enemy_message_id(msg["message_id"],int(str(BotDB.get_user_id(i)[0])[1:][:-2]))
                    BotDB.figure(0,message.from_user.id)
                    msg = await bot.send_message(text='Соперник найден, удачной игры, вы играете за\n'+config.SYMBOLS[2]+'\nСейчас ход противника', reply_markup=get_keyboard(message.from_user.id), chat_id=int(str(BotDB.get_user_id(i)[0])[1:][:-2]))
                    BotDB.figure(2,int(str(BotDB.get_user_id(i)[0])[1:][:-2]))
                    BotDB.enemy_message_id(msg["message_id"],message.from_user.id)
                    BotDB.turn(1,message.from_user.id)
                    BotDB.turn(0,int(str(BotDB.get_user_id(i)[0])[1:][:-2]))
                    break
        else:
            await message.reply('Бот не может использоваться в группах')
    else:
        BotDB.add_user(message.from_user.id, message.from_user.username)
        await message.answer(config.HELP)

@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.answer(config.HELP)



@dp.callback_query_handler(callback_numbers.filter(action=["b1","b2","b3","b4","b5","b6","b7","b8","b9","b0"]))
async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
    if(BotDB.get_turn(call.message.chat.id)==0):
        return 0
    action = callback_data["action"]
    if action == "b0":
        await update_num_text_fab(call.message,0,call.message.chat.id,call.message.message_id)
    elif action == "b1":
        await update_num_text_fab(call.message,1,call.message.chat.id,call.message.message_id)
    elif action == "b2":
        await update_num_text_fab(call.message,2,call.message.chat.id,call.message.message_id)
    elif action == "b3":
        await update_num_text_fab(call.message,3,call.message.chat.id,call.message.message_id)
    elif action == "b4":
        await update_num_text_fab(call.message,4,call.message.chat.id,call.message.message_id)
    elif action == "b5":
        await update_num_text_fab(call.message,5,call.message.chat.id,call.message.message_id)
    elif action == "b6":
        await update_num_text_fab(call.message,6,call.message.chat.id,call.message.message_id)
    elif action == "b7":
        await update_num_text_fab(call.message,7,call.message.chat.id,call.message.message_id)
    elif action == "b8":
        await update_num_text_fab(call.message,8,call.message.chat.id,call.message.message_id)
    elif action == "b9":
        await end_of_game(call.message,call.message.chat.id,call.message.message_id)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
