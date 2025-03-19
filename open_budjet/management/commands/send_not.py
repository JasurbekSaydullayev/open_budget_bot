from django.core.management import BaseCommand
from open_budjet.models import Customers
from django.conf import settings
from telebot import TeleBot, types

BOT_TOKEN = settings.BOT_TOKEN
bot = TeleBot(BOT_TOKEN)

class Command(BaseCommand):
    help = 'Run Telegram bot'

    def handle(self, *args, **kwargs):
        chat_ids = set(Customers.objects.values_list('chat_id', flat=True))

        for chat_id in chat_ids:
            try:
                bot.send_message(
                    chat_id,
                    "Botdagi nosozliklar tufayli ba'zi foydalanuvchilar ma'lumotlari saqlanmay qolibdi. Nosozliklar bartaraf etildi. Qayta yuborish uchun /start tugmasini bosing. Noqulayliklar uchun uzur so'raymiz",
                )
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
