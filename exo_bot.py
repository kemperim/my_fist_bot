from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command


BOT_TOKEN = ''
bot = Bot(token =BOT_TOKEN)
dp = Dispatcher()

print("starting bot")

async def process_start_command(message: Message):
    print(f"Пользователь {message.from_user.full_name}   user info {message.from_user.id}  ")
    await message.answer('Привет! ')

async def procces_help_command(message: Message):
    await message.answer(
        'Напиши мне что нибуть и в ответ'
        ' я пришлю тебе твое сообщение'
    )
@dp.message(F.photo)
async def send_photo_echo(message:Message):
    await message.answer_photo(message.photo[0].file_id)

async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id = message.chat.id)
    except TypeError: 
        await message.reply(text='Данный тип апдейтов не поддерживается методом send_copy')
        

dp.message.register(process_start_command,Command(commands="start"))
dp.message.register(procces_help_command, Command(commands="help"))

dp.message.register(send_echo)


if __name__ =='__main__':
    dp.run_polling(bot)
    print("starting bot")