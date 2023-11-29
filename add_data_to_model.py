from main.models import Sites
from django.core.files import File
import json 


with open('sites.json', encoding='utf-8') as f:
    vuzs_json = json.load(f)

num = len(vuzs_json)
for vuz in vuzs_json:
    num -= 1
    print(vuz)
    if num >= 0:
        site = Sites(name=vuz, url=vuzs_json[vuz]['site'], reports={'0': '0'})
        site.save()
        site.siteprofile.image.save(f'{vuz}.png', File(open(vuzs_json[vuz]['logo_file'], 'rb')))
        print(vuz, vuzs_json[vuz])
