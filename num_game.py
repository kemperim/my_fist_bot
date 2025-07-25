from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command
import random
import logging

BOT_TOKEN = '8119594343:AAHY2NOdleuudG7CPMnaKmV9b8cv94ZPtaM'
bot = Bot(token =BOT_TOKEN)
dp = Dispatcher()
print("starting bot")
logging.basicConfig(level=logging.INFO)
user = {'in_game': False,
        'secret_number':None,
        'attempts': None,
        'total_games':0,
        'wins':0}
ATTEMPTS = 5
users = {}
def get_random_number() ->int:
    return random.randint(1,100)

async def process_start_command(message: Message):
    print(f"Пользователь {message.from_user.full_name}   user info {message.from_user.id}  ")
    await message.answer('Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help')
    if message.from_user.id not in users:
        users[message.from_user.id]={
        'in_game': False,
        'secret_number':None,
        'attempts': None,
        'total_games':0,
        'wins':0 }   

async def procces_help_command(message: Message):
    await message.answer(
         'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        'попыток\n\nДоступные команды:\n/help - правила '
        'игры и список команд\n/cancel - выйти из игры\n'
        '/stat - посмотреть статистику\n\nДавай сыграем?'
    )

async def process_cancel_command(message:Message):
    if user[message.from_user.id]['in_game']:
        user[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть'
            'снова - напишите нам'
        )

async def process_stat_command(message:Message):
        await message.answer(
            f'Всего игр сыграно: {user[message.from_user.id]["total_games"]}\n'
            f'Игр выиграно: {user[message.from_user.id]["wins"]}'
        )

@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def process_positive_answer(message:Message):
    if not user[message.from_user.id]['in_game']:
        user[message.from_user.id]['in_game'] = True
        user[message.from_user.id]['secret_number'] = get_random_number()
        user [message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, попробуй угадать!')
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )
@dp.message(lambda x: x.text and x.text.isdigit() and 1<=int(x.text)<=100)
async def process_numbers_answer(message: Message):
    if user[message.from_user.id]['in_game']: 
        if int(message.text) == user[message.from_user.id]['secret_number']:
            user[message.from_user.id]['in_game'] = False
            user[message.from_user.id]['total_games'] += 1
            user[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > user[message.from_user.id]['secret_number']:
            user[message.from_user.id]['attempts'] -= 1
            await message.answer(f'Мое число меньше \n Кол-во оставшися попыток: {user[message.from_user.id]["attempts"]}')
        elif int(message.text) < user['secret_number']:
            user['attempts'] -= 1
            await message.answer(f'Мое число больше \n Кол-во оставшися попыток: {user[message.from_user.id]["attempts"]}')

        if user[message.from_user.id]['attempts'] == 0:
            user[message.from_user.id]['in_game'] = False
            user[message.from_user.id]['total_games'] += 1
            await message.answer(
                'К сожалению, у вас больше не осталось '
                'попыток. Вы проиграли :(\n\nМое число '
                f'было {user["secret_number"]}\n\nДавайте '
                'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


async def send_echo(message: Message):
    if user[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )

dp.message.register(process_start_command,Command(commands="start"))
dp.message.register(procces_help_command, Command(commands="help"))
dp.message.register(procces_help_command, Command(commands="stat"))
dp.message.register(procces_help_command, Command(commands="cancel"))
dp.message.register(send_echo)


if __name__ =='__main__':
    dp.run_polling(bot)
    print("starting bot")