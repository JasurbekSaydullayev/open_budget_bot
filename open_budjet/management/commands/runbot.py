import os
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot, types
from telebot.handler_backends import State, StatesGroup
from telebot.storage.memory_storage import StateMemoryStorage
from telebot.custom_filters import StateFilter
from open_budjet.models import Customers

# Bot sozlamalari
BOT_TOKEN = settings.BOT_TOKEN
state_storage = StateMemoryStorage()
bot = TeleBot(BOT_TOKEN, state_storage=state_storage)
bot.add_custom_filter(StateFilter(bot))  # StateFilterni ro'yxatdan o'tkazish


# State-lar
class UserStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_photo = State()
    waiting_for_card = State()


def create_application(chat_id, phone_number, username):
    application_number = str(random.randint(10000000, 99999999))
    Customers.objects.create(
        phone_number=phone_number,
        username=username,
        chat_id=chat_id,
        status='waiting_for_photo',
        application_number=application_number
    )
    return application_number


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "Assalomu alaykum! Iltimos, telefon raqamingizni 901234657 formatda yuboring yoki kontakt jo‘nating.",
        reply_markup=get_phone_keyboard()
    )
    bot.set_state(message.chat.id, UserStates.waiting_for_phone)


def get_phone_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("\ud83d\udcde Telefon raqamni yuborish", request_contact=True))
    return keyboard


@bot.message_handler(state=UserStates.waiting_for_phone, content_types=['contact', 'text'])
def handle_contact_or_phone(message):
    chat_id = message.chat.id
    username = message.chat.username or message.chat.first_name

    if message.content_type == 'contact':
        phone_number = message.contact.phone_number
    elif message.text.isdigit() and 9 <= len(message.text) <= 15:
        phone_number = message.text
    else:
        bot.send_message(chat_id, "❌ Iltimos, to‘g‘ri telefon raqamini kiriting yoki kontakt jo‘nating.")
        return

    create_application(chat_id, phone_number, username)
    bot.send_message(chat_id, "✅ Telefon raqam qabul qilindi. Endi iltimos, screenshotni yuboring.")
    bot.set_state(chat_id, UserStates.waiting_for_photo)


@bot.message_handler(state=UserStates.waiting_for_photo, content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    customer = Customers.objects.filter(chat_id=chat_id, status='waiting_for_photo').first()
    if not customer:
        bot.send_message(chat_id, "Iltimos, avval telefon raqamingizni yuboring.")
        return

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = f"{chat_id}_{customer.application_number}_photo.jpg"
    image_path = os.path.join(settings.MEDIA_ROOT, filename)

    with open(image_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    customer.image = filename
    customer.status = 'waiting_for_card'
    customer.save()

    bot.send_message(chat_id, "✅ Rasm qabul qilindi. Endi iltimos, karta raqamingizni yuboring (16 ta raqam).")
    bot.set_state(chat_id, UserStates.waiting_for_card)


@bot.message_handler(state=UserStates.waiting_for_card, content_types=['text'])
def handle_card(message):
    chat_id = message.chat.id
    customer = Customers.objects.filter(chat_id=chat_id, status='waiting_for_card').first()
    if not customer:
        bot.send_message(chat_id, "Iltimos, avval telefon raqam va rasm yuboring.")
        return

    if len(message.text) == 16 and message.text.isdigit():
        customer.card_number = message.text
        customer.status = 'new'
        customer.save()

        bot.send_message(chat_id, "✅ Ma'lumotlaringiz qabul qilindi! Tasdiqlanishi bilan kartangizga pul o'tkazamiz.")
        bot.delete_state(chat_id)
    else:
        bot.send_message(chat_id, "❌ Iltimos, 16 ta raqamdan iborat to‘g‘ri karta raqamini yuboring.")


class Command(BaseCommand):
    help = 'Run Telegram bot'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Bot ishga tushdi...'))
        while True:
            try:
                bot.polling(none_stop=True, skip_pending=True, timeout=10, long_polling_timeout=5)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Xatolik: {e}'))
