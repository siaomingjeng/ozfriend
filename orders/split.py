from .models import Order, OrderItem
import re


def split_save(req, obj_id):
    '''
    Move the deleted Items into a new Order!
    New Order points to Originial Order.
    Orginial Order points to itself. None-split Order points to 0.
    '''
    res = {'status': 'success', 'msg': 'No need for split!'}

    def item_split(oi_req, oi, del_id):
        '''
        return a dict containing orderitem id, and the different between
        request and database(the amount to be moved.)
        '''
        data = {}
        for o in oi:
            if o.id not in del_id and o.quantity > int(oi_req[str(o.id)]):
                data[str(o.id)] = o.quantity - int(oi_req[str(o.id)])
        return data

    if req.POST:
        keystr = str(req.POST.keys())
        # get id of inputs, 0,1,2,...
        ids = re.findall(r'(?<=items-)\d*(?=-id)', keystr)
        # get id with DELETE selected, 0,1,2,...
        dels = re.findall(r'(?<=items-)\d*(?=-DELETE)', keystr)
        obj = Order.objects.get(id=obj_id)
        oi = OrderItem.objects.filter(order=obj)
        # split order is not allowed to split again.
        if obj.original != 0 and obj.original != obj.id:
            return {'status': 'error',
                    'msg': 'This order is not original order!'}
        # Orderitem num must be the num in database, otherwise remind to save.
        if len(ids) > 0 and len(oi) > 0 and len(ids) == len(oi):
            del_id = []  # OrderItem ids to be moved to new order.
            for d in dels:
                itemid = "items-{}-id".format(d)
                del_id.append(req.POST[itemid])
            oi_req = {}  # OrderItem id:quanitity from request.
            for i in ids:
                itemid = "items-{}-id".format(i)
                qid = "items-{}-quantity".format(i)
                oi_req[req.POST[itemid]] = req.POST[qid]
            data_split = item_split(oi_req, oi, del_id)
            if del_id or data_split:
                new_order = Order.objects.create(
                        receiver=obj.receiver, phone=obj.phone,
                        address=obj.address, message=obj.message,
                        paid=obj.paid, payer=obj.payer, original=obj.id)
            if del_id:
                for d in del_id:
                    del_item = OrderItem.objects.get(id=d)
                    del_item.order = new_order
                    del_item.save()
            if data_split:
                for id, num in data_split.items():
                    o = OrderItem.objects.get(id=id)
                    o.quantity -= num
                    o.save()
                    oo = OrderItem.objects.create(
                        order=new_order, quantity=num,
                        price_rmb=o.price_rmb, price_aud=o.price_aud,
                        expense_aud=o.expense_aud, product=o.product,
                        expense_aud_card=o.expense_aud_card,
                        expense_rmb=o.expense_rmb)
            if del_id or data_split:
                new_order.total_price_rmb = new_order.get_total_price_rmb()
                new_order.total_price_aud = new_order.get_total_price_aud()
                new_order.total_expense_rmb = new_order.get_total_expense_rmb()
                new_order.total_expense_aud = new_order.get_total_expense_aud()
                new_order.save()
                obj.total_price_rmb = obj.get_total_price_rmb()
                obj.total_price_aud = obj.get_total_price_aud()
                obj.total_expense_rmb = obj.get_total_expense_rmb()
                obj.total_expense_aud = obj.get_total_expense_aud()
                obj.original = obj.id  # this means original order.
                obj.save()
                res = {'status': 'success', 'msg': 'OrderItems have been split\
                         into Order {}'.format(new_order.id)}
        else:
            res = {'status': 'error', 'msg': 'Some items have not been saved!'}
    else:
        res = {'status': 'error', 'msg': 'POST needed!'}
    return res
