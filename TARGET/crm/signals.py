from django.db.models import Q, Sum
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from TARGET.crm.models import *

from .middlewares import RequestMiddleware

@receiver(post_save, sender=AccountingChild)
def post_save_accountingchild(sender, instance, created, **kwargs):
    if created:
        AccountingParent.objects.get(id=instance.parent).accounting_child.add(instance.pk)

@receiver(post_save, sender=PurchaseProduct)
def post_save_purchaseproduct(sender, instance, created, **kwargs):
    if created:
        warehouseid = PurchaseOrder.objects.get(pk=instance.purchaseorder_id)
        warehouses = Warehouse.objects.get(pk=warehouseid.warehouse_id)
        vendors = Vendor.objects.get(pk=warehouseid.vendor_id)
        products = Product.objects.get(pk=instance.product_id)
        if instance.uom_id == 2:
            if products.unit_2 > 0 and products.unit_2 is not None:
                pcsqty = instance.qty * products.unit_2
                crtqty = instance.qty
            else:
                pcsqty = instance.qty
                crtqty = instance.qty
        elif instance.uom_id == 1 and products.unit_2 > 0:
            crtqty = round(instance.qty / products.unit_2, 1)
            pcsqty = instance.qty
        else:
            pcsqty = instance.qty
            crtqty = instance.qty

        Transactions.objects.create(source='PurchaseOrder',source_id=instance.purchaseorder_id,product=instance.product
                                    ,vendor_id=warehouseid.vendor_id,qty=pcsqty,price=instance.price,total=instance.subtotal,warehouse_id=warehouseid.warehouse_id, country_id=warehouses.country_id,
                                    area_id=warehouses.area_id, city_id=warehouses.city_id, category_id=products.category_id, ctrqty = crtqty)

@receiver(post_save, sender=PurchaseReturnProduct)
def post_save_purchasereturnproduct(sender, instance, created, **kwargs):
    if created:
        warehouseid = PurchaseReturnOrder.objects.get(pk=instance.purchaseorder_id)
        vendors = Vendor.objects.get(pk=warehouseid.vendor_id)
        warehouses = Warehouse.objects.get(pk=warehouseid.warehouse_id)
        products = Product.objects.get(pk=instance.product_id)
        if instance.uom_id == 2:
            if products.unit_2 > 0 and products.unit_2 is not None:
                pcsqty = instance.qty * products.unit_2
                crtqty = instance.qty
            else:
                pcsqty = instance.qty
                crtqty = instance.qty
        elif instance.uom_id == 1 and products.unit_2 > 0:
            crtqty = round(instance.qty / products.unit_2, 1)
            pcsqty = instance.qty
        else:
            pcsqty = instance.qty
            crtqty = instance.qty

        Transactions.objects.create(source='PurchaseReturnOrder',source_id=instance.purchaseorder_id,product=instance.product
                                    ,vendor_id=warehouseid.vendor_id,qty=-pcsqty,price=-instance.price,total=-instance.subtotal,warehouse_id=warehouseid.warehouse_id, country_id=warehouses.country_id,
                                    area_id=warehouses.area_id, city_id=warehouses.city_id, category_id=products.category_id, ctrqty = -crtqty)

@receiver(post_save, sender=SalesProduct)
def post_save_salesproduct(sender, instance, created, **kwargs):
    companies = Company.objects.all().values('sales_auto', 'sales_prefix')
    if companies[0]['sales_auto'] is True:
        Sales_Auto = 1
    else:
        Sales_Auto = 0
    if created:
        try:
            acutalvisits = ActualVisit.objects.get(conv_salesorder_id=999999999)
            acutalvisits.conv_salesorder_id = instance.salesorder_id
            acutalvisits.save()
        except:
            pass

        warehouseid = SalesOrder.objects.get(pk=instance.salesorder_id)
        warehouseid.salesorder_number = companies[0]['sales_prefix'] + str(instance.salesorder_id)
        if Sales_Auto == 1:
            warehouseid.status = 2
            warehouseid.save()
        else:
            warehouseid.status = 1
            warehouseid.save()
        if warehouseid.status == 2:
            customers = Customer.objects.get(pk=warehouseid.customer_id)
            products= Product.objects.get(pk=instance.product_id)
            if instance.uom_id == 2 :
                if products.unit_2 > 0 and products.unit_2 is not None:
                    pcsqty = instance.qty * products.unit_2
                    crtqty = instance.qty
                else:
                    pcsqty = instance.qty
                    crtqty = instance.qty
            elif instance.uom_id == 1 and products.unit_2 > 0:
                crtqty = round(instance.qty / products.unit_2,1)
                pcsqty = instance.qty
            else:
                pcsqty = instance.qty
                crtqty = instance.qty

            Transactions.objects.create(source='SalesOrder',source_id=instance.salesorder_id,product=instance.product
                                        ,qty=pcsqty,price=instance.price,total=instance.subtotal,warehouse_id=warehouseid.warehouse_id,
                                        customer_id=warehouseid.customer_id, customer_size=customers.customer_size, country_id=customers.country_id,
                                        area_id=customers.area_id, city_id=customers.city_id, salesman_id=warehouseid.salesman_id, category_id=products.category_id,
                                        channel_id=customers.channel_id, account_id=customers.account_id, ctrqty = crtqty, tax=instance.tax)

            request = RequestMiddleware(get_response=None)
            request = request.thread_local.current_request
            from_user = User.objects.get(id=request.user.id)
            salesman = Salesman.objects.filter(pk=warehouseid.salesman_id).values()
            if request.user.is_superuser:
                to_user = User.objects.get(id=salesman[0]['user_id'])
                Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
                                            message="You have new sales order", from_user=from_user,
                                            to_user=to_user, read=False, url='crm:edit_salesorder')
            else:
                if salesman[0]['reporting_to_id'] == request.user.id:
                    to_user = User.objects.get(id=salesman[0]['user_id'])
                    admin = User.objects.get(id=1)
                    Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
                                                message="You have new sales order", from_user=from_user,
                                                to_user=admin, read=False, url='crm:edit_salesorder')
                    Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
                                                message="You have new sales order", from_user=from_user,
                                                to_user=to_user, read=False, url='crm:edit_salesorder')

                elif salesman[0]['user_id'] == request.user.id:
                    to_user = User.objects.get(id=salesman[0]['reporting_to_id'])
                    Notification.objects.create(source='SalesOrder',source_id=instance.salesorder_id ,
                                                message="You have new sales order", from_user=from_user,
                                                to_user=to_user, read=False, url='crm:edit_salesorder')


            qcollection= Collection.objects.filter(salesorder=warehouseid.pk)
            if qcollection.count() == 0:
                if warehouseid.payment_terms == 1:
                    Collection.objects.create(customer_id=warehouseid.customer_id, salesorder=warehouseid.pk, amount= warehouseid.total , description= 'auto created from Sales Order #'+ str(warehouseid.pk) )
    else:
        warehouseid = SalesOrder.objects.get(pk=instance.salesorder_id)
        if warehouseid.status == 2  and Sales_Auto == 0:
            customers = Customer.objects.get(pk=warehouseid.customer_id)
            products= Product.objects.get(pk=instance.product_id)
            if instance.uom_id == 2 :
                if products.unit_2 > 0 and products.unit_2 is not None:
                    pcsqty = instance.qty * products.unit_2
                    crtqty = instance.qty
                else:
                    pcsqty = instance.qty
                    crtqty = instance.qty
            elif instance.uom_id == 1 and products.unit_2 > 0:
                crtqty = round(instance.qty / products.unit_2,1)
                pcsqty = instance.qty
            else:
                pcsqty = instance.qty
                crtqty = instance.qty

            Transactions.objects.create(source='SalesOrder',source_id=instance.salesorder_id,product=instance.product
                                        ,qty=pcsqty,price=instance.price,total=instance.subtotal,warehouse_id=warehouseid.warehouse_id,
                                        customer_id=warehouseid.customer_id, customer_size=customers.customer_size, country_id=customers.country_id,
                                        area_id=customers.area_id, city_id=customers.city_id, salesman_id=warehouseid.salesman_id, category_id=products.category_id,
                                        channel_id=customers.channel_id, account_id=customers.account_id, ctrqty = crtqty, tax=instance.tax)

            request = RequestMiddleware(get_response=None)
            request = request.thread_local.current_request
            from_user = User.objects.get(id=request.user.id)
            salesman = Salesman.objects.filter(pk=warehouseid.salesman_id).values()
            if request.user.is_superuser:
                to_user = User.objects.get(id=salesman[0]['user_id'])
                Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
                                            message="You have new sales order", from_user=from_user,
                                            to_user=to_user, read=False, url='crm:edit_salesorder')
            else:
                if salesman[0]['reporting_to_id'] == request.user.id:
                    to_user = User.objects.get(id=salesman[0]['user_id'])
                    admin = User.objects.get(id=1)
                    Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
                                                message="You have new sales order", from_user=from_user,
                                                to_user=admin, read=False, url='crm:edit_salesorder')
                    Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
                                                message="You have new sales order", from_user=from_user,
                                                to_user=to_user, read=False, url='crm:edit_salesorder')

                elif salesman[0]['user_id'] == request.user.id:
                    to_user = User.objects.get(id=salesman[0]['reporting_to_id'])
                    Notification.objects.create(source='SalesOrder',source_id=instance.salesorder_id ,
                                                message="You have new sales order", from_user=from_user,
                                                to_user=to_user, read=False, url='crm:edit_salesorder')


            qcollection= Collection.objects.filter(salesorder=warehouseid.pk)
            if qcollection.count() == 0:
                if warehouseid.payment_terms == 1:
                    Collection.objects.create(customer_id=warehouseid.customer_id, salesorder=warehouseid.pk, amount= warehouseid.total , description= 'auto created from Sales Order #'+ str(warehouseid.pk) )

# @receiver(post_save, sender=ActualVisitProduct)
# def post_save_actualvisitproduct(sender, instance, created, **kwargs):
#     companies = Company.objects.all().values('sales_auto', 'sales_prefix')
#     try:
#         maxpoid = int(SalesOrder.objects.latest('pk').pk) + 1
#     except:
#         maxpoid = 1
#     if companies[0]['sales_prefix'] is True:
#         sales_no = companies[0]['sales_prefix'] + str(maxpoid)
#     else:
#         sales_no = 'SO-' + str(maxpoid)
#     if companies[0]['sales_auto'] is True:
#         Sales_Auto = 1
#     else:
#         Sales_Auto = 0
#     if created:
#         actualvisits = ActualVisit.objects.get(pk=instance.actualvisit)
#         if Sales_Auto == 1:
#             sales_status = 2
#         else:
#             sales_status = 1
#         SalesOrder.objects.create(salesorder_number=2, subject='', duedate='', customer=actualvisits.customer_id, salesman=actualvisits.salesman_id,
#                                   warehouse='', payment_terms=2, payment_days=2, total=actualvisits.amount, so_tax=actualvisits.so_tax,
#                                   tax_number=actualvisits.tax_number, subtotal=actualvisits.subtotal, paid=1, status=sales_status)
#
#
#         if sales_status == 2:
#             customers = Customer.objects.get(pk=actualvisits.customer_id)
#             products= Product.objects.get(pk=instance.product_id)
#             if instance.uom_id == 2 :
#                 if products.unit_2 > 0 and products.unit_2 is not None:
#                     pcsqty = instance.qty * products.unit_2
#                     crtqty = instance.qty
#                 else:
#                     pcsqty = instance.qty
#                     crtqty = instance.qty
#             elif instance.uom_id == 1 and products.unit_2 > 0:
#                 crtqty = round(instance.qty / products.unit_2,1)
#                 pcsqty = instance.qty
#             else:
#                 pcsqty = instance.qty
#                 crtqty = instance.qty
#
#             Transactions.objects.create(source='SalesOrder',source_id=instance.salesorder_id,product=instance.product
#                                         ,qty=pcsqty,price=instance.price,total=instance.subtotal,warehouse_id=actualvisits.warehouse_id,
#                                         customer_id=actualvisits.customer_id, customer_size=customers.customer_size, country_id=customers.country_id,
#                                         area_id=customers.area_id, city_id=customers.city_id, salesman_id=actualvisits.salesman_id, category_id=products.category_id,
#                                         channel_id=customers.channel_id, account_id=customers.account_id, ctrqty = crtqty, tax=instance.tax)
#
#             request = RequestMiddleware(get_response=None)
#             request = request.thread_local.current_request
#             from_user = User.objects.get(id=request.user.id)
#             salesman = Salesman.objects.filter(pk=actualvisits.salesman_id).values()
#             if request.user.is_superuser:
#                 to_user = User.objects.get(id=salesman[0]['user_id'])
#                 Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
#                                             message="You have new sales order", from_user=from_user,
#                                             to_user=to_user, read=False, url='crm:edit_salesorder')
#             else:
#                 if salesman[0]['reporting_to_id'] == request.user.id:
#                     to_user = User.objects.get(id=salesman[0]['user_id'])
#                     admin = User.objects.get(id=1)
#                     Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
#                                                 message="You have new sales order", from_user=from_user,
#                                                 to_user=admin, read=False, url='crm:edit_salesorder')
#                     Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
#                                                 message="You have new sales order", from_user=from_user,
#                                                 to_user=to_user, read=False, url='crm:edit_salesorder')
#
#                 elif salesman[0]['user_id'] == request.user.id:
#                     to_user = User.objects.get(id=salesman[0]['reporting_to_id'])
#                     Notification.objects.create(source='SalesOrder',source_id=instance.salesorder_id ,
#                                                 message="You have new sales order", from_user=from_user,
#                                                 to_user=to_user, read=False, url='crm:edit_salesorder')
#
#
#             qcollection= Collection.objects.filter(salesorder=actualvisits.pk)
#             if qcollection.count() == 0:
#                 if warehouseid.payment_terms == 1:
#                     Collection.objects.create(customer_id=actualvisits.customer_id, salesorder=warehouseid.pk, amount= warehouseid.total , description= 'auto created from Sales Order #'+ str(warehouseid.pk) )
#     else:
#         warehouseid = SalesOrder.objects.get(pk=instance.salesorder_id)
#         if warehouseid.status == 2  and Sales_Auto == 0:
#             customers = Customer.objects.get(pk=warehouseid.customer_id)
#             products= Product.objects.get(pk=instance.product_id)
#             if instance.uom_id == 2 :
#                 if products.unit_2 > 0 and products.unit_2 is not None:
#                     pcsqty = instance.qty * products.unit_2
#                     crtqty = instance.qty
#                 else:
#                     pcsqty = instance.qty
#                     crtqty = instance.qty
#             elif instance.uom_id == 1 and products.unit_2 > 0:
#                 crtqty = round(instance.qty / products.unit_2,1)
#                 pcsqty = instance.qty
#             else:
#                 pcsqty = instance.qty
#                 crtqty = instance.qty
#
#             Transactions.objects.create(source='SalesOrder',source_id=instance.salesorder_id,product=instance.product
#                                         ,qty=pcsqty,price=instance.price,total=instance.subtotal,warehouse_id=warehouseid.warehouse_id,
#                                         customer_id=warehouseid.customer_id, customer_size=customers.customer_size, country_id=customers.country_id,
#                                         area_id=customers.area_id, city_id=customers.city_id, salesman_id=warehouseid.salesman_id, category_id=products.category_id,
#                                         channel_id=customers.channel_id, account_id=customers.account_id, ctrqty = crtqty, tax=instance.tax)
#
#             request = RequestMiddleware(get_response=None)
#             request = request.thread_local.current_request
#             from_user = User.objects.get(id=request.user.id)
#             salesman = Salesman.objects.filter(pk=warehouseid.salesman_id).values()
#             if request.user.is_superuser:
#                 to_user = User.objects.get(id=salesman[0]['user_id'])
#                 Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
#                                             message="You have new sales order", from_user=from_user,
#                                             to_user=to_user, read=False, url='crm:edit_salesorder')
#             else:
#                 if salesman[0]['reporting_to_id'] == request.user.id:
#                     to_user = User.objects.get(id=salesman[0]['user_id'])
#                     admin = User.objects.get(id=1)
#                     Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
#                                                 message="You have new sales order", from_user=from_user,
#                                                 to_user=admin, read=False, url='crm:edit_salesorder')
#                     Notification.objects.create(source='SalesOrder', source_id=instance.salesorder_id,
#                                                 message="You have new sales order", from_user=from_user,
#                                                 to_user=to_user, read=False, url='crm:edit_salesorder')
#
#                 elif salesman[0]['user_id'] == request.user.id:
#                     to_user = User.objects.get(id=salesman[0]['reporting_to_id'])
#                     Notification.objects.create(source='SalesOrder',source_id=instance.salesorder_id ,
#                                                 message="You have new sales order", from_user=from_user,
#                                                 to_user=to_user, read=False, url='crm:edit_salesorder')
#
#
#             qcollection= Collection.objects.filter(salesorder=warehouseid.pk)
#             if qcollection.count() == 0:
#                 if warehouseid.payment_terms == 1:
#                     Collection.objects.create(customer_id=warehouseid.customer_id, salesorder=warehouseid.pk, amount= warehouseid.total , description= 'auto created from Sales Order #'+ str(warehouseid.pk) )

@receiver(post_save, sender=SalesReturnProduct)
def post_save_salesreturnproduct(sender, instance, created, **kwargs):
    if created:
        products= Product.objects.get(pk=instance.product_id)
        if instance.uom_id == 2 :
            if products.unit_2 > 0 and products.unit_2 is not None:
                pcsqty = instance.qty * products.unit_2
                crtqty = instance.qty
            else:
                pcsqty = instance.qty
                crtqty = instance.qty
        elif instance.uom_id == 1 and products.unit_2 > 0:
            crtqty = round(instance.qty / products.unit_2,1)
            pcsqty = instance.qty
        else:
            pcsqty = instance.qty
            crtqty = instance.qty

        warehouseid = SalesReturnOrder.objects.get(pk=instance.salesorder_id)
        customers = Customer.objects.get(pk=warehouseid.customer_id)
        products= Product.objects.get(pk=instance.product_id)
        Transactions.objects.create(source='SalesReturnOrder',source_id=instance.salesorder_id,product=instance.product
                                    ,qty=-pcsqty,price=-instance.price,total=-instance.subtotal,warehouse_id=warehouseid.warehouse_id,
                                    customer_id=warehouseid.customer_id, customer_size=customers.customer_size, country_id=customers.country_id,
                                    area_id=customers.area_id, city_id=customers.city_id, salesman_id=warehouseid.salesman_id, category_id=products.category_id,
                                    channel_id=customers.channel_id, account_id=customers.account_id, ctrqty = -crtqty, tax=instance.tax)

        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        from_user = User.objects.get(id=request.user.id)
        salesman = Salesman.objects.filter(pk=warehouseid.salesman_id).values()
        if request.user.is_superuser:
            to_user = User.objects.get(id=salesman[0]['user_id'])
            Notification.objects.create(source='SalesReturnOrder', source_id=instance.salesorder_id,
                                        message="You have new sales return order", from_user=from_user,
                                        to_user=to_user, read=False, url='crm:edit_salesreturnorder')
        else:
            if salesman[0]['reporting_to_id'] == request.user.id:
                to_user = User.objects.get(id=salesman[0]['user_id'])
                admin = User.objects.get(id=1)
                Notification.objects.create(source='SalesReturnOrder', source_id=instance.salesorder_id,
                                            message="You have new sales return order", from_user=from_user,
                                            to_user=admin, read=False, url='crm:edit_salesreturnorder')

                Notification.objects.create(source='SalesReturnOrder', source_id=instance.salesorder_id,
                                            message="You have new sales return order", from_user=from_user,
                                            to_user=to_user, read=False, url='crm:edit_salesreturnorder')
            elif salesman[0]['user_id'] == request.user.id:
                to_user = User.objects.get(id=salesman[0]['reporting_to_id'])

                Notification.objects.create(source='SalesReturnOrder', source_id=instance.salesorder_id,
                                            message="You have new sales return order", from_user=from_user,
                                            to_user=to_user, read=False, url='crm:edit_salesreturnorder')



        if customers.payment_terms == 1:
            Collection.objects.create(customer_id=warehouseid.customer_id, salesorder=warehouseid.salesorderid, amount= -warehouseid.total , description= 'auto created from Sales Return Order #'+ str(warehouseid.pk) )

@receiver(post_save, sender=TransferProduct)
def post_save_transferproduct(sender, instance, created, **kwargs):
    fromwarehouses = Warehouse.objects.get(pk=instance.from_warehouse_id)
    towarehouses = Warehouse.objects.get(pk=instance.to_warehouse_id)
    products = Product.objects.get(pk=instance.product_id)
    if products.unit_1 != None or products.unit_1 != 0 or products.unit_2 !=0 or products.unit_2 != None:
        pcsqty = instance.qty * products.unit_2
        crtqty = instance.qty
    else:
        pcsqty = instance.qty
        crtqty = instance.qty

    if created:
        Transactions.objects.create(source='TransferIn',source_id=instance.transferorder_id,product=instance.product,
                                    qty=pcsqty,warehouse_id=instance.to_warehouse_id, area_id=towarehouses.area_id, city_id=towarehouses.city_id, ctrqty = instance.qty, country_id=towarehouses.country_id)
        Transactions.objects.create(source='TransferOut',source_id=instance.transferorder_id,product=instance.product,
                                    qty=(pcsqty)*-1,warehouse_id=instance.from_warehouse_id, area_id=fromwarehouses.area_id, city_id=fromwarehouses.city_id, ctrqty = -instance.qty, country_id=fromwarehouses.country_id)

@receiver(post_save, sender=TargetBuildingBlocksAccountsProducts)
def post_save_TargetBuildingBlocksAccounts(sender, instance, created, **kwargs):
    if created:
        targetid = TargetBuildingBlocksAccounts.objects.get(pk=instance.targetbuildingblocksaccounts_id)
        products= Product.objects.get(pk=instance.product_id)
        m1 = round((products.m1 * instance.monthly_target)/100)
        m2 = round((products.m2 * instance.monthly_target)/100)
        m3 = round((products.m3 * instance.monthly_target)/100)
        m4 = round((products.m4 * instance.monthly_target)/100)
        m5 = round((products.m5 * instance.monthly_target)/100)
        m6 = round((products.m6 * instance.monthly_target)/100)
        m7 = round((products.m7 * instance.monthly_target)/100)
        m8 = round((products.m8 * instance.monthly_target)/100)
        m9 = round((products.m9 * instance.monthly_target)/100)
        m10 = round((products.m10 * instance.monthly_target)/100)
        m11 = round((products.m11 * instance.monthly_target)/100)
        m12 = round((products.m12 * instance.monthly_target)/100)
        accounts= Account.objects.get(pk=targetid.account_id)
        customers= Customer.objects.filter(account_id=accounts.id).filter(customer_size=targetid.customer_size)
        for customer in customers:
            TargetTransactions.objects.create(source='targetbuildingblocksaccounts', source_id=instance.targetbuildingblocksaccounts_id,
                                        product=instance.product,price=products.price_2, yearly_target=instance.monthly_target,
                                        account_id=accounts.id, channel_id=accounts.channel_id, customer_size=targetid.customer_size,
                                              name=targetid.name, customer_id=customer.id, salesman_id=customer.salesman_id,
                                              country_id=customer.country_id, area_id=customer.area_id, city_id=customer.city_id,
                                              category_id=products.category_id,
                                              m1=m1 ,m2=m2 ,m3=m3 ,m4=m4 ,m5=m5 ,m6=m6 ,m7=m7 ,m8=m8 ,m9=m9 ,m10=m10 ,m11=m11 ,m12=m12)
    else:
        try:
            targetid = TargetBuildingBlocksAccounts.objects.get(pk=instance.targetbuildingblocksaccounts_id)
        except:
            targetid = TargetBuildingBlocksAccounts.objects.get(pk=instance.pk)
        products= Product.objects.get(pk=instance.product_id)
        m1 = round((products.m1 * instance.monthly_target)/100)
        m2 = round((products.m2 * instance.monthly_target)/100)
        m3 = round((products.m3 * instance.monthly_target)/100)
        m4 = round((products.m4 * instance.monthly_target)/100)
        m5 = round((products.m5 * instance.monthly_target)/100)
        m6 = round((products.m6 * instance.monthly_target)/100)
        m7 = round((products.m7 * instance.monthly_target)/100)
        m8 = round((products.m8 * instance.monthly_target)/100)
        m9 = round((products.m9 * instance.monthly_target)/100)
        m10 = round((products.m10 * instance.monthly_target)/100)
        m11 = round((products.m11 * instance.monthly_target)/100)
        m12 = round((products.m12 * instance.monthly_target)/100)
        accounts= Account.objects.get(pk=targetid.account_id)
        customers= Customer.objects.filter(account_id=accounts.id).filter(customer_size=targetid.customer_size)

        # targetblockfilter = TargetBuildingBlocksAccountsProducts.objects.filter(changed__gte = 2)
        # targetblockfilter.update(changed=0)
        for customer in customers:
            qTargetTransactionsp = TargetTransactions.objects.filter(product=instance.product,
                                                                     source_id=instance.targetbuildingblocksaccounts_id,
                                                                     source='targetbuildingblocksaccounts',
                                                                     customer_id=customer.id)
            qTargetTransactionsp.delete()
            qTargetTransactionsp.create(source='targetbuildingblocksaccounts',
                                              source_id=instance.targetbuildingblocksaccounts_id,
                                              product=instance.product, price=products.price_2,
                                              yearly_target=instance.monthly_target,
                                              account_id=accounts.id, channel_id=accounts.channel_id,
                                              customer_size=targetid.customer_size,
                                              name=targetid.name, customer_id=customer.id, salesman_id=customer.salesman_id,
                                              country_id=customer.country_id, area_id=customer.area_id,
                                              city_id=customer.city_id,
                                              category_id=products.category_id,
                                              m1=m1, m2=m2, m3=m3, m4=m4, m5=m5, m6=m6, m7=m7, m8=m8, m9=m9, m10=m10,
                                              m11=m11, m12=m12)

@receiver(post_save, sender=TargetBuildingBlocksChannelsProducts)
def post_save_TargetBuildingBlocksChannels(sender, instance, created, **kwargs):
    if created:
        targetid = TargetBuildingBlocksChannels.objects.get(pk=instance.targetbuildingblockschannels_id)
        products= Product.objects.get(pk=instance.product_id)
        m1 = round((products.m1 * instance.monthly_target)/100)
        m2 = round((products.m2 * instance.monthly_target)/100)
        m3 = round((products.m3 * instance.monthly_target)/100)
        m4 = round((products.m4 * instance.monthly_target)/100)
        m5 = round((products.m5 * instance.monthly_target)/100)
        m6 = round((products.m6 * instance.monthly_target)/100)
        m7 = round((products.m7 * instance.monthly_target)/100)
        m8 = round((products.m8 * instance.monthly_target)/100)
        m9 = round((products.m9 * instance.monthly_target)/100)
        m10 = round((products.m10 * instance.monthly_target)/100)
        m11 = round((products.m11 * instance.monthly_target)/100)
        m12 = round((products.m12 * instance.monthly_target)/100)
        customers= Customer.objects.filter(channel_id=targetid.channel_id).filter(customer_size=targetid.customer_size)
        for customer in customers:
            if customer.account_id is None:
                TargetTransactions.objects.create(source='targetbuildingblockschannels', source_id=instance.targetbuildingblockschannels_id,
                                            product=instance.product,price=products.price_2, yearly_target=instance.monthly_target,
                                            account_id=None, channel_id=targetid.channel_id, customer_size=targetid.customer_size,
                                                  name=targetid.name, customer_id=customer.id, salesman_id=customer.salesman_id,
                                                  country_id=customer.country_id, area_id=customer.area_id, city_id=customer.city_id,
                                                  category_id=products.category_id,
                                                  m1=m1 ,m2=m2 ,m3=m3 ,m4=m4 ,m5=m5 ,m6=m6 ,m7=m7 ,m8=m8 ,m9=m9 ,m10=m10 ,m11=m11 ,m12=m12)

    else:
        try:
            targetid = TargetBuildingBlocksChannels.objects.get(pk=instance.targetbuildingblockschannels_id)
        except:
            targetid = TargetBuildingBlocksChannels.objects.get(pk=instance.pk)
        products= Product.objects.get(pk=instance.product_id)
        m1 = round((products.m1 * instance.monthly_target)/100)
        m2 = round((products.m2 * instance.monthly_target)/100)
        m3 = round((products.m3 * instance.monthly_target)/100)
        m4 = round((products.m4 * instance.monthly_target)/100)
        m5 = round((products.m5 * instance.monthly_target)/100)
        m6 = round((products.m6 * instance.monthly_target)/100)
        m7 = round((products.m7 * instance.monthly_target)/100)
        m8 = round((products.m8 * instance.monthly_target)/100)
        m9 = round((products.m9 * instance.monthly_target)/100)
        m10 = round((products.m10 * instance.monthly_target)/100)
        m11 = round((products.m11 * instance.monthly_target)/100)
        m12 = round((products.m12 * instance.monthly_target)/100)
        customers= Customer.objects.filter(channel_id=targetid.channel_id).filter(customer_size=targetid.customer_size)

        # targetblockfilter = TargetBuildingBlocksChannelsProducts.objects.filter(changed__gte = 2)
        # targetblockfilter.update(changed=0)
        for customer in customers:

            if customer.account_id is None:
                qTargetTransactionsp = TargetTransactions.objects.filter(product=instance.product,
                                                                         source_id=instance.targetbuildingblockschannels_id,
                                                                         source='targetbuildingblockschannels',
                                                                         customer_id=customer.id)
                qTargetTransactionsp.delete()
                qTargetTransactionsp.create(source='targetbuildingblockschannels', source_id=instance.targetbuildingblockschannels_id,
                                            product=instance.product,price=products.price_2, yearly_target=instance.monthly_target,
                                            account_id=None, channel_id=targetid.channel_id, customer_size=targetid.customer_size,
                                                  name=targetid.name, customer_id=customer.id, salesman_id=customer.salesman_id,
                                                  country_id=customer.country_id, area_id=customer.area_id, city_id=customer.city_id,
                                                  category_id=products.category_id,
                                                  m1=m1 ,m2=m2 ,m3=m3 ,m4=m4 ,m5=m5 ,m6=m6 ,m7=m7 ,m8=m8 ,m9=m9 ,m10=m10 ,m11=m11 ,m12=m12)

@receiver(post_save, sender=TargetCategoryChannelsProducts)
def post_save_TargetCategoryChannels(sender, instance, created, **kwargs):
    if created:
        targetid = TargetCategoryChannels.objects.get(pk=instance.targetcategorychannels_id)
        categories= Category.objects.filter(pk=instance.category_id)
        products= Product.objects.filter(category__in=categories)
        for prod in products:
            m1 = round((prod.m1 * instance.monthly_target)/100)
            m2 = round((prod.m2 * instance.monthly_target)/100)
            m3 = round((prod.m3 * instance.monthly_target)/100)
            m4 = round((prod.m4 * instance.monthly_target)/100)
            m5 = round((prod.m5 * instance.monthly_target)/100)
            m6 = round((prod.m6 * instance.monthly_target)/100)
            m7 = round((prod.m7 * instance.monthly_target)/100)
            m8 = round((prod.m8 * instance.monthly_target)/100)
            m9 = round((prod.m9 * instance.monthly_target)/100)
            m10 = round((prod.m10 * instance.monthly_target)/100)
            m11 = round((prod.m11 * instance.monthly_target)/100)
            m12 = round((prod.m12 * instance.monthly_target)/100)
            customers= Customer.objects.filter(channel_id=targetid.channel_id).filter(customer_size=targetid.customer_size)
            for customer in customers:
                if customer.account_id is None:
                    TargetTransactions.objects.create(source='targetcategorychannels', source_id=instance.targetcategorychannels_id,
                                                product_id=prod.id,price=prod.price_2, yearly_target=instance.monthly_target,
                                                account_id=None, channel_id=targetid.channel_id, customer_size=targetid.customer_size,
                                                      name=targetid.name, customer_id=customer.id, salesman_id=customer.salesman_id,
                                                      country_id=customer.country_id, area_id=customer.area_id, city_id=customer.city_id,
                                                      category_id=prod.category_id,
                                                      m1=m1 ,m2=m2 ,m3=m3 ,m4=m4 ,m5=m5 ,m6=m6 ,m7=m7 ,m8=m8 ,m9=m9 ,m10=m10 ,m11=m11 ,m12=m12)

    else:
        try:
            targetid = TargetCategoryChannels.objects.get(pk=instance.targetcategorychannels_id)
        except:
            targetid = TargetCategoryChannels.objects.get(pk=instance.pk)

        categories = Category.objects.filter(pk=instance.category_id)
        products = Product.objects.filter(category__in=categories)
        for prod in products:
            m1 = round((prod.m1 * instance.monthly_target)/100)
            m2 = round((prod.m2 * instance.monthly_target)/100)
            m3 = round((prod.m3 * instance.monthly_target)/100)
            m4 = round((prod.m4 * instance.monthly_target)/100)
            m5 = round((prod.m5 * instance.monthly_target)/100)
            m6 = round((prod.m6 * instance.monthly_target)/100)
            m7 = round((prod.m7 * instance.monthly_target)/100)
            m8 = round((prod.m8 * instance.monthly_target)/100)
            m9 = round((prod.m9 * instance.monthly_target)/100)
            m10 = round((prod.m10 * instance.monthly_target)/100)
            m11 = round((prod.m11 * instance.monthly_target)/100)
            m12 = round((prod.m12 * instance.monthly_target)/100)
            customers= Customer.objects.filter(channel_id=targetid.channel_id).filter(customer_size=targetid.customer_size)

            for customer in customers:

                if customer.account_id is None:
                    qTargetTransactionsp = TargetTransactions.objects.filter(product_id=prod.id,
                                                                             source_id=instance.targetcategorychannels_id,
                                                                             source='targetcategorychannels',
                                                                             customer_id=customer.id)
                    qTargetTransactionsp.delete()
                    qTargetTransactionsp.create(source='targetcategorychannels', source_id=instance.targetcategorychannels_id,
                                                product_id=prod.id,price=prod.price_2, yearly_target=instance.monthly_target,
                                                account_id=None, channel_id=targetid.channel_id, customer_size=targetid.customer_size,
                                                      name=targetid.name, customer_id=customer.id, salesman_id=customer.salesman_id,
                                                      country_id=customer.country_id, area_id=customer.area_id, city_id=customer.city_id,
                                                      category_id=prod.category_id,
                                                      m1=m1 ,m2=m2 ,m3=m3 ,m4=m4 ,m5=m5 ,m6=m6 ,m7=m7 ,m8=m8 ,m9=m9 ,m10=m10 ,m11=m11 ,m12=m12)

@receiver(post_save, sender=TargetBuildingBlocksProducts)
def post_save_TargetBuildingBlocksProducts(sender, instance, created, **kwargs):
    if created:
        targetid = TargetBuildingBlocksold.objects.get(pk=instance.targetbuildingblocks_id)
        products= Product.objects.get(pk=targetid.product_id)
        m1 = products.m1
        m2 = products.m2
        m3 = products.m3
        m4 = products.m4
        m5 = products.m5
        m6 = products.m6
        m7 = products.m7
        m8 = products.m8
        m9 = products.m9
        m10 = products.m10
        m11 = products.m11
        m12 = products.m12


        exceptionaccount = TargetBuildingBlocksExeption.objects.values('account').filter(targetbuildingblocks_id=instance.targetbuildingblocks_id)
        if instance.small > 0:
            if exceptionaccount.count() > 0 :
                customers= Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=2)\
                    .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(targetbuildingblocks_id=instance.targetbuildingblocks_id))
            else:
                customers= Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=2)
            CustCount = customers.count()
            for customer in customers:
                TargetTransactions.objects.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
                                            product=targetid.product,price=products.price_2, yearly_target=instance.small,
                                            account_id=None, channel_id=instance.channel_id, customer_size=2,
                                                  name=targetid.name, customer_id=customer.id, salesman_id=customer.salesman_id,
                                                  country_id=customer.country_id, area_id=customer.area_id, city_id=customer.city_id,
                                                  category_id=products.category_id,
                                                  m1=round(round((products.m1 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m2=round(round((products.m2 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m3=round(round((products.m3 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m4=round(round((products.m4 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m5=round(round((products.m5 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m6=round(round((products.m6 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m7=round(round((products.m7 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m8=round(round((products.m8 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m9=round(round((products.m9 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m10=round(round((products.m10 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m11=round(round((products.m11 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m12=round(round((products.m12 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100))/CustCount)

        if instance.medium > 0:
            if exceptionaccount.count() > 0:
                customers = Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=3) \
                    .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(
                    targetbuildingblocks_id=instance.targetbuildingblocks_id))
            else:
                customers = Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=3)

            CustCount = customers.count()
            for customer in customers:
                TargetTransactions.objects.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
                                                  product=targetid.product, price=products.price_2,
                                                  yearly_target=instance.medium,
                                                  account_id=None, channel_id=instance.channel_id, customer_size=3,
                                                  name=targetid.name, customer_id=customer.id,
                                                  salesman_id=customer.salesman_id,
                                                  country_id=customer.country_id, area_id=customer.area_id,
                                                  city_id=customer.city_id,
                                                  category_id=products.category_id,
                                                  m1=round(round((products.m1 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m2=round(round((products.m2 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m3=round(round((products.m3 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m4=round(round((products.m4 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m5=round(round((products.m5 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m6=round(round((products.m6 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m7=round(round((products.m7 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m8=round(round((products.m8 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m9=round(round((products.m9 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m10=round(round((products.m10 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m11=round(round((products.m11 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m12=round(round((products.m12 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100))/CustCount)

        if instance.large > 0:
            if exceptionaccount.count() > 0:
                customers = Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=4) \
                    .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(
                    targetbuildingblocks_id=instance.targetbuildingblocks_id))
            else:
                customers = Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=4)

            CustCount = customers.count()
            for customer in customers:
                TargetTransactions.objects.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
                                                  product=targetid.product, price=products.price_2,
                                                  yearly_target=instance.large,
                                                  account_id=None, channel_id=instance.channel_id, customer_size=4,
                                                  name=targetid.name, customer_id=customer.id,
                                                  salesman_id=customer.salesman_id,
                                                  country_id=customer.country_id, area_id=customer.area_id,
                                                  city_id=customer.city_id,
                                                  category_id=products.category_id,
                                                  m1=round(round((products.m1 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m2=round(round((products.m2 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m3=round(round((products.m3 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m4=round(round((products.m4 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m5=round(round((products.m5 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m6=round(round((products.m6 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m7=round(round((products.m7 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m8=round(round((products.m8 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m9=round(round((products.m9 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m10=round(round((products.m10 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m11=round(round((products.m11 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
                                                  m12=round(round((products.m12 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100))/CustCount)


    else:
        try:
            targetid = TargetBuildingBlocksold.objects.get(pk=instance.targetbuildingblocks_id)
        except:
            targetid = TargetBuildingBlocksold.objects.get(pk=instance.pk)
        targetblockfilter = TargetBuildingBlocksProducts.objects.filter(changed__gte = 2)
        targetblockfilter.update(changed=0)
        products= Product.objects.get(pk=targetid.product_id)
        m1 = products.m1
        m2 = products.m2
        m3 = products.m3
        m4 = products.m4
        m5 = products.m5
        m6 = products.m6
        m7 = products.m7
        m8 = products.m8
        m9 = products.m9
        m10 = products.m10
        m11 = products.m11
        m12 = products.m12

        exceptionaccount = TargetBuildingBlocksExeption.objects.values('account').filter(targetbuildingblocks_id=instance.targetbuildingblocks_id)
        if instance.small > 0:
            if exceptionaccount.count() > 0 :
                customers= Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=2)\
                    .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(targetbuildingblocks_id=instance.targetbuildingblocks_id))
            else:
                customers= Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=2)

            CustCount = customers.count()
            # qTargetTransactionsp.delete()
            for customer in customers:
                qTargetTransactionsp = TargetTransactions.objects.filter(product=targetid.product,
                                                                         channel_id=instance.channel_id,
                                                                         customer_size=2,
                                                                         source_id=instance.targetbuildingblocks_id,
                                                                         source='targettopdown',
                                                                         customer_id=customer.id)

                qTargetTransactionsp.delete()
                qTargetTransactionsp.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
                                            product=targetid.product,price=products.price_2, yearly_target=instance.small,
                                            account_id=None, channel_id=instance.channel_id, customer_size=2,
                                                  name=targetid.name, customer_id=customer.id, salesman_id=customer.salesman_id,
                                                  country_id=customer.country_id, area_id=customer.area_id, city_id=customer.city_id,
                                                  category_id=products.category_id,
                                                  m1=round(round((products.m1 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m2=round(round((products.m2 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m3=round(round((products.m3 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m4=round(round((products.m4 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m5=round(round((products.m5 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m6=round(round((products.m6 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m7=round(round((products.m7 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m8=round(round((products.m8 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m9=round(round((products.m9 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m10=round(round((products.m10 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m11=round(round((products.m11 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
                                                  m12=round(round((products.m12 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100))/CustCount)

        if instance.medium > 0:
            if exceptionaccount.count() > 0:
                customers = Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=3) \
                    .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(
                    targetbuildingblocks_id=instance.targetbuildingblocks_id))
            else:
                customers = Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=3)

            CustCount = customers.count()
            # qTargetTransactionsp.delete()
            for customer in customers:
                qTargetTransactionsp = TargetTransactions.objects.filter(product=targetid.product,
                                                                         channel_id=instance.channel_id,
                                                                         customer_size=3,
                                                                         source_id=instance.targetbuildingblocks_id,
                                                                         source='targettopdown',
                                                                         customer_id=customer.id)
                qTargetTransactionsp.delete()
                qTargetTransactionsp.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
                                            product=targetid.product, price=products.price_2,
                                            yearly_target=instance.small,
                                            account_id=None, channel_id=instance.channel_id, customer_size=3,
                                            name=targetid.name, customer_id=customer.id,
                                            salesman_id=customer.salesman_id,
                                            country_id=customer.country_id, area_id=customer.area_id,
                                            city_id=customer.city_id,
                                            category_id=products.category_id,
                                            m1=round(round((products.m1 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m2=round(round((products.m2 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m3=round(round((products.m3 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m4=round(round((products.m4 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m5=round(round((products.m5 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m6=round(round((products.m6 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m7=round(round((products.m7 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m8=round(round((products.m8 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m9=round(round((products.m9 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m10=round(round((products.m10 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m11=round(round((products.m11 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m12=round(round((products.m12 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100)) / CustCount)

        if instance.large > 0:
            if exceptionaccount.count() > 0:
                customers = Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=4) \
                    .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(
                    targetbuildingblocks_id=instance.targetbuildingblocks_id))
            else:
                customers = Customer.objects.filter(channel_id=instance.channel_id).filter(customer_size=4)

            CustCount = customers.count()
            # qTargetTransactionsp.delete()
            for customer in customers:
                qTargetTransactionsp = TargetTransactions.objects.filter(product=targetid.product,
                                                                         channel_id=instance.channel_id,
                                                                         customer_size=4,
                                                                         source_id=instance.targetbuildingblocks_id,
                                                                         source='targettopdown',
                                                                         customer_id=customer.id)
                qTargetTransactionsp.delete()
                qTargetTransactionsp.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
                                            product=targetid.product, price=products.price_2,
                                            yearly_target=instance.small,
                                            account_id=None, channel_id=instance.channel_id, customer_size=4,
                                            name=targetid.name, customer_id=customer.id,
                                            salesman_id=customer.salesman_id,
                                            country_id=customer.country_id, area_id=customer.area_id,
                                            city_id=customer.city_id,
                                            category_id=products.category_id,
                                            m1=round(round((products.m1 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m2=round(round((products.m2 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m3=round(round((products.m3 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m4=round(round((products.m4 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m5=round(round((products.m5 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m6=round(round((products.m6 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m7=round(round((products.m7 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m8=round(round((products.m8 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m9=round(round((products.m9 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m10=round(round((products.m10 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m11=round(round((products.m11 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
                                            m12=round(round((products.m12 * round(((targetid.yearly_qty * (
                                                        instance.small * instance.contribution) / 100) / 100))) / 100)) / CustCount)


@receiver(post_save, sender=Collection)
def post_save_collection(sender, instance, created, **kwargs):
    qSalesOrder = SalesOrder.objects.filter(pk=instance.salesorder).values()
    try:
        qSalesOrderv = qSalesOrder[0]['total']
    except:
        qSalesOrderv = 0
    if qSalesOrderv is None:
        qSalesOrderv = 0

    qcollection = Collection.objects.values('salesorder').order_by('salesorder').annotate(totalsr=Sum('amount')).filter(salesorder=instance.salesorder)
    totalcollection = qcollection.aggregate(Sum('amount'))
    try:
        totalcollectionv = totalcollection['amount__sum']
    except:
        totalcollectionv = 0

    if int(totalcollectionv) >= int(qSalesOrderv):
        qSalesOrder.update(paid=True)
