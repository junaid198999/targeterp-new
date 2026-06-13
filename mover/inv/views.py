import calendar, io
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

from ar.models import CustomersCategories
from .forms import *
from .models import *
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import (
    CreateView, ListView, UpdateView)
from django.http.response import HttpResponseRedirect
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum, F, IntegerField, Q, Count
from django.views.generic import TemplateView, DetailView, FormView

import _datetime
from . import signals
#from . import signals
from django.apps import apps

from django.views.generic.edit import CreateView
from django.utils import timezone
from bootstrap_modal_forms.generic import (BSModalCreateView,BSModalUpdateView,BSModalReadView,BSModalDeleteView)
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from itertools import chain

driver = None


######### Load operations

def load_operations(request):
    opkind = request.GET.get('kind')
    opkind_ids = LookUp.objects.filter(keyname='OperationsKinds',remarks__contains=opkind).values('pk')
    #lstopkind_ids = list(opkind_ids)
    otypes = OperationsTypes.objects.all().filter(operationkind_id__in=opkind_ids)
    lstotypes=list(otypes)
    return render(request, 'inv/dropdownlist/operationstype_menu_list_options.html', {'otypes': lstotypes})
######### End Load operations


######### Load Items Units

def load_itemuom(request):
    item_id = request.GET.get('item')
    itemsuom = ItemsUOM.objects.filter(item_id=item_id)
    itemsuomlst=list(itemsuom)
    #itemsuom = Units.objects.filter(ItemsUOM__Items__id=item_id).values('code','pk')
    #itemsuom = ItemsUOM.objects.filter(item_id=item_id).order_by('pk').values('barcode','baseunitfactor','unit')
    return render(request, 'inv/dropdownlist/itemuom_dropdown_list_options.html', {'itemsuom': itemsuomlst})

def load_accountbalance(request):
    accounttype_id = request.GET.get('accounttypeid')
    account_id = request.GET.get('accountid')

    strsql = """
        Select * from   public.getaccountbalance(accounttypeid,accountid) ;
        """
    strsql = strsql.replace('accounttypeid', accounttype_id)
    strsql = strsql.replace('accountid', account_id)
    print(strsql)
    strcursor = connection.cursor()
    strcursor.execute(strsql)
    strrow = strcursor.fetchall()
    accountbalance = strrow[0][0]
    print(accountbalance)
    return render(request, 'inv/dropdownlist/accountbalance_dropdown_value.html', {'accountbalance':accountbalance,'credit': 300 } )


######### Load Items Price

def load_itemprice(request):
        item_id = request.GET.get('item')
        if item_id != None:
            invloc_id = request.GET.get('invlocation')
            defuomid = Items.objects.filter(pk=item_id).order_by('pk').values('baseuom_id')
            prclvlid = int(request.GET.get('pricelevel'))

            if invloc_id != None:
                uom_id = request.GET.get('uom')
                if uom_id == None:
                    uom_id = defuomid

                itemsprc = ItemsPricesLists.objects.filter(item_id=item_id,invlocation_id=invloc_id ,itemuom_id=uom_id,pricelevel_id=prclvlid).order_by('pk').values('price')
                lstprc= list(itemsprc)

                return render(request, 'inv/dropdownlist/unitprice_dropdown_list_options.html', {'prices':lstprc} )
            else:
                return render(request, 'inv/dropdownlist/unitprice_dropdown_list_options.html', {'prices': 0})
        else:
            return render(request, 'inv/dropdownlist/unitprice_dropdown_list_options.html', {'prices': 0})


######### End Load Items


######### Load Items Barcode

def load_itembarcode(request):

    item_id = request.GET.get('item')
    uom_id = request.GET.get('uom')
    itembarcode = ItemsUOM.objects.filter(item_id=item_id,id=uom_id).order_by('pk').values('barcode')
    itmbc=list(itembarcode)
    return render(request, 'inv/dropdownlist/itembarcode_dropdown_value.html', {'barcodes': itmbc})

######### End Load Barcode


######### Load Items Tax value

def load_itemtaxvalue(request):

    vitem_id = request.GET.get('item')
    print(vitem_id)
    taxgroupsale_ids = Items.objects.filter(id=vitem_id).values('taxgroupsale_id','taxgroupsaleincludedprice')
    print(taxgroupsale_ids)

    taxgroupPurchaseids = Items.objects.filter(id=vitem_id).values('taxgroupPurchase_id','taxgroupPurchaseincludedprice')

    taxgroupsale_idslst = list(taxgroupsale_ids)
    print(taxgroupsale_idslst)
    taxgroupsaleid = taxgroupsale_idslst[0]['taxgroupsale_id']
    taxgroupsaleincludedprice = taxgroupsale_idslst[0]['taxgroupsaleincludedprice']

    currentdate = datetime.now().date().strftime('%Y-%m-%d')
    taxids = TaxesGroupsLine.objects.all().filter(taxgroup_id=taxgroupsaleid,fromdate__lt= currentdate,todate__gt=currentdate ).values('tax_id','taxgroup_id')
    #taxids = TaxesGroupsLine.objects.all().filter(taxgroup_id=taxgroupsaleid).values('tax_id','taxgroup_id')

    taxidslst = list(taxids)
    taxid=taxidslst[0]['tax_id']

    taxvalue = TaxesLine.objects.all().filter(tax_id=taxid).values('value').first()

    if taxgroupsaleincludedprice == True:
        taxsign = -1
    else:
        taxsign = 1
    tax_value = taxsign * taxvalue['value']


    return render(request, 'inv/dropdownlist/itemtaxvalue_dropdown_value.html', {'taxvalue': tax_value})

######### End Load Items Tax value

######### Load Operation Details Info
def load_operation_Details_Info(request):
    currentoperationtype_id = request.GET.get('curroptypreid')

    operationdetinfo = Operations.objects.filter(id=currentoperationtype_id).order_by('pk')


    soarr = []
    print('kkk')


    if operationdetinfo.count() > 0:
        print('Check Before ')
        for so in operationdetinfo:
            print(so.operationtype.accounttype.keyid)
            soarr.append({'operation': so.id, 'accounttypekeyid':so.operationtype.accounttype.keyid,  #'accounttype': so.operationtype__accounttype,
                          #'ledger': so.ledger.code + ' - ' + so.ledger.engname,
                          'ledger': so.ledger ,
                          'customerid': so.customer_id ,'customer': so.customer,
                          'vendorid': so.vendor_id ,'vendor': so.vendor,
                          # 'costcenter1': so.costcenter1.code + ' - ' + so.costcenter1.engname,
                          # 'costcenter2': so.costcenter2.code + ' - ' + so.costcenter2.engname,
                          # 'costcenter3': so.costcenter3.code + ' - ' + so.costcenter3.engname,
                          # 'costcenter4': so.costcenter4.code + ' - ' + so.costcenter4.engname,
                          'invlocationid': so.invlocation_id, 'invlocation': so.invlocation,
                          'discper1': so.discper1, 'discper2': so.discper2, 'discper3': so.discper3,
                          'discamt1': so.discamt2, 'discamt2': so.discamt2, 'discamt3': so.discamt3,
                          'expenseamount': so.expenseamount, 'grossamount': so.grossamount,
                          'netamount': so.netamount, 'totalcost': so.totalcost,
                          #'taxpercent': so.taxpercent, 'taxamount': so.taxamount,
                          #'keyid':so.operationtype__accounttype__keyid,
                         })

    else:
        messages.warning(request, 'You have to Post All Old Operations Before Create New one')
            #return request.response

        #print(soarr)
    return render(request, 'inv/dropdownlist/operations_Details_Info.html', {'operationsdetinfo': soarr })

######### End Load Operation Details Info


######### Load Operation Line
def load_operation_line(request):
    currentoperationtype_id = request.GET.get('curroptypreid')
    operation_id = request.GET.get('parentopid')

    operationlines = OperationsLine.objects.filter(operation_id=operation_id).order_by('pk')
    #print(operationlines.count())
    alloperationlinesdone = OperationsLine.objects.filter(operation__operationtype_id= currentoperationtype_id ,operation__parent_id=operation_id).exclude (operation__status__keyid= 10004 ).order_by('pk')
    soarr = []
    if alloperationlinesdone.count() == 0:
        #print(operationlines.count())
        if operationlines.count() > 0:
            for so in operationlines:
                #alloperationlinesdone = OperationsLine.objects.filter(operation__operationtype_id=currentoperationtype_id).filter(item=so.item_id)
                alloperationlinesdone = OperationsLine.objects.filter(
                    operation__operationtype_id=currentoperationtype_id, operation__parent_id=operation_id ,item=so.item_id).exclude(
                    operation__status__keyid=10004).order_by('pk')



                itemqtydone = alloperationlinesdone.aggregate(Sum('quantity'))

                if alloperationlinesdone.count() > 0 :
                    if itemqtydone['quantity__sum'] is not None:
                        qtydone = itemqtydone['quantity__sum']
                        if so.quantity > qtydone:
                            netqty = so.quantity - qtydone

                            soarr.append({'operation': operation_id,'parent': so.id, 'item_id': so.item_id, 'item_name':  so.item.code + ' - ' + so.item.engname,
                                          'quantity': netqty , 'itemuom_id' :so.itemuom_id , 'price': so.price , 'taxpercent': so.taxpercent , 'taxamount': so.taxamount ,
                                          'barcode': so.barcode, 'linetotal' : so.linetotal ,
                                          'itemuom_name':  so.itemuom.unit.code + ' - ' + str(int(so.itemuom.baseunitfactor)) + ' - ' + so.itemuom.barcode } )

                else:
                    soarr.append({'operation': operation_id,'parent': so.id, 'item_id': so.item_id, 'item_name':  so.item.code + ' - ' + so.item.engname,
                                  'quantity': so.quantity , 'itemuom_id' :so.itemuom_id , 'price': so.price , 'taxpercent': so.taxpercent , 'taxamount': so.taxamount ,
                                  'barcode' : so.barcode , 'linetotal' : so.linetotal ,
                                  'itemuom_name':  so.itemuom.unit.code + ' - ' + str(int(so.itemuom.baseunitfactor)) + ' - ' + so.itemuom.barcode })

        else:
            messages.warning(request, 'You have to Post All Old Operations Before Create New one')

    return render(request, 'inv/dropdownlist/operations_lines_list.html', {'operationslines': soarr })

######### End Load Operation Line


######### Load Operation Line Count
def load_operation_line_count(request):
    currentoperationtype_id = request.GET.get('curroptypreid')
    operation_id = request.GET.get('parentopid')

    operationlines = OperationsLine.objects.filter(operation_id=operation_id).order_by('pk')
    #alloperationlinesdone = OperationsLine.objects.filter(operation__operationtype_id= currentoperationtype_id ).order_by('pk')
    #soarr = []

    alloperationlinesdone = OperationsLine.objects.filter(operation__operationtype_id= currentoperationtype_id ,operation__parent_id=operation_id).exclude (operation__status__keyid= 10004 ).order_by('pk')
    soarr = []
    linescount = 0
    if alloperationlinesdone.count() == 0:

        if operationlines.count() > 0:
            linescount = operationlines.count()

            for so in operationlines:
                #alloperationlinesdone = OperationsLine.objects.filter(operation__operationtype_id=currentoperationtype_id).filter(item=so.item_id)
                alloperationlinesdone = OperationsLine.objects.filter(
                    operation__operationtype_id=currentoperationtype_id, operation__parent_id=operation_id ,item=so.item_id).exclude(
                    operation__status__keyid=10004).order_by('pk')

                #print(alloperationlinesdone.query)
                itemqtydone = alloperationlinesdone.aggregate(Sum('quantity'))
                if alloperationlinesdone.count() > 0 :
                    if itemqtydone['quantity__sum'] is not None:
                        if so.quantity == itemqtydone['quantity__sum']:
                            linescount = linescount - 1
    else:
        messages.warning(request, 'You have to Post All Old Operations Before Create New one')


    return render(request, 'inv/dropdownlist/operations_line_count_list.html', {'linescount': linescount })


######### End Load Operation Line Count




######### Units

class UnitsListView(LoginRequiredMixin, generic.ListView):
    model = Units
    context_object_name = 'units'
    template_name = 'inv/master/list-units.html'


class UnitsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Units
    form_class = UnitsForm
    template_name = 'inv/master/create_units.html'
    success_message = 'Success: Units was created.'
    success_url = reverse_lazy('inv:list-units')

class UnitsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Units
    template_name = 'inv/master/edit_units.html'
    form_class = UnitsForm
    success_message = 'Success: Units was updated.'
    success_url = reverse_lazy("inv:list-units")

    def form_valid(self, form):
        Units = form.save()
        Units.save
        return super(UnitsUpdateView, self).form_valid(form)

class UnitsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Units
    template_name = 'inv/master/delete_units.html'
    success_message = 'Success: Units was deleted.'
    success_url = reverse_lazy('inv:list-units')
######### End Units



######### Warehouses

class WarehousesListView(LoginRequiredMixin, generic.ListView):
    model = Warehouses
    context_object_name = 'warehouses'
    template_name = 'inv/master/list-warehouses.html'


class WarehousesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = Warehouses
    form_class = WarehousesForm
    template_name = 'inv/master/create_warehouses.html'
    success_message = 'Success: Warehouses was created.'
    success_url = reverse_lazy('inv:list-warehouses')

class WarehousesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = Warehouses
    template_name = 'inv/master/edit_warehouses.html'
    form_class = WarehousesForm
    success_message = 'Success: Warehouses was updated.'
    success_url = reverse_lazy("inv:list-warehouses")

    def form_valid(self, form):
        Warehouses = form.save()
        Warehouses.save
        return super(WarehousesUpdateView, self).form_valid(form)

class WarehousesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Warehouses
    template_name = 'inv/master/delete_warehouses.html'
    success_message = 'Success: Warehouses was deleted.'
    success_url = reverse_lazy('inv:list-warehouses')
######### End Warehouses



######### StorageMethodsTypes

class StorageMethodsTypesListView(LoginRequiredMixin, generic.ListView):
    model = StorageMethodsTypes
    context_object_name = 'storagemethodstypes'
    template_name = 'inv/master/list-storagemethodstypes.html'


class StorageMethodsTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = StorageMethodsTypes
    form_class = StorageMethodsTypesForm
    template_name = 'inv/master/create_storagemethodstypes.html'
    success_message = 'Success: Storage Methods Types was created.'
    success_url = reverse_lazy('inv:list-storagemethodstypes')

class StorageMethodsTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = StorageMethodsTypes
    template_name = 'inv/master/edit_storagemethodstypes.html'
    form_class = StorageMethodsTypesForm
    success_message = 'Success: Storage Methods Types was updated.'
    success_url = reverse_lazy("inv:list-storagemethodstypes")

    def form_valid(self, form):
        StorageMethodsTypes = form.save()
        StorageMethodsTypes.save
        return super(StorageMethodsTypesUpdateView, self).form_valid(form)

class StorageMethodsTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = StorageMethodsTypes
    template_name = 'inv/master/delete_storagemethodstypes.html'
    success_message = 'Success: Storage Methods Types was deleted.'
    success_url = reverse_lazy('inv:list-storagemethodstypes')
######### End StorageMethodsTypes



######### InventoriesLocationsTypes

class InventoriesLocationsTypesListView(LoginRequiredMixin, generic.ListView):
    model = InventoriesLocationsTypes
    context_object_name = 'inventorieslocationstypes'
    template_name = 'inv/master/list-inventorieslocationstypes.html'


class InventoriesLocationsTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = InventoriesLocationsTypes
    form_class = InventoriesLocationsTypesForm
    template_name = 'inv/master/create_inventorieslocationstypes.html'
    success_message = 'Success: Inventorie Location Type was created.'
    success_url = reverse_lazy('inv:list-inventorieslocationstypes')

class InventoriesLocationsTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = InventoriesLocationsTypes
    template_name = 'inv/master/edit_inventorieslocationstypes.html'
    form_class = InventoriesLocationsTypesForm
    success_message = 'Success: Inventorie Location Type was updated.'
    success_url = reverse_lazy("inv:list-inventorieslocationstypes")

    def form_valid(self, form):
        InventoriesLocationsTypes = form.save()
        InventoriesLocationsTypes.save
        return super(InventoriesLocationsTypesUpdateView, self).form_valid(form)

class InventoriesLocationsTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = InventoriesLocationsTypes
    template_name = 'inv/master/delete_inventorieslocationstypes.html'
    success_message = 'Success: Inventorie Location Type was deleted.'
    success_url = reverse_lazy('inv:list-inventorieslocationstypes')
######### End InventoriesLocationsTypes


######### InventoriesLocations

class InventoriesLocationsListView(LoginRequiredMixin, generic.ListView):
    model = InventoriesLocations
    context_object_name = 'inventorieslocations'
    template_name = 'inv/master/list-inventorieslocations.html'


class InventoriesLocationsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = InventoriesLocations
    form_class = InventoriesLocationsForm
    template_name = 'inv/master/create_inventorieslocations.html'
    success_message = 'Success: Inventorie Location was created.'
    success_url = reverse_lazy('inv:list-inventorieslocations')

class InventoriesLocationsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = InventoriesLocations
    template_name = 'inv/master/edit_inventorieslocations.html'
    form_class = InventoriesLocationsForm
    success_message = 'Success: Inventorie Location was updated.'
    success_url = reverse_lazy("inv:list-inventorieslocations")

    def form_valid(self, form):
        InventoriesLocations = form.save()
        InventoriesLocations.save
        return super(InventoriesLocationsUpdateView, self).form_valid(form)

class InventoriesLocationsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = InventoriesLocations
    template_name = 'inv/master/delete_inventorieslocations.html'
    success_message = 'Success: Inventorie Location was deleted.'
    success_url = reverse_lazy('inv:list-inventorieslocations')
######### End InventoriesLocations



######### InventoriesBinLocations

class InventoriesBinLocationsListView(LoginRequiredMixin, generic.ListView):
    model = InventoriesBinLocations
    context_object_name = 'inventoriesbinlocations'
    template_name = 'inv/master/list-inventoriesbinlocations.html'


class InventoriesBinLocationsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = InventoriesBinLocations
    form_class = InventoriesBinLocationsForm
    template_name = 'inv/master/create_inventoriesbinlocations.html'
    success_message = 'Success: Inventorie Bin Location was created.'
    success_url = reverse_lazy('inv:list-inventoriesbinlocations')

class InventoriesBinLocationsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = InventoriesBinLocations
    model = InventoriesBinLocations
    template_name = 'inv/master/edit_inventoriesbinlocations.html'
    form_class = InventoriesBinLocationsForm
    success_message = 'Success: Inventorie Bin Location was updated.'
    success_url = reverse_lazy("inv:list-inventoriesbinlocations")

    def form_valid(self, form):
        InventoriesBinLocations = form.save()
        InventoriesBinLocations.save
        return super(InventoriesBinLocationsUpdateView, self).form_valid(form)

class InventoriesBinLocationsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = InventoriesBinLocations
    template_name = 'inv/master/delete_inventoriesbinlocations.html'
    success_message = 'Success: Inventorie Bin Location was deleted.'
    success_url = reverse_lazy('inv:list-inventoriesbinlocations')

    def post(self, request, *args, **kwargs):
        try:
            return super(InventoriesBinLocationsDeleteView, self).delete(*args, **kwargs)
        except:
            return render(request, 'inv/master/list-inventoriesbinlocations.html', {"protected_error": "Couldn't be deleted Inventory Bin Loacation because it's already aligned with others"})

######### End InventoriesBinLocations


######### ItemsTypes

class ItemsTypesListView(LoginRequiredMixin, generic.ListView):
    model = ItemsTypes
    context_object_name = 'itemstypes'
    template_name = 'inv/master/list-itemstypes.html'

class ItemsTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = ItemsTypes
    form_class = ItemsTypesForm
    template_name = 'inv/master/create_itemstypes.html'
    success_message = 'Success: Items Types was created.'
    success_url = reverse_lazy('inv:list-itemstypes')

class ItemsTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = ItemsTypes
    template_name = 'inv/master/edit_itemstypes.html'
    form_class = ItemsTypesForm
    success_message = 'Success: Items Types was updated.'
    success_url = reverse_lazy("inv:list-itemstypes")

    def form_valid(self, form):
        ItemsTypes = form.save()
        ItemsTypes.save
        return super(ItemsTypesUpdateView, self).form_valid(form)

class ItemsTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ItemsTypes
    template_name = 'inv/master/delete_itemstypes.html'
    success_message = 'Success: Items Types was deleted.'
    success_url = reverse_lazy('inv:list-itemstypes')
######### End ItemsTypes

######### ItemsCategories

class ItemsCategoriesListView(LoginRequiredMixin, generic.ListView):
    model = ItemsCategories
    context_object_name = 'itemscategories'
    template_name = 'inv/master/list-itemscategories.html'

class ItemsCategoriesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = ItemsCategories
    form_class = ItemsCategoriesForm
    template_name = 'inv/master/create_itemscategories.html'
    success_message = 'Success: Items Categories was created.'
    success_url = reverse_lazy('inv:list-itemscategories')

class ItemsCategoriesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = ItemsCategories
    template_name = 'inv/master/edit_itemscategories.html'
    form_class = ItemsCategoriesForm
    success_message = 'Success: Items Categories was updated.'
    success_url = reverse_lazy("inv:list-itemscategories")

    def form_valid(self, form):
        ItemsCategories = form.save()
        ItemsCategories.save
        return super(ItemsCategoriesUpdateView, self).form_valid(form)

class ItemsCategoriesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ItemsCategories
    template_name = 'inv/master/delete_itemscategories.html'
    success_message = 'Success: Items Categories was deleted.'
    success_url = reverse_lazy('inv:list-itemscategories')
######### End ItemsCategories


######### ItemsGroups

class ItemsGroupsListView(LoginRequiredMixin, generic.ListView):
    model = ItemsGroups
    context_object_name = 'itemsgroups'
    template_name = 'inv/master/list-itemsgroups.html'

class ItemsGroupsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = ItemsGroups
    form_class = ItemsGroupsForm
    template_name = 'inv/master/create_itemsgroups.html'
    success_message = 'Success: Items Groups was created.'
    success_url = reverse_lazy('inv:list-itemsgroups')

class ItemsGroupsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = ItemsGroups
    template_name = 'inv/master/edit_itemsgroups.html'
    form_class = ItemsGroupsForm
    success_message = 'Success: Items Groups was updated.'
    success_url = reverse_lazy("inv:list-itemsgroups")

    def form_valid(self, form):
        ItemsGroups = form.save()
        ItemsGroups.save
        return super(ItemsGroupsUpdateView, self).form_valid(form)

class ItemsGroupsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ItemsGroups
    template_name = 'inv/master/delete_itemsgroups.html'
    success_message = 'Success: Items Groups was deleted.'
    success_url = reverse_lazy('inv:list-itemsgroups')
######### End ItemsGroups


######### ItemsBrands

class ItemsBrandsListView(LoginRequiredMixin, generic.ListView):
    model = ItemsBrands
    context_object_name = 'itemsbrands'
    template_name = 'inv/master/list-itemsbrands.html'

class ItemsBrandsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = ItemsBrands
    form_class = ItemsBrandsForm
    template_name = 'inv/master/create_itemsbrands.html'
    success_message = 'Success: Items Brands was created.'
    success_url = reverse_lazy('inv:list-itemsbrands')

class ItemsBrandsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = ItemsBrands
    template_name = 'inv/master/edit_itemsbrands.html'
    form_class = ItemsBrandsForm
    success_message = 'Success: Items Brands was updated.'
    success_url = reverse_lazy("inv:list-itemsbrands")

    def form_valid(self, form):
        ItemsBrands = form.save()
        ItemsBrands.save
        return super(ItemsBrandsUpdateView, self).form_valid(form)

class ItemsBrandsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ItemsBrands
    template_name = 'inv/master/delete_itemsbrands.html'
    success_message = 'Success: Items Brands was deleted.'
    success_url = reverse_lazy('inv:list-itemsbrands')
######### End ItemsBrands


######### GenericNamesCategories

class GenericNamesCategoriesListView(LoginRequiredMixin, generic.ListView):
    model = GenericNamesCategories
    context_object_name = 'genericnamescategories'
    template_name = 'inv/master/list-genericnamescategories.html'

class GenericNamesCategoriesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = GenericNamesCategories
    form_class = GenericNamesCategoriesForm
    template_name = 'inv/master/create_genericnamescategories.html'
    success_message = 'Success: Generic Names Categories was created.'
    success_url = reverse_lazy('inv:list-genericnamescategories')

class GenericNamesCategoriesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = GenericNamesCategories
    template_name = 'inv/master/edit_genericnamescategories.html'
    form_class = GenericNamesCategoriesForm
    success_message = 'Success: Generic Names Categories was updated.'
    success_url = reverse_lazy("inv:list-genericnamescategories")

    def form_valid(self, form):
        GenericNamesCategories = form.save()
        GenericNamesCategories.save
        return super(GenericNamesCategoriesUpdateView, self).form_valid(form)

class GenericNamesCategoriesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = GenericNamesCategories
    template_name = 'inv/master/delete_genericnamescategories.html'
    success_message = 'Success: Generic Names Categories was deleted.'
    success_url = reverse_lazy('inv:list-genericnamescategories')
######### End GenericNamesCategories


######### GenericNames

class GenericNamesListView(LoginRequiredMixin, generic.ListView):
    model = GenericNames
    context_object_name = 'genericnames'
    template_name = 'inv/master/list-genericnames.html'

class GenericNamesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = GenericNames
    form_class = GenericNamesForm
    template_name = 'inv/master/create_genericnames.html'
    success_message = 'Success: Generic Names was created.'
    success_url = reverse_lazy('inv:list-genericnames')

class GenericNamesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = GenericNames
    template_name = 'inv/master/edit_genericnames.html'
    form_class = GenericNamesForm
    success_message = 'Success: Generic Names was updated.'
    success_url = reverse_lazy("inv:list-genericnames")

    def form_valid(self, form):
        GenericNames = form.save()
        GenericNames.save
        return super(GenericNamesUpdateView, self).form_valid(form)

class GenericNamesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = GenericNames
    template_name = 'inv/master/delete_genericnames.html'
    success_message = 'Success: Generic Names  was deleted.'
    success_url = reverse_lazy('inv:list-genericnames')
######### End GenericNames

######### ItemsClasses

class ItemsClassesListView(LoginRequiredMixin, generic.ListView):
    model = ItemsClasses
    context_object_name = 'itemsclasses'
    template_name = 'inv/master/list-itemsclasses.html'

class ItemsClassesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = ItemsClasses
    form_class = ItemsClassesForm
    template_name = 'inv/master/create_itemsclasses.html'
    success_message = 'Success: Items Classes was created.'
    success_url = reverse_lazy('inv:list-itemsclasses')

class ItemsClassesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = ItemsClasses
    template_name = 'inv/master/edit_itemsclasses.html'
    form_class = ItemsClassesForm
    success_message = 'Success: Items Classes was updated.'
    success_url = reverse_lazy("inv:list-itemsclasses")

    def form_valid(self, form):
        ItemsClasses = form.save()
        ItemsClasses.save
        return super(ItemsClassesUpdateView, self).form_valid(form)

class ItemsClassesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ItemsClasses
    template_name = 'inv/master/delete_itemsclasses.html'
    success_message = 'Success: Items Classes  was deleted.'
    success_url = reverse_lazy('inv:list-itemsclasses')
######### End ItemsClasses


######### Items

class ItemsListView(LoginRequiredMixin, ListView):
    model = Items
    context_object_name = 'items'
    template_name = 'inv/master/list-items.html'

class ItemsCreateView(LoginRequiredMixin,  CreateView):
    model = Items
    form_class = ItemsForm

    #fields = '__all__'
    template_name = 'inv/master/create_items.html'
    success_message = 'Success: Items was created.'
    success_url = reverse_lazy('inv:list-items')

    def get_context_data(self, **kwargs):
        context = super(ItemsCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['itemsinvlocations'] = ItemsInventoriesLocationsFormSet(self.request.POST, instance=self.object)
            context['itemsinvlocations'].full_clean()

            context['itemsuom'] = ItemsUOMFormSet(self.request.POST, instance=self.object)
            context['itemsuom'].full_clean()

            context['itemsseasonality'] = ItemsSeasonalityFormSet(self.request.POST, instance=self.object)
            context['itemsseasonality'].full_clean()

        else:
            context['itemsuom'] = ItemsUOMFormSet(instance=self.object)
            context['itemsinvlocations'] = ItemsInventoriesLocationsFormSet(instance=self.object)
            context['itemsseasonality'] = ItemsSeasonalityFormSet (instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        Itemslines = context['itemsuom']
        invlocations = context['itemsinvlocations']
        itemsseason = context['itemsseasonality']
        print('validate')
        response = super().form_valid(form)
        n = form.save()

        new_id = n.id

        if invlocations.is_valid():
            print('validate Itemslines')
            invlocations.instance = self.object
            invlocations.save()
            form.save()
        else:
            print(invlocations.errors)
            context['itemsinvlocations'] = ItemsInventoriesLocationsFormSet
            return response

        if Itemslines.is_valid():
            print('validate itemsuom')
            response = super().form_valid(form)
            Itemslines.instance = self.object
            Itemslines.save()
        else:
            print(Itemslines.errors)
            context['itemsuom'] = ItemsUOMFormSet()
            #return response

        cursor = connection.cursor()
        cursor.execute("call in_ItemsAfterSave(" + str(new_id) + "  );")

        if itemsseason.is_valid():
            print('validate itemsseason')
            itemsseason.instance = self.object
            itemsseason.save()
            form.save()

        else:
            print(itemsseason.errors)
            context['itemsseasonality'] = ItemsSeasonalityFormSet
            return response

        return HttpResponseRedirect(self.get_success_url())

class ItemsUpdateView(LoginRequiredMixin, UpdateView):
    model = Items
    form_class = ItemsForm
    #fields = '__all__'
    template_name = 'inv/master/edit_items.html'
    success_message = 'Success: Items was updated.'
    success_url = reverse_lazy("inv:list-items")

    def get_context_data(self, **kwargs):
        context = super(ItemsUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['itemsinvlocations'] = ItemsInventoriesLocationsFormSet(self.request.POST, instance=self.object)
            context['itemsinvlocations'].full_clean()

            context['itemsuom'] = ItemsUOMFormSet(self.request.POST, instance=self.object)
            context['itemsuom'].full_clean()

            context['itemsseasonality'] = ItemsSeasonalityFormSet(self.request.POST, instance=self.object)
            context['itemsseasonality'].full_clean()


        else:
            context['itemsuom'] = ItemsUOMFormSet(instance=self.object)
            context['itemsinvlocations'] = ItemsInventoriesLocationsFormSet(instance=self.object)
            context['itemsseasonality'] = ItemsSeasonalityFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)

        Itemslines = context['itemsuom']
        invlocations = context['itemsinvlocations']
        itemsseason = context['itemsseasonality']


        response = super().form_valid(form)

        if invlocations.is_valid():
            #print('validate invlocations')
            invlocations.instance = self.object
            invlocations.save()
            form.save()
        else:
            print(invlocations.errors)
            context['itemsinvlocations'] = ItemsInventoriesLocationsFormSet
            return response

        print('before Line')


        if Itemslines.is_valid():
            print('validate itemsuom')
            response = super().form_valid(form)
            Itemslines.instance = self.object

            Itemslines.save()

            form.save()



        else:
            print(Itemslines.errors)
            context['itemsuom'] = ItemsUOMFormSet()
            #return response

        print('Before Proc')
        cursor = connection.cursor()
        cursor.execute(
            "call in_ItemsAfterSave(" + str(self.kwargs['pk']) + "  );")

        if itemsseason.is_valid():
            #print('validate itemsseason')
            #print(itemsseason)
            itemsseason.instance = self.object

            itemsseason.save()
            form.save()
        else:
            print(itemsseason.errors)
            context['itemsseasonality'] = ItemsSeasonalityFormSet
            return response



        return HttpResponseRedirect(self.get_success_url())



        #return response

class ItemsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Items
    template_name = 'inv/master/delete_items.html'
    success_message = 'Success: Items was deleted.'
    success_url = reverse_lazy('inv:list-items')


######### End Items

######### ExpensesTypes

class ExpensesTypesListView(LoginRequiredMixin, generic.ListView):
    model = ExpensesTypes
    context_object_name = 'expensestypes'
    template_name = 'inv/setting/list-expensestypes.html'

class ExpensesTypesCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = ExpensesTypes
    form_class = ExpensesTypesForm
    template_name = 'inv/setting/create_expensestypes.html'
    success_message = 'Success: expenses types was created.'
    success_url = reverse_lazy('inv:list-expensestypes')

class ExpensesTypesUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = ExpensesTypes
    template_name = 'inv/setting/edit_expensestypes.html'
    form_class = ExpensesTypesForm
    success_message = 'Success: expenses types was updated.'
    success_url = reverse_lazy("inv:list-expensestypes")

    def form_valid(self, form):
        expensestypes = form.save()
        expensestypes.save
        return super(ExpensesTypesUpdateView, self).form_valid(form)

class ExpensesTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ExpensesTypes
    template_name = 'inv/setting/delete_expensestypes.html'
    success_message = 'Success: expense stypes  was deleted.'
    success_url = reverse_lazy('inv:list-expensestypes')
######### End ExpensesTypes

######### Agencies

class AgenciesListView(LoginRequiredMixin, ListView):
    model = Agencies
    context_object_name = 'agencies'
    template_name = 'inv/setting/list-agencies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AgenciesCreateView(LoginRequiredMixin,  CreateView):
    model = Agencies
    #form_class = agenciesForm
    fields = '__all__'
    template_name = 'inv/setting/create_agencies.html'
    success_message = 'Success: agencies created.'
    success_url = reverse_lazy('inv:list-agencies')

    def get_context_data(self, **kwargs):
        context = super(AgenciesCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['agenciesexpensesline'] = AgenciesExpensesLineFormSet(self.request.POST, instance=self.object)
            context['agenciesexpensesline'].full_clean()
        else:
            context['agenciesexpensesline'] = AgenciesExpensesLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        agenciesexpensesline = context['agenciesexpensesline']
        agenciesexpensesline.clean()
        response = super().form_valid(form)
        if agenciesexpensesline.is_valid():
            print('validate')
            response = super().form_valid(form)
            agenciesexpensesline.instance = self.object
            agenciesexpensesline.save()
            form.save()
            print(agenciesexpensesline.errors)
            #return response
        elif agenciesexpensesline.is_valid() == False:
            print(agenciesexpensesline.errors)
            messages.error(self.request, "Error")
            print(agenciesexpensesline.errors)
            return super().form_invalid(form)

        return response

class AgenciesUpdateView(LoginRequiredMixin, UpdateView):
    model = Agencies
    fields = '__all__'
    template_name = 'inv/setting/edit_agencies.html'
    success_message = 'Success: Agencies was updated.'
    success_url = reverse_lazy("inv:list-agencies")

    def get_context_data(self, **kwargs):
        context = super(AgenciesUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['agenciesexpensesline'] = AgenciesExpensesLineFormSet(self.request.POST, instance=self.object)
            context['agenciesexpensesline'].full_clean()
        else:
            context['agenciesexpensesline'] = AgenciesExpensesLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        agenciesexpensesline = context['agenciesexpensesline']
        agenciesexpensesline.clean()
        if agenciesexpensesline.is_valid():
            response = super().form_valid(form)
            agenciesexpensesline.instance = self.object
            form.save()
            agenciesexpensesline.save()
            return response

        elif agenciesexpensesline.is_valid() == False:
            messages.error(self.request, "Error")
            return super().form_invalid(form)

class AgenciesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Agencies
    template_name = 'inv/setting/delete_agencies.html'
    success_message = 'Success: Agencies was deleted.'
    success_url = reverse_lazy('inv:list-agencies')

######### End Agencies





######### OperationsTypes

class OperationsTypesListView(LoginRequiredMixin, generic.ListView):
    model = OperationsTypes
    context_object_name = 'operationstypes'
    template_name = 'inv/setting/list-operationstypes.html'


class OperationsTypesCreateView(LoginRequiredMixin,  CreateView):
    model = OperationsTypes
    form_class = OperationsTypesForm
    template_name = 'inv/setting/create_operationstypes.html'
    success_message = 'Success: Operations Types was created.'
    success_url = reverse_lazy('inv:list-operationstypes')


    def get_context_data(self, **kwargs):
        context = super(OperationsTypesCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            print('kha')

            context['operationstypesexpensesline'] = OperationsTypesExpensesLineFormSet(self.request.POST, instance=self.object)
            context['operationstypesexpensesline'].full_clean()

            context['operationtypelineview'] = OperationsTypesLineViewsForm(self.request.POST, instance=self.object)
            context['operationtypelineview'].full_clean()
            print(context)


        else:
            context['operationstypesexpensesline'] = OperationsTypesExpensesLineFormSet(instance=self.object)
            context['operationtypelineview'] = OperationsTypesLineViewsForm(instance=self.object)

        #print(context['customersaddress'])
        return context


    def form_valid(self, form):
        context = self.get_context_data(form=form)
        operationstypesexpensesline = context['operationstypesexpensesline']
        operationtypelineview = context['operationtypelineview']
        response = super().form_valid(form)
        print('kha')

        if operationstypesexpensesline.is_valid():
            print('validate operationstypesexpensesline')
            response = super().form_valid(form)
            operationstypesexpensesline.instance = self.object

            operationstypesexpensesline.save()

            form.save()

        else:
            print(operationstypesexpensesline.errors)

        if operationtypelineview.is_valid() :
            response = super().form_valid(form)
            operationtypelineview.instance = self.object
            form.save()
            operationtypelineview.save()
        else:
            context['operationtypelineview'] = OperationsTypesLineViewsFormSet()

        return response



class OperationsTypesUpdateView(LoginRequiredMixin,  UpdateView):
    model = OperationsTypes
    template_name = 'inv/setting/edit_operationstypes.html'
    form_class = OperationsTypesForm
    #fields = '__all__'
    success_message = 'Success: Operations Types was updated.'
    success_url = reverse_lazy("inv:list-operationstypes")


    def get_context_data(self, **kwargs):
        context = super(OperationsTypesUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['operationstypesexpensesline'] = OperationsTypesExpensesLineFormSet(self.request.POST, instance=self.object)
            context['operationstypesexpensesline'].full_clean()

            context['operationtypelineview'] = OperationsTypesLineViewsForm(self.request.POST, instance=self.object)
            context['operationtypelineview'].full_clean()
        else:
            context['operationstypesexpensesline'] = OperationsTypesExpensesLineFormSet(instance=self.object)
            context['operationtypelineview'] = OperationsTypesLineViewsForm(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        operationstypesexpensesline = context['operationstypesexpensesline']
        operationtypelineview = context['operationtypelineview']
        response = super().form_valid(form)

        if operationstypesexpensesline.is_valid():
            print('validate operationstypesexpensesline')
            response = super().form_valid(form)
            operationstypesexpensesline.instance = self.object

            operationstypesexpensesline.save()

            form.save()

        else:
            print(operationstypesexpensesline.errors)

        if operationtypelineview.is_valid() :
            response = super().form_valid(form)
            operationtypelineview.instance = self.object

            operationtypelineview.save()
            form.save()
            print('operationtypelineview')

        else:
            print(operationtypelineview.errors)
            context['operationtypelineview'] = OperationsTypesLineViewsFormSet()

        return response

class OperationsTypesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = OperationsTypes
    template_name = 'inv/setting/delete_operationstypes.html'
    success_message = 'Success: Operations Types was deleted.'
    success_url = reverse_lazy('inv:list-operationstypes')

######### End OperationsTypes


######### Operations

class OperationsListView(LoginRequiredMixin, ListView):

    model = Operations
    context_object_name = 'operations'
    template_name = 'inv/trans/list-operations.html'

    def get_context_data(self, **kwargs):
        otype = self.kwargs
        #print(otype['pk'])
        otype_id = otype['pk']

        context = super().get_context_data(**kwargs)

        if get_language() == 'ar':
            oprationname = OperationsTypes.objects.filter(pk=otype_id).select_related('operationkind').values('arbname','operationkind__keyid')
            oprationnamelst = list(oprationname)
            onamestr = oprationnamelst[0]['arbname']
            okindkeyid = oprationnamelst[0]['operationkind__keyid']
        else:
            oprationname = OperationsTypes.objects.filter(pk=otype_id).select_related('operationkind').values('engname','operationkind__keyid')
            oprationnamelst = list(oprationname)
            onamestr = oprationnamelst[0]['engname']
            okindkeyid = oprationnamelst[0]['operationkind__keyid']


        context['oprationname'] = onamestr
        context['otype_id']=otype_id
        context['okindkeyid']=okindkeyid




        return context

    def get_queryset(self):
        otype = self.kwargs
        otype_id= otype['pk']

        #print(Operations.objects.filter(operationtype_id=otype_id).values('pk','operationtype','number','operationdate','status','invlocation__code','status__engname').query)
        return Operations.objects.filter(operationtype_id=otype_id).values('pk','operationtype','number','operationdate','status','invlocation__code','status__engname','rdstatus__engname','amountstatus__engname')





class OperationsCreateView(LoginRequiredMixin,  CreateView):
    model = Operations
    form_class = OperationsForm

    #fields = '__all__'
    template_name = 'inv/trans/create_operations.html'
    success_message = 'Success: Operation created.'

    #success_url = reverse_lazy('inv:list-operations')



    def get_success_url(self):
        otype = self.kwargs

        otype_id= otype['pk']
        return reverse('inv:list-operations', kwargs={'pk': otype_id})



    def get_context_data(self, **kwargs):
        context = super(OperationsCreateView, self).get_context_data(**kwargs)
        otype = self.kwargs
        otype_id= otype['pk']

        print('get_context_data')


        possibleparent=None
        if get_language() == 'ar':
            oprationname = OperationsTypes.objects.filter(pk=otype_id).values('arbname','code','pk','possibleparent','pricelevel_id','viewparent')
            oprationnamelst = list(oprationname)
            onamestr = oprationnamelst[0]['arbname']
            otcodestr = oprationnamelst[0]['code']
            possibleparent= oprationnamelst[0]['possibleparent']
            viewparent= oprationnamelst[0]['viewparent']
            opricelevel = oprationnamelst[0]['pricelevel_id']

        else:
            oprationname = OperationsTypes.objects.filter(pk=otype_id).values('engname','code','pk','possibleparent','pricelevel_id','viewparent')
            oprationnamelst = list(oprationname)
            onamestr = oprationnamelst[0]['engname']
            otcodestr = oprationnamelst[0]['code']
            possibleparent= oprationnamelst[0]['possibleparent']
            viewparent= oprationnamelst[0]['viewparent']
            opricelevel = oprationnamelst[0]['pricelevel_id']

        parents=None
        if viewparent==True :
            parentids=[]
            for parent in oprationname:
                parentids.append(parent['possibleparent'])

                parents=Operations.objects.filter(operationtype_id__in= list(parentids) ).exclude(rdstatus__keyid= 10033).values('id','operationtype','number','operationdate','status','invlocation__code','status__engname','rdstatus','rdstatus__code','rdstatus__engname')
                #parents=Operations.objects.filter(operationtype_id__in= list(parentids) ).values('id','operationtype','number','operationdate','status','invlocation__code','status__engname','rdstatus__code','rdstatus__engname')
        else:
            parents=[]

        context['parent'] = parents

        inventlocationsids = []
        model = apps.get_model('crm', 'UserBusinessRoles')
        inventlocations = model.objects.filter(user_id = self.request.user.pk ).values('id','invlocation')
        userbusrole_id =0
        if inventlocations == None or inventlocations.count() ==  0 :
            pass
        else :
            print(inventlocations)
            userbusrole_id = inventlocations[0]['id']
            for invloc in inventlocations:
                inventlocationsids.append(invloc['invlocation'])


        model = apps.get_model('crm', 'UserBusinessRolesotline')
        inventlocations = model.objects.filter(userbusinessrole_id = userbusrole_id , operationstype_id = otype_id ).values()

        if inventlocations == None or inventlocations.count() ==  0 :
            context['cancreate'] = 'False'
            context['canedit'] = 'False'
            context['canview'] = 'False'
            context['cansubmit'] = 'False'
            context['canapprove'] = 'False'
            context['canpost'] = 'False'
            context['canrejct'] = 'False'
            context['cancancel'] = 'False'
        else:
            context['cancreate'] =str( to_bool(inventlocations[0]['cancreate']))
            context['canedit'] = 'False'
            context['canview'] = 'False'
            context['cansubmit'] = 'False'
            context['canapprove'] = 'False'
            context['canpost'] = 'False'
            context['canrejct'] = 'False'
            context['cancancel'] = 'False'

            # context['canedit'] =str(to_bool( inventlocations[0]['canedit']))
            # context['canview'] =str(to_bool( inventlocations[0]['canview']))
            # context['cansubmit'] =str(to_bool( inventlocations[0]['cansubmit']))
            # context['canapprove'] =str(to_bool( inventlocations[0]['canapprove']))
            # context['canpost'] = str(to_bool(inventlocations[0]['canpost']))
            # context['canrejct'] = str(to_bool(inventlocations[0]['canrejct']))


        if opricelevel ==None:
            opricelevel = 0

        context['opricelevel'] = opricelevel

        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()

        if companyprofile == None :
            messages.error(self.request, 'Please Create Company')
            return reverse('inv:list-operations', kwargs={'pk': otype_id})

        else:
            context['comusecostcenter1'] = companyprofile['usecostcenter1']
            context['comusecostcenter2'] = companyprofile['usecostcenter2']
            context['comusecostcenter3'] = companyprofile['usecostcenter3']
            context['comusecostcenter4'] = companyprofile['usecostcenter4']

            context['oprationname'] = onamestr

            context['otype_id'] = otype_id
            context['currencydecimal'] = 2
            context['quantitydecimal'] = 2

        try:
            maxid = Operations.objects.filter(operationtype_id=otype_id).count() + 1
        except:
            maxid = 1
        print(otcodestr)
        context['lastnumber'] =  otcodestr + '-' + str(maxid)

        otset = OperationsTypes.objects.filter(id=otype_id).values(
                            'pk','code','engname','arbname','accounttype','usepaymethod',
                            'viewlocationqty','viewaccountbalance','viewlocationqty','allowadditem','allowdeleteitem','allowadjustqty',
                            'defaultqty','defaultdiscounttype','useshipping','operationkind','usedepartment','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4',
                            'usesaleperson','useexpense','usedisc1','usedisc2','usedisc3','pricelevel',
                            'viewparent','viewitem', 'viewitemidentifier', 'viewitemengdesc', 'viewitemarbdesc', 'viewinvbinlocation',
                            'viewquantity', 'viewquantitycount', 'viewisbonus', 'viewitemuom', 'viewunit', 'viewbaseunitfactor',
                            'viewbaseequivalentquantity', 'viewbaseunit', 'viewprice', 'viewpricelist', 'vieworiginalprice',
                            'viewcostprice', 'viewlastdi', 'viewdiscper1', 'viewdiscper2',
                            'viewdiscper3', 'viewdiscamt1', 'viewdiscamt2', 'viewdiscamt3', 'viewbarcode', 'viewexpiredate',
                            'viewbatchnumber', 'viewlotdate', 'viewlotnumber', 'viewserialnumber',
                            'viewlinetotal', 'viewtaxpercent', 'viewtaxamount'
                            )
        lstotset= list(otset)
        acset = LookUp.objects.filter(pk=lstotset[0]['accounttype']).values('keyid')
        lstaccounttype = list(acset)
        print( acset.count( ) )
        print('countArr')
        if acset.count()  >0 :
            context['accounttype']=lstaccounttype[0]['keyid']
            context['accounttypeid']=lstotset[0]['accounttype']
        else:
            context['accounttype'] ='None'
            context['accounttypeid'] = 'None'

        print(context['accounttype'])
        print('accounttype')
        okset = LookUp.objects.filter(pk=lstotset[0]['operationkind']).values('keyid')
        lstoperationkind = list(okset)
        context['operationkind']=lstoperationkind[0]['keyid']
        context['usepaymethod']=lstotset[0]['usepaymethod']
        context['viewlocationqty']=lstotset[0]['viewlocationqty']
        context['viewaccountbalance']=lstotset[0]['viewaccountbalance']
        context['viewlocationqty']=lstotset[0]['viewlocationqty']
        context['allowadditem']=lstotset[0]['allowadditem']
        context['allowdeleteitem']=lstotset[0]['allowdeleteitem']
        context['allowadjustqty']=lstotset[0]['allowadjustqty']
        context['defaultqty']=lstotset[0]['defaultqty']
        context['defaultdiscounttype']=lstotset[0]['defaultdiscounttype']
        context['useshipping']=lstotset[0]['useshipping']
        context['usedepartment']=lstotset[0]['usedepartment']
        context['usecostcenter1']=lstotset[0]['usecostcenter1']
        context['usecostcenter2']=lstotset[0]['usecostcenter2']
        context['usecostcenter3']=lstotset[0]['usecostcenter3']
        context['usecostcenter4']=lstotset[0]['usecostcenter4']
        context['usesaleperson']=lstotset[0]['usesaleperson']
        context['useexpense']=lstotset[0]['useexpense']
        context['usedisc1']=lstotset[0]['usedisc1']
        context['usedisc2']=lstotset[0]['usedisc2']
        context['usedisc3']=lstotset[0]['usedisc3']
        context['pricelevel'] = lstotset[0]['pricelevel']

        context['viewparent'] = lstotset[0]['viewparent']
        context['viewitem'] = lstotset[0]['viewitem']
        context['viewitemidentifier'] = lstotset[0]['viewitemidentifier']
        context['viewitemengdesc'] = lstotset[0]['viewitemengdesc']
        context['viewbarcode'] = lstotset[0]['viewbarcode']
        context['viewitemarbdesc'] = lstotset[0]['viewitemarbdesc']
        context['viewinvbinlocation'] = lstotset[0]['viewinvbinlocation']
        context['viewquantity'] = lstotset[0]['viewquantity']
        context['viewquantitycount'] = lstotset[0]['viewquantitycount']
        context['viewisbonus'] = lstotset[0]['viewisbonus']
        context['viewitemuom'] = lstotset[0]['viewitemuom']
        context['viewunit'] = lstotset[0]['viewunit']
        context['viewbaseunitfactor'] = lstotset[0]['viewbaseunitfactor']
        context['viewbaseequivalentquantity'] = lstotset[0]['viewbaseequivalentquantity']
        context['viewbaseunit'] = lstotset[0]['viewbaseunit']
        context['viewprice'] = lstotset[0]['viewprice']
        context['viewpricelist'] = lstotset[0]['viewpricelist']
        context['vieworiginalprice'] = lstotset[0]['vieworiginalprice']
        context['viewcostprice'] = lstotset[0]['viewcostprice']
        context['viewlastdi'] = lstotset[0]['viewlastdi']
        context['viewdiscper1'] = lstotset[0]['viewdiscper1']
        context['viewdiscper2'] = lstotset[0]['viewdiscper2']
        context['viewdiscper3'] = lstotset[0]['viewdiscper3']
        context['viewdiscamt1'] = lstotset[0]['viewdiscamt1']
        context['viewdiscamt2'] = lstotset[0]['viewdiscamt2']
        context['viewdiscamt3'] = lstotset[0]['viewdiscamt3']
        context['viewbarcode'] = lstotset[0]['viewbarcode']
        context['viewexpiredate'] = lstotset[0]['viewexpiredate']
        context['viewbatchnumber'] = lstotset[0]['viewbatchnumber']
        context['viewlotdate'] = lstotset[0]['viewlotdate']
        context['viewlotnumber'] = lstotset[0]['viewlotnumber']
        context['viewserialnumber'] = lstotset[0]['viewserialnumber']
        context['viewlinetotal'] = lstotset[0]['viewlinetotal']
        context['viewtaxpercent'] = lstotset[0]['viewtaxpercent']
        context['viewtaxamount'] = lstotset[0]['viewtaxamount']



        context['currentdate'] = datetime.now().date().strftime('%Y-%m-%d')
        #context['currentdate'] =  timezone.now().strftime('%Y-%m-%d')

        if self.request.POST:

            context['operationsline'] = OperationsLineFormSet(self.request.POST, instance=self.object)
            context['operationsline'].full_clean()

            context['operationsexpensesline'] = OperationsExpensesLineFormSet(self.request.POST, instance=self.object)
            context['operationsexpensesline'].full_clean()

        else:
            context['operationsline'] = OperationsLineFormSet(instance=self.object)
            context['operationsexpensesline'] = OperationsExpensesLineFormSet(instance=self.object)



        return context


    def form_valid(self, form):
        context = self.get_context_data(form=form)


        otype = self.kwargs
        otype_id= otype['pk']
        oprationname = OperationsTypes.objects.filter(pk=otype_id).values('engname', 'code', 'pk', 'possibleparent',
                                                                          'pricelevel_id', 'viewparent')
        oprationnamelst = list(oprationname)
        onamestr = oprationnamelst[0]['engname']
        otcodestr = oprationnamelst[0]['code']

        try:
            maxid = Operations.objects.filter(operationtype_id=otype_id).count() + 1
        except:
            maxid = 1

        context['lastnumber'] =  otcodestr + '-' + str(maxid)


        inistatus = LookUp.objects.filter(keyid=10001).values('id')
        form.instance.status_id = inistatus[0]['id']  # initiated ID
        form.instance.number = otcodestr + '-' + str(maxid)
        form.instance.statuschangedby=self.request.user
        form.instance.statusdate = timezone.now()
        form.instance.operationdate = timezone.now()
        sign=int( form.instance.operationtype.operationkind.value)
        print(form.instance.parent)


        parentoperationkind = []
        if form.instance.parent != None:
            parentoperationkind  = form.instance.parent.operationtype.operationkind.keyid

        invloc_id = form.instance.invlocation.pk
        wh = InventoriesLocations.objects.filter(id=invloc_id).values('warehouse_id')
        wh_id=wh[0]['warehouse_id']
        operationsline = context['operationsline']
        operationsline.clean()

        operationsexpensesline = context['operationsexpensesline']
        operationsexpensesline.clean()

        print('validate')

        if operationsline.is_valid():

            for childform in  operationsline:
                print()
                print('childform.instance.itemuom.pk')

                item_id = childform.instance.item.pk
                vbarcode = childform.instance.barcode
                vitemunit_id = childform.instance.itemuom.pk
                vbatchnumber = childform.instance.batchnumber
                vexpiredate = childform.instance.expiredate
                vlotnumber = childform.instance.lotnumber
                vserialnumber = childform.instance.serialnumber

                itemident=None
                itemclasskeyid = childform.instance.item.itemclass.itemtrack.keyid
                posibalekinds=[3206,3208,3213]
                if itemclasskeyid== 3001 : #"None" No Tracking
                    print(item_id)
                    print(vitemunit_id)

                    itemident = ItemsIdentifiers.objects.filter(item_id=item_id,itemuom_id=vitemunit_id).values('id').first()
                    print(itemident)
                    itemident_id = itemident['id']

                    # Only create item itenditifier in Purchace And  phisical Count
                    if (itemident_id == None or itemident_id == 0) and (parentoperationkind in posibalekinds):
                        newitemident = ItemsIdentifiers.objects.create(item_id=item_id, itemuom_id=vitemunit_id,barcode=vbarcode + str(self.id))
                        itemident = newitemident


                elif itemclasskeyid== 3002 : #"Serial Number" Tracking
                    itemident = ItemsIdentifiers.objects.filter(item_id=item_id,itemuom_id=vitemunit_id,serialnumber= vserialnumber).values('id').first()
                    itemident_id = itemident['id']
                    # Only create item itenditifier in Purchace And  phisical Count
                    if (itemident_id == None or itemident_id == 0) and (parentoperationkind in posibalekinds):
                        newitemident = ItemsIdentifiers.objects.create(item_id=item_id, itemuom_id=vitemunit_id,barcode=vbarcode + str(self.id),serialnumber= vserialnumber)
                        itemident = newitemident

                elif itemclasskeyid== 3003 : #Lot number Tracking
                    itemident = ItemsIdentifiers.objects.filter(item_id=item_id,itemuom_id=vitemunit_id,lotnumber= vlotnumber).values('id').first()
                    itemident_id = itemident['id']
                    # Only create item itenditifier in Purchace And  phisical Count
                    if (itemident_id == None or itemident_id == 0) and (parentoperationkind in posibalekinds):
                        newitemident = ItemsIdentifiers.objects.create(item_id=item_id, itemuom_id=vitemunit_id,barcode=vbarcode + str(self.id),lotnumber= vlotnumber)
                        itemident = newitemident
                elif itemclasskeyid== 3004 : #Batch Number Tracking
                    itemident = ItemsIdentifiers.objects.filter(item_id=item_id,itemuom_id=vitemunit_id,batchnumber= vbatchnumber).values('id').first()
                    itemident_id = itemident['id']
                    # Only create item itenditifier in Purchace And  phisical Count
                    if (itemident_id == None or itemident_id == 0) and (parentoperationkind in posibalekinds):
                        newitemident = ItemsIdentifiers.objects.create(item_id=item_id, itemuom_id=vitemunit_id,barcode=vbarcode + str(self.id),batchnumber= vbatchnumber)
                        itemident = newitemident
                elif itemclasskeyid== 3005 : #Expiration Date Tracking
                    itemident = ItemsIdentifiers.objects.filter(item_id=item_id,itemuom_id=vitemunit_id,expiredate= vexpiredate).values('id').first()
                    itemident_id = itemident['id']
                    # Only create item itenditifier in Purchace And  phisical Count
                    if (itemident_id == None or itemident_id == 0) and (parentoperationkind in posibalekinds):
                        newitemident = ItemsIdentifiers.objects.create(item_id=item_id, itemuom_id=vitemunit_id,barcode=vbarcode + str(self.id),expiredate= vexpiredate)
                        itemident = newitemident
                elif itemclasskeyid== 3006 : #Serial Number And Expiration Date Tracking
                    itemident = ItemsIdentifiers.objects.filter(item_id=item_id,itemuom_id=vitemunit_id,expiredate= vexpiredate,serialnumber= vserialnumber).values('id').first()
                    itemident_id = itemident['id']
                    # Only create item itenditifier in Purchace And  phisical Count
                    if (itemident_id == None or itemident_id == 0) and (parentoperationkind in posibalekinds):
                        newitemident = ItemsIdentifiers.objects.create(item_id=item_id, itemuom_id=vitemunit_id,barcode=vbarcode + str(self.id),expiredate= vexpiredate,serialnumber= vserialnumber)
                        itemident = newitemident
                elif itemclasskeyid== 3007 : #Batch Number And Expiration Date Tracking
                    itemident = ItemsIdentifiers.objects.filter(item_id=item_id,itemuom_id=vitemunit_id,expiredate= vexpiredate,batchnumber= vbatchnumber).values('id').first()
                    itemident_id = itemident['id']
                    # Only create item itenditifier in Purchace And  phisical Count
                    if (itemident_id == None or itemident_id == 0) and (parentoperationkind in posibalekinds):
                        newitemident = ItemsIdentifiers.objects.create(item_id=item_id, itemuom_id=vitemunit_id,barcode=vbarcode + str(self.id),expiredate= vexpiredate,batchnumber= vbatchnumber)
                        itemident = newitemident

                itemident_id = itemident['id']



                itemunit_id = childform.instance.item.baseunit_id
                baseitemuom_id = childform.instance.item.baseuom_id

                txgrpid = childform.instance.item.taxgroupsale
                if txgrpid == None:
                    # Error No Tax Setting
                    pass


                taxid=TaxesGroupsLine.objects.filter(taxgroup_id=txgrpid,fromdate__lte= datetime.now(),todate__gte=_datetime.date.today()).values('tax_id').first()
                if taxid== None:
                    # Error No Tax Setting
                    pass
                print(taxid)
                #print(taxid['tax_id'])
                #print('taxid')

                vcp = ItemsCosts.objects.filter(item_id=item_id,unit_id=itemunit_id,warehouse_id = wh_id).values('costprice').order_by('-transdate').first()
                if vcp == None:
                    costprice = 0
                else:
                    costprice = vcp['costprice']

                print('barcode')
                print(vbarcode)
                print(childform.instance.barcode)
                childform.instance.originalprice = childform.instance.price
                childform.instance.costprice = costprice
                childform.instance.baseunit_id = itemunit_id
                childform.instance.baseuom_id = baseitemuom_id

                childform.instance.baseunit_id = childform.instance.itemuom.unit_id
                childform.instance.baseunitfactor = childform.instance.itemuom.baseunitfactor

                childform.instance.baseequivalentquantity = childform.instance.itemuom.baseunitfactor * childform.instance.quantity #* sign
                childform.instance.quantity =  childform.instance.quantity #* sign

                childform.instance.tax_id = taxid['tax_id']

                childform.instance.unit_id = itemunit_id
                childform.instance.itemidentifier_id = itemident_id
                childform.instance.lastdi = 1
                print(operationsline.errors)

            response = super().form_valid(form)
            operationsline.instance = self.object
            form.oprationtype = context['otype_id']
            operationsline.save()

            if operationsexpensesline.is_valid():
                response = super().form_valid(form)
                operationsexpensesline.instance = self.object
                form.save()
                operationsline.save()
                operationsexpensesline.save()
                return response
            # elif operationsexpensesline.is_valid() == False:
            #     messages.error(self.request, "Error")
            #     print(operationsexpensesline.errors)
            #     return super().form_invalid(form)

            form.save()



            return response
        elif operationsline.is_valid() == False:
            print(operationsline.errors)
            messages.error(self.request, "Error")
            print(operationsline.errors)
            return super().form_invalid(form)


class OperationsUpdateView(LoginRequiredMixin, UpdateView):
    model = Operations
    form_class = OperationsForm
    #fields = '__all__'
    template_name = 'inv/trans/edit_operations.html'
    success_message = 'Success: Operation was updated.'

    #success_url = reverse_lazy("inv:edit_operations")

    def get_success_url(self):
        otype = self.kwargs
        print(otype)
        otype_id= otype['pk']
        return reverse('inv:edit_operations', kwargs={'pk': otype_id})


    def get_context_data(self, **kwargs):
        context = super(OperationsUpdateView, self).get_context_data(**kwargs)

        op_id = self.kwargs
        otype = Operations.objects.filter(pk=op_id['pk']).values('operationtype_id','number','operationdate','status__keyid')
        otype_id = otype[0]['operationtype_id']
        statuskeyid = otype[0]['status__keyid']
        context['number'] = otype[0]['number']

        context['operationdate'] = otype[0]['operationdate'].strftime('%Y-%m-%d')
        print(context['operationdate'])


        if get_language() == 'ar':
            oprationname = OperationsTypes.objects.filter(pk=otype_id).values('arbname','code','pk','possibleparent','pricelevel_id','viewparent')
            oprationnamelst = list(oprationname)
            onamestr = oprationnamelst[0]['arbname']
            otcodestr = oprationnamelst[0]['code']
            possibleparent= oprationnamelst[0]['possibleparent']
            viewparent= oprationnamelst[0]['viewparent']
            opricelevel = oprationnamelst[0]['pricelevel_id']

        else:
            oprationname = OperationsTypes.objects.filter(pk=otype_id).values('engname','code','pk','possibleparent','pricelevel_id','viewparent')
            oprationnamelst = list(oprationname)
            onamestr = oprationnamelst[0]['engname']
            otcodestr = oprationnamelst[0]['code']
            possibleparent= oprationnamelst[0]['possibleparent']
            viewparent= oprationnamelst[0]['viewparent']
            opricelevel = oprationnamelst[0]['pricelevel_id']



        if viewparent==True :
            parentids=[]
            for parent in oprationname:
                parentids.append(parent['possibleparent'])
            parents=Operations.objects.filter(operationtype_id__in= list(parentids) ).exclude(rdstatus__keyid= 10033) .values('id','operationtype','number','operationdate','status','invlocation__code','status__engname','rdstatus__code','rdstatus__engname')
        else:
            parents=[]

        context['parent'] = parents


        inventlocationsids = []
        model = apps.get_model('crm', 'UserBusinessRoles')
        inventlocations = model.objects.filter(user_id = self.request.user.pk ).values('id','invlocation')
        userbusrole_id =0
        if inventlocations == None or inventlocations.count() ==  0 :
            pass
        else :
            print(inventlocations)
            userbusrole_id = inventlocations[0]['id']
            for invloc in inventlocations:
                inventlocationsids.append(invloc['invlocation'])


        print(inventlocationsids)


        model = apps.get_model('crm', 'UserBusinessRolesotline')
        inventlocations = model.objects.filter(userbusinessrole_id = userbusrole_id , operationstype_id = otype_id ).values()
        if inventlocations == None or inventlocations.count() ==  0 :
            print(inventlocations)
            context['cancreate'] = 'False'
            context['canedit'] = 'False'
            context['canview'] = 'False'
            context['cansubmit'] = 'False'
            context['canapprove'] = 'False'
            context['canpost'] = 'False'
            context['canrejct'] = 'False'
            context['cancancel'] = 'False'
        else:
            if statuskeyid == 10001:   #initiated
                context['cancreate'] = str(inventlocations[0]['cancreate'])
                context['canedit'] = str(inventlocations[0]['canedit'])
                context['canview'] = str(inventlocations[0]['canview'])
                context['cansubmit'] = str(inventlocations[0]['cansubmit'])
                context['canapprove'] = 'False'
                context['canpost'] = 'False'
                context['canrejct'] = 'False'
                context['cancancel'] = 'False'
            elif statuskeyid == 10002:  #submitted
                context['cancreate'] = str(inventlocations[0]['cancreate'])
                context['canedit'] = str(inventlocations[0]['canedit'])
                context['canview'] = str(inventlocations[0]['canview'])
                context['cansubmit'] = 'False'
                context['canapprove'] =str( inventlocations[0]['canapprove'])
                context['canpost'] = 'False'
                context['canrejct'] = str(inventlocations[0]['canrejct'])
                context['cancancel'] = 'False'

            elif statuskeyid == 10003: #Approved
                context['cancreate'] = 'False'
                context['canedit'] = 'False'
                context['canview'] = 'False'
                context['cansubmit'] = 'False'
                context['canapprove'] ='False'
                context['canpost'] = str(inventlocations[0]['canpost'])
                context['canrejct'] = 'False'
                context['cancancel'] = str(inventlocations[0]['cancancel'])

            elif statuskeyid == 10004: #posted
                context['cancreate'] = 'False'
                context['canedit'] = 'False'
                context['canview'] = 'False'
                context['cansubmit'] = 'False'
                context['canapprove'] ='False'
                context['canpost'] = 'False'
                context['canrejct'] = 'False'
                context['cancancel'] = 'False'

            elif statuskeyid == 10003: #Rejcted
                context['cancreate'] = 'False'
                context['canedit'] = 'False'
                context['canview'] = 'False'
                context['cansubmit'] = 'False'
                context['canapprove'] ='False'
                context['canpost'] = 'False'
                context['canrejct'] = 'False'
                context['cancancel'] = 'False'

            elif statuskeyid == 10003: #Canceled
                context['cancreate'] = 'False'
                context['canedit'] = 'False'
                context['canview'] = 'False'
                context['cansubmit'] = 'False'
                context['canapprove'] ='False'
                context['canpost'] = 'False'
                context['canrejct'] = 'False'
                context['cancancel'] = 'False'


            # context['cancreate'] =str( inventlocations[0]['cancreate'])
            # context['canedit'] =str( inventlocations[0]['canedit'])
            # context['canview'] =str( inventlocations[0]['canview'])
            # context['cansubmit'] =str( inventlocations[0]['cansubmit'])
            # context['canapprove'] =str( inventlocations[0]['canapprove'])
            # context['canpost'] = str(inventlocations[0]['canpost'])
            # context['canrejct'] = str(inventlocations[0]['canrejct'])



        print(possibleparent)
        context['opricelevel'] = opricelevel


        print(possibleparent)

        companyprofile=CompanyProfile.objects.values('id','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4').first()
        context['comusecostcenter1'] = companyprofile['usecostcenter1']
        context['comusecostcenter2'] = companyprofile['usecostcenter2']
        context['comusecostcenter3'] = companyprofile['usecostcenter3']
        context['comusecostcenter4'] = companyprofile['usecostcenter4']


        context['oprationname'] = onamestr

        context['otype_id'] = otype_id
        context['currencydecimal'] = 2
        context['quantitydecimal'] = 2




        otset = OperationsTypes.objects.filter(pk=otype_id).values(
                            'pk','code','engname','arbname','accounttype','usepaymethod',
                            'viewlocationqty','viewaccountbalance','viewlocationqty','allowadditem','allowdeleteitem','allowadjustqty',
                            'defaultqty','defaultdiscounttype','useshipping','operationkind','usedepartment','usecostcenter1','usecostcenter2','usecostcenter3','usecostcenter4',
                            'usesaleperson','useexpense','usedisc1','usedisc2','usedisc3',
                            'viewparent','viewitem', 'viewitemidentifier', 'viewitemengdesc', 'viewitemarbdesc', 'viewinvbinlocation',
                            'viewquantity', 'viewquantitycount', 'viewisbonus', 'viewitemuom', 'viewunit', 'viewbaseunitfactor',
                            'viewbaseequivalentquantity', 'viewbaseunit', 'viewprice', 'viewpricelist', 'vieworiginalprice',
                            'viewcostprice', 'viewlastdi', 'viewdiscper1', 'viewdiscper2',
                            'viewdiscper3', 'viewdiscamt1', 'viewdiscamt2', 'viewdiscamt3', 'viewbarcode', 'viewexpiredate',
                            'viewbatchnumber', 'viewlotdate', 'viewlotnumber', 'viewserialnumber',
                            'viewlinetotal', 'viewtaxpercent', 'viewtaxamount'
                            )
        lstotset= list(otset)
        acset = LookUp.objects.filter(pk=lstotset[0]['accounttype']).values('keyid')
        lstaccounttype = list(acset)

        if acset.count()  >0 :
            context['accounttype']=lstaccounttype[0]['keyid']
            context['accounttypeid']=lstotset[0]['accounttype']
        else:
            context['accounttype'] ='None'
            context['accounttypeid']='None'


        okset = LookUp.objects.filter(pk=lstotset[0]['operationkind']).values('keyid')
        lstoperationkind = list(okset)
        context['operationkind']=lstoperationkind[0]['keyid']
        context['usepaymethod']=lstotset[0]['usepaymethod']
        context['viewlocationqty']=lstotset[0]['viewlocationqty']
        context['viewaccountbalance']=lstotset[0]['viewaccountbalance']
        context['viewlocationqty']=lstotset[0]['viewlocationqty']
        context['allowadditem']=lstotset[0]['allowadditem']
        context['allowdeleteitem']=lstotset[0]['allowdeleteitem']
        context['allowadjustqty']=lstotset[0]['allowadjustqty']
        context['defaultqty']=lstotset[0]['defaultqty']
        context['defaultdiscounttype']=lstotset[0]['defaultdiscounttype']
        context['useshipping']=lstotset[0]['useshipping']
        context['usedepartment']=lstotset[0]['usedepartment']
        context['usecostcenter1']=lstotset[0]['usecostcenter1']
        context['usecostcenter2']=lstotset[0]['usecostcenter2']
        context['usecostcenter3']=lstotset[0]['usecostcenter3']
        context['usecostcenter4']=lstotset[0]['usecostcenter4']
        context['usesaleperson']=lstotset[0]['usesaleperson']
        context['useexpense']=lstotset[0]['useexpense']
        context['usedisc1']=lstotset[0]['usedisc1']
        context['usedisc2']=lstotset[0]['usedisc2']
        context['usedisc3']=lstotset[0]['usedisc3']

        context['viewparent'] = lstotset[0]['viewparent']
        context['viewitem'] = lstotset[0]['viewitem']
        context['viewitemidentifier'] = lstotset[0]['viewitemidentifier']
        context['viewitemengdesc'] = lstotset[0]['viewitemengdesc']
        context['viewbarcode'] = lstotset[0]['viewbarcode']
        context['viewitemarbdesc'] = lstotset[0]['viewitemarbdesc']
        context['viewinvbinlocation'] = lstotset[0]['viewinvbinlocation']
        context['viewquantity'] = lstotset[0]['viewquantity']
        context['viewquantitycount'] = lstotset[0]['viewquantitycount']
        context['viewisbonus'] = lstotset[0]['viewisbonus']
        context['viewitemuom'] = lstotset[0]['viewitemuom']
        context['viewunit'] = lstotset[0]['viewunit']
        context['viewbaseunitfactor'] = lstotset[0]['viewbaseunitfactor']
        context['viewbaseequivalentquantity'] = lstotset[0]['viewbaseequivalentquantity']
        context['viewbaseunit'] = lstotset[0]['viewbaseunit']
        context['viewprice'] = lstotset[0]['viewprice']
        context['viewpricelist'] = lstotset[0]['viewpricelist']
        context['vieworiginalprice'] = lstotset[0]['vieworiginalprice']
        context['viewcostprice'] = lstotset[0]['viewcostprice']
        context['viewlastdi'] = lstotset[0]['viewlastdi']
        context['viewdiscper1'] = lstotset[0]['viewdiscper1']
        context['viewdiscper2'] = lstotset[0]['viewdiscper2']
        context['viewdiscper3'] = lstotset[0]['viewdiscper3']
        context['viewdiscamt1'] = lstotset[0]['viewdiscamt1']
        context['viewdiscamt2'] = lstotset[0]['viewdiscamt2']
        context['viewdiscamt3'] = lstotset[0]['viewdiscamt3']
        context['viewbarcode'] = lstotset[0]['viewbarcode']
        context['viewexpiredate'] = lstotset[0]['viewexpiredate']
        context['viewbatchnumber'] = lstotset[0]['viewbatchnumber']
        context['viewlotdate'] = lstotset[0]['viewlotdate']
        context['viewlotnumber'] = lstotset[0]['viewlotnumber']
        context['viewserialnumber'] = lstotset[0]['viewserialnumber']
        context['viewlinetotal'] = lstotset[0]['viewlinetotal']
        context['viewtaxpercent'] = lstotset[0]['viewtaxpercent']
        context['viewtaxamount'] = lstotset[0]['viewtaxamount']



        if self.request.POST:
            context['operationsline'] = OperationsLineFormSet(self.request.POST, instance=self.object)
            context['operationsline'].full_clean()

            context['operationsexpensesline'] = OperationsExpensesLineFormSet(self.request.POST, instance=self.object)
            context['operationsexpensesline'].full_clean()


        else:
            context['operationsline'] = OperationsLineFormSet(instance=self.object)
            context['operationsexpensesline'] = OperationsExpensesLineFormSet(instance=self.object)



        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        print('form_valid')
        op_id = self.kwargs
        retislocked = Operations.objects.filter(pk=op_id['pk']).values('islocked')
        islocked = retislocked[0]['islocked']

        operationsline = context['operationsline']
        operationsline.clean()


        operationsexpensesline = context['operationsexpensesline']
        operationsexpensesline.clean()


        invloc_id = form.instance.invlocation.pk
        wh = InventoriesLocations.objects.filter(id=invloc_id).values('warehouse_id')
        wh_id=wh[0]['warehouse_id']


        okindkeyid = context['operationkind']

        # if self.request.method == 'POST':

            # if islocked == True:
            #     try:
            #         raise forms.ValidationError("Error Record Locked")
            #     except Exception as e:
            #         messages.error(self.request, 'Locked Record')
            #         return HttpResponseRedirect(self.request.path_info)



        if operationsline.is_valid():
            print('operationsline.is_valid')
            try:
                if 'save' in self.request.POST:
                    if islocked == True:
                        try:
                            raise forms.ValidationError("Error Record Locked")
                        except Exception as e:
                            messages.error(self.request, 'Locked Record')
                            return HttpResponseRedirect(self.request.path_info)

                    response = super().form_valid(form)
                    operationsline.instance = self.object
                    for childform in operationsline:
                        item_id = childform.instance.item.pk
                        vitemunit_id = childform.instance.itemuom.pk
                        vbatchnumber = childform.instance.batchnumber
                        vexpiredate = childform.instance.expiredate
                        vlotnumber = childform.instance.lotnumber
                        vserialnumber = childform.instance.serialnumber

                        itemident = None
                        itemclasskeyid = childform.instance.item.itemclass.itemtrack.keyid
                        if itemclasskeyid == 3001:  # "None" No Tracking
                            itemident = ItemsIdentifiers.objects.filter(item_id=item_id,
                                                                        itemuom_id=vitemunit_id).values('id').first()

                        elif itemclasskeyid == 3002:  # "Serial Number" Tracking
                            itemident_id = ItemsIdentifiers.objects.filter(item_id=item_id, itemuom_id=vitemunit_id,serialnumber=vserialnumber).values('id')
                        elif itemclasskeyid == 3003:  # Lot number Tracking
                            itemident_id = ItemsIdentifiers.objects.filter(item_id=item_id, itemuom_id=vitemunit_id,lotnumber=vlotnumber).values('id').first()
                        elif itemclasskeyid == 3004:  # Batch Number Tracking
                            itemident_id = ItemsIdentifiers.objects.filter(item_id=item_id, itemuom_id=vitemunit_id,batchnumber=vbatchnumber).values('id').first()
                        elif itemclasskeyid == 3005:  # Expiration Date Tracking
                            itemident_id = ItemsIdentifiers.objects.filter(item_id=item_id, itemuom_id=vitemunit_id,expiredate=vexpiredate).values('id').first()
                        elif itemclasskeyid == 3006:  # Serial Number And Expiration Date Tracking
                            itemident_id = ItemsIdentifiers.objects.filter(item_id=item_id, itemuom_id=vitemunit_id,expiredate=vexpiredate,serialnumber=vserialnumber).values('id').first()
                        elif itemclasskeyid == 3007:  # Batch Number And Expiration Date Tracking
                            itemident_id = ItemsIdentifiers.objects.filter(item_id=item_id, itemuom_id=vitemunit_id,expiredate=vexpiredate,batchnumber=vbatchnumber).values('id').first()

                        itemident_id = itemident['id']

                        item_id = childform.instance.item.pk
                        txgrpid = childform.instance.item.taxgroupsale
                        itemunit_id = childform.instance.item.baseunit_id
                        baseitemuom_id = childform.instance.item.baseuom_id
                        childform.instance.itemidentifier_id = itemident_id

                        taxid = TaxesGroupsLine.objects.filter(taxgroup_id=txgrpid, fromdate__lte=datetime.now(),
                                                               todate__gte=datetime.now()).values('tax_id').first()

                        vcp = ItemsCosts.objects.filter(item_id=item_id, unit_id=itemunit_id,
                                                        warehouse_id=wh_id).values('costprice').order_by(
                            '-transdate').first()
                        if vcp == None:
                            costprice = 0
                        else:
                            costprice = vcp['costprice']

                        childform.instance.originalprice = childform.instance.price
                        childform.instance.costprice = costprice
                        childform.instance.baseunit_id = itemunit_id
                        childform.instance.baseuom_id = baseitemuom_id

                        childform.instance.baseunit_id = childform.instance.itemuom.unit_id
                        childform.instance.baseunitfactor = childform.instance.itemuom.baseunitfactor

                        childform.instance.baseequivalentquantity = childform.instance.itemuom.baseunitfactor * childform.instance.quantity  # * sign
                        childform.instance.quantity = childform.instance.quantity  # * sign
                        childform.instance.tax_id = taxid['tax_id']

                        childform.instance.unit_id = itemunit_id
                        childform.instance.lastdi = 1


                    operationsline.save()
                    needsaveexp = False
                    for childformexp in operationsexpensesline :
                        if childformexp.instance.agency_id == None:
                            needsaveexp = False
                        else:
                            needsaveexp = True


                    if needsaveexp == True :
                        if operationsexpensesline.is_valid():
                            response = super().form_valid(form)
                            operationsexpensesline.instance = self.object
                            form.save()

                            operationsexpensesline.save()
                            messages.success(self.request,'Successfully Update' )

                            return response

                        elif operationsexpensesline.is_valid() == False:

                            messages.error(self.request, "Error")
                            print(operationsexpensesline.errors)
                            return super().form_invalid(form)

                    else:
                        messages.success(self.request, 'Successfully Update')

                    return response

                elif 'post' in self.request.POST:
                    # Only Goods receive Or Goods Delivery
                    print('post')
                    if okindkeyid== 3219 or okindkeyid == 3218 :
                        try:
                            cursor = connection.cursor()
                            cursor.execute("call in_OperationPostInventory_new(" + str(self.kwargs['pk']) + "," + str(
                                self.request.user.pk) + "  );")
                            messages.success(self.request, 'Successfully Posted')
                            return HttpResponseRedirect(self.get_success_url())
                        except Exception as e:
                            messages.warning(self.request, e)
                            return HttpResponseRedirect(self.request.path_info)
                    else:

                        try:
                            cursor = connection.cursor()
                            cursor.execute("call in_OperationPost(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")
                            messages.success(self.request,'Successfully Posted' )
                            return HttpResponseRedirect(self.get_success_url())
                        except Exception as e:
                            messages.warning(self.request, e)
                            return HttpResponseRedirect(self.request.path_info)

#                        return HttpResponse(e)

                elif 'approve' in self.request.POST:
                    try:
                        cursor = connection.cursor()
                        cursor.execute("call in_OperationApproval(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")
                        messages.success(self.request, 'Successfully Approved')
                        return HttpResponseRedirect(self.get_success_url())
                    except Exception as e:
                        print('errorerror')
                        messages.warning(self.request, e)
                        return HttpResponseRedirect(self.request.path_info)
                        #messages.error(self.request, 'error message kh')
                        #return HttpResponse(e)


                elif 'submit' in self.request.POST:
                    try:
                        print('error submit')
                        cursor = connection.cursor()
                        cursor.execute("call in_OperationSubmit(" + str(self.kwargs['pk']) + "," + str(self.request.user.pk) + "  );")
                        messages.success(self.request, 'Successfully Submited')
                        return HttpResponseRedirect(self.get_success_url())
                    except Exception as e:
                        messages.warning(self.request, e)
                        return HttpResponseRedirect(self.request.path_info)

                        #return HttpResponse(e)


                elif 'reject' in self.request.POST:
                    print('reject')

            except Exception as e:
                print(e)

                #print('error')

        elif operationsline.is_valid() == False:
            print('operationsline.is_valid() == False')
            messages.error(self.request, "Error")
            print(operationsline.errors)
            return super().form_invalid(form)



class OperationsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Operations
    template_name = 'inv/trans/delete_operations.html'
    success_message = 'Success: Operation was deleted.'
    success_url = reverse_lazy('inv:list-operations')

######### End Operations


######### Items

class ItemsPLListView(LoginRequiredMixin, ListView):
    model = Items
    context_object_name = 'itemspricelist'
    template_name = 'inv/master/list-itemspricelist.html'


class ItemsPLUpdateView(LoginRequiredMixin, UpdateView):
    model = Items
    #form_class = ItemsPriceListForm
    fields = ['code','engname','arbname']

    template_name = 'inv/master/edit_itemspricelist.html'
    success_message = 'Success: Items was updated.'
    success_url = reverse_lazy("inv:list-itemspricelist")

    def get_context_data(self, **kwargs):
        context = super(ItemsPLUpdateView, self).get_context_data(**kwargs)
        #context['invslocs'] = InventoriesLocations.objects.all()
        if self.request.POST:
            context['itempricelist'] = ItemsPriceListFormSet(self.request.POST, instance=self.object)
            context['itempricelist'].full_clean()
            #print('context')

        else:
            context['itempricelist'] = ItemsPriceListFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        itempricelist = context['itempricelist']
        response = super().form_valid(form)
        for childform in itempricelist:
            invloc_id = childform.instance.invlocation.pk
            childform.instance.InventoriesLocations = invloc_id
        print('validate')

        if itempricelist.is_valid():
            print('pricelistline')


            print('validate itempricelist')
            response = super().form_valid(form)
            itempricelist.instance = self.object

            itempricelist.save()

            form.save()

        else:

            print(itempricelist.errors)
            context['itempricelist'] = ItemsPriceListFormSet()


        return response


######### End Items Price List


######### Workflow Groups

class WFGroupsListView(LoginRequiredMixin, ListView):
    model = WFGroups
    context_object_name = 'wfgroups'
    template_name = 'inv/setting/list-wfgroups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class WFGroupsCreateView(LoginRequiredMixin,  CreateView):
    model = WFGroups
    #form_class = WFGroupsForm
    fields = '__all__'
    template_name = 'inv/setting/create_wfgroups.html'
    success_message = 'Success: wfgroups created.'
    success_url = reverse_lazy('inv:list-wfgroups')

    def get_context_data(self, **kwargs):
        context = super(WFGroupsCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['wfgroupsusers'] = WFGroupsUsersFormSet(self.request.POST, instance=self.object)
            context['wfgroupsusers'].full_clean()
        else:
            context['wfgroupsusers'] = WFGroupsUsersFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        wfgroupsusers = context['wfgroupsusers']
        wfgroupsusers.clean()
        response = super().form_valid(form)
        if wfgroupsusers.is_valid():
            print('validate')
            response = super().form_valid(form)
            wfgroupsusers.instance = self.object
            wfgroupsusers.save()
            form.save()
            print(wfgroupsusers.errors)
            #return response
        elif wfgroupsusers.is_valid() == False:
            print(wfgroupsusers.errors)
            messages.error(self.request, "Error")
            print(wfgroupsusers.errors)
            return super().form_invalid(form)

        return response

class WFGroupsUpdateView(LoginRequiredMixin, UpdateView):
    model = WFGroups
    fields = '__all__'
    template_name = 'inv/setting/edit_wfgroups.html'
    success_message = 'Success: wfgroups was updated.'
    success_url = reverse_lazy("inv:list-wfgroups")


    def get_context_data(self, **kwargs):
        context = super(WFGroupsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['wfgroupsusers'] = WFGroupsUsersFormSet(self.request.POST, instance=self.object)
            context['wfgroupsusers'].full_clean()
        else:
            context['wfgroupsusers'] = WFGroupsUsersFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        wfgroupsusers = context['wfgroupsusers']
        wfgroupsusers.clean()
        print('validate')
        if wfgroupsusers.is_valid():
            response = super().form_valid(form)
            wfgroupsusers.instance = self.object
            form.save()
            wfgroupsusers.save()
            return response

        elif wfgroupsusers.is_valid() == False:
            messages.error(self.request, "Error")
            print(wfgroupsusers.errors)
            return super().form_invalid(form)

class WFGroupsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = WFGroups
    template_name = 'inv/setting/delete_wfgroups.html'
    success_message = 'Success: wf groups was deleted.'
    success_url = reverse_lazy('inv:list-wfgroups')

######### End Workflow Groups

######### WFActionsStatus

class WFActionsStatusListView(LoginRequiredMixin, generic.ListView):
    model = WFActionsStatus
    context_object_name = 'wfactionsstatus'
    template_name = 'inv/setting/list-wfactionsstatus.html'


class WFActionsStatusCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = WFActionsStatus
    form_class = WFActionsStatusForm
    template_name = 'inv/setting/create_wfactionsstatus.html'
    success_message = 'Success: Units was created.'
    success_url = reverse_lazy('inv:list-wfactionsstatus')

class WFActionsStatusUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = WFActionsStatus
    form_class = WFActionsStatusForm
    template_name = 'inv/setting/edit_wfactionsstatus.html'
    success_message = 'Success: wfactionsstatus was updated.'
    success_url = reverse_lazy("inv:list-wfactionsstatus")

    def form_valid(self, form):
        wfactionsstatus = form.save()
        wfactionsstatus.save
        return super(WFActionsStatusUpdateView, self).form_valid(form)

class WFActionsStatusDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = WFActionsStatus
    template_name = 'inv/setting/delete_wfactionsstatus.html'
    success_message = 'Success: WF Actions Status was deleted.'
    success_url = reverse_lazy('inv:list-wfactionsstatus')
######### End WFActionsStatus


######### WF Operations Cycles

class WFOperationsCyclesListView(LoginRequiredMixin, ListView):
    model = WFOperationsCycles
    context_object_name = 'wfoperationscycles'
    template_name = 'inv/setting/list-wfoperationscycles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class WFOperationsCyclesCreateView(LoginRequiredMixin,  CreateView):
    model = WFOperationsCycles
    #form_class = WFOperationsCyclesForm
    fields = '__all__'
    template_name = 'inv/setting/create_wfoperationscycles.html'
    success_message = 'Success: wfgroups created.'
    success_url = reverse_lazy('inv:list-wfoperationscycles')

    def get_context_data(self, **kwargs):
        context = super(WFOperationsCyclesCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['wfoperationsCyclesline'] = WFOperationsCyclesLineFormSet(self.request.POST, instance=self.object)
            context['wfoperationsCyclesline'].full_clean()
        else:
            context['wfoperationsCyclesline'] = WFOperationsCyclesLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        wfoperationsCyclesline = context['wfoperationsCyclesline']
        wfoperationsCyclesline.clean()
        response = super().form_valid(form)
        if wfoperationsCyclesline.is_valid():
            print('validate')
            response = super().form_valid(form)
            wfoperationsCyclesline.instance = self.object
            wfoperationsCyclesline.save()
            form.save()
            print(wfoperationsCyclesline.errors)
            #return response
        elif wfoperationsCyclesline.is_valid() == False:
            print(wfoperationsCyclesline.errors)
            messages.error(self.request, "Error")
            print(wfoperationsCyclesline.errors)
            return super().form_invalid(form)

        return response

class WFOperationsCyclesUpdateView(LoginRequiredMixin, UpdateView):
    model = WFOperationsCycles
    fields = '__all__'
    template_name = 'inv/setting/edit_wfoperationscycles.html'
    success_message = 'Success: wfoperationsCyclesline was updated.'
    success_url = reverse_lazy("inv:list-wfoperationscycles")


    def get_context_data(self, **kwargs):
        context = super(WFOperationsCyclesUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['wfoperationsCyclesline'] = WFOperationsCyclesLineFormSet(self.request.POST, instance=self.object)
            context['wfoperationsCyclesline'].full_clean()
        else:
            context['wfoperationsCyclesline'] = WFOperationsCyclesLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        wfoperationsCyclesline = context['wfoperationsCyclesline']
        wfoperationsCyclesline.clean()
        print('validate')
        response = super().form_valid(form)

        if wfoperationsCyclesline.is_valid():
            try:
                print('suc')
                response = super().form_valid(form)
                wfoperationsCyclesline.instance = self.object
                form.save()
                wfoperationsCyclesline.save()

                return response
            except Exception as e:
                print(e)

                #print('error')

        elif wfoperationsCyclesline.is_valid() == False:
            messages.error(self.request, "Error")
            print(wfoperationsCyclesline.errors)
            return super().form_invalid(form)

class WFOperationsCyclesDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = WFOperationsCycles
    template_name = 'inv/setting/delete_wfoperationscycles.html'
    success_message = 'Success: WFOperationsCycles was deleted.'
    success_url = reverse_lazy('inv:list-wfoperationscycles')

######### End WF Operations Cycles


##------------- START TARGET VIEWS

class TargetBildingBlocksListView(LoginRequiredMixin, ListView):
    model = TargetBuildingBlocks
    context_object_name = 'targetbuildingblocks'
    template_name = 'inv/target/list-targetbuildingblocks.html'

    def get_context_data(self, **kwargs):
        years = int(_datetime.date.today().year)
        context = super(TargetBildingBlocksListView, self).get_context_data(**kwargs)
        context['targetbuildingblocks'] = TargetBuildingBlocks.objects.all().filter(year=years)

        return context

class TargetBuildingBlocksCreateView(LoginRequiredMixin, CreateView):

    model = TargetBuildingBlocks
    template_name = 'inv/target/create_targetbuildingblocks.html'
    fields = '__all__'
    success_url = reverse_lazy('inv:targetbuildingblocks')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblocks'] = TargetBuildingBlocksItemsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocks'].full_clean()
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocksExcetion'].full_clean()
        else:
            context['targetbuildingblocks'] = TargetBuildingBlocksItemsFormSet(instance=self.object)
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        targetbuildingblocks = context['targetbuildingblocks']
        targetbuildingblocksExcetion = context['targetbuildingblocksExcetion']
        print('start - TargetBuildingBlocksCreateView')
        if targetbuildingblocks.is_valid() == False:
            print(targetbuildingblocks.errors)

            return self.render_to_response(self.get_context_data(form=form, targetbuildingblocks=targetbuildingblocks))
        if targetbuildingblocksExcetion.is_valid():
            response = super().form_valid(form)
            print('targetbuildingblocksExcetion - TargetBuildingBlocksCreateView')
            targetbuildingblocksExcetion.instance = self.object
            targetbuildingblocksExcetion.save()
        else:
            print('targetbuildingblocksExcetion - TargetBuildingBlocksCreateView')
            print(targetbuildingblocksExcetion.errors)

        if targetbuildingblocks.is_valid():
            print('targetbuildingblocks.is_valid() - TargetBuildingBlocksCreateView')

            response = super().form_valid(form)
            targetbuildingblocks.instance = self.object
            print('before save new Record')
            targetbuildingblocks.save()

        else:
            print('targetbuildingblocks.is_valid() - TargetBuildingBlocksCreateView')
            print(targetbuildingblocks.errors)
            context['targetbuildingblocks'] = TargetBuildingBlocksItemsFormSet()
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet()
        return response

class TargetBuildingBlocksRebuildView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        print('get get get get TargetBuildingBlocksRebuildView')
        target_id = int(request.GET.get('id'))

        targets = TargetBuildingBlocks.objects.get(pk=target_id)
        targetproducts = TargetBuildingBlocksItems.objects.filter(targetbuildingblocks_id=targets.id).values()


        for tproduct in targetproducts:
            print('tproduct')
            print(tproduct['id'])
            instance = TargetBuildingBlocksItems.objects.get(pk= tproduct['id'])
            print(instance.id)

            #signals.post_save_TargetBuildingBlocksItems(sender=TargetBuildingBlocksItems, instance=instance, created=False)
        return redirect('/inv/targetbuildingblocks/')

class TargetBuildingBlocksAccountsRebuildView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        print('TargetBuildingBlocksAccountsRebuildView')

        target_id = int(request.GET.get('id'))
        targets = TargetBuildingBlocksAccounts.objects.get(pk=target_id)
        targetproducts = TargetBuildingBlocksAccountsItems.objects.filter(targetbuildingblocksaccounts=targets.id)
        for tproduct in targetproducts:
            instance = TargetBuildingBlocksAccountsItems.objects.get(pk= tproduct.id)
            signals.post_save_TargetBuildingBlocksAccounts(sender=TargetBuildingBlocksAccountsItems, instance=instance, created=False)
        return redirect('/inv/targetbuildingblocksaccounts/')


class TargetBuildingBlocksUpdateView(LoginRequiredMixin, UpdateView):
    model = TargetBuildingBlocks
    template_name = 'inv/target/edit_targetbuildingblocks.html'
    fields = '__all__'
    success_url = reverse_lazy('inv:targetbuildingblocks')

    def get_context_data(self, **kwargs):
        print('TargetBuildingBlocksUpdateView')
        context = super(TargetBuildingBlocksUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblocks'] = TargetBuildingBlocksItemsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocks'].full_clean()
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocksExcetion'].full_clean()
        else:
            context['targetbuildingblocks'] = TargetBuildingBlocksItemsFormSet(instance=self.object)
            context['targetbuildingblocksExcetion'] = TargetBuildingBlocksExceptFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['targetbuildingblocks']
        targetbuildingblocksExcetion = context['targetbuildingblocksExcetion']
        if targetbuildingblocksExcetion.is_valid():
            response = super().form_valid(form)
            targetbuildingblocksExcetion.instance = self.object
            targetbuildingblocksExcetion.save()
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class TargetBuildingBlocksAccountsListView(LoginRequiredMixin, ListView):
    model = TargetBuildingBlocksAccounts
    context_object_name = 'targetbuildingblocksaccounts'
    template_name = 'inv/target/list-targetbuildingblocksaccounts.html'

    def get_context_data(self, **kwargs):
        years = int(_datetime.date.today().year)
        context = super(TargetBuildingBlocksAccountsListView, self).get_context_data(**kwargs)
        context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccounts.objects.all().filter(year=years)

        return context



class TargetBuildingBlocksAccountsCreateView(LoginRequiredMixin, CreateView):
    model = TargetBuildingBlocksAccounts
    template_name = 'inv/target/create_targetbuildingblocksaccounts.html'
    fields = ['code','engname','arbname','account','customer_size','channel','year']
    success_url = reverse_lazy('inv:targetbuildingblocksaccounts')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksAccountsCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsItemsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocksaccounts'].full_clean()
        else:
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsItemsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        targetbuildingblocksaccounts = context['targetbuildingblocksaccounts']
        if targetbuildingblocksaccounts.is_valid() == False:
            print(targetbuildingblocksaccounts.errors)
            return self.render_to_response(self.get_context_data(form=form, targetbuildingblocksaccounts=targetbuildingblocksaccounts))
        if targetbuildingblocksaccounts.is_valid():
            response = super().form_valid(form)
            targetbuildingblocksaccounts.instance = self.object
            targetbuildingblocksaccounts.save()
        else:
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsItemsFormSet()

        return response

class TargetBuildingBlocksAccountsUpdateView(LoginRequiredMixin, UpdateView):
    model = TargetBuildingBlocksAccounts
    template_name = 'inv/target/edit_targetbuildingblocksaccounts.html'
    fields = '__all__'
    success_url = reverse_lazy('inv:targetbuildingblocksaccounts')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksAccountsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            print('formset.errors')
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsItemsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblocksaccounts'].full_clean()
        else:
            context['targetbuildingblocksaccounts'] = TargetBuildingBlocksAccountsItemsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        print('formset.errors')

        context = self.get_context_data(form=form)
        formset = context['targetbuildingblocksaccounts']

        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            print(formset.errors)
            return super().form_invalid(form)

class TargetBuildingBlocksChannelsListView(LoginRequiredMixin, ListView):
    model = TargetBuildingBlocksChannels
    context_object_name = 'targetbuildingblockschannels'
    template_name = 'inv/target/list-targetbuildingblockschannels.html'

    def get_context_data(self, **kwargs):
        years = int(_datetime.date.today().year)
        context = super(TargetBuildingBlocksChannelsListView, self).get_context_data(**kwargs)
        context['targetbuildingblockschannels'] = TargetBuildingBlocksChannels.objects.all().filter(year=years)

        return context

class TargetBuildingBlocksChannelsCreateView(LoginRequiredMixin, CreateView):
    model = TargetBuildingBlocksChannels
    template_name = 'inv/target/create_targetbuildingblockschannels.html'
    fields = ['code','arbname','engname','customer_size','channel','year']
    success_url = reverse_lazy('inv:targetbuildingblockschannels')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksChannelsCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsItemsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblockschannels'].full_clean()
        else:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsItemsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        targetbuildingblockschannels = context['targetbuildingblockschannels']
        if targetbuildingblockschannels.is_valid() == False:
            print(targetbuildingblockschannels.errors)
            return self.render_to_response(self.get_context_data(form=form, targetbuildingblockschannels=targetbuildingblockschannels))
        if targetbuildingblockschannels.is_valid():
            response = super().form_valid(form)
            targetbuildingblockschannels.instance = self.object
            targetbuildingblockschannels.save()
        else:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsItemsFormSet()
        return response

class TargetBuildingBlocksChannelsUpdateView(LoginRequiredMixin, UpdateView):
    model = TargetBuildingBlocksChannels
    template_name = 'inv/target/edit_targetbuildingblockschannels.html'
    fields = '__all__'
    success_url = reverse_lazy('inv:targetbuildingblockschannels')

    def get_context_data(self, **kwargs):
        context = super(TargetBuildingBlocksChannelsUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsItemsFormSet(self.request.POST, instance=self.object)
            context['targetbuildingblockschannels'].full_clean()
        else:
            context['targetbuildingblockschannels'] = TargetBuildingBlocksChannelsItemsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['targetbuildingblockschannels']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)

class TargetBuildingBlocksChannelsRebuildView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        print('TargetBuildingBlocksChannelsRebuildView')
        target_id = int(request.GET.get('id'))
        targets = TargetBuildingBlocksChannels.objects.get(pk=target_id)
        targetproducts = TargetBuildingBlocksChannelsItems.objects.filter(targetbuildingblockschannels=targets.id)
        for tproduct in targetproducts:
            instance = TargetBuildingBlocksChannelsItems.objects.get(pk= tproduct.id)
            signals.post_save_TargetBuildingBlocksChannels(sender=TargetBuildingBlocksChannelsItems, instance=instance, created=False)
        return redirect('/inv/targetbuildingblockschannels/')


##------------- END TARGET VIEWS

###------------ Target Reports
class CustTargetRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')

        try:
            channel_id = int(request.GET.get('channel'))
        except:
            channel_id = 9898989998

        try:
            areas_id = int(request.GET.get('area'))
        except:
            areas_id = 9898989998

        try:
            city_id = int(request.GET.get('city'))
        except:
            city_id = 9898989998

        try:
            month_id = int(request.GET.get('month'))
        except:
            month_id = 9898989998
        print(channel_id)
        print(areas_id)
        print(city_id)

        today = _datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        current_month1 = months[today.month]
        current_month = int(current_month1)
        print(currentYear)
        financialyears = FiscalYearsPeriods.objects.filter(fiscalyear__code=currentYear ).values('code','rank')
        print(financialyears)
        print(current_month)

        monthn = 0
        for financialyear in financialyears:
            print(financialyear['rank'])

            if financialyear['rank'] == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear['rank'] == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear['rank'] == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear['rank'] == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear['rank'] == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear['rank'] == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear['rank'] == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear['rank'] == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear['rank'] == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear['rank'] == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear['rank'] == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear['rank'] == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31
        channels = CustomersClasses.objects.all()
        categories = CustomersCategories.objects.all()
        customers = Customers.objects.all()
        areas = Areas.objects.all()

        cities = Cities.objects.all()
        if areas_id != 9898989998:
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities
        print('khaldoun')
        #parent_cat = Channel.objects.all().filter(parent_channel_id=channel_id)
        #if parent_cat.count() == 0:
        if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
            targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
        elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
            targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
        elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
            targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
        elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
            targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
        elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
            targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
                channel_id=channel_id)
        elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
            targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                channel_id=channel_id)
        elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
            targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
                channel_id=channel_id).filter(city_id=city_id)

        else:
            targettransactions = TargetTransactions.objects.all()

        #else:
            # if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
            #     targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            # elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
            #     targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_cat)
            # elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
            #     targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            # elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
            #     targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            # elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
            #     targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(
            #         channel_id__in=parent_cat)
            # elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
            #     targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
            #         channel_id__in=parent_cat)
            # elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
            #     targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(
            #         channel_id__in=parent_cat).filter(city_id=city_id)
            #
            # else:
            #     targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        #salesorders = SalesOrder.objects.all()

        channelcount = channels.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        channelear = []
        catear = []

        if month_id != 9898989998:
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if customers.count() == 0:
            channelear.append({'customer': '',
                               't1': 0, 't2': 0, 't3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0, 't9': 0,
                               't10': 0, 't11': 0, 't12': 0,
                               'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0, 'q6': 0, 'q7': 0, 'q8': 0, 'q9': 0,
                               'q10': 0, 'q11': 0, 'q12': 0,
                               'monthint': 0,

                               })


        print('channelear')
        print(channelear)

        for customer in customers:
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            print(customer)
            qt1 = targettransactions.annotate(total=Sum(F('m1') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t1 = qt1.aggregate(Sum('total'))

            qt2 = targettransactions.annotate(total=Sum(F('m2') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t2 = qt2.aggregate(Sum('total'))

            qt3 = targettransactions.annotate(total=Sum(F('m3') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t3 = qt3.aggregate(Sum('total'))

            qt4 = targettransactions.annotate(total=Sum(F('m4') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t4 = qt4.aggregate(Sum('total'))

            qt5 = targettransactions.annotate(total=Sum(F('m5') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t5 = qt5.aggregate(Sum('total'))

            qt6 = targettransactions.annotate(total=Sum(F('m6') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t6 = qt6.aggregate(Sum('total'))

            qt7 = targettransactions.annotate(total=Sum(F('m7') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t7 = qt7.aggregate(Sum('total'))

            qt8 = targettransactions.annotate(total=Sum(F('m8') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t8 = qt8.aggregate(Sum('total'))

            qt9 = targettransactions.annotate(total=Sum(F('m9') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t9 = qt9.aggregate(Sum('total'))

            qt10 = targettransactions.annotate(total=Sum(F('m10') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t10 = qt10.aggregate(Sum('total'))

            qt11 = targettransactions.annotate(total=Sum(F('m11') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t11 = qt11.aggregate(Sum('total'))

            qt12 = targettransactions.annotate(total=Sum(F('m12') * F('price'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            t12 = qt12.aggregate(Sum('total'))
            if t1['total__sum'] != None:
                t1 = t1['total__sum']
            else:
                t1 = 0
            if t2['total__sum'] != None:
                t2 = t2['total__sum']
            else:
                t2 = 0
            if t3['total__sum'] != None:
                t3 = t3['total__sum']
            else:
                t3 = 0
            if t4['total__sum'] != None:
                t4 = t4['total__sum']
            else:
                t4 = 0
            if t5['total__sum'] != None:
                t5 = t5['total__sum']
            else:
                t5 = 0
            if t6['total__sum'] != None:
                t6 = t6['total__sum']
            else:
                t6 = 0
            if t7['total__sum'] != None:
                t7 = t7['total__sum']
            else:
                t7 = 0
            if t8['total__sum'] != None:
                t8 = t8['total__sum']
            else:
                t8 = 0
            if t9['total__sum'] != None:
                t9 = t9['total__sum']
            else:
                t9 = 0
            if t10['total__sum'] != None:
                t10 = t10['total__sum']
            else:
                t10 = 0
            if t11['total__sum'] != None:
                t11 = t11['total__sum']
            else:
                t11 = 0
            if t12['total__sum'] != None:
                t12 = t12['total__sum']
            else:
                t12 = 0

            qq1 = targettransactions.annotate(qty=Sum(F('m1'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q1 = qq1.aggregate(Sum('qty'))

            qq2 = targettransactions.annotate(qty=Sum(F('m2'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q2 = qq2.aggregate(Sum('qty'))

            qq3 = targettransactions.annotate(qty=Sum(F('m3'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q3 = qq3.aggregate(Sum('qty'))

            qq4 = targettransactions.annotate(qty=Sum(F('m4'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q4 = qq4.aggregate(Sum('qty'))

            qq5 = targettransactions.annotate(qty=Sum(F('m5'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q5 = qq5.aggregate(Sum('qty'))

            qq6 = targettransactions.annotate(qty=Sum(F('m6'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q6 = qq6.aggregate(Sum('qty'))

            qq7 = targettransactions.annotate(qty=Sum(F('m7'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q7 = qq7.aggregate(Sum('qty'))

            qq8 = targettransactions.annotate(qty=Sum(F('m8'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q8 = qq8.aggregate(Sum('qty'))

            qq9 = targettransactions.annotate(qty=Sum(F('m9'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q9 = qq9.aggregate(Sum('qty'))

            qq10 = targettransactions.annotate(qty=Sum(F('m10'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q10 = qq10.aggregate(Sum('qty'))

            qq11 = targettransactions.annotate(qty=Sum(F('m11'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q11 = qq11.aggregate(Sum('qty'))

            qq12 = targettransactions.annotate(qty=Sum(F('m12'), output_field=IntegerField())).filter(
                created_date__year=currentYear).filter(customer_id=customer.id)
            q12 = qq12.aggregate(Sum('qty'))

            if q1['qty__sum'] != None:
                q1 = q1['qty__sum']
            else:
                q1 = 0
            if q2['qty__sum'] != None:
                q2 = q2['qty__sum']
            else:
                q2 = 0
            if q3['qty__sum'] != None:
                q3 = q3['qty__sum']
            else:
                q3 = 0
            if q4['qty__sum'] != None:
                q4 = q4['qty__sum']
            else:
                q4 = 0
            if q5['qty__sum'] != None:
                q5 = q5['qty__sum']
            else:
                q5 = 0
            if q6['qty__sum'] != None:
                q6 = q6['qty__sum']
            else:
                q6 = 0
            if q7['qty__sum'] != None:
                q7 = q7['qty__sum']
            else:
                q7 = 0
            if q8['qty__sum'] != None:
                q8 = q8['qty__sum']
            else:
                q8 = 0
            if q9['qty__sum'] != None:
                q9 = q9['qty__sum']
            else:
                q9 = 0
            if q10['qty__sum'] != None:
                q10 = q10['qty__sum']
            else:
                q10 = 0
            if q11['qty__sum'] != None:
                q11 = q11['qty__sum']
            else:
                q11 = 0
            if q12['qty__sum'] != None:
                q12 = q12['qty__sum']
            else:
                q12 = 0

            mm = 1
            salestotal = 0
            qtytotal = 0
            while mm <= 12:
                montht = 'm' + str(mm)
                qsalestotal = targettransactions.annotate(
                    total=Sum(F(montht) * F('price'), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(customer_id=customer.id)
                qqsalestotal = qsalestotal.aggregate(Sum('total'))
                try:
                    salestotal = salestotal + qqsalestotal['total__sum']
                except:
                    salestotal = 0
                if salestotal == None:
                    salestotal = 0


                qqtytotal = targettransactions.annotate(qty=Sum(F(montht), output_field=IntegerField())).filter(
                    created_date__year=currentYear).filter(customer_id=customer.id)
                qqqtytotal = qqtytotal.aggregate(Sum('qty'))
                try:
                    qtytotal = qtytotal + qqqtytotal['qty__sum']
                except:
                    qtytotal = 0
                if qtytotal == None:
                    qtytotal = 0
                mmname = calendar.month_name[mm]
                mm += 1
            if salestotal != 0:
                catear.append({'customer': customer.engname, 'salestotal': salestotal, 'qtytotal': qtytotal})

            mname = calendar.month_name[thismonth]
            if t1 != 0 and t2 != 0 and t3 != 0 and t4 != 0 and t5 != 0 and t6 != 0 and t7 != 0 and t8 != 0 and t9 != 0 and t10 != 0 and t11 != 0 and t12 != 0:
                channelear.append({'customer': customer.engname,
                                   't1': t1, 't2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 't8': t8,
                                   't9': t9, 't10': t10, 't11': t11, 't12': t12,
                                   'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5, 'q6': q6, 'q7': q7, 'q8': q8,
                                   'q9': q9, 'q10': q10, 'q11': q11, 'q12': q12,
                                   'monthint': thismonth,

                                   })

        mname = calendar.month_name[thismonth]
        print(mname)
        print('mname')

        context = {
            #'salesorders': salesorders,
            'channelear': channelear,
            'channels': channels,
            'categories': categories,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'catear': catear,

        }
        return render(request, 'inv/target/report/customer-target.html', context)



###------------ End  Target Reports

def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))




