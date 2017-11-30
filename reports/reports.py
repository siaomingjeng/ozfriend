from orders.models import OrderItem, Order
from fx.models import FX
from decimal import Decimal
from pytz import timezone
import datetime as dt


class Report(object):
    def __init__(self):
        # for naive (non-timezone aware) datetime Warning
        self.tz = timezone('Australia/Sydney')

    def get_result(self, F, T):
        orders = Order.objects.filter(created__range=[
                dt.datetime(F.year, F.month, F.day, F.hour, F.minute,
                            tzinfo=self.tz),
                dt.datetime(T.year, T.month, T.day, T.hour, T.minute,
                            tzinfo=self.tz)],
                paid=True)
        # items = OrderItem.objects.filter(order__in=orders)
        res = {'expense_aud_cn': 0, 'expense_aud_oz': 0, 'price_rmb': 0,
               'item_num': 0, 'expense_rmb': 0, 'price_aud': 0,
               'price_aud_order': 0, 'expense_rmb_order': 0,
               'order_num': len(orders), 'price_rmb_order': 0,
               'expense_aud_order': 0, 'error': [], 'warn': [],
               'lost': []}
        res['fx'] = self.get_fx(F, T)
        res['end'] = T
        res['begin'] = F
        for order in orders:
            res['item_num'] += 1
            op = {'expense_aud_cn': 0, 'expense_aud_oz': 0, 'price_rmb': 0,
                  'item_num': 0, 'expense_rmb': 0, 'price_aud': 0,
                  'expense_aud': 0, 'warn': []}
            for i in OrderItem.objects.filter(order=order):
                op['price_rmb'] += i.quantity*i.price_rmb
                op['price_aud'] += i.quantity*i.price_aud
                op['expense_rmb'] += i.quantity*i.expense_rmb
                if i.expense_aud_card == 'CN':
                    op['expense_aud_cn'] += i.quantity*i.expense_aud
                if i.expense_aud_card == 'OZ':
                    op['expense_aud_oz'] += i.quantity*i.expense_aud
                # delivery fee and discount are not counted into quanity.
                if i.product_id not in [1, 2]:
                    op['item_num'] += i.quantity
                    if (i.price_rmb * i.price_aud != 0 or
                            i.expense_rmb * i.expense_aud != 0):
                        op['warn'].append("{0}:{1}".format(order.id, i.id))
            op['expense_aud'] = op['expense_aud_cn'] + op['expense_aud_oz']
            res['expense_aud_cn'] += op['expense_aud_cn']
            res['expense_aud_oz'] += op['expense_aud_oz']
            res['expense_aud_order'] += order.total_expense_aud
            res['price_rmb'] += op['price_rmb']
            res['price_rmb_order'] += order.total_price_rmb
            res['price_aud'] += op['price_aud']
            res['price_aud_order'] += order.total_price_aud
            res['expense_rmb'] += op['expense_rmb']
            res['expense_rmb_order'] += order.total_expense_rmb
            res['item_num'] += op['item_num']
            # check value parity
            if (order.total_price_rmb != op['price_rmb'] or
                    order.total_expense_aud != op['expense_aud'] or
                    order.total_price_aud != op['price_aud'] or
                    order.total_expense_rmb != op['expense_rmb']):
                res['error'].append(order.id)
            if ((op['price_rmb']/res['fx']['fx']+op['price_aud']) <
                    (op['expense_rmb']/res['fx']['fx']+op['expense_aud'])):
                res['lost'].append(order.id)
            if (op['warn']):  # check aud and rmb, not happen at the same time!
                res['warn'] += op['warn']
        res['net_income_aud'] = round(
                res['price_aud_order'] +
                res['price_rmb_order']/res['fx']['fx'] -
                res['expense_aud_order'] -
                res['expense_rmb_order']/res['fx']['fx'], 2)
        res['parity'] = False if res['error'] else True
        return res

    def get_this_year(self, date_from=0, date_to=0):
        if date_from and date_to:
            begin = dt.datetime(date_from.year, date_from.month, date_from.day,
                                0, 0, 0)
            if date_to >= dt.datetime.now().date():
                t = dt.datetime.now()
                end = dt.datetime(t.year, t.month, t.day, t.hour, t.minute)
            else:
                end = dt.datetime(date_to.year, date_to.month, date_to.day,
                                  23, 59, 59)
        else:
            t = dt.datetime.now()
            end = dt.datetime(t.year, t.month, t.day, t.hour, t.minute)
            begin = dt.datetime(t.year, 1, 1, 0, 0, 0)
        return self.get_result(begin, end)

    def get_this_month(self, date_from=0, date_to=0):
        if date_from and date_to:
            begin = dt.datetime(date_from.year, date_from.month, date_from.day,
                                0, 0, 0)
            if date_to >= dt.datetime.now().date():
                t = dt.datetime.now()
                end = dt.datetime(t.year, t.month, t.day, t.hour, t.minute)
            else:
                end = dt.datetime(date_to.year, date_to.month, date_to.day,
                                  23, 59, 59)
        else:
            t = dt.datetime.now()
            end = dt.datetime(t.year, t.month, t.day, t.hour, t.minute)
            begin = dt.datetime(t.year, t.month, 1, 0, 0, 0)
        return self.get_result(begin, end)

    def get_payers(self, F, T, Value=0):
        orders = Order.objects.filter(created__range=[
            dt.datetime(F.year, F.month, F.day, F.hour, F.minute,
                        tzinfo=self.tz),
            dt.datetime(T.year, T.month, T.day, T.hour, T.minute,
                        tzinfo=self.tz)],
            paid=True)
        res = {'payer_list': {}, 'end': T, 'begin': F}
        fx = self.get_fx(F, T)
        for i in orders:
            if i.payer in res['payer_list'].keys():
                res['payer_list'][i.payer]['expense'] += round(
                        i.total_expense_aud + i.total_expense_rmb/fx['fx'], 2)
                res['payer_list'][i.payer]['price'] += round(
                        i.total_price_rmb/fx['fx'] + i.total_price_aud, 2)
                res['payer_list'][i.payer]['order_num'] += 1
            else:
                res['payer_list'][i.payer] = {
                    'expense': round(i.total_expense_aud +
                                     i.total_expense_rmb/fx['fx'], 2),
                    'price': round(i.total_price_rmb/fx['fx'] +
                                   i.total_price_aud, 2),
                    'order_num': 1, 'item_num': 0}
            items = OrderItem.objects.filter(order=i)
            for item in items:
                if item.product_id not in [1, 2] and item.price_rmb >= Value:
                    res['payer_list'][i.payer]['item_num'] += item.quantity
        for i in res['payer_list'].keys():
            res['payer_list'][i]['profit'] = round(
                    res['payer_list'][i]['price'] -
                    res['payer_list'][i]['expense'], 2)
        #  descending order
        res['payer_list'] = sorted(res['payer_list'].items(),
                                   key=lambda item: item[1]['profit'],
                                   reverse=True)
        return res

    def get_payers_year(self, date_from=0, date_to=0, over=0):
        if date_from and date_to:
            begin = dt.datetime(date_from.year, date_from.month, date_from.day,
                                0, 0, 0)
            if date_to >= dt.datetime.now().date():
                t = dt.datetime.now()
                end = dt.datetime(t.year, t.month, t.day, t.hour, t.minute)
            else:
                end = dt.datetime(date_to.year, date_to.month, date_to.day,
                                  23, 59, 59)
        else:
            t = dt.datetime.now()
            end = dt.datetime(t.year, t.month, t.day, t.hour, t.minute)
            begin = dt.datetime(t.year, 1, 1, 0, 0, 0)
        return self.get_payers(begin, end, over)

    def get_fx(self, F, T):
        fx = FX.objects.filter(date__range=[
                dt.datetime(F.year, F.month, F.day, F.hour, F.minute,
                            tzinfo=self.tz),
                dt.datetime(T.year, T.month, T.day, T.hour, T.minute,
                            tzinfo=self.tz)])
        res_fx = {'aud_cn': 0, 'rmb': 0, 'fx': 0, 'num': 0}
        if fx:
            for f in fx:
                res_fx['aud_cn'] += f.aud
                res_fx['rmb'] += f.rmb
                res_fx['num'] += 1
            res_fx['fx'] += round(res_fx['rmb']/res_fx['aud_cn'], 2)
            return res_fx
        else:
            return {'aud_cn': 0, 'rmb': 0, 'fx': Decimal(5.3)}

    def get_capital_year(self, date_from=0, date_to=0):
        if date_from and date_to:
            begin = dt.datetime(date_from.year, date_from.month, date_from.day,
                                0, 0, 0)
            if date_to >= dt.datetime.now().date():
                t = dt.datetime.now()
                end = dt.datetime(t.year, t.month, t.day, t.hour, t.minute)
            else:
                end = dt.datetime(date_to.year, date_to.month, date_to.day,
                                  23, 59, 59)
        else:
            t = dt.datetime.now()
            end = dt.datetime(t.year, t.month, t.day, t.hour, t.minute)
            begin = dt.datetime(t.year, 1, 1, 0, 0, 0)

        res = self.get_result(begin, end)
        res['summary'] = {  # AUD in Australia, AUD in China, RMB in China.
            'expense_aud_oz': res['price_aud']-res['expense_aud_oz'],
            'expense_aud_cn': res['fx']['aud_cn']-res['expense_aud_cn'],
            'price_rmb_cn':
                res['price_rmb']-res['expense_rmb']-res['fx']['rmb']}
        res['summary']['price_rmb_to_aud'] = round(
                res['summary']['price_rmb_cn']/res['fx']['fx'], 2)
        return res


def YMD():
    def get_days_of_month(Y, M):
        D = [31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if M == 2:
            return 27 if Y % 4 else 28
        else:
            return D[M]
    now = dt.datetime.now()
    dy = now.year-2016
    dm = now.month-3
    dd = now.day-25
    if dd < 0:
        dm -= 1
        dd += get_days_of_month(now.year, now.month)
    if dm < 0:
        dy -= 1
        dm += 12
    days = (now-dt.datetime(2016, 3, 25)).days
    return (dy, dm, dd, days)
