from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView
from TARGET.crm.models import Transactions, Customer, FinancialYear, ToDoList, Channel, City, TargetTransactions, Area, Category, Collection, Salesman
from django.utils import timezone
from django.db.models import Sum, F, IntegerField, Q, Count
import datetime
from django.db.models.functions import ExtractMonth


User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        today = datetime.date.today()
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']

        try:
            year_id = int(self.request.GET.get('year'))
        except:
            year_id = timezone.now().year
        try:
            date_id = int(self.request.GET.get('month'))
            if date_id == 111:
                date_id = 9999999
        except:
            current_month1 = months[today.month]
            current_month = int(current_month1)
            date_id = current_month

        financialyears = FinancialYear.objects.all()
        current_month1 = months[today.month]
        if date_id != 44 and date_id != 55 and date_id != 66 and date_id != 77 and date_id != 9999999 and date_id != 88 and date_id != 99:
            current_month = date_id
        else:
            current_month = int(current_month1)

        for financialyear in financialyears:
            Quarter1 = [financialyear.m1, financialyear.m2, financialyear.m3]
            Quarter2 = [financialyear.m4, financialyear.m5, financialyear.m6]
            Quarter3 = [financialyear.m7, financialyear.m8, financialyear.m9]
            Quarter4 = [financialyear.m10, financialyear.m11, financialyear.m12]
            FirstHalf = [financialyear.m1, financialyear.m2, financialyear.m3, financialyear.m4, financialyear.m5, financialyear.m6]
            SecondHalf = [financialyear.m7, financialyear.m8, financialyear.m9, financialyear.m10, financialyear.m11, financialyear.m12]
            numberofdaysQ1 = 31+28+31
            numberofdaysQ2 = 30+31+30 + numberofdaysQ1
            numberofdaysQ3 = 31+31+30 + numberofdaysQ2
            numberofdaysQ4 = 31+30+31 + numberofdaysQ3

            numberofdaysAQ1 = 31+28+31
            numberofdaysAQ2 = 30+31+30
            numberofdaysAQ3 = 31+31+30
            numberofdaysAQ4 = 31+30+31

            numberofdaysFH = 31+28+31+30+31+30
            numberofdaysSH = 31+31+30+31+30+31
            numberofdaysFY = 31+28+31+30+31+30+31+31+30+31+30+31
            if financialyear.m1 == current_month:
                cmonths = 'm1'
                monthn = '1'
                monthname = 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths = 'm2'
                monthn = '2'
                monthname = 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths = 'm3'
                monthn = '3'
                monthname = 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths = 'm4'
                monthn = '4'
                monthname = 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname = 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname = 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname = 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname = 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname = 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname = 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname = 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname = 'Dec'
                numberofdays = 31

        currentY = timezone.now().year
        lastYear = timezone.now().year - 1
        print('jjnjj' , date_id)
        if year_id == lastYear and date_id == 9999999:
            monthn = [1,2,3,4,5,6,7,8,9,10,11,12]
            Quarter = "None"
            numberofdays = numberofdaysFY
            numberofdaysA = numberofdaysFY
        elif year_id == currentY and date_id == 9999999:
            monthn = [1,2,3,4,5,6,7,8,9,10,11,12]
            Quarter = "None"
            numberofdays = numberofdaysFY
            numberofdaysA = numberofdaysFY
        elif date_id == 44:
            Quarter = Quarter1
            cmonth1 = 'm1'
            cmonth2 = 'm2'
            cmonth3 = 'm3'
            numberofdays = numberofdaysQ1
            numberofdaysA = numberofdaysAQ1
        elif date_id == 55:
            Quarter = Quarter2
            cmonth1 = 'm4'
            cmonth2 = 'm5'
            cmonth3 = 'm6'
            numberofdays = numberofdaysQ2
            numberofdaysA = numberofdaysAQ2
        elif date_id == 66:
            Quarter = Quarter3
            cmonth1 = 'm7'
            cmonth2 = 'm8'
            cmonth3 = 'm9'
            numberofdays = numberofdaysQ3
            numberofdaysA = numberofdaysAQ3
        elif date_id == 77:
            Quarter = Quarter4
            cmonth1 = 'm10'
            cmonth2 = 'm11'
            cmonth3 = 'm12'
            numberofdays = numberofdaysQ4
            numberofdaysA = numberofdaysAQ4
        elif date_id == 88:
            Quarter = FirstHalf
            cmonth1 = 'm1'
            cmonth2 = 'm2'
            cmonth3 = 'm3'
            cmonth4 = 'm4'
            cmonth5 = 'm5'
            cmonth6 = 'm6'
            numberofdays = numberofdaysFH
            numberofdaysA = numberofdaysFH
        elif date_id == 99:
            Quarter = SecondHalf
            cmonth1 = 'm7'
            cmonth2 = 'm8'
            cmonth3 = 'm9'
            cmonth4 = 'm10'
            cmonth5 = 'm1'
            cmonth6 = 'm12'
            numberofdays = numberofdaysSH
            numberofdaysA = numberofdaysSH
        else:
            Quarter = "None"
            monthn = int(monthn)

        currentYear = year_id
        print('currentYear', year_id)
        yearsq = Transactions.objects.dates('created_date', 'year')
        yearlist = []
        if yearsq.count() > 0:
            for Years in yearsq:
                yearlist.append({'Year': Years.year })
        else:
            yearlist.append({'Year': currentY})



        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querysourcetotal = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)
            querysourcetotalp = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            queryavailablestock = Transactions.objects.annotate(totalq=Sum('ctrqty')).values('ctrqty').filter(
                created_date__year=currentYear).filter(created_date__month__in=Quarter)
            queryavailablestockV = Transactions.objects.annotate(totalq=Sum('total')).values('total').filter(
                created_date__year=currentYear).filter(created_date__month__in=Quarter)
        else:

            querysourcetotal = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__year=currentYear)
            querysourcetotalp = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__year=currentYear)

            queryavailablestock = Transactions.objects.annotate(totalq=Sum('ctrqty')).values('ctrqty').filter(
                created_date__year=currentYear)
            queryavailablestockV = Transactions.objects.annotate(totalq=Sum('total')).values('total').filter(
                created_date__year=currentYear)

        qproductactual = Transactions.objects.annotate(Sum('ctrqty')).filter(
            Q(source='SalesOrder') | Q(source='SalesReturnOrder') | Q(source='TransferOut') | Q(
                source='TransferIn'))

        qproductactualV = Transactions.objects.annotate(Sum('total')).filter(
            Q(source='SalesOrder') | Q(source='SalesReturnOrder') | Q(source='TransferOut') | Q(
                source='TransferIn'))

        salesmanncount = 0

        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
                salesmanncount = 0
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))
                salesmanncount = salesmanid.count()

            querysourcetotal = querysourcetotal.filter(salesman__in=salesmanid)


        totalqty = queryavailablestockV.aggregate(Sum('total'))
        qqproductactual = qproductactualV.aggregate(total=Sum('total'))
        try:
            productactual = qqproductactual['total']
        except:
            productactual = 0
        if productactual == None:
            productactual = 0

        qproductpur = Transactions.objects.annotate(Sum('total')).filter(
            Q(source='PurchaseOrder') | Q(source='PurchaseReturnOrder'))
        qqproductpur = qproductpur.aggregate(total=Sum('total'))
        try:
            productpurchase = qqproductpur['total']
        except:
            productpurchase = 0
        if productpurchase == None:
            productpurchase = 0

        netstock = productpurchase - productactual

        ctrqty = round(netstock)

        custcount = Customer.objects.all().count()
        chcount = Channel.objects.all().count()
        citycount = City.objects.all().count()


        if self.request.user.is_superuser:
            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
                targettransactions = TargetTransactions.objects.all().filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))
            else:
                targettransactions = TargetTransactions.objects.all().filter(created_date__year=currentYear)
        else:
            if Quarter is not "None":
                targettransactions = TargetTransactions.objects.all().filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter)).filter(salesman__in=salesmanid)
            else:
                targettransactions = TargetTransactions.objects.all().filter(created_date__year=currentYear).filter(salesman__in=salesmanid)

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalpurchase = querysourcetotal.filter(source='PurchaseOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))

            querytotalsales = querysourcetotal.filter(source='SalesOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))

            querytotalsalesreturn = querysourcetotal.filter(source='SalesReturnOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))

            querytotalpurchasereturn = querysourcetotal.filter(source='PurchaseReturnOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querymonthlytarget = targettransactions.annotate(
                    total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3))  * F('price'), output_field=IntegerField()))
            elif date_id == 88 or date_id == 99:
                querymonthlytarget = targettransactions.annotate(
                    total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6))  * F('price'), output_field=IntegerField()))

            querymonthlysales = Transactions.objects.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month__in=Quarter))


        else:

            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:

                querytotalpurchase = querysourcetotalp.filter(source='PurchaseOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month=monthn))

                querytotalsales = querysourcetotal.filter(source='SalesOrder').values('total').filter(Q(created_date__year=currentYear)).filter(Q(created_date__month=monthn))


                querytotalsalesreturn = querysourcetotal.filter(source='SalesReturnOrder').values('total').filter(
                    created_date__month=monthn).filter(created_date__year=currentYear)

                querytotalpurchasereturn = querysourcetotalp.filter(source='PurchaseReturnOrder').values('total').filter(
                    created_date__month=monthn).filter(created_date__year=currentYear)

                querymonthlytarget = targettransactions.annotate(
                    total=Sum(F(cmonths) * F('price'),
                              output_field=IntegerField())).filter(created_date__year=currentYear)
                querymonthlysales = Transactions.objects.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(created_date__month=monthn).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total')


            else:

                querytotalpurchase = querysourcetotalp.filter(source='PurchaseOrder').values('total').filter(Q(created_date__year=currentYear)).filter(
                    created_date__month__in=monthn)
                querytotalsales = querysourcetotal.filter(source='SalesOrder').values('total').filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotalsalesreturn = querysourcetotal.filter(source='SalesReturnOrder').values('total').filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotalpurchasereturn = querysourcetotalp.filter(source='PurchaseReturnOrder').values('total').filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querymonthlytarget = targettransactions.annotate(
                    total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                              output_field=IntegerField()))
                querymonthlysales = Transactions.objects.values('source').order_by('source') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(
                    created_date__year=currentYear)


        totalpurchase = querytotalpurchase.aggregate(Sum('total'))
        totalsales = querytotalsales.aggregate(Sum('total'))
        totalsalesreturn = querytotalsalesreturn.aggregate(Sum('total'))
        totalpurchasereturn = querytotalpurchasereturn.aggregate(Sum('total'))
        if totalpurchasereturn['total__sum'] is not None and totalpurchase['total__sum'] is not None:
            netpurchase = round(totalpurchase['total__sum'] + totalpurchasereturn['total__sum'])
        elif totalpurchase['total__sum'] is not None:
            netpurchase = round(totalpurchase['total__sum'])
        else:
            netpurchase = 0
        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99 or date_id == 9999999:
            if date_id != 9999999 and date_id != 88 and date_id != 99:
                print( Quarter[0])
                if len(str(Quarter[0])) == 1:
                    currentQ = "0" + str(Quarter[0])
                else:
                    currentQ = str(Quarter[0])

                startdateformat = str(currentYear) + "-" + currentQ + "-01"
                print(startdateformat)
                currday = timezone.now().date()
                startday = datetime.datetime.strptime(startdateformat, "%Y-%m-%d").date()
                print(currday)
                currentday = (currday - startday).days
                print(currentday)
                print(numberofdaysA)
                daysspent = round(currentday / numberofdaysA * 100)
                if int(current_month1) not in Quarter:
                    print('yes')
                    daysspent = 100
            else:
                startdateformat = str(currentYear) + "-01-01"
                currday = timezone.now().date()
                startday = datetime.datetime.strptime(startdateformat, "%Y-%m-%d").date()
                currentday = (currday - startday).days
                daysspent = round(currentday / numberofdays * 100)
                if Quarter != "None":
                    if int(current_month1) not in Quarter and (date_id == 88 or date_id == 99) and date_id != 9999999:
                        daysspent = 100
                    elif date_id == 88 or date_id == 99 and date_id != 9999999:
                        if len(str(Quarter[0])) == 1:
                            currentQ = "0" + str(Quarter[0])
                        else:
                            currentQ = str(Quarter[0])

                        startdateformat = str(currentYear) + "-" + currentQ + "-01"
                        print(startdateformat)
                        currday = timezone.now().date()
                        startday = datetime.datetime.strptime(startdateformat, "%Y-%m-%d").date()
                        currentday = (currday - startday).days
                        print(currentday)
                        print(numberofdays)
                        daysspent = round(currentday / numberofdays * 100)

        elif date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:
            currentday = timezone.now().day
            daysspent = 100
            print(date_id)
            print(numberofdays)
            if int(current_month1) == int(date_id):
                daysspent = round(currentday / numberofdays * 100)
                print(daysspent)

        totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
        totalmonthlytargets = totalmonthlytarget['total__sum']


        if self.request.user.is_superuser is False:
            querymonthlysales = querymonthlysales.filter(salesman__in=salesmanid)

        totalmonthlysaless = querymonthlysales.aggregate(Sum('total'))
        try:
            totalmonthlysaless = round(int(totalmonthlysaless['total__sum']), 1)
        except:
            totalmonthlysaless = 0


        # Sales vs Target - Monthly view
        allmonthsales = []

        mc = 0
        allmonthsales = []
        while mc < 12:
            salesmonths = 'm' + str(mc + 1)

            monthfinancialyear = financialyears.values(salesmonths)

            queryallmonthsales = Transactions.objects.annotate(month=ExtractMonth('created_date')).values(
                'month').order_by(
                'month').filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                created_date__month=monthfinancialyear[0][salesmonths]) \
                .annotate(total=Sum('total')).values('month', 'total').filter(created_date__year=currentYear)

            if self.request.user.is_superuser is False:
                queryallmonthsales = queryallmonthsales.filter(salesman__in=salesmanid)

            queryallmonthtarget = targettransactions.annotate(
                total=Sum(F(salesmonths) * F('price'), output_field=IntegerField())).order_by('total')
            totalallmonthtarget = queryallmonthtarget.aggregate(Sum('total'))
            try:
                ee = queryallmonthsales[0]['total']
                if totalallmonthtarget['total__sum'] is not None:
                    allmonthsales.append(
                        {'month': monthfinancialyear[0][salesmonths], 'sales': int(round(queryallmonthsales[0]['total'])),
                         'target': round(totalallmonthtarget['total__sum'])})
                else:
                    allmonthsales.append(
                        {'month': monthfinancialyear[0][salesmonths], 'sales': int(round(queryallmonthsales[0]['total'])),
                         'target': 0})
            except:
                if totalallmonthtarget['total__sum'] is not None:
                    allmonthsales.append({'month': monthfinancialyear[0][salesmonths], 'sales': 0,
                                          'target': int(round(totalallmonthtarget['total__sum']))})

                else:
                    allmonthsales.append({'month': monthfinancialyear[0][salesmonths], 'sales': 0,
                                          'target': 0})

            mc += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalescustomer = Transactions.objects.values('customer') \
            .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
            '-total').filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            querytotalsaleschannel = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querytotaltargetchannel = TargetTransactions.objects.values('channel') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))

                querymonthlytargetcustomer = targettransactions.values('customer') \
                .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('-total')
            elif date_id == 88 or date_id == 99:
                querytotaltargetchannel = TargetTransactions.objects.values('channel') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))

                querymonthlytargetcustomer = targettransactions.values('customer') \
                .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'), output_field=IntegerField())).order_by('-total')

        else:
            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:

                querytotalsalescustomer = Transactions.objects.values('customer') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month=monthn).filter(created_date__year=currentYear)

                querytotalsaleschannel = Transactions.objects.values('channel').order_by('channel') \
                    .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                    created_date__month=monthn).filter(created_date__year=currentYear)

                querytotaltargetchannel = TargetTransactions.objects.values('channel') \
                    .annotate(total=Sum(F(cmonths) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(created_date__year=currentYear)
                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum(F(cmonths) * F('price'),
                                        output_field=IntegerField())).order_by('-total')
            else:

                querytotalsalescustomer = Transactions.objects.values('customer') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotalsaleschannel = Transactions.objects.values('channel').order_by('channel') \
                    .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotaltargetchannel = TargetTransactions.objects.values('channel') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(created_date__year=currentYear)
                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                                        output_field=IntegerField())).order_by('-total')


        if self.request.user.is_superuser is False:
            querytotalsaleschannel = querytotalsaleschannel.filter(salesman__in=salesmanid)
            querytotaltargetchannel = querytotaltargetchannel.filter(salesman__in=salesmanid)

        channelcount = int(querytotalsaleschannel.count())
        channelTotal = []
        channelLabel = ''
        channelLabels = []
        channelsales = []
        c = 0
        if channelcount == 0 :
            channelsales.append(
                {'channel': '',
                 'sales': 0,
                 'salest': 0,
                 'target': 0,
                 'targetFull': 0
                 }
            )

        while c < channelcount:
            channelLabel1 = Channel.objects.filter(pk=querytotalsaleschannel[c]['channel']).values('name')
            channeltargettotalq = querytotaltargetchannel.filter(channel=querytotalsaleschannel[c]['channel'])

            channeltargettotalqv = 0
            querytotalsaleschannelv = 0
            try:
                channeltargettotalqv = round(int(channeltargettotalq[0]['total']))
            except:
                channeltargettotalqv = 0

            try:
                querytotalsaleschannelv = round(int(querytotalsaleschannel[c]['total']))
            except:
                querytotalsaleschannelv = 0

            targetotal = channeltargettotalqv - querytotalsaleschannelv
            if targetotal < 0:
                targetotal = 0

            try:
                temp = querytotaltargetchannel[c]['total']
                if totalmonthlysaless != 0:
                    channelsales.append(
                        {'channel': channelLabel1[0]['name'],
                         'sales': round(int(querytotalsaleschannel[c]['total']) / totalmonthlysaless * 100),
                         'salest': round(int(querytotalsaleschannel[c]['total'])),
                         'target': targetotal,
                         'targetFull': round(int(querytotaltargetchannel[c]['total']))
                         }
                    )
                else:
                    channelsales.append(
                        {'channel': channelLabel1[0]['name'],
                         'sales': round(int(querytotalsaleschannel[c]['total']) ),
                         'salest': round(int(querytotalsaleschannel[c]['total'])),
                         'target': targetotal,
                         'targetFull': round(int(querytotaltargetchannel[c]['total']))
                         }
                    )
            except:
                if totalmonthlysaless != 0:
                    channelsales.append(
                        {'channel': channelLabel1[0]['name'],
                         'sales': round(int(querytotalsaleschannel[c]['total']) / totalmonthlysaless * 100),
                         'salest': round(int(querytotalsaleschannel[c]['total'])),
                         'target': 0
                         }
                    )
                else:
                    channelsales.append(
                        {'channel': channelLabel1[0]['name'],
                         'sales': round(int(querytotalsaleschannel[c]['total']) ),
                         'salest': round(int(querytotalsaleschannel[c]['total'])),
                         'target': 0
                         }
                    )

            c += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalescustomer = Transactions.objects.values('customer') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                '-total').filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            querytotalsalesarea = Transactions.objects.values('area').order_by('area') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querytotaltargetarea = TargetTransactions.objects.values('area') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))

                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('-total')
            elif date_id == 88 or date_id == 99:
                querytotaltargetarea = TargetTransactions.objects.values('area') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('total').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)

                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('-total')

        else:

            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:

                querytotalsalescustomer = Transactions.objects.values('customer') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month=monthn).filter(created_date__year=currentYear)

                querytotalsalesarea = Transactions.objects.values('area').order_by('area') \
                    .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                    created_date__month=monthn).filter(created_date__year=currentYear)
                querytotaltargetarea = TargetTransactions.objects.values('area') \
                    .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).order_by('total').filter(
                    created_date__year=currentYear)

                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).order_by('-total')
            else:
                querytotalsalescustomer = Transactions.objects.values('customer') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotalsalesarea = Transactions.objects.values('area').order_by('area') \
                    .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                    created_date__month__in=monthn).filter(created_date__year=currentYear)

                querytotaltargetarea = TargetTransactions.objects.values('area') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'), output_field=IntegerField())).order_by('total').filter(
                    created_date__year=currentYear)

                querymonthlytargetcustomer = targettransactions.values('customer') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'), output_field=IntegerField())).order_by('-total')


        if self.request.user.is_superuser is False:
            querytotalsalesarea = querytotalsalesarea.filter(salesman__in=salesmanid)
            querytotaltargetarea = querytotaltargetarea.filter(salesman__in=salesmanid)

        arealcount = int(querytotalsalesarea.count())
        areaTotal = []
        areaLabel = ''
        areaLabels = []
        areasales = []
        c = 0
        if arealcount == 0:
            areasales.append(
                {'area': '',
                 'sales': 0,
                 'salest': 0,
                 'target': 0,
                 'targetFull': 0
                 }
            )

        while c < arealcount:
            areaLabel1 = Area.objects.filter(pk=querytotalsalesarea[c]['area']).values('name')
            areatargettotalq = querytotaltargetarea.filter(area=querytotalsalesarea[c]['area'])
            try:
                targetotal = round(int(areatargettotalq[0]['total'])) - round(
                         int(querytotalsalesarea[c]['total']))
            except:
                targetotal = 0

            if targetotal < 0:
                targetotal = 0
            try:
                temp = querytotaltargetarea[c]['total']
                if totalmonthlysaless != 0:
                    areasales.append(
                        {'area': areaLabel1[0]['name'],
                         'sales': round(int(querytotalsalesarea[c]['total']) / totalmonthlysaless * 100, 0),
                         'salest': round(int(querytotalsalesarea[c]['total'])),
                         'target': targetotal,
                         'targetFull': round(int(querytotaltargetarea[c]['total']))
                         }
                    )
                else:
                    areasales.append(
                        {'area': areaLabel1[0]['name'],
                         'sales': round(int(querytotalsalesarea[c]['total']) , 0),
                         'salest': round(int(querytotalsalesarea[c]['total'])),
                         'target': targetotal,
                         'targetFull': round(int(querytotaltargetarea[c]['total']))
                         }
                    )

            except:
                if totalmonthlysaless != 0:
                    areasales.append(
                        {'area': areaLabel1[0]['name'],
                         'sales': round(int(querytotalsalesarea[c]['total']) / totalmonthlysaless * 100, 0),
                         'salest': round(int(querytotalsalesarea[c]['total'])),
                         'target': 0
                         }
                    )
                else:
                    areasales.append(
                        {'area': areaLabel1[0]['name'],
                         'sales': round(int(querytotalsalesarea[c]['total']) , 0),
                         'salest': round(int(querytotalsalesarea[c]['total'])),
                         'target': 0
                         }
                    )

            c += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalessalesman = Transactions.objects.values('salesman') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                '-total').filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querymonthlytargetsalesman = TargetTransactions.objects.values('salesman') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('-total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))
            elif date_id == 88 or date_id == 99:
                querymonthlytargetsalesman = TargetTransactions.objects.values('salesman') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)
        else:


            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:
                querytotalsalessalesman = Transactions.objects.values('salesman') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month=monthn).filter(created_date__year=currentYear)
                querymonthlytargetsalesman = TargetTransactions.objects.values('salesman') \
                    .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear)
            else:
                querytotalsalessalesman = Transactions.objects.values('salesman') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month__in=monthn).filter(created_date__year=currentYear)
                querymonthlytargetsalesman = TargetTransactions.objects.values('salesman') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'), output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear)

        if self.request.user.is_superuser is False:
            querytotalsalessalesman = querytotalsalessalesman.filter(salesman__in=salesmanid)
            querymonthlytargetsalesman = querymonthlytargetsalesman.filter(salesman__in=salesmanid)

        salesmancount = int(querytotalsalessalesman.count())
        salesmanTotal = []
        salesmanLabel = ''
        salesmanLabels = []
        salesmantargetLabels = []
        salesmantargettotal = []
        s = 0
        if salesmancount == 0 :
            salesmanTotal.append(
                {
                    'salesman': '',
                    'total': 0,
                    'target': 0
                }
            )

        while s < salesmancount:
            salesmanLabel = Salesman.objects.filter(pk=querytotalsalessalesman[s]['salesman']).values('name')
            salesmantargettotalq = querymonthlytargetsalesman.filter(salesman=querytotalsalessalesman[s]['salesman'])
            if salesmantargettotalq.count() > 0:
                salesmantargetLabel = Salesman.objects.filter(pk=salesmantargettotalq[0]['salesman']).values('name')
                targetotal = round(int(salesmantargettotalq[0]['total']), 1) - round(
                            int(querytotalsalessalesman[s]['total']), 1)
                if targetotal < 0:
                    targetotal = 0
                salesmanTotal.append(
                    {
                        'salesman': salesmanLabel[0]['name'],
                        'total': round(int(querytotalsalessalesman[s]['total']), 1),
                        'target': targetotal
                    }
                )
            else:
                salesmanTotal.append(
                    {'salesman': salesmanLabel[0]['name'], 'total': round(int(querytotalsalessalesman[s]['total']), 1),
                     'target': 0})
            s += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalescategory = Transactions.objects.values('category') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                '-total').filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querymonthlytargetcategory = TargetTransactions.objects.values('category') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'), output_field=IntegerField())).order_by('-total').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))
            elif date_id == 88 or date_id == 99:
                querymonthlytargetcategory = TargetTransactions.objects.values('category') \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).order_by('-total').filter(
                                        created_date__year=currentYear).filter(created_date__month__in=Quarter)
        else:
            if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                    or date_id == 10 or date_id == 11 or date_id == 12:
                querytotalsalescategory = Transactions.objects.values('category') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month=monthn).filter(created_date__year=currentYear)

                querymonthlytargetcategory = TargetTransactions.objects.values('category') \
                    .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear)
            else:
                querytotalsalescategory = Transactions.objects.values('category') \
                    .annotate(total=Sum('total')).filter(
                    Q(source='SalesOrder') | Q(source='SalesReturnOrder')).order_by(
                    '-total').filter(created_date__month__in=monthn).filter(created_date__year=currentYear)

                querymonthlytargetcategory = TargetTransactions.objects.values('category') \
                    .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'), output_field=IntegerField())).order_by('-total').filter(
                    created_date__year=currentYear)

        if self.request.user.is_superuser is False:
            querytotalsalescategory = querytotalsalescategory.filter(salesman__in=salesmanid)
            querymonthlytargetcategory = querymonthlytargetcategory.filter(salesman__in=salesmanid)

        categorycount = int(querytotalsalescategory.count())
        categoryLabel = ''
        categorytargetLabels = []
        categorytargettotal = []
        categorysalesTotal = []
        categorytargettotal = []
        cat = 0
        if categorycount == 0 :
            categorysalesTotal.append(
                {'category': '',
                 'sales': 0,
                 'target': 0}
            )

        while cat < categorycount:
            categoryLabel = Category.objects.filter(pk=querytotalsalescategory[cat]['category']).values('name')
            categorytargettotalq = querymonthlytargetcategory.filter(category=querytotalsalescategory[cat]['category'])
            try:
                categorytargettotalqv = categorytargettotalq[0]['total']
            except:
                categorytargettotalqv = 0

            try:
                querytotalsalescategoryv = querytotalsalescategory[cat]['total']
            except:
                querytotalsalescategoryv = 0

            targetotal = round(int(categorytargettotalqv), 1) - round(
                         int(querytotalsalescategoryv), 1)
            if targetotal < 0:
                targetotal = 0

            if categorytargettotalq.count() > 0:
                categorytargetLabel = Category.objects.filter(pk=categorytargettotalq[0]['category']).values('name')
                categorysalesTotal.append(
                    {'category': categoryLabel[0]['name'],
                     'sales': round(int(querytotalsalescategory[cat]['total']), 1),
                     'target': targetotal})
            else:
                categorysalesTotal.append(
                    {'category': categoryLabel[0]['name'],
                     'sales': round(int(querytotalsalescategory[cat]['total']), 1), 'target': 0})
                categorytargetLabels.append('')
                categorytargettotal.append(0)
            cat += 1

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            qtotchsm1 = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)
        elif date_id == 9999999:
            qtotchsm1 = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                created_date__month__in=monthn).filter(created_date__year=currentYear)
        else:
            qtotchsm1 = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(
                created_date__month=monthn).filter(created_date__year=currentYear)


        if date_id == 1 or date_id == 2 or date_id == 3 or date_id == 4 or date_id == 5 or date_id == 6 or date_id == 7 or date_id == 8 or date_id == 9 \
                or date_id == 10 or date_id == 11 or date_id == 12:
            querytotalsalessalesman = Transactions.objects.values('channel').order_by('channel').annotate(total=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month=monthn).filter(created_date__year=currentYear)
            querytotalsales = Transactions.objects.annotate(totals=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month=monthn).filter(created_date__year=currentYear)

            querymonthlytargetsalesman = TargetTransactions.objects.values('channel').order_by('channel') \
                .annotate(totals=Sum(F(cmonths) * F('price'), output_field=IntegerField())).values('totals').filter(
                created_date__year=currentYear)
            querymonthlytarget = TargetTransactions.objects \
                .annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).values('total').filter(
                created_date__year=currentYear)
        elif date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            querytotalsalessalesman = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)
            querytotalsales = Transactions.objects \
                .annotate(totals=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month__in=Quarter).filter(created_date__year=currentYear)

            if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77:
                querymonthlytargetsalesman = TargetTransactions.objects.values('channel').order_by('channel') \
                    .annotate(totals=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'),
                                         output_field=IntegerField())).values('totals').filter(Q(created_date__year=currentYear) | Q(created_date__month__in=Quarter))
                querymonthlytarget = TargetTransactions.objects \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3)) * F('price'),
                                        output_field=IntegerField())).values('total').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)

            elif date_id == 88 or date_id == 99:
                querymonthlytargetsalesman = TargetTransactions.objects.values('channel').order_by('channel') \
                    .annotate(totals=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                         output_field=IntegerField())).values('totals').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)
                querymonthlytarget = TargetTransactions.objects \
                    .annotate(total=Sum((F(cmonth1) + F(cmonth2) + F(cmonth3) + F(cmonth4) + F(cmonth5) + F(cmonth6)) * F('price'),
                                        output_field=IntegerField())).values('total').filter(
                    created_date__year=currentYear).filter(created_date__month__in=Quarter)


        else:
            querytotalsalessalesman = Transactions.objects.values('channel').order_by('channel') \
                .annotate(total=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month__in=monthn).filter(created_date__year=currentYear)
            querytotalsales = Transactions.objects \
                .annotate(totals=Sum('total')).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__month__in=monthn).filter(created_date__year=currentYear)

            querymonthlytargetsalesman = TargetTransactions.objects.values('channel').order_by('channel') \
                .annotate(totals=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                                    output_field=IntegerField())).values('totals').filter(
                created_date__year=currentYear)
            querymonthlytarget = TargetTransactions.objects \
                .annotate(total=Sum((F('m1') + F('m2') + F('m3') + F('m4') + F('m5') + F('m6') + F('m7') + F('m8') + F('m9') + F('m10') + F('m11') + F('m12')) * F('price'),
                                    output_field=IntegerField())).values('total').filter(created_date__year=currentYear)

        querytotalsalesv = querytotalsales.aggregate(total=Sum('total'))

        if querytotalsalesv['total'] is None:
            totalsalesv = 0
        else:
            totalsalesv = int(querytotalsalesv['total'])

        try:
            totaltargetv = int(querymonthlytarget[0]['total'])
        except:
            totaltargetv = 0


        if totaltargetv != 0:
            acheivedv = (totalsalesv / totaltargetv) * 100
        else:
            acheivedv = 0

        chcount = int(qtotchsm1.count())
        chsm1 = 0
        chsmqs1 = []
        while chsm1 < chcount:


            qtotsm = querytotalsalessalesman.values('salesman', 'total').order_by('-total').filter(
                channel_id=qtotchsm1[chsm1]['channel'])

            ttotsm = querymonthlytargetsalesman.values('salesman', 'totals').order_by('-totals').filter(
                channel_id=qtotchsm1[chsm1]['channel'])
            if qtotsm.count() > 0:
                try:
                    chsalesv = int(qtotsm[0]['total'])
                except:
                    chsalesv = 0

                try:
                    chtargetv = int(ttotsm[0]['totals'])
                except:
                    chtargetv = 0

                try:
                    chsalesp = int((chsalesv / totalsalesv) * 100)
                except:
                    chsalesp = 0

                try:
                    acheivedv = (chsalesv / chtargetv) * 100
                except:
                    chtargetp = 0

                try:
                    chtargetp = (chtargetv / totaltargetv) * 100
                except:
                    chtargetp = 0


                chsmLabel = Channel.objects.filter(pk=qtotchsm1[chsm1]['channel']).values('name')

                chsmsalesmanLabel = Salesman.objects.filter(pk=qtotsm[0]['salesman']).values('name')

                chsmqs1.append({'channel': chsmLabel[0]['name'], 'salesman': chsmsalesmanLabel[0]['name'],
                                'total': chsalesv,
                                'salesp': round(acheivedv)})
            chsm1 += 1

        ch1 = 0
        chq1 = []
        while ch1 < chcount:
            qtot = qtotchsm1.values('customer', 'total').order_by('-total').filter(channel_id=qtotchsm1[ch1]['channel'])
            chLabel = Channel.objects.filter(pk=qtotchsm1[ch1]['channel']).values('name')
            chLabels = Customer.objects.filter(pk=qtot[0]['customer']).values('name')
            if qtot[0]['total'] is None:
                totalqq = 0
            else:
                totalqq = round(int(qtot[0]['total']), 1)
            chq1.append({'customer': chLabels[0]['name'], 'channel': chLabel[0]['name'],
                         'total': totalqq})
            ch1 += 1

        if totalmonthlysaless is None:
            totalmonthlysaless = 0
        if totalmonthlytargets is None:
            totalmonthlytargets = 0
        if chcount is None:
            chcount = 0
        targetvsactual = totalmonthlysaless - totalmonthlytargets
        if totalmonthlysaless > totalmonthlytargets:
            if totalmonthlysaless > 0:
                totalmonthlysalessperc = round(((((totalmonthlysaless - totalmonthlytargets) / totalmonthlysaless)) * 100))
            else:
                totalmonthlysalessperc = 0
            totalmonthlytargetsperc = 0
        else:
            if totalmonthlytargets != 0 and  totalmonthlysaless !=0:
                totalmonthlytargetsperc = round(((totalmonthlysaless / totalmonthlytargets) * 100))
            else:
                totalmonthlytargetsperc = 0
            totalmonthlysalessperc = 0

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all()
        else:
            customers = Customer.objects.all().filter(salesman__in=salesmanid)
            qcollections = Collection.objects.all().filter(customer_id__in=customers)

        if date_id == 44 or date_id == 55 or date_id == 66 or date_id == 77 or date_id == 88 or date_id == 99:
            qqcollections = qcollections \
                .annotate(total=Sum('amount')).filter(created_date__year=currentYear).filter(created_date__month__in=Quarter)
        elif date_id == 9999999:
            qqcollections = qcollections \
                .annotate(total=Sum('amount')).filter(created_date__month__in=monthn).filter(created_date__year=currentYear)
        else:
            qqcollections = qcollections \
                .annotate(total=Sum('amount')).filter(created_date__year=currentYear).filter(created_date__month=monthn)

        collectionamount = qqcollections.aggregate(total=Sum('amount'))
        collectamount = collectionamount['total']
        if collectamount is None:
            collectamount = 0
        else:
            collectamount = round(collectionamount['total'])

        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser:
            users = User.objects.all().exclude(pk=self.request.user.id)
            todos = ToDoList.objects.all().filter(done=0).order_by('-priority', '-created_date')
            todos_done = ToDoList.objects.all().filter(done=1).order_by('-priority', '-created_date')
        else:
            if salesmanid.count() == 0:
                users = User.objects.all().filter(pk=self.request.user.id)
                salesmanid = Salesman.objects.filter(user=self.request.user.id).values('user')
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id)).values('user')
                users = User.objects.all().filter(pk__in=salesmanid)

            todos = ToDoList.objects.all().filter(done=0, to_user__in=salesmanid).order_by('-priority', '-created_date')
            todos_done = ToDoList.objects.all().filter(done=1, to_user__in=salesmanid).order_by('-priority', '-created_date')

        context = {
            'custcount': custcount,
            'chcount': chcount,
            'citycount': citycount,
            'totalpurchase': totalpurchase,
            'totalsales': totalsales,
            'totalsalesreturn': totalsalesreturn,
            'totalpurchasereturn': totalpurchasereturn,
            'netpurchase': netpurchase,
            'totalqty': totalqty,
            'ctrqty': ctrqty,
            'querymonthlytarget': querymonthlytarget,
            'totalmonthlytargets': totalmonthlytargets,
            'totalmonthlysaless': totalmonthlysaless,
            'targettransactions': targettransactions,
            'targetvsactual': targetvsactual,
            'cmonths': cmonths,
            'monthname': monthname,
            'totalmonthlytargetsperc': totalmonthlytargetsperc,
            'totalmonthlysalessperc': totalmonthlysalessperc,
            'daysspent': daysspent,
            'querytotalsaleschannel': querytotalsaleschannel,
            'querytotalsalessalesman': querytotalsalessalesman,
            'querymonthlytargetsalesman': querymonthlytargetsalesman,
            'channelTotal': channelTotal,
            'channelcount': range(0, channelcount),
            'channelLabels': channelLabels,
            'salesmanTotal': salesmanTotal,
            'salesmanLabels': salesmanLabels,
            'salesmantargettotal': salesmantargettotal,
            'salesmantargetLabels': salesmantargetLabels,
            'querytotalsalescategory': querytotalsalescategory,
            'categorytargetLabels': categorytargetLabels,
            'categorytargettotal': categorytargettotal,
            'chsmqs1': chsmqs1,
            'chq1': chq1,
            'queryallmonthsales': queryallmonthsales,
            'channelsales': channelsales,
            'categorysalesTotal': categorysalesTotal,
            'allmonthsales': allmonthsales,
            'querytotaltargetchannel': querytotaltargetchannel,
            'channelsales': channelsales,
            'areasales': areasales,
            'collectamount': collectamount,
            'salesmanncount': salesmanncount,
            'currentYear': currentY,
            'lastyear': lastYear,
            'date_id': date_id,
            'yearsq': yearsq,
            'yearlist': yearlist,
            'thismonth': date_id,
            'CurrentYY': year_id,
            'todos': todos,
            'todos_done': todos_done,
            'users': users,

        }
        return context


dashboard_view = DashboardView.as_view(template_name="dashboard/dashboard2.html")
