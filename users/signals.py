from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

import telebot
from telebot.apihelper import ApiException

token = '6261335234:AAGKSM2l-Sc_WX22YQLzMN6fCsW_3UDr3jQ'
bot = telebot.TeleBot(token)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()

	def notify_connect(user_id):
		try:
			bot.send_message(user_id, 'Вы успешно привязали этот телеграмм к своему личному кабинету на нашем сайте!ы')
		except Exception as exc:
			print(exc)
	notify_connect(instance.profile.telegram)
