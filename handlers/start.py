from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import F
from aiogram.filters import CommandStart, Command
import hashlib
from loader import router, bot
from database.db_handlers import add_user
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.keybords import *

ADMIN_ID = 5365352662

#-------------------------FOR HASH STATES -----------------------
class HashState(StatesGroup):
    hashmessage = State()

#-------------------------FOR CHAT STATES------------------------
class MSG(StatesGroup):
    messaga = State()

class Answer(StatesGroup):
    asnwer = State()

class anonimMSG(StatesGroup):
    messaga = State()

class anonimAnswer(StatesGroup):
    asnwer = State()

#---------------------------------------------------START MAIN--------------------------------------------------------------
@router.message(CommandStart()) 
async def start(msg: Message):
    full_name = msg.from_user.full_name # type: ignore
    surname = msg.from_user.last_name or '' # type: ignore
    user_id = msg.from_user.id # type: ignore


    await add_user(user_id, full_name, surname)
    if msg.from_user.id == ADMIN_ID: # type: ignore
        await msg.answer_sticker('CAACAgIAAxkBAAN_Z1vQQPl7CoeFAVCslnkycvYbDPAAAiIBAAKmREgLEfW5zI8V9GY2BA')
        await msg.answer("<b>Assalomu aleykum Xasan!</b>")
    else:
        await msg.answer_sticker('CAACAgIAAxkBAAN_Z1vQQPl7CoeFAVCslnkycvYbDPAAAiIBAAKmREgLEfW5zI8V9GY2BA')
        await msg.answer(
            f"<b>Assalomu aleykum, {msg.from_user.full_name}!</b> 😊\n" # type: ignore
            f"👨🏻‍💻 <b>Mening shaxsiy botimga xush kelibsiz!</b>\n\n"           
            f"Botimdan foydalanayotganingizdan xursandman! 😊")


        await check_subscription(msg)
        
async def check_subscription(message: Message):
    channel_ids = ["@xasansblog", "@xlifemovies"]  # Kanal username'lari yoki ID'lari
    channel_urls = {
        "@xasansblog": "https://t.me/xasansblog",
        "@xlifemovies": "https://t.me/xlifemovies"
    }
    user_id = message.from_user.id # type: ignore
    subscribed_channels = set()  

    for channel_id in channel_ids:
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status != 'left':
                subscribed_channels.add(channel_id) 
        except Exception as e:
            print(f"Kanal tekshirishda xatolik: {channel_id} - {e}")

    not_subscribed_channels = set(channel_ids) - subscribed_channels

    inline_keyboard = []

    for channel_id in not_subscribed_channels:
        inline_keyboard.append([InlineKeyboardButton(text=f"{channel_id[1:]}", url=channel_urls[channel_id])])

    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    if not_subscribed_channels:
        await message.answer(
            "Kanallarga obuna bo'lishingizni so'raymiz.\nObuna bo'lgandan so'ng /start buyrug'ini yuboring!\nIltimos, quyidagi kanallarga obuna bo'ling:👇🏻",
            reply_markup=markup
        )
    else:
        await message.answer("<b>Taklif va savollaringiz bo'lsa yozishingiz mumkin!✍🏻</b>", reply_markup=send_msg)

#--------------------------------------------------Savol yuborish--------------------------------------------------------
@router.message(F.text == "Savol yuborish✍🏻")
async def get_msg(msg: Message, state: FSMContext): # type: ignore
    await state.set_state(MSG.messaga)
    await msg.answer(f"Savollaringizni yuboring {msg.from_user.full_name}!") # type: ignore

@router.message(MSG.messaga)
async def question(msg: Message, state: FSMContext): # type: ignore
    await msg.answer("Admin tez oradi sizga javob qaytaradi!")
    text = msg.text
    user_id = msg.from_user.id # type: ignore
    user_name = msg.from_user.full_name # type: ignore
    answer_btn = InlineKeyboardButton(text='Javob qaytarish', callback_data=f'answer:{user_id}')
    answer_key = InlineKeyboardMarkup(inline_keyboard=[[answer_btn]])
    await bot.send_message(chat_id=ADMIN_ID, text=f"<b>💬Sizda yangi xabar mavjud</b>\n\n<b>Savol yuboruvchi:</b> {user_name}\n<b>Savol:</b> {text}", reply_markup=answer_key)
    await state.clear()

@router.callback_query(F.data.startswith('answer:'))
async def answeruser(call: CallbackQuery, state: FSMContext): # type: ignore
    user_id = call.data.split(':') # type: ignore
    await state.update_data(user_id = user_id[1])
    await state.set_state(Answer.asnwer)
    await bot.send_message(ADMIN_ID, text= f"ID: {user_id[1]}\nJavob yozishingiz mumkin Xasan")

@router.message(Answer.asnwer)
async def answer(msg:Message, state:FSMContext): # type: ignore
    data = await state.get_data()
    await bot.send_message(chat_id = int(data['user_id']), text=f"<b>Admindan javob:</b>\n{msg.text}\n\n<b>Savolingiz uchun rahmat!</b>")

#--------------------------------------------------Anonim Savol yuborish--------------------------------------------------------
@router.message(F.text == "Anonim savol yuborish🤫✍️")
async def get_msg(msg: Message, state: FSMContext):
    await state.set_state(anonimMSG.messaga)
    await msg.answer(f"Savollaringizni yuboring {msg.from_user.full_name}!") # type: ignore

@router.message(anonimMSG.messaga)
async def question(msg: Message, state: FSMContext):
    await msg.answer("Admin tez oradi sizga javob qaytaradi!")
    text = msg.text
    user_id = msg.from_user.id # type: ignore
    user_name = msg.from_user.full_name # type: ignore
    answer_btn = InlineKeyboardButton(text='Javob qaytarish', callback_data=f'answer:{user_id}')
    answer_key = InlineKeyboardMarkup(inline_keyboard=[[answer_btn]])
    await bot.send_message(chat_id=ADMIN_ID, text=f"<b>💬Sizda yangi xabar mavjud</b>\n\n<b>Savol</b>: {text}", reply_markup=answer_key)
    await state.clear()

@router.callback_query(F.data.startswith('answer:'))
async def answeruser(call: CallbackQuery, state: FSMContext):
    user_id = call.data.split(':') # type: ignore
    await state.update_data(user_id = user_id[1])
    await state.set_state(anonimAnswer.asnwer)
    await bot.send_message(ADMIN_ID, text= f"ID: {user_id[1]}\nJavob yozishingiz mumkin Xasan")

@router.message(anonimAnswer.asnwer)
async def answer(msg:Message, state:FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_id = int(data['user_id']), text=f"<b>Admindan javob:</b>\n{msg.text}\n\n<b>Savolingiz uchun rahmat!</b>")

#---------------------------------------------------HASHLIB ----------------------------------------------------------------
@router.message(Command('hash'))
async def hashlash(msg: Message, state: FSMContext):
    await state.set_state(HashState.hashmessage)
    await msg.answer("Hash lamoqchi bo'lgan so'zingizni yuboring!")

@router.message(HashState.hashmessage)
async def hash_msg(msg: Message, state: FSMContext):
    await state.update_data(hashmessage=msg.text)
    data = await state.get_data()
    txt_data = data.get('hashmessage')
    md5_data = hashlib.md5(str(txt_data).encode('utf-8'))
    await msg.answer(f"md5 da: \n<b>{md5_data.hexdigest()}</b>\n")
    
#------------------------------------------------ID--------------------------------------------------------
@router.message(Command('id'))
async def echo_id(msg: Message):
     await msg.answer(f"Sizning ID: <b>{msg.from_user.id}</b>") # type: ignore

#------------------------------------------------HELP------------------------------------------------------
@router.message(Command('help'))
async def help(msg: Message):
    await msg.reply("<b>Murojaat uchun @xxa571 !</b>")


#------------------------------------------------Sticker--------------------------------------------------------
@router.message(F.sticker)
async def echo_sticker(msg: Message):
    await msg.answer(f"Siz yuborgan stiker identifikatori:\n{msg.sticker.file_id}") # type: ignore

#-------------------------------------------------Photo--------------------------------------------------------
@router.message(F.photo)
async def echo_photo(msg: Message):
    photo_id = msg.photo[-1].file_id # type: ignore
    await msg.answer(f"Siz yuborgan photo identifikatori: \n{photo_id}")

#-------------------------------------------------Document--------------------------------------------------------
@router.message(F.document)
async def echo_document(msg: Message):
    document_id = msg.document.file_id # type: ignore
    await msg.answer(f"Siz yuborgan document identifikatori: \n{document_id}")

#-------------------------------------------------Video--------------------------------------------------------
@router.message(F.video)
async def echo_video(msg: Message):
    video_id = msg.video.file_id # type: ignore
    await msg.answer(f"Siz yuborgan video identifikatori: \n{video_id}")
    