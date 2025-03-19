from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import telebot
from .models import Customers

BOT_TOKEN = settings.BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'username', 'phone_number', 'image', 'card_number', 'status', 'application_number')
    list_filter = ('status',)
    search_fields = ('username', 'phone_number', 'card_number', 'application_number')
    list_editable = ('status',)

    def save_model(self, request, obj, form, change):
        if change:
            try:
                old_obj = Customers.objects.get(pk=obj.pk)
                if old_obj.status != obj.status:
                    if obj.status == 'accepted':
                        self.notify_user_accept(obj)
                    elif obj.status == 'rejected':
                        self.notify_user_rejected(obj)
            except ObjectDoesNotExist:
                pass
        super().save_model(request, obj, form, change)

    def notify_user_rejected(self, customer):
        if customer.chat_id:
            try:
                bot.send_message(customer.chat_id,
                                 f"❌ Sizning yuborgan ma'lumotlaringiz tasdiqlanmadi. Shu sababli rad etildi")
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")

    def notify_user_accept(self, customer):
        if customer.chat_id:
            try:
                bot.send_message(customer.chat_id,
                                 f"✅ Sizning ma'lumotlaringiz tasdiqlandi va kartangiz pul mablag'lari o'tkazib berildi")
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
