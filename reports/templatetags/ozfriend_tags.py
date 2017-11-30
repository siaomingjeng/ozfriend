from django import template
from decimal import Decimal
register = template.Library()


@register.filter
def xmean(value):
    l = list(str(value))
    tail = sum(int(i) for i in l)//len(l)
    l.append(str(tail))
    if len(l) < 6:
        l.insert(0, '0'*(6-len(l)))
    return "".join(l)


@register.filter
def add_minus(value):
    return float(value) * -1


@register.filter
def show_aud(value):
    if isinstance(value, (Decimal, float, int)):
        return "-$%.2f" % (-1*value) if value < 0 else "$%.2f" % value


@register.filter
def show_rmb(value):
    if isinstance(value, (Decimal, float, int)):
        return "-￥%.2f" % (-1*value) if value < 0 else "￥%.2f" % value


@register.filter
def rmb2aud(value, fx):
    if isinstance(value, (Decimal, float, int)) and fx != 0:
        return round(value/fx, 2)
