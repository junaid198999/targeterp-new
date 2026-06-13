
from django.urls import path
from . import views
from .importexport  import *

app_name = "inv"

urlpatterns = [
    #path('', views.index, name ='index'),

#Dropdown
    path("ajax/load-itemprice/", views.load_itemprice, name="ajax_load_itemprice"),
    path("ajax/load-itemuom/", views.load_itemuom, name="ajax_load_itemuom"),
    path("ajax/load-itembarcode/", views.load_itembarcode, name="ajax_load_itembarcode"),
    path("ajax/load-accountbalance/", views.load_accountbalance, name="ajax_load_accountbalance"),



    path("ajax/load_operations/", views.load_operations, name="ajax_load_operations"),
    path("ajax/load_itemtaxvalue/", views.load_itemtaxvalue, name="ajax_load_itemtaxvalue"),
       #add 28-05-22
    path("ajax/load_agencytaxvalue/", views.load_agencytaxvalue, name="ajax_load_agencytaxvalue"),
  


    path("ajax/load-operations-detail-info/", views.load_operation_Details_Info, name="ajax_load-operations-detail-info"),
    path("ajax/load-invlocations-detail-info/", views.load_invlocation_Details_Info, name="ajax_load-invlocations-detail-info"),
    path("ajax/load-operations-lines/", views.load_operation_line, name="ajax_load-operations-lines"),
    path("ajax/load-operations-lines-count/", views.load_operation_line_count, name="ajax_load-operations-lines-count"),


#Units
    path("units/", views.UnitsListView.as_view(), name = "list-units"),
    path("units/create/", views.UnitsCreateView.as_view(), name="create_units"),
    path("units/update/<int:pk>", views.UnitsUpdateView.as_view(), name="edit_units"),
    path("units/<int:pk>/delete/", views.UnitsDeleteView.as_view(), name="delete_units"),
    path('units/delete/',views.deleteunits, name="delete_units"),


#Import And Export
    path("dataimport/", DataImport, name="dataimport"),
    path("export/", Export, name="data_export"),



#Warehouses
    path("warehouses/", views.WarehousesListView.as_view(), name = "list-warehouses"),
    path("warehouses/create/", views.WarehousesCreateView.as_view(), name="create_warehouses"),
    path("warehouses/update/<int:pk>", views.WarehousesUpdateView.as_view(), name="edit_warehouses"),
    path("warehouses/<int:pk>/delete/", views.WarehousesDeleteView.as_view(), name="delete_warehouses"),
    path('warehouses/delete/',views.deletewarehouses, name="delete_warehouses"),


#StorageMethodsTypes
    path("storagemethodstypes/", views.StorageMethodsTypesListView.as_view(), name = "list-storagemethodstypes"),
    path("storagemethodstypes/create/", views.StorageMethodsTypesCreateView.as_view(), name="create_storagemethodstypes"),
    path("storagemethodstypes/update/<int:pk>", views.StorageMethodsTypesUpdateView.as_view(), name="edit_storagemethodstypes"),
    path("storagemethodstypes/<int:pk>/delete/", views.StorageMethodsTypesDeleteView.as_view(), name="delete_storagemethodstypes"),
    path('storagemethodstypes/delete/',views.deletestoragemethodstypes, name="delete_storagemethodstypes"),

#InventoriesLocationsTypes
    path("inventorieslocationstypes/", views.InventoriesLocationsTypesListView.as_view(), name = "list-inventorieslocationstypes"),
    path("inventorieslocationstypes/create/", views.InventoriesLocationsTypesCreateView.as_view(), name="create_inventorieslocationstypes"),
    path("inventorieslocationstypes/update/<int:pk>", views.InventoriesLocationsTypesUpdateView.as_view(), name="edit_inventorieslocationstypes"),
    path("inventorieslocationstypes/<int:pk>/delete/", views.InventoriesLocationsTypesDeleteView.as_view(), name="delete_inventorieslocationstypes"),
    path('inventorieslocationstypes/delete/',views.deleteinventorieslocationstypes, name="delete_inventorieslocationstypes"),


#InventoriesLocations
    path("inventorieslocations/", views.InventoriesLocationsListView.as_view(), name = "list-inventorieslocations"),
    path("inventorieslocations/create/", views.InventoriesLocationsCreateView.as_view(), name="create_inventorieslocations"),
    path("inventorieslocations/update/<int:pk>", views.InventoriesLocationsUpdateView.as_view(), name="edit_inventorieslocations"),
    path("inventorieslocations/<int:pk>/delete/", views.InventoriesLocationsDeleteView.as_view(), name="delete_inventorieslocations"),
    path('inventorieslocations/delete/',views.deleteinventorieslocations, name="delete_inventorieslocations"),

#InventoriesBinLocations
    path("inventoriesbinlocations/", views.InventoriesBinLocationsListView.as_view(), name = "list-inventoriesbinlocations"),
    path("inventoriesbinlocations/create/", views.InventoriesBinLocationsCreateView.as_view(), name="create_inventoriesbinlocations"),
    path("inventoriesbinlocations/update/<int:pk>", views.InventoriesBinLocationsUpdateView.as_view(), name="edit_inventoriesbinlocations"),
    path("inventoriesbinlocations/<int:pk>/delete/", views.InventoriesBinLocationsDeleteView.as_view(), name="delete_inventoriesbinlocations"),
    path('inventoriesbinlocations/delete/',views.deleteinventoriesbinlocations, name="delete_inventoriesbinlocations"),
    # path('inventoriesbinlocations/infobin/',views.infobin, name="infobin"),    

#ItemsTypes
    path("itemstypes/", views.ItemsTypesListView.as_view(), name = "list-itemstypes"),
    path("itemstypes/create/", views.ItemsTypesCreateView.as_view(), name="create_itemstypes"),
    path("itemstypes/update/<int:pk>", views.ItemsTypesUpdateView.as_view(), name="edit_itemstypes"),
    path("itemstypes/<int:pk>/delete/", views.ItemsTypesDeleteView.as_view(), name="delete_itemstypes"),
    path('itemstypes/delete/',views.deleteitemstypes, name="delete_itemstypes"),


#itemscategories
    path("itemscategories/", views.ItemsCategoriesListView.as_view(), name = "list-itemscategories"),
    path("itemscategories/create/", views.ItemsCategoriesCreateView.as_view(), name="create_itemscategories"),
    path("itemscategories/update/<int:pk>", views.ItemsCategoriesUpdateView.as_view(), name="edit_itemscategories"),
    path("itemscategories/<int:pk>/delete/", views.ItemsCategoriesDeleteView.as_view(), name="delete_itemscategories"),
    path('itemscategories/delete/',views.deleteitemscategories, name="delete_itemscategories"),

#ItemsGroups
    path("itemsgroups/", views.ItemsGroupsListView.as_view(), name = "list-itemsgroups"),
    path("itemsgroups/create/", views.ItemsGroupsCreateView.as_view(), name="create_itemsgroups"),
    path("itemsgroups/update/<int:pk>", views.ItemsGroupsUpdateView.as_view(), name="edit_itemsgroups"),
    path("itemsgroups/<int:pk>/delete/", views.ItemsGroupsDeleteView.as_view(), name="delete_itemsgroups"),
    path('itemsgroups/delete/',views.deleteitemsgroups, name="delete_itemsgroups"),

#ItemsBrands
    path("itemsbrands/", views.ItemsBrandsListView.as_view(), name = "list-itemsbrands"),
    path("itemsbrands/create/", views.ItemsBrandsCreateView.as_view(), name="create_itemsbrands"),
    path("itemsbrands/update/<int:pk>", views.ItemsBrandsUpdateView.as_view(), name="edit_itemsbrands"),
    path("itemsbrands/<int:pk>/delete/", views.ItemsBrandsDeleteView.as_view(), name="delete_itemsbrands"),
    path('itemsbrands/delete/',views.deleteitemsbrands, name="delete_itemsbrands"),


#GenericNamesCategories
    path("genericnamescategories/", views.GenericNamesCategoriesListView.as_view(), name = "list-genericnamescategories"),
    path("genericnamescategories/create/", views.GenericNamesCategoriesCreateView.as_view(), name="create_genericnamescategories"),
    path("genericnamescategories/update/<int:pk>", views.GenericNamesCategoriesUpdateView.as_view(), name="edit_genericnamescategories"),
    path("genericnamescategories/<int:pk>/delete/", views.GenericNamesCategoriesDeleteView.as_view(), name="delete_genericnamescategories"),
    path('genericnamescategories/delete/',views.deletegenericnamescategories, name="delete_genericnamescategories"),

#GenericNames
    path("genericnames/", views.GenericNamesListView.as_view(), name = "list-genericnames"),
    path("genericnames/create/", views.GenericNamesCreateView.as_view(), name="create_genericnames"),
    path("genericnames/update/<int:pk>", views.GenericNamesUpdateView.as_view(), name="edit_genericnames"),
    path("genericnames/<int:pk>/delete/", views.GenericNamesDeleteView.as_view(), name="delete_genericnames"),
    path('genericnames/delete/',views.deletegenericnames, name="delete_genericnames"),

#ItemsClasses
    path("itemsclasses/", views.ItemsClassesListView.as_view(), name = "list-itemsclasses"),
    path("itemsclasses/create/", views.ItemsClassesCreateView.as_view(), name="create_itemsclasses"),
    path("itemsclasses/update/<int:pk>", views.ItemsClassesUpdateView.as_view(), name="edit_itemsclasses"),
    path("itemsclasses/<int:pk>/delete/", views.ItemsClassesDeleteView.as_view(), name="delete_itemsclasses"),
    path('itemsclasses/delete/',views.deleteitemsclasses, name="delete_itemsclasses"),

#Items
    path("items/", views.ItemsListView.as_view(), name = "list-items"),
    path("items/create/", views.ItemsCreateView.as_view(), name="create_items"),
    path("items/update/<int:pk>", views.ItemsUpdateView.as_view(), name="edit_items"),
    path("items/<int:pk>/delete/", views.ItemsDeleteView.as_view(), name="delete_items"),
    path('items/delete/',views.deleteitems, name="delete_items"),

#ExpensesTypes
    path("expensestypes/", views.ExpensesTypesListView.as_view(), name = "list-expensestypes"),
    path("expensestypes/create/", views.ExpensesTypesCreateView.as_view(), name="create_expensestypes"),
    path("expensestypes/update/<int:pk>", views.ExpensesTypesUpdateView.as_view(), name="edit_expensestypes"),
    path("expensestypes/<int:pk>/delete/", views.ExpensesTypesDeleteView.as_view(), name="delete_expensestypes"),
    path('expensestypes/delete/',views.deleteexpensestypes, name="delete_expensestypes"),

#Agencies
    path("agencies/", views.AgenciesListView.as_view(), name = "list-agencies"),
    path("agencies/create/", views.AgenciesCreateView.as_view(), name="create_agencies"),
    path("agencies/update/<int:pk>", views.AgenciesUpdateView.as_view(), name="edit_agencies"),
    path("agencies/<int:pk>/delete/", views.AgenciesDeleteView.as_view(), name="delete_agencies"),
    path('agencies/delete/',views.deleteagencies, name="delete_agencies"),


#operationstypes
    path("operationstypes/", views.OperationsTypesListView.as_view(), name = "list-operationstypes"),
    path("operationstypes/create/", views.OperationsTypesCreateView.as_view(), name="create_operationstypes"),
    path("operationstypes/update/<int:pk>", views.OperationsTypesUpdateView.as_view(), name="edit_operationstypes"),
    path("operationstypes/<int:pk>/delete/", views.OperationsTypesDeleteView.as_view(), name="delete_operationstypes"),
    path('operationstypes/delete/',views.deleteoperationstypes, name="delete_operationstypes"),


#Operations
    # path("operations/", views.OperationsListView.as_view(), name = "list-operations"),
    # path("operations/create/", views.OperationsCreateView.as_view(), name="create_operations"),
    # path("operations/update/<int:pk>", views.OperationsUpdateView.as_view(), name="edit_operations"),
    # path("operations/<int:pk>/delete/", views.OperationsDeleteView.as_view(), name="delete_operations"),
    
#Operations
    path("operations/<int:pk>/", views.OperationsListView.as_view(), name = "list-operations"),
    path("operations/create/<int:pk>", views.OperationsCreateView.as_view(), name="create_operations"),
    path("operations/update/<int:pk>", views.OperationsUpdateView.as_view(), name="edit_operations"),
    path("operations/<int:pk>/delete/", views.OperationsDeleteView.as_view(), name="delete_operations"),


#Items Price List
    path("itemspricelist/", views.ItemsPLListView.as_view(), name = "list-itemspricelist"),
    path("itemspricelist/update/<int:pk>", views.ItemsPLUpdateView.as_view(), name="edit_itemspricelist"),


            #Workflow Operations

#Workflow Groups
    path("wfgroups/", views.WFGroupsListView.as_view(), name = "list-wfgroups"),
    path("wfgroups/create/", views.WFGroupsCreateView.as_view(), name="create_wfgroups"),
    path("wfgroups/update/<int:pk>", views.WFGroupsUpdateView.as_view(), name="edit_wfgroups"),
    path("wfgroups/<int:pk>/delete/", views.WFGroupsDeleteView.as_view(), name="delete_wfgroups"),
    path('wfgroups/delete/',views.deletewfgroups, name="delete_wfgroups"),

#WFActionsStatus
    path("wfactionsstatus/", views.WFActionsStatusListView.as_view(), name = "list-wfactionsstatus"),
    path("wfactionsstatus/create/", views.WFActionsStatusCreateView.as_view(), name="create_wfactionsstatus"),
    path("wfactionsstatus/update/<int:pk>", views.WFActionsStatusUpdateView.as_view(), name="edit_wfactionsstatus"),
    path("wfactionsstatus/<int:pk>/delete/", views.WFActionsStatusDeleteView.as_view(), name="delete_wfactionsstatus"),
    path('wfactionsstatus/delete/',views.deletewfactionsstatus, name="delete_wfactionsstatus"),

#WFActionsStatus
    path("wfoperationscycles/", views.WFOperationsCyclesListView.as_view(), name = "list-wfoperationscycles"),
    path("wfoperationscycles/create/", views.WFOperationsCyclesCreateView.as_view(), name="create_wfoperationscycles"),
    path("wfoperationscycles/update/<int:pk>", views.WFOperationsCyclesUpdateView.as_view(), name="edit_wfoperationscycles"),
    path("wfoperationscycles/<int:pk>/delete/", views.WFOperationsCyclesDeleteView.as_view(), name="delete_wfoperationscycles"),
    path('wfoperationscycles/delete/',views.deletewfoperationscycles, name="delete_wfoperationscycles"),



##---------  START TARGET URL
    path("targetbuildingblocks/", views.TargetBildingBlocksListView.as_view(), name="targetbuildingblocks"),
    path("targetbuildingblocks/create/", views.TargetBuildingBlocksCreateView.as_view(),
         name="create_targetbuildingblocks"),
    path("targetbuildingblocks/update/<int:pk>", views.TargetBuildingBlocksUpdateView.as_view(),
         name="edit_targetbuildingblocks"),
    path("targetbuildingblocks/rebuild/", views.TargetBuildingBlocksRebuildView.as_view(),
         name="rebuild_targetbuildingblocks"),
    path('targetbuildingblocks/delete/',views.deletetargetbuildingblocks, name="delete_targetbuildingblocks"),

    path("targetbuildingblocksaccounts/", views.TargetBuildingBlocksAccountsListView.as_view(),
         name="targetbuildingblocksaccounts"),
    path("targetbuildingblocksaccounts/create/", views.TargetBuildingBlocksAccountsCreateView.as_view(),
         name="create_targetbuildingblocksaccounts"),
    path("targetbuildingblocksaccounts/update/<int:pk>", views.TargetBuildingBlocksAccountsUpdateView.as_view(),
         name="edit_targetbuildingblocksaccounts"),
    path("targetbuildingblocksaccounts/rebuild/", views.TargetBuildingBlocksAccountsRebuildView.as_view(),
         name="rebuild_targetbuildingblocksaccounts"),
    path('targetbuildingblocksaccounts/delete/',views.deletetargetbuildingblocksaccounts, name="delete_targettargetbuildingblocksaccounts"),

    path("targetbuildingblockschannels/", views.TargetBuildingBlocksChannelsListView.as_view(),
         name="targetbuildingblockschannels"),
    path("targetbuildingblockschannels/create/", views.TargetBuildingBlocksChannelsCreateView.as_view(),
         name="create_targetbuildingblockschannels"),
    path("targetbuildingblockschannels/update/<int:pk>", views.TargetBuildingBlocksChannelsUpdateView.as_view(),
         name="edit_targetbuildingblockschannels"),
    path("targetbuildingblockschannels/rebuild/", views.TargetBuildingBlocksChannelsRebuildView.as_view(),
         name="rebuild_targetbuildingblockschannels"),
    path('targetbuildingblockschannels/delete/',views.deletetargetbuildingblockschannels, name="delete_targetbuildingblockschannels"),

    ### Target Reports
    path("custtargetrep/", views.CustTargetRepView.as_view(), name="custtargetrep"),

    ##--------- END TARGET URL




]