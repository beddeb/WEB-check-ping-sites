from django import template

register = template.Library()

@register.filter(name='dict_range')
def filter_dict_range(a, stroke):
    return range(a ,len(stroke.values.values()))

@register.filter(name='get_key')
def filter_get_key(dictionary, i):
    return list(dictionary.values.keys())[i]

@register.filter(name='get_value')
def filter_get_value(dictionary, i):
    return (list(dictionary.values.values())[i],list(dictionary.reports.values())[i])

@register.filter(name='user_get_value')
def filter_user_get_value(dictionary, i):
    return (list(dictionary.values.values())[i])

@register.filter(name='multiply')
def filter_multiply(number, n):
    return number*n

@register.filter(name='mean')
def mean(array):
    rates = []
    print(array)
    for i in array.values():
        rates.append(i['rate'])
    return round(sum(rates)/len(rates), 2)

@register.filter(name='mean_sites')
def mean_sites(array):
    vals = list(map(int,list(array.values())))
    if len(vals) > 0:
        return round(sum(vals)/len(vals), 2)
    else:
        return 0