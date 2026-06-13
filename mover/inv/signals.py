##signals

from django.db.models import Q, Sum
from django.db.models.signals import post_save, pre_delete
#from django.dispatch import receiver
#from TARGET.crm.models import *
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from ar.models import *
from .models import *

from .middlewares import RequestMiddleware



# def get_all_children(self, container=None):
#     if container is None:
#         container = []
#     result = container
#     for child in self.children.all():
#         result.append(child)
#         if child.children.count() > 0:
#             child.get_all_children(result)
#     return result

# def get_all_children(self, include_self=True):
#     r = []
#     print('cccccccccccccc')
#
#     if include_self:
#         r.append(self)
#     for c in Customers.objects.filter(parent=self):
#         print(c)
#         _r = c.get_all_children(include_self=True)
#         if 0 < len(_r):
#             r.extend(_r)
#     return r

@receiver(post_save, sender=TargetBuildingBlocksAccountsItems)
def post_save_TargetBuildingBlocksAccounts(sender, instance, created, **kwargs):
    pass
    # if created:
    #     targetid = TargetBuildingBlocksAccounts.objects.get(pk=instance.targetbuildingblocksaccounts_id)
    #
    #     accounts= Customers.objects.get(pk=targetid.account_id)
    #     customers= Customers.objects.filter(code__icontains=accounts.code)
    #     #customers= Customers.objects.filter(pk__in=customers).filter(customer_size=targetid.customer_size)
    #     #custlst=get_all_children(Customers,True)
    #     itemlist = TargetBuildingBlocksAccountsItems.objects.filter(targetbuildingblocksaccounts=targetid.id)
    #     for item in itemlist:
    #         for customer in customers:
    #             try:
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customer.id).first()
    #                 countryid = custaddr.country_id
    #                 areaid = custaddr.city.area_id
    #                 cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=item.item_id, area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality = False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #             TargetTransactions.objects.create(source='targetbuildingblocksaccounts', source_id=instance.targetbuildingblocksaccounts_id,
    #                                         item=instance.item,price=1, yearly_target=instance.monthly_target,
    #                                         channel_id=accounts.customerclass_id, customer_size_id=targetid.customer_size.id,
    #                                         engname=targetid.engname, customer_id=customer.id, #salesman_id=customer.salesman_id,
    #                                         country_id=countryid, area_id=areaid, city_id=cityid,isautoseasonality = isautoseasonality,
    #                                         itemuom_id=item.itemuom_id,
    #                                               m1=m1 ,m2=m2 ,m3=m3 ,m4=m4 ,m5=m5 ,m6=m6 ,m7=m7 ,m8=m8 ,m9=m9 ,m10=m10 ,m11=m11 ,m12=m12)
    # else:
    #     try:
    #         targetid = TargetBuildingBlocksAccounts.objects.get(pk=instance.targetbuildingblocksaccounts_id)
    #     except:
    #         targetid = TargetBuildingBlocksAccounts.objects.get(pk=instance.pk)
    #
    #     accounts= Customers.objects.get(pk=targetid.account_id)
    #     customers= Customers.objects.filter(code__icontains=accounts.code)
    #     #customers= Customers.objects.filter(pk__=customers).filter(customer_size=targetid.customer_size)
    #     #print('custlst')
    #     #custlst= customers.get_all_children()
    #
    #     #print(custlst)
    #     itemlist = TargetBuildingBlocksAccountsItems.objects.filter(targetbuildingblocksaccounts=targetid.id)
    #     for item in itemlist:
    #
    #     # targetblockfilter = TargetBuildingBlocksAccountsProducts.objects.filter(changed__gte = 2)
    #     # targetblockfilter.update(changed=0)
    #         for customer in customers:
    #             try:
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customer.id).first()
    #                 countryid = custaddr.country_id
    #                 areaid = custaddr.city.area_id
    #                 cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=item.item_id, area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality = False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #             qTargetTransactionsp = TargetTransactions.objects.filter(item=instance.item,
    #                                                                      source_id=instance.targetbuildingblocksaccounts_id,
    #                                                                      source='targetbuildingblocksaccounts',
    #                                                                      customer_id=customer.id)
    #             qTargetTransactionsp.delete()
    #             qTargetTransactionsp.create(source='targetbuildingblocksaccounts',
    #                                               source_id=instance.targetbuildingblocksaccounts_id,
    #                                               item=instance.item, price=1,
    #                                               yearly_target=instance.monthly_target,
    #                                               account_id=accounts.id, channel_id=accounts.customerclass_id,
    #                                               customer_size_id=targetid.customer_size.id,
    #                                               engname=targetid.engname, customer_id=customer.id, #salesman_id=customer.salesman_id,
    #                                               country_id=countryid, area_id=areaid,
    #                                               city_id=cityid,isautoseasonality=isautoseasonality,
    #                                                 itemuom_id=item.itemuom_id,
    #
    #                                         m1=m1, m2=m2, m3=m3, m4=m4, m5=m5, m6=m6, m7=m7, m8=m8, m9=m9, m10=m10,
    #                                               m11=m11, m12=m12)

@receiver(post_save, sender=TargetBuildingBlocksChannelsItems)
def post_save_TargetBuildingBlocksChannels(sender, instance, created, **kwargs):
    pass
    # print('post_save_TargetBuildingBlocksChannels')
    # if created:
    #     targetid = TargetBuildingBlocksChannels.objects.get(pk=instance.targetbuildingblockschannels_id)
    #     customers= Customers.objects.filter(customerclass_id=targetid.channel_id).filter(accountsize=targetid.customer_size)
    #     itemlist = TargetBuildingBlocksChannelsItems.objects.filter(targetbuildingblockschannels=targetid.id)
    #     for item in itemlist:
    #
    #         for customer in customers:
    #             try:
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customer.id).first()
    #                 countryid = custaddr.country_id
    #                 areaid = custaddr.city.area_id
    #                 cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=item.item_id, area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality = False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #             TargetTransactions.objects.create(source='targetbuildingblockschannels', source_id=instance.targetbuildingblockschannels_id,
    #                                             item=instance.item,price=1, yearly_target=instance.monthly_target,
    #                                             account_id=None, channel_id=targetid.channel_id, customer_size_id=targetid.customer_size.id,
    #                                                   engname=targetid.engname, customer_id=customer.id, #salesman_id=customer.salesman_id,
    #                                                   country_id=countryid, area_id=areaid, city_id=cityid,isautoseasonality=isautoseasonality,
    #                                               itemuom_id=item.itemuom_id,
    #
    #                                               m1=m1 ,m2=m2 ,m3=m3 ,m4=m4 ,m5=m5 ,m6=m6 ,m7=m7 ,m8=m8 ,m9=m9 ,m10=m10 ,m11=m11 ,m12=m12)
    #
    # else:
    #     try:
    #         targetid = TargetBuildingBlocksChannels.objects.get(pk=instance.targetbuildingblockschannels_id)
    #     except:
    #         targetid = TargetBuildingBlocksChannels.objects.get(pk=instance.pk)
    #     # items= ItemsSeasonality.objects.get(pk=instance.item_id)
    #     # m1 = round((items.m1 * instance.monthly_target)/100)
    #     # m2 = round((items.m2 * instance.monthly_target)/100)
    #     # m3 = round((items.m3 * instance.monthly_target)/100)
    #     # m4 = round((items.m4 * instance.monthly_target)/100)
    #     # m5 = round((items.m5 * instance.monthly_target)/100)
    #     # m6 = round((items.m6 * instance.monthly_target)/100)
    #     # m7 = round((items.m7 * instance.monthly_target)/100)
    #     # m8 = round((items.m8 * instance.monthly_target)/100)
    #     # m9 = round((items.m9 * instance.monthly_target)/100)
    #     # m10 = round((items.m10 * instance.monthly_target)/100)
    #     # m11 = round((items.m11 * instance.monthly_target)/100)
    #     # m12 = round((items.m12 * instance.monthly_target)/100)
    #     customers= Customers.objects.filter(customerclass_id=targetid.channel_id).filter(accountsize=targetid.customer_size)
    #
    #     # targetblockfilter = TargetBuildingBlocksChannelsProducts.objects.filter(changed__gte = 2)
    #     # targetblockfilter.update(changed=0)
    #     itemlist = TargetBuildingBlocksChannelsItems.objects.filter(targetbuildingblockschannels=targetid.id)
    #     for item in itemlist:
    #
    #         for customer in customers:
    #             try:
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customer.id).first()
    #                 countryid = custaddr.country_id
    #                 areaid = custaddr.city.area_id
    #                 cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=item.item_id, area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality = False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #             #if customer.account_id is None:
    #             qTargetTransactionsp = TargetTransactions.objects.filter(item=instance.item,
    #                                                                      source_id=instance.targetbuildingblockschannels_id,
    #                                                                      source='targetbuildingblockschannels',
    #                                                                      customer_id=customer.id)
    #             qTargetTransactionsp.delete()
    #             qTargetTransactionsp.create(source='targetbuildingblockschannels', source_id=instance.targetbuildingblockschannels_id,
    #                                         item=instance.item,price=1, yearly_target=instance.monthly_target,
    #                                         account_id=None, channel_id=targetid.channel_id, customer_size_id=targetid.customer_size.id,
    #                                               engname=targetid.engname, customer_id=customer.id, #salesman_id=customer.salesman_id,
    #                                               country_id=countryid, area_id=areaid, city_id=cityid,isautoseasonality=isautoseasonality,
    #                                         itemuom_id=item.itemuom_id,
    #
    #                                         m1=m1 ,m2=m2 ,m3=m3 ,m4=m4 ,m5=m5 ,m6=m6 ,m7=m7 ,m8=m8 ,m9=m9 ,m10=m10 ,m11=m11 ,m12=m12)

@receiver(post_save, sender=TargetBuildingBlocksItems)
def post_save_TargetBuildingBlocksItems(sender, instance, created, **kwargs):
    pass
    # if  created:
    #     print('post_save_TargetBuildingBlocksItems >>>')
    #     print(instance.targetbuildingblocks_id)
    #     targetid = TargetBuildingBlocks.objects.get(pk=instance.targetbuildingblocks_id)
    #     print(targetid.item_id)
    #     print('targetid.item_id')
    #
    #     exceptionaccount = TargetBuildingBlocksExeption.objects.values('account').filter(targetbuildingblocks_id=instance.targetbuildingblocks_id)
    #     if instance.small > 0:
    #         if exceptionaccount.count() > 0 :
    #             customers= Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2102)\
    #                 .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(targetbuildingblocks_id=instance.targetbuildingblocks_id))
    #         else:
    #             customers= Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2102)
    #         CustCount = customers.count()
    #         for customer in customers:
    #             try:
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customer.id).first()
    #                 countryid = custaddr.country_id
    #                 areaid = custaddr.city.area_id
    #                 cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=targetid.item_id,area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality =False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #
    #             TargetTransactions.objects.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
    #                                         item=targetid.item,price=1, yearly_target=instance.small,
    #                                         account_id=None, channel_id=instance.channel_id, customer_size_id=customer.accountsize.id,
    #                                               engname=targetid.engname, customer_id=customer.id, #salesman_id=customer.salesman_id,
    #                                               country_id=countryid, area_id=areaid, city_id=cityid,isautoseasonality =isautoseasonality,
    #                                               itemuom_id=targetid.itemuom_id,
    #
    #                                               m1=round(round((m1 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m2=round(round((m2 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m3=round(round((m3 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m4=round(round((m4 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m5=round(round((m5 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m6=round(round((m6 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m7=round(round((m7 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m8=round(round((m8 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m9=round(round((m9 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m10=round(round((m10 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m11=round(round((m11 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m12=round(round((m12 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100))/CustCount)
    #
    #     if instance.medium > 0:
    #         if exceptionaccount.count() > 0:
    #             customers = Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2103) \
    #                 .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(
    #                 targetbuildingblocks_id=instance.targetbuildingblocks_id))
    #         else:
    #             customers = Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2103)
    #
    #         CustCount = customers.count()
    #         for customer in customers:
    #             try:
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customer.id).first()
    #                 countryid = custaddr.country_id
    #                 areaid = custaddr.city.area_id
    #                 cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=targetid.item_id,area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality =False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #             TargetTransactions.objects.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
    #                                               item=targetid.item, price=1,   #products.price_2 =1
    #                                               yearly_target=instance.medium,
    #                                               account_id=None, channel_id=instance.channel_id, customer_size_id=customer.accountsize.id,
    #                                               engname=targetid.engname, customer_id=customer.id,
    #                                               #salesman_id=customer.salesman_id,
    #                                               country_id=countryid, area_id=areaid,
    #                                               city_id=cityid,
    #                                               itemuom_id=targetid.itemuom_id,
    #                                               m1=round(round((m1 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m2=round(round((m2 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m3=round(round((m3 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m4=round(round((m4 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m5=round(round((m5 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m6=round(round((m6 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m7=round(round((m7 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m8=round(round((m8 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m9=round(round((m9 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m10=round(round((m10 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m11=round(round((m11 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m12=round(round((m12 * round(((targetid.yearly_qty * (instance.medium * instance.contribution)/100)/100))) / 100))/CustCount)
    #
    #     if instance.large > 0:
    #         if exceptionaccount.count() > 0:
    #             customers = Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2102) \
    #                 .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(
    #                 targetbuildingblocks_id=instance.targetbuildingblocks_id))
    #         else:
    #             customers = Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2102)
    #
    #         CustCount = customers.count()
    #         for customer in customers:
    #             try:
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customer.id).first()
    #                 countryid = custaddr.country_id
    #                 areaid = custaddr.city.area_id
    #                 cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=targetid.item_id,area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality =False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #             TargetTransactions.objects.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
    #                                               item=targetid.item, price=1,
    #                                               yearly_target=instance.large,
    #                                               account_id=None, channel_id=instance.channel_id, customer_size_id=customer.accountsize.id,
    #                                               engname=targetid.engname, customer_id=customer.id,
    #                                               #salesman_id=customer.salesman_id,
    #                                               country_id=countryid, area_id=areaid,
    #                                               city_id=cityid,isautoseasonality = isautoseasonality,
    #                                               itemuom_id=targetid.itemuom_id,
    #                                               m1=round(round((m1 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m2=round(round((m2 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m3=round(round((m3 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m4=round(round((m4 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m5=round(round((m5 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m6=round(round((m6 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m7=round(round((m7 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m8=round(round((m8 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m9=round(round((m9 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m10=round(round((m10 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m11=round(round((m11 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100)/CustCount),
    #                                               m12=round(round((m12 * round(((targetid.yearly_qty * (instance.large * instance.contribution)/100)/100))) / 100))/CustCount)
    #
    #
    # else:
    #     try:
    #         targetid = TargetBuildingBlocks.objects.get(pk=instance.targetbuildingblocks_id)
    #         print('hi post try')
    #     except:
    #         targetid = TargetBuildingBlocks.objects.get(pk=instance.pk)
    #
    #
    #
    #     print('targetid2')
    #
    #     targetblockfilter = TargetBuildingBlocksItems.objects.filter(changed__gte = 2).values()
    #     print(targetblockfilter)
    #     targetblockfilter.update(changed=0)
    #
    #
    #     exceptionaccount = TargetBuildingBlocksExeption.objects.values('account').filter(targetbuildingblocks_id=instance.targetbuildingblocks_id)
    #     if instance.small > 0:
    #         if exceptionaccount.count() > 0 :
    #             customers= Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2102)\
    #                 .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(targetbuildingblocks_id=instance.targetbuildingblocks_id))
    #         else:
    #             customers= Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2102).values()
    #
    #         CustCount = customers.count()
    #         # qTargetTransactionsp.delete()
    #         for customer in customers:
    #             try:
    #                 print(customer['id'])
    #                 print('customer.id')
    #                 customerid=customer['id']
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customerid).first()
    #                 countryid = custaddr.country_id
    #                 areaid = custaddr.city.area_id
    #                 cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=targetid.item_id,area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality =False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #
    #             qTargetTransactionsp = TargetTransactions.objects.filter(item=targetid.item,
    #                                                                      channel_id=instance.channel_id,
    #                                                                      customer_size_id=customer['accountsize_id'],
    #                                                                      source_id=instance.targetbuildingblocks_id,
    #                                                                      source='targettopdown',
    #                                                                      customer_id=customer['id'])
    #
    #             qTargetTransactionsp.delete()
    #             qTargetTransactionsp.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
    #                                         item=targetid.item,price=1, yearly_target=instance.small,
    #                                         account_id=None, channel_id=instance.channel_id, customer_size_id=customer['accountsize_id'],
    #                                               engname=targetid.engname, customer_id=customer['id'], #salesman_id=customer.salesman_id,
    #                                               country_id=countryid, area_id=areaid, city_id=cityid,isautoseasonality=isautoseasonality,
    #                                         itemuom_id=targetid.itemuom_id,
    #                                               m1=round(round((m1 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m2=round(round((m2 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m3=round(round((m3 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m4=round(round((m4 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m5=round(round((m5 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m6=round(round((m6 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m7=round(round((m7 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m8=round(round((m8 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m9=round(round((m9 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m10=round(round((m10 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m11=round(round((m11 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100)/CustCount) ,
    #                                               m12=round(round((m12 * round(((targetid.yearly_qty * (instance.small * instance.contribution)/100)/100))) / 100))/CustCount)
    #
    #     if instance.medium > 0:
    #         if exceptionaccount.count() > 0:
    #             customers = Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2103) \
    #                 .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(
    #                 targetbuildingblocks_id=instance.targetbuildingblocks_id))
    #         else:
    #             customers = Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2103)
    #
    #         CustCount = customers.count()
    #         # qTargetTransactionsp.delete()
    #         for customer in customers:
    #             try:
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customer.id).first()
    #                 countryid = custaddr.country_id
    #                 areaid = custaddr.city.area_id
    #                 cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=targetid.item_id,area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality =False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #             qTargetTransactionsp = TargetTransactions.objects.filter(item=targetid.item,
    #                                                                      channel_id=instance.channel_id,
    #                                                                      customer_size_id=customer.accountsize.id,
    #                                                                      source_id=instance.targetbuildingblocks_id,
    #                                                                      source='targettopdown',
    #                                                                      customer_id=customer.id)
    #             qTargetTransactionsp.delete()
    #             qTargetTransactionsp.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
    #                                         item=targetid.item, price=1,
    #                                         yearly_target=instance.small,
    #                                         account_id=None, channel_id=instance.channel_id, customer_size_id=customer.accountsize.id,
    #                                         engname=targetid.engname, customer_id=customer.id,
    #                                         #salesman_id=customer.salesman_id,
    #                                         country_id=countryid, area_id=areaid,
    #                                         city_id=cityid,isautoseasonality=isautoseasonality,
    #                                         itemuom_id=targetid.itemuom_id,
    #                                         m1=round(round((m1 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m2=round(round((m2 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m3=round(round((m3 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m4=round(round((m4 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m5=round(round((m5 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m6=round(round((m6 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m7=round(round((m7 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m8=round(round((m8 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m9=round(round((m9 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m10=round(round((m10 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m11=round(round((m11 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m12=round(round((m12 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100)) / CustCount)
    #
    #     if instance.large > 0:
    #
    #         if exceptionaccount.count() > 0:
    #             customers = Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2104) \
    #                 .exclude(account_id__in=TargetBuildingBlocksExeption.objects.values('account').filter(
    #                 targetbuildingblocks_id=instance.targetbuildingblocks_id))
    #         else:
    #             customers = Customers.objects.filter(customerclass_id=instance.channel_id).filter(accountsize__keyid=2104)
    #
    #         CustCount = customers.count()
    #         # qTargetTransactionsp.delete()
    #         for customer in customers:
    #             try:
    #                 custaddr = CustomersAddresses.objects.filter(customer_id=customer.id).first()
    #                 if custaddr:
    #                     countryid = custaddr.country_id
    #                     areaid = custaddr.city.area_id
    #                     cityid = custaddr.city_id
    #
    #             except ObjectDoesNotExist:
    #                 countryid = None
    #                 areaid = None
    #                 cityid = None
    #                 print("Either the blog or entry doesn't exist.")
    #
    #             try:
    #                 items = ItemsSeasonality.objects.get(item_id=targetid.item_id,area_id=areaid)
    #                 m1 = items.m1
    #                 m2 = items.m2
    #                 m3 = items.m3
    #                 m4 = items.m4
    #                 m5 = items.m5
    #                 m6 = items.m6
    #                 m7 = items.m7
    #                 m8 = items.m8
    #                 m9 = items.m9
    #                 m10 = items.m10
    #                 m11 = items.m11
    #                 m12 = items.m12
    #                 isautoseasonality =False
    #             except ObjectDoesNotExist:
    #                 m1 = 8.33
    #                 m2 = 8.33
    #                 m3 = 8.33
    #                 m4 = 8.33
    #                 m5 = 8.33
    #                 m6 = 8.33
    #                 m7 = 8.33
    #                 m8 = 8.33
    #                 m9 = 8.34
    #                 m10 = 8.34
    #                 m11 = 8.34
    #                 m12 = 8.34
    #                 isautoseasonality = True
    #
    #             qTargetTransactionsp = TargetTransactions.objects.filter(item=targetid.item,
    #                                                                      channel_id=instance.channel_id,
    #                                                                      customer_size_id=customer.accountsize.id ,
    #                                                                      source_id=instance.targetbuildingblocks_id,
    #                                                                      source='targettopdown',
    #                                                                      customer_id=customer.id)
    #             qTargetTransactionsp.delete()
    #             qTargetTransactionsp.create(source='targettopdown', source_id=instance.targetbuildingblocks_id,
    #                                         item=targetid.item, price=1,
    #                                         yearly_target=instance.small,
    #                                         account_id=None, channel_id=instance.channel_id, customer_size_id=customer.accountsize.id,
    #                                         engname=targetid.engname, customer_id=customer.id,
    #                                         #salesman_id=customer.salesman_id,
    #                                         country_id=  countryid, area_id=areaid,
    #                                         city_id=cityid,isautoseasonality=isautoseasonality,
    #                                         itemuom_id=targetid.itemuom_id,
    #                                         m1=round(round((m1 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m2=round(round((m2 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m3=round(round((m3 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m4=round(round((m4 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m5=round(round((m5 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m6=round(round((m6 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m7=round(round((m7 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m8=round(round((m8 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m9=round(round((m9 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m10=round(round((m10 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m11=round(round((m11 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100) / CustCount),
    #                                         m12=round(round((m12 * round(((targetid.yearly_qty * (
    #                                                     instance.small * instance.contribution) / 100) / 100))) / 100)) / CustCount)
    #
    #
