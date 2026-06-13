from django.urls import path
from . import views

app_name = "sy"

urlpatterns = [

#Modules
    path("modules/", views.ModulesListView.as_view(), name = "list-modules"),
    path("modules/create/", views.ModulesCreateView.as_view(), name="create_modules"),
    path("modules/<int:pk>/delete/", views.ModulesDeleteView.as_view(), name="delete_modules"),
    path("modules/update/<int:pk>", views.ModulesUpdateView.as_view(), name="edit_modules"),
    path('modules/delete/',views.deletemodules, name="delete_modules"),

# LookUp
    path("lookup/", views.LookUpListView.as_view(), name = "list-lookup"),
    path("lookup/create/", views.LookUpCreateView.as_view(), name="create_lookup"),
    path("lookup/<int:pk>/delete/", views.LookUpDeleteView.as_view(), name="delete_lookup"),
    path("lookup/update/<int:pk>", views.LookUpUpdateView.as_view(), name="edit_lookup"),
    path('lookup/delete/',views.deletelookup, name="delete_lookup"),

# Fiscal Years
    path("fiscalyears/", views.FiscalYearsListView.as_view(), name = "list-fiscalyears"),
    path("fiscalyears/create/", views.FiscalYearsCreateView.as_view(), name="create_fiscalyears"),
    path("fiscalyears/update/<int:pk>", views.FiscalYearsUpdateView.as_view(), name="edit_fiscalyears"),
    path("fiscalyears/<int:pk>/delete/", views.FiscalYearsDeleteView.as_view(), name="delete_fiscalyears"),
    path('fiscalyears/delete/',views.deletefiscalyears, name="delete_fiscalyears"),

# Fiscal Years Periods Modules
    path("fiscalyearsperiodsmodules/", views.FiscalYearsPeriodsModulesListView.as_view(), name = "list-fiscalyearsperiodsmodules"),
    path("fiscalyearsperiodsmodules/update/<int:pk>", views.FiscalYearsPeriodsModulesUpdateView.as_view(), name="edit_fiscalyearsperiodsmodules"),


# Payments Methods
    path("paymentsmethods/", views.PaymentsMethodsListView.as_view(), name = "list-paymentsmethods"),
    path("paymentsmethods/create/", views.PaymentsMethodsCreateView.as_view(), name="create_paymentsmethods"),
    path("paymentsmethods/<int:pk>/delete/", views.PaymentsMethodsDeleteView.as_view(), name="delete_paymentsmethods"),
    path("paymentsmethods/update/<int:pk>", views.PaymentsMethodsUpdateView.as_view(), name="edit_paymentsmethods"),
    path('paymentsmethods/delete/',views.deletepaymentsmethods, name="delete_paymentsmethods"),

# Credit Cards Types
    path("creditcardstypes/", views.CreditCardsTypesListView.as_view(), name = "list-creditcardstypes"),
    path("creditcardstypes/create/", views.CreditCardsTypesCreateView.as_view(), name="create_creditcardstypes"),
    path("creditcardstypes/<int:pk>/delete/", views.CreditCardsTypesDeleteView.as_view(), name="delete_creditcardstypes"),
    path("creditcardstypes/update/<int:pk>", views.CreditCardsTypesUpdateView.as_view(), name="edit_creditcardstypes"),
    path('creditcardstypes/delete/',views.deletecreditcardstypes, name="delete_creditcardstypes"),


# Languages
    path("languages/", views.LanguagesListView.as_view(), name = "list-languages"),
    path("languages/create/", views.LanguagesCreateView.as_view(), name="create_languages"),
    path("languages/<int:pk>/delete/", views.LanguagesDeleteView.as_view(), name="delete_languages"),
    path("languages/update/<int:pk>", views.LanguagesUpdateView.as_view(), name="edit_languages"),
    path('languages/delete/',views.deletelanguages, name="delete_languages"),

# Nationalities
    path("nationalities/", views.NationalitiesListView.as_view(), name = "list-nationalities"),
    path("nationalities/create/", views.NationalitiesCreateView.as_view(), name="create_nationalities"),
    path("nationalities/<int:pk>/delete/", views.NationalitiesDeleteView.as_view(), name="delete_nationalities"),
    path("nationalities/update/<int:pk>", views.NationalitiesUpdateView.as_view(), name="edit_nationalities"),
    path('nationalities/delete/',views.deletenationalities, name="delete_nationalities"),

# Regions
    path("regions/", views.RegionsListView.as_view(), name = "list-regions"),
    path("regions/create/", views.RegionsCreateView.as_view(), name="create_regions"),
    path("regions/<int:pk>/delete/", views.RegionsDeleteView.as_view(), name="delete_regions"),
    path("regions/update/<int:pk>", views.RegionsUpdateView.as_view(), name="edit_regions"),
    path('regions/delete/',views.deleteregions, name="delete_regions"),


# Countries
    path("countries/", views.CountriesListView.as_view(), name = "list-countries"),
    path("countries/create/", views.CountriesCreateView.as_view(), name="create_countries"),
    path("countries/<int:pk>/delete/", views.CountriesDeleteView.as_view(), name="delete_countries"),
    path("countries/update/<int:pk>", views.CountriesUpdateView.as_view(), name="edit_countries"),
    path('countries/delete/',views.deletecountries, name="delete_countries"),

# Areas
    path("areas/", views.AreasListView.as_view(), name = "list-areas"),
    path("areas/create/", views.AreasCreateView.as_view(), name="create_areas"),
    path("areas/<int:pk>/delete/", views.AreasDeleteView.as_view(), name="delete_areas"),
    path("areas/update/<int:pk>", views.AreasUpdateView.as_view(), name="edit_areas"),
    path('areas/delete/',views.deleteareas, name="delete_areas"),


# Cities
    path("cities/", views.CitiesListView.as_view(), name = "list-cities"),
    path("cities/create/", views.CitiesCreateView.as_view(), name="create_cities"),
    path("cities/<int:pk>/delete/", views.CitiesDeleteView.as_view(), name="delete_cities"),
    path("cities/update/<int:pk>", views.CitiesUpdateView.as_view(), name="edit_cities"),
    path('cities/delete/',views.deletecities, name="delete_cities"),

# Districts
    path("districts/", views.DistrictsListView.as_view(), name = "list-districts"),
    path("districts/create/", views.DistrictsCreateView.as_view(), name="create_districts"),
    path("districts/<int:pk>/delete/", views.DistrictsDeleteView.as_view(), name="delete_districts"),
    path("districts/update/<int:pk>", views.DistrictsUpdateView.as_view(), name="edit_districts"),
    path('districts/delete/',views.deletedistricts, name="delete_districts"),


# AddressesTypes
    path("addressestypes/", views.AddressesTypesListView.as_view(), name = "list-addressestypes"),
    path("addressestypes/create/", views.AddressesTypesCreateView.as_view(), name="create_addressestypes"),
    path("addressestypes/<int:pk>/delete/", views.AddressesTypesDeleteView.as_view(), name="delete_addressestypes"),
    path("addressestypes/update/<int:pk>", views.AddressesTypesUpdateView.as_view(), name="edit_addressestypes"),
    path('addressestypes/delete/',views.deleteaddressestypes, name="delete_addressestypes"),


# ContactsTypes
    path("contactstypes/", views.ContactsTypesListView.as_view(), name = "list-contactstypes"),
    path("contactstypes/create/", views.ContactsTypesCreateView.as_view(), name="create_contactstypes"),
    path("contactstypes/<int:pk>/delete/", views.ContactsTypesDeleteView.as_view(), name="delete_contactstypes"),
    path("contactstypes/update/<int:pk>", views.ContactsTypesUpdateView.as_view(), name="edit_contactstypes"),
    path('contactstypes/delete/',views.deletecontactstypes, name="delete_contactstypes"),

# BusinessActivitiesTypes
    path("businessactivitiestypes/", views.BusinessActivitiesTypesListView.as_view(), name = "list-businessactivitiestypes"),
    path("businessactivitiestypes/create/", views.BusinessActivitiesTypesCreateView.as_view(), name="create_businessactivitiestypes"),
    path("businessactivitiestypes/<int:pk>/delete/", views.BusinessActivitiesTypesDeleteView.as_view(), name="delete_businessactivitiestypes"),
    path("businessactivitiestypes/update/<int:pk>", views.BusinessActivitiesTypesUpdateView.as_view(), name="edit_businessactivitiestypes"),
    path('businessactivitiestypes/delete/',views.deletebusinessactivitiestypes, name="delete_businessactivitiestypes"),


# Taxes
    path("taxes/", views.TaxesListView.as_view(), name = "list-taxes"),
    path("taxes/create/", views.TaxesCreateView.as_view(), name="create_taxes"),
    path("taxes/<int:pk>/delete/", views.TaxesDeleteView.as_view(), name="delete_taxes"),
    path("taxes/update/<int:pk>", views.TaxesUpdateView.as_view(), name="edit_taxes"),
    path('taxes/delete/',views.deletetaxes, name="delete_taxes"),


# Taxes
    path("taxesgroups/", views.TaxesGroupsListView.as_view(), name = "list-taxesgroups"),
    path("taxesgroups/create/", views.TaxesGroupsCreateView.as_view(), name="create_taxesgroups"),
    path("taxesgroups/<int:pk>/delete/", views.TaxesGroupsDeleteView.as_view(), name="delete_taxesgroups"),
    path("taxesgroups/update/<int:pk>", views.TaxesGroupsUpdateView.as_view(), name="edit_taxesgroups"),
    path('taxesgroups/delete/',views.deletetaxesgroups, name="delete_taxesgroups"),

    path("companyprofile/", views.CompanyProfileListView.as_view(), name="list-companyprofile"),
    path("companyprofile/create/", views.CompanyProfileCreateView.as_view(), name="create_companyprofile"),
    path("companyprofile/update/<int:pk>", views.CompanyProfileUpdateView.as_view(), name="edit_companyprofile"),
    path("companyprofile/<int:pk>/delete/", views.CompanyProfileDeleteView.as_view(), name="delete_companyprofile"),
    path('companyprofile/delete/',views.deletecompanyprofile, name="delete_companyprofile"),


# Prices Levels
    path("pricelevels/", views.PriceLevelsListView.as_view(), name = "list-pricelevels"),
    path("pricelevels/create/", views.PriceLevelsCreateView.as_view(), name="create_pricelevels"),
    path("pricelevels/<int:pk>/delete/", views.PriceLevelsDeleteView.as_view(), name="delete_pricelevels"),
    path("pricelevels/update/<int:pk>", views.PriceLevelsUpdateView.as_view(), name="edit_pricelevels"),
    path('pricelevels/delete/',views.deletepricelevels, name="delete_pricelevels"),


# Payment Tearm
    path("paymentstearms/", views.PaymentsTearmsListView.as_view(), name = "list-paymentstearms"),
    path("paymentstearms/create/", views.PaymentsTearmsCreateView.as_view(), name="create_paymentstearms"),
    path("paymentstearms/update/<int:pk>", views.PaymentsTearmsUpdateView.as_view(), name="edit_paymentstearms"),
    path("paymentstearms/<int:pk>/delete/", views.PaymentsTearmsDeleteView.as_view(), name="delete_paymentstearms"),
    path('paymentstearms/delete/',views.deletepaymentstearms, name="delete_paymentstearms"),


# Cash Discounts Roles
    path("cashdiscountsroles/", views.CashDiscountsRolesListView.as_view(), name = "list-cashdiscountsroles"),
    path("cashdiscountsroles/create/", views.CashDiscountsRolesCreateView.as_view(), name="create_cashdiscountsroles"),
    path("cashdiscountsroles/update/<int:pk>", views.CashDiscountsRolesUpdateView.as_view(), name="edit_cashdiscountsroles"),
    path("cashdiscountsroles/<int:pk>/delete/", views.CashDiscountsRolesDeleteView.as_view(), name="delete_cashdiscountsroles"),
    path('cashdiscountsroles/delete/',views.deletecashdiscountsroles, name="delete_cashdiscountsroles"),

]
