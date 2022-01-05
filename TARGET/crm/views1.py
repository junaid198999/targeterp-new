class SalesmanSalesRepView(LoginRequiredMixin, TemplateView):
    def get(self, request):
        salesmanid = Salesman.objects.all().filter(reporting_to=self.request.user.id).values('reporting_to')
        if self.request.user.is_superuser is False:
            customers = Customer.objects.filter(salesman__in=salesmanid)
        else:
            customers = Customer.objects.all()

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

        today = datetime.date.today()
        currentYear = timezone.now().year
        months = ['zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12']
        if month_id == 9898989998:
            current_month1 = months[today.month]
        else:
            current_month1 = month_id
        current_month = int(current_month1)
        financialyears = FinancialYear.objects.all()

        for financialyear in financialyears:
            if financialyear.m1 == current_month:
                cmonths= 'm1'
                monthn = '1'
                monthname= 'Jan'
                numberofdays = 31
            elif financialyear.m2 == current_month:
                cmonths= 'm2'
                monthn = '2'
                monthname= 'Feb'
                numberofdays = 28
            elif financialyear.m3 == current_month:
                cmonths= 'm3'
                monthn = '3'
                monthname= 'Mar'
                numberofdays = 31
            elif financialyear.m4 == current_month:
                cmonths= 'm4'
                monthn = '4'
                monthname= 'Apr'
                numberofdays = 30
            elif financialyear.m5 == current_month:
                cmonths = 'm5'
                monthn = '5'
                monthname= 'May'
                numberofdays = 31
            elif financialyear.m6 == current_month:
                cmonths = 'm6'
                monthn = '6'
                monthname= 'Jun'
                numberofdays = 30
            elif financialyear.m7 == current_month:
                cmonths = 'm7'
                monthn = '7'
                monthname= 'Jul'
                numberofdays = 31
            elif financialyear.m8 == current_month:
                cmonths = 'm8'
                monthn = '8'
                monthname= 'Aug'
                numberofdays = 31
            elif financialyear.m9 == current_month:
                cmonths = 'm9'
                monthn = '9'
                monthname= 'Sep'
                numberofdays = 30
            elif financialyear.m10 == current_month:
                cmonths = 'm10'
                monthn = '10'
                monthname= 'Oct'
                numberofdays = 31
            elif financialyear.m11 == current_month:
                cmonths = 'm11'
                monthn = '11'
                monthname= 'Nov'
                numberofdays = 30
            elif financialyear.m12 == current_month:
                cmonths = 'm12'
                monthn = '12'
                monthname= 'Dec'
                numberofdays = 31
        channels = Channel.objects.all()
        salesmans = Salesman.objects.all()
        areas = Area.objects.all()

        cities = City.objects.all()
        if areas_id != 9898989998 :
            citiylist = cities.filter(area_id=areas_id)
        else:
            citiylist = cities

        parent_ch = Channel.objects.all().filter(parent_channel_id=channel_id)
        if parent_ch.count() == 0:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id=channel_id)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id=channel_id).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()
        else:
            if areas_id != 9898989998 and channel_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id)
            elif channel_id != 9898989998 and areas_id == 9898989998 and city_id == 9898989998:
                transactions = Transactions.objects.all().filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id == 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(area_id=areas_id)
            elif city_id != 9898989998 and areas_id == 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(city_id=city_id).filter(channel_id__in=parent_ch)
            elif city_id == 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch)
            elif city_id != 9898989998 and areas_id != 9898989998 and channel_id != 9898989998:
                transactions = Transactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)
                targettransactions = TargetTransactions.objects.all().filter(area_id=areas_id).filter(channel_id__in=parent_ch).filter(city_id=city_id)

            else:
                transactions = Transactions.objects.all()
                targettransactions = TargetTransactions.objects.all()

        if self.request.user.is_superuser is False:
            if salesmanid.count() == 0:
                salesmanid = Salesman.objects.filter(user=self.request.user.id)
            elif salesmanid.count() > 0:
                salesmanid = Salesman.objects.filter(Q(reporting_to__in=salesmanid) | Q(user=self.request.user.id))

            transactions = transactions.filter(salesman__in=salesmanid)
            targettransactions = targettransactions.filter(salesman__in=salesmanid)

        queryavailablestock = transactions.annotate(totalq=Sum('ctrqty')).values('ctrqty')
        totalqty = queryavailablestock.aggregate(qty=Sum('qty'))


        areacount = areas.count()
        totalmonthlylasttargetsqty = 0
        totalmonthlylastytargets = 0
        num_customers = 0
        activecustomers = 0
        channelear = []

        if month_id != 9898989998 :
            thismonth = month_id
        else:
            thismonth = int(monthn)

        if self.request.user.is_superuser:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear)
        else:
            qcollections = Collection.objects.all().filter(created_date__year = currentYear).filter(customer_id__in=customers)

        for salesman in salesmans :

            querymonthlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalmqty = querymonthlyqty.aggregate(Sum('qty'))
            if stotalmqty['qty__sum'] is None:
                stotalmqty['qty__sum'] = 0


            querymonthlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalmsales = querymonthlysales.aggregate(Sum('total'))
            if stotalmsales['total__sum'] is None:
                stotalmsales['total__sum'] = 0


            queryyearlyqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalyqty = queryyearlyqty.aggregate(Sum('qty'))
            if stotalyqty['qty__sum'] is None:
                stotalyqty['qty__sum'] = 0

            qyearlysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            stotalysales = qyearlysales.aggregate(Sum('total'))
            if stotalysales['total__sum'] is None:
                stotalysales['total__sum'] = 0


            queryyearlytarget = targettransactions.annotate(total=Sum(F(cmonths) * F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            totalyearlytarget = queryyearlytarget.aggregate(Sum('total'))
            if totalyearlytarget['total__sum'] is None:
                totalyearlytarget['total__sum'] = 0
            queryyearlytargetqty = targettransactions.annotate(qty=Sum(F(cmonths), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
            totalyearlytargetqty = queryyearlytargetqty.aggregate(Sum('qty'))
            if totalyearlytargetqty['qty__sum'] is None:
                totalyearlytargetqty['qty__sum'] = 0

            mm = 1
            totalmonthlytargets = 0
            totalmonthlytargetsqty = 0
            while mm <= thismonth:
                monthss = "m" + str(mm)
                querymonthlytarget = targettransactions.annotate(total=Sum(F(monthss)*F('price'), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
                totalmonthlytarget = querymonthlytarget.aggregate(Sum('total'))
                try:
                    totalmonthlytargets = totalmonthlytargets + totalmonthlytarget['total__sum']
                except:
                    totalmonthlytargets = 0

                querymonthlytargetqty = targettransactions.annotate(qty=Sum(F(monthss), output_field=IntegerField())).filter(created_date__year = currentYear).filter(salesman_id = salesman.id)
                totalmonthlytargetqty = querymonthlytargetqty.aggregate(Sum('qty'))
                try:
                    totalmonthlytargetsqty = totalmonthlytargetsqty + totalmonthlytargetqty['qty__sum']
                except:
                    totalmonthlytargetsqty = 0
                mm += 1

            querymonthlycustomers = customers.filter(salesman_id = salesman.id)
            collectamount_act = 0
            collectamount = 0
            for co in querymonthlycustomers:
                collections = qcollections.values('customer').order_by('customer') \
                    .annotate(total=Sum('amount')).filter(created_date__month=thismonth).filter(created_date__year = currentYear).filter(customer_id=co.id)
                collectionamount = collections.aggregate(total=Sum('amount'))
                try:
                    collectamount_act = collectamount_act + collectionamount['total']
                except:
                    collectamount_act = collectamount_act


            querymonthlylastsalesqty = transactions.values('source').order_by('source') \
                .annotate(qty=Sum('ctrqty')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).filter(created_date__year = currentYear-1).filter(salesman_id = salesman.id)
            totalmonthlylastsalesqty = querymonthlylastsalesqty.aggregate(Sum('qty'))
            if totalmonthlylastsalesqty['qty__sum'] is None:
                totalmonthlylastsalesqty['qty__sum'] = 0

            querymonthlylastysales = transactions.values('source').order_by('source') \
                .annotate(total=Sum('total')).filter(created_date__month__lte=thismonth).filter(
                Q(source='SalesOrder') | Q(source='SalesReturnOrder')).values('total').filter(created_date__year = currentYear-1).filter(salesman_id = salesman.id)
            totalmonthlylastysales = querymonthlylastysales.aggregate(Sum('total'))
            if totalmonthlylastysales['total__sum'] is None:
                totalmonthlylastysales['total__sum'] = 0

            try:
                achievedqtym = round(stotalmqty['qty__sum'] / totalyearlytargetqty['qty__sum']  * 100,1)
            except:
                achievedqtym = 0
            try:
                achievedpercm = round(stotalmsales['total__sum'] / totalyearlytarget['total__sum']  * 100,1)
            except:
                achievedpercm = 0
            try:
                achievedqtythisy = round(stotalyqty['qty__sum'] / totalmonthlytargetsqty  * 100,1)
            except:
                achievedqtythisy = 0
            try:
                achievedtotalthisy = round(stotalysales['total__sum'] / totalmonthlytargets  * 100,1)
            except:
                achievedtotalthisy = 0

            try:
                achievedqtylasty = round(stotalyqty['qty__sum'] / totalmonthlylastsalesqty['qty__sum']  * 100,1)
            except:
                achievedqtylasty = 0
            try:
                achievedtotallasty = round(stotalysales['total__sum'] / totalmonthlylastysales['total__sum']  * 100,1)
            except:
                achievedtotallasty = 0

            targetrmain = totalyearlytarget['total__sum'] - stotalmsales['total__sum']
            mname = calendar.month_name[thismonth]


            if totalyearlytarget['total__sum'] != 0 or stotalmsales['total__sum'] !=0:
                channelear.append({'salesman': salesman.name, 'salesqty': stotalmqty['qty__sum'],
                                'salestotal': stotalmsales['total__sum'],
                                'targetqty': totalyearlytargetqty['qty__sum'],
                                'targettotal': totalyearlytarget['total__sum'],
                                'targetrmain': targetrmain,
                                'achievedqtym': achievedqtym,
                                'achievedpercm': achievedpercm,
                                'achievedqtythisy': achievedqtythisy,
                                'achievedtotalthisy': achievedtotalthisy,
                                'totalmonthlytargets': totalmonthlytargets,
                                'totalmonthlytargetsqty': totalmonthlytargetsqty,
                                'achievedqtylasty': achievedqtylasty,
                                'achievedtotallasty': achievedtotallasty,
                                'monthint': thismonth,
                                'collectamount': collectamount_act,

                                })
                num_customers = num_customers + 1
                if stotalmsales['total__sum'] != 0:
                    activecustomers = activecustomers + 1

        if totalmonthlytargetsqty == 0:
            achievedqtyy = 0
        else:
            achievedqtyy = stotalyqty['qty__sum'] / totalmonthlytargetsqty
        if totalmonthlytargets == 0:
            achievedpercy = 0
        else:
            achievedpercy = stotalysales['total__sum'] / totalmonthlytargets

        activecustomersper = round(activecustomers / num_customers * 100)

        context = {
            'channelear': channelear,
            'channels': channels,
            'salesmans': salesmans,
            'areas': areas,
            'channel_id': channel_id,
            'areas_id': areas_id,
            'city_id': city_id,
            'citiylist': citiylist,
            'thismonth': thismonth,
            'mname': mname,
            'num_customers': num_customers,
            'activecustomers': activecustomers,
            'activecustomersper': activecustomersper,

        }
        return render(request, 'crm/reports/salesman-sales.html', context)
