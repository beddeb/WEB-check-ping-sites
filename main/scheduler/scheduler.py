from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from main.models import Sites, UserSite
from django.utils import timezone, dateformat
from django.core.mail import EmailMessage

from telebot.apihelper import ApiException
import sys
import re
import requests
import telebot

requests.packages.urllib3.disable_warnings()

token = '6261335234:AAGKSM2l-Sc_WX22YQLzMN6fCsW_3UDr3jQ'
bot = telebot.TeleBot(token)

values_number = 24


def check_site(url):
    try:
        ping = round(requests.get(url, timeout=10, verify=False).elapsed.total_seconds(), 2)
    except requests.exceptions.Timeout:
        return 9999
    except requests.exceptions.TooManyRedirects:
        return 9999
    except requests.exceptions.RequestException:
        return 9999
    print(url)
    return ping


def update_site_values():
    sites = Sites.objects.all()
    for site in sites:
        vals = site.values
        reports = site.reports
        if len(vals) < values_number:
            url_with_protocol = site.url
            url = re.sub('www\.', '', url_with_protocol)
            formatted_date = dateformat.format(timezone.now(), 'G:i')
            vals[str(formatted_date)] = check_site(url)
        else:
            vals.pop(list(vals.keys())[0])
            url_with_protocol = site.url
            url = re.sub('www\.', '', url_with_protocol)
            formatted_date = dateformat.format(timezone.now(), 'G:i')
            vals[str(formatted_date)] = check_site(url)

        if len(reports) <= len(vals):
            reports[str(formatted_date)] = 0
        site.save()


def update_user_site_values():
    sites = UserSite.objects.all()

    def send_notify(user_id, site_link):
        try:
            bot.send_message(user_id, f'Наш сайт обнаружил проблему на сайте {site_link}!\n'
                                      f'Ресурс недоступен')
        except ApiException:
            pass

    for site in sites:
        vals = site.values
        url_with_protocol = site.url
        # url = re.search(r'https?://(www.)?([A-Za-z_0-9.-]+).*', url_with_protocol).group(2)
        url = re.sub('www\.', '', url_with_protocol)
        formatted_date = dateformat.format(timezone.now(), 'G:i')
        site_check = check_site(url)
        if site_check == 9999:
            send_notify(site.owner.profile.telegram, site.url)
            EmailMessage('Оповещение о недоступности', f'Сайт {site.url} недоступен!', to=[site.owner.email]).send()
        if len(vals) < values_number:
            vals[str(formatted_date)] = site_check
        else:
            vals.pop(list(vals.keys())[0])
            vals[str(formatted_date)] = site_check
        site.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(update_site_values, 'interval', minutes=25, name='clean_accounts', jobstore='default')
    # register_events(scheduler)
    # scheduler.start()
    print("Scheduler started...", file=sys.stdout)
