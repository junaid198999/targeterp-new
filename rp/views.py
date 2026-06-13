from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from gl.models import *
from rp.forms import *
from rp.models import *
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import (
    CreateView, ListView, UpdateView)
from django.http.response import HttpResponseRedirect
from datetime import datetime ,date
from django.db.models import F
import sy.models
from django.views.generic.edit import CreateView
from django.utils import timezone
from bootstrap_modal_forms.generic import (BSModalCreateView,BSModalUpdateView,BSModalReadView,BSModalDeleteView)
from django.db import connection
from django.http import HttpResponse
from inv.views import to_bool
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import decimal
import os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
import json
from django.http import QueryDict
from ast import literal_eval
import psycopg2
from psycopg2.extras import RealDictCursor


driver = None


def index(request):
    return render(request, 'rp/index.html')



######### Load Reports

def load_reports(request):
    isdash = request.GET.get('isdash')

    rptgroups = ReportsGroups.objects.all()
    rpt = Reports.objects.all().select_related('reportgroup').filter(isdashboard=to_bool(isdash)).values('id','code','engname','arbname','reportgroup__code').annotate(groupcode = F('reportgroup__code'))
    #rpt = Reports.objects.all()
    lstrpt=list(rpt)

    if to_bool(isdash)==False:
        return render(request, 'rp/dropdownlist/reports_menu_list.html', {'rpt': lstrpt,'rptgroups': rptgroups})
    else:
        return render(request, 'rp/dropdownlist/dashboards_menu_list.html', {'rpt': lstrpt, 'rptgroups': rptgroups})
######### End Load Reports



######### Reports Groups

class ReportsGroupsListView(LoginRequiredMixin, generic.ListView):
    model = ReportsGroups
    context_object_name = 'reportsgroups'
    template_name = 'rp/setting/list-reportsgroups.html'


class ReportsGroupsCreateView(LoginRequiredMixin,  BSModalCreateView):
    model = ReportsGroups
    form_class = ReportsGroupsForm
    template_name = 'rp/setting/create_reportsgroups.html'
    success_message = 'Success: Reports Groups was created.'
    success_url = reverse_lazy('rp:list-reportsgroups')

class ReportsGroupsUpdateView(LoginRequiredMixin, BSModalUpdateView):
    model = ReportsGroups
    template_name = 'rp/setting/edit_reportsgroups.html'
    form_class = ReportsGroupsForm
    success_message = 'Success: Reports Groups was updated.'
    success_url = reverse_lazy("rp:list-reportsgroups")

    def form_valid(self, form):
        reportsgroups = form.save()
        reportsgroups.save
        return super(ReportsGroupsUpdateView, self).form_valid(form)

class ReportsGroupsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = ReportsGroups
    template_name = 'rp/setting/delete_reportsgroups.html'
    success_message = 'Success: Reports Groups was deleted.'
    success_url = reverse_lazy('rp:list-reportsgroups')

def deletereportsgroups(request):
    Lc= ReportsGroups.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/rp/reportsgroups/")

######### End Reports Groups


######### Reports

class ReportsListView(LoginRequiredMixin, ListView):
    model = Reports
    context_object_name = 'reports'
    template_name = 'rp/setting/list-reports.html'

class ReportsCreateView(LoginRequiredMixin,  CreateView):
    model = Reports
    fields = '__all__'
    template_name = 'rp/setting/create_reports.html'
    success_message = 'Success: Reports was created.'
    success_url = reverse_lazy('rp:list-reports')

    def get_context_data(self, **kwargs):
        context = super(ReportsCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['reportsparameters'] = ReportsParametersFormSet(self.request.POST, instance=self.object)
            context['reportsparameters'].full_clean()

        else:
            context['reportsparameters'] = ReportsParametersFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        reportsparameters = context['reportsparameters']
        print('validate')
        response = super().form_valid(form)
        if reportsparameters.is_valid():
            print('validate reportsparameters')
            response = super().form_valid(form)
            reportsparameters.instance = self.object

            reportsparameters.save()
            form.save()

        else:
            print(reportsparameters.errors)
            context['reportsparameters'] = ReportsParametersFormSet()

        return response

class ReportsUpdateView(LoginRequiredMixin, UpdateView):
    model = Reports
    fields = '__all__'
    template_name = 'rp/setting/edit_reports.html'
    success_message = 'Success: Reports was updated.'
    success_url = reverse_lazy("rp:list-reports")

    def get_context_data(self, **kwargs):
        context = super(ReportsUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['reportsparameters'] = ReportsParametersFormSet(self.request.POST, instance=self.object)
            context['reportsparameters'].full_clean()
        else:
            context['reportsparameters'] = ReportsParametersFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)

        reportsparameters = context['reportsparameters']
        print('validate')
        response = super().form_valid(form)
        if reportsparameters.is_valid():
            print('validate reportsparameters')
            reportsparameters.instance = self.object
            reportsparameters.save()
            form.save()
        else:
            print(reportsparameters.errors)
            context['reportsparameters'] = ReportsParametersFormSet

        return response

class ReportsDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Reports
    template_name = 'rp/setting/delete_reports.html'
    success_message = 'Success: Reports was deleted.'
    success_url = reverse_lazy('rp:list-reports')

def deletereports(request):
    Lc= Reports.objects.all()
    for l in Lc:
       try:
            print(l)
            l.delete()
       except:
            print("not deleted connection somwhere")
    return redirect("/rp/reports/")

######### End Reports


######### New Run Reports



class ReportsRunView(LoginRequiredMixin,UpdateView):
    model = ReportsParameters
    form_class = ReportsRunForm

    #fields = '__all__'
    template_name = 'rp/trans/reportsrun.html'
    success_message = 'Success: Reports Run was updated.'


    def get_success_url(self):
        rep = self.kwargs
        rep_id= rep['pk']
        return reverse('rp:reportrun', kwargs={'id': rep_id})


    def get_context_data(self, **kwargs):
        context = super(ReportsRunView, self).get_context_data(**kwargs)
        print('get_context_data')
        rep = self.kwargs
        rep_id= rep['pk']
        rep = Reports.objects.filter(id=rep_id).values('id','code','engname','arbname','rank')
        lstrep = list(rep)
        context['reportname'] = lstrep[0]['engname']

        param_arr = []
        param_arrval = []
        repparam = ReportsParameters.objects.filter(report_id=rep_id).values('id', 'fieldname', 'engname', 'arbname',
                                                                             'rank', 'datatype', 'controltype',
                                                                             'defaultvalue', 'report_id')
        lstrepparam = list(repparam)
        for pr in lstrepparam:
            param_arr.append(pr)
            param_arr.append(
                [{'id': pr['id'], 'pname': pr['engname'], 'fieldname': pr['fieldname'],
                  'datatype': pr['datatype'], 'controltype': pr['controltype']}])

            param_arrval.append({'fieldname': pr['fieldname'], 'value': ''})
        repparams = param_arrval

        context['repparams'] = repparams
        print(context['repparams'])
        return context


    def form_valid(self, form):
        context = self.get_context_data(form=form)
        rep = self.kwargs
        rep_id = rep['id']
        print('form_valid')
        response = super().form_valid(form)
        procname = ''
        if 'preview' in self.request.POST:
            response = super().form_valid(form)

            procname = Reports.objects.filter(id=rep_id).values('datasource')

            strsql = """
            SELECT  
                'select json_agg(row)
                         From(
                            Select * from  
                            """ + procname + """
                            (' ||
                        string_agg(aa, ', ' ) 
                        || ')) row;'
                        AS sqlstring
                        FROM   
                        (
                        select  '@' || SPLIT_PART( Trim( unnest( regexp_split_to_array( pg_get_function_identity_arguments((Select oid from pg_proc 
                        where upper(proname) like upper('""" + procname + """'))), ','))),' ',1) aa )d    """


            print(strsql)
            strcursor = connection.cursor()
            strcursor.execute(strsql)
            strrow = strcursor.fetchall()
            strfun = strrow[0][0]
            strfun = strfun.replace(r'\n', ' ').replace(r'\r', '')
            # print(strfun)

            #  Replace param With Values

            usecode = os.getlogin()
            usecode = usecode
            cursor = connection.cursor()

            sql = '''
            select json_agg(row)
             From(
                Select * from  @procname(
                     @pledcode,
                    '',	'','','','','','',
                    @pfromdate,
                    @ptodate,	
                    '', -9999999999, 999999999,	'','', False, false, false, false,1
                )
                ) row;
    
            '''
            pledcode = "'101010010010'"
            pfromdate = "'2020-01-01'"
            ptodate = "'2021-01-31'"

            sql = sql.replace('@pledcode', pledcode)
            sql = sql.replace('@pfromdate', pfromdate)
            sql = sql.replace('@ptodate', ptodate)

            sql = sql.replace('@procname', procname)
            #context = super(ReportsRunView , self).get_context_data(**kwargs)

            cursor.execute(sql)
            row = cursor.fetchall()

            json_string = json.dumps(row, ensure_ascii=False)

            str = json_string
            str = str.replace(r'\n', ' ').replace(r'\r', '')
            str = str.replace('null', '""')
            str = str[2:len(str) - 2]
            str = """  "datarep" :  """ + str

            strsys = """    "datasys" :[{"usercode": "@usercode" }]     """
            strsys = strsys.replace('@usercode', usecode)
            strsys = strsys.replace('\n', '').replace('\r', '')

            strcom = """
                "company" :[
                            {"companyname":"ABC","email":"ABC@gmail.com","phone_number":"1234567","logo":null,"address":"Jed","taxregnumber":""}
                            ]
                """
            strcom = strcom.replace('\n', '').replace('\r', '')

            totstr = "{" + strcom + "," + str + "," + strsys + "}"
            totstr = totstr.rstrip('\r\n')

            context['ledgersoa'] = totstr

            return context
        else:
            print('Error')

######### End  New Run Reports


######### Reports Viewer
class ReportsContainerView(LoginRequiredMixin, ListView):
#def ReportsContainerView(request):
    model = ReportsParameters
    #context_object_name = 'reportcontainerview'
    template_name = 'rp/trans/reportcontainerview.html'



    def get_success_url(self):
        rep = self.kwargs
        rep_id= rep['id']
        #print('khaldoun')
        return reverse('rp:view_reportview', kwargs={'id': rep_id})

    def get_context_data(self, **kwargs):
        context = super(ReportsContainerView, self).get_context_data(**kwargs)
        rep = self.kwargs
        rep_id= rep['id']
        context['rep_id']=rep_id
        #print(rep_id)
        #print('rep_id')
        repparam = ReportsParameters.objects.filter(report_id=rep_id).values('id','fieldname','engname','arbname','rank','datatype','controltype','defaultvalue','report_id')

        rep = Reports.objects.filter(id=rep_id).values('id','code','engname','arbname','rank')
        lstrep = list(rep)
        context['reportname'] = lstrep[0]['engname']



        if self.request.POST:

            pass
        else:
            pass

        return context



class ReportsParamView(LoginRequiredMixin, ListView ):
#def ReportsParamView(request):
    #model = ReportsParameters
    fields = '__all__'
    context_object_name = 'reportparams'
    template_name = 'rp/trans/reportparamview.html'
    #success_message = 'Success: Items was created.'
    #success_url = reverse_lazy('rp:view-reportparam')
    #print('ReportsParamView')
    params = []



    def get_queryset(self):
        rep = self.kwargs
        rep_id= rep['id']
        #print("self.request")


        param_arr = []
        param_arrval = []

        repparam = ReportsParameters.objects.filter(report_id=rep_id).values('id','fieldname','engname','arbname','rank','datatype','controltype','defaultvalue','report_id').order_by('rank')
        lstrepparam = list(repparam)
        #print('lstrepparam',lstrepparam)
        for pr in lstrepparam:
            #print('pr',pr)
            param_arr.append(pr)

            param_arr.append(
                [{'id': pr['id'], 'pname': pr['engname'], 'fieldname': pr['fieldname'],
                 'datatype': pr['datatype'], 'controltype': pr['controltype']}])

            param_arrval.append( {'fieldname': pr['fieldname'], 'value':'' })

        #print('param_arr', param_arr)
        #return JsonResponse(param_arr, safe=False)
        #print(param_arrval)
        repparams=param_arrval
#        return repparams

        params =repparams
        #print(params)
       # print("params")

        return rep_id
    def get_context_data(self, **kwargs):
        context = super(ReportsParamView, self).get_context_data(**kwargs)
        #print(context)
        param_arr = []
        param_arrval = []
        rep = self.kwargs
        rep_id= rep['id']
        context["repid"]= rep_id
        repparam = ReportsParameters.objects.filter(report_id=rep_id).values('id','fieldname','engname','arbname','rank','datatype','controltype','defaultvalue','report_id').order_by('rank')
        lstrepparam = list(repparam)
        #context['reportname'] = lstrepparam[0]['engname']

        #print('lstrepparam',lstrepparam)
        for pr in lstrepparam:
            #print('pr',pr)
            #param_arr.append(pr)
            #print(pr['defaultvalue'])
            defval = ''
            if  pr['defaultvalue']  == None:
                if pr['controltype'] == 'check' :
                    defval = 'false'
                elif pr['controltype'] == 'date':
                    if  'from' in pr['fieldname']   :
                        first_day = date.today().replace(day=1)
                        first_day = first_day.replace(month=1)
                        defval = str(first_day)
                    else:
                        defval = str(date.today())

                elif pr['controltype'] == 'number':
                    defval = 0
            else:
                defval = pr['defaultvalue']


            #print(defval)

            param_arr.append(
                [{'id': pr['id'], 'pname': pr['engname'], 'fieldname': pr['fieldname'],
                 'datatype': pr['datatype'], 'controltype': pr['controltype'] , 'defaultvalue': defval }])

            param_arrval.append( {'fieldname': pr['fieldname'], 'name': pr['engname'] ,'datatype': pr['datatype']  , 'value':defval})

            lstparam_arrval=list(param_arrval)

        repparams =param_arrval
        #print(repparams)
        params = repparams
        #print("params")
        context['reportparams'] = repparams # lstparam_arrval

        if self.request.POST:
            #print('post')
            pass
        else:
           # print(' not post')
            #print(repparams)
            pass

        #print(context['reportparams'])

        return context
        #render(self.request, "rp/trans/reportparamview.html", {"reportparam": repparam})






######### End Reports Viewer

class ReportView(LoginRequiredMixin, ListView):
    template_name = "rp/trans/reportview.html"
    paramval = None

    def post(self, request, *args, **kwargs):
        global paramval
        paramval =request.POST.getlist

        return HttpResponse('Hello world')

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        parjson =str (paramval)
        parjson = parjson.replace(r'\n', ' ').replace(r'\r', '')
        parjson = parjson.replace('[', '').replace(']', '')
        lstjson=parjson.split(',')
        rep_id=None
        companyhead = True
        dstr='{'
        for par in lstjson:

            if "val_" in par:
                if "val_companyhead" in par:
                    x = par.split(':')
                    companyhead = x[1]

                    print(x[1])
                    #companyhead = int(x[1].replace("'", ''))

                else:
                    x = par.split(':')
                    dstr +=  x[0] + ':' + x[1] +','

            else:
                if "repid" in par:
                    x = par.split(':')
                    rep_id= int(x[1].replace("'",'') )



        repinfo =Reports.objects.filter(id=rep_id).values('datasource','josndesign')
        procname = repinfo[0]['datasource']
        #print( procname[0]['josndesign'])
        josndesign = repinfo[0]['josndesign']
        #print(procname)
        strsql =  """
        SELECT  
            'select json_agg(row)
                     From(
                        Select * from  
                        """ +  procname + """
                        (' ||
                    string_agg(aa, ', ' ) 
                    || ')) row;'
                    AS sqlstring
                    FROM   
                    (
                    select  '@' || SPLIT_PART( Trim( unnest( regexp_split_to_array( pg_get_function_identity_arguments((Select oid from pg_proc 
                    where upper(proname) like upper('""" +  procname +  """'))), ','))),' ',1) aa )d    """

        print(strsql)
        strcursor = connection.cursor()
        strcursor.execute(strsql)
        strrow = strcursor.fetchall()
        strfun = strrow[0][0]
        strfun = str(strfun)
        strfun = strfun.replace(r'\n', ' ').replace(r'\r', '')

        print(strfun)

        dstr = dstr.replace('}','').replace('>>','')
        dstr = dstr[0:len(dstr) - 1]
        dstr+='}'
        dstr1 = eval(str(dstr))
        dictparam=dict(dstr1)
        print(dictparam)

        for key in dictparam.keys():
            vp=str(key).replace('val_','@')
            strfun= strfun.replace(vp,"'" + dictparam[key] + "'")

        print(strfun)
        usecode =  self.request.user #os.getlogin()
        print(usecode)
        print('usecode')

#        usecode =  os.getlogin()
        print(usecode)

        usecode = str(usecode)
        cursor = connection.cursor()

        context = super(ReportView, self).get_context_data(**kwargs)

        cursor.execute(strfun)
        row = cursor.fetchall()

        json_string = json.dumps(row, ensure_ascii =False)

        jstr = json_string
        jstr = jstr.replace(r'\n', ' ').replace(r'\r', '')
        jstr = jstr.replace('null', '""')
        jstr = jstr[2:len(jstr)-2]
        jstr = """  "datarep" :  """ + jstr
        #print(jstr)

        strsys =  """    "datasys" :[{"usercode": "@usercode" }]     """
        strsys = strsys.replace('@usercode', usecode)
        strsys = strsys.replace('\n', '').replace('\r', '')



        strcompsql =  """
select json_agg(row)
		 From(	Select cp.code , cp.engname companyname , cp.arbname  , cpe.email, cp.logo , cp.taxregisterno , address1  address , PhoneNo phone_number
				from  sy_companyprofile cp
				left Join (
				Select address1 ,company_id
				from sy_companyprofileaddresses ca
				left join sy_addressestypes adt on ca.addresstype_id = adt.id 
				where adt.code='CURRENT'
				)cpa on cp.id = cpa.company_id
				left Join (
				Select cc.value PhoneNo ,cc.company_id from  
				sy_companyprofilecontacts cc 
				inner join sy_contactstypes ct on ct.id = cc.contacttype_id
				Where Code = 'Phone'
				)cpc on cp.id = cpC.company_id

				left Join (
				Select cc.value email ,cc.company_id from  
				sy_companyprofilecontacts cc 
				inner join sy_contactstypes ct on ct.id = cc.contacttype_id
				Where Code = 'Email'
				)cpe on cp.id = cpe.company_id
			 
		 	) row;        """

        #print(strsql)
        strcompcursor = connection.cursor()
        strcompcursor.execute(strcompsql)
        strcomprow = strcompcursor.fetchall()
        strcompfun = strcomprow[0][0]

        json_comp_string = json.dumps(strcompfun, ensure_ascii =False)

        jcomstr = json_comp_string
        jcomstr = jcomstr.replace(r'\n', ' ').replace(r'\r', '')
        jcomstr = jcomstr.replace('null', '""')
        jcomstr = jcomstr[2:len(jstr)-2]
        jcomstr = """  "company" : [{ """ + jcomstr
        #print(jcomstr)



        strcom =jcomstr
        #strcom = strcom.replace('\n', '').replace('\r', '')


        totstr = "{"  + strcom + "," + jstr +  "," + strsys + "}"
        totstr = totstr.rstrip('\r\n')

        context['josndesign'] = josndesign

        context['companyhead'] = companyhead

        context['datareport'] = totstr

        return context


class ReportsMenuListView(LoginRequiredMixin, generic.ListView):
    model = Reports
    template_name = 'rp/list-reportsmenu.html'
    path = "rp:list-reportsmenu"


class LedgerSOAListView(LoginRequiredMixin, generic.ListView):
    model = LedgerTrans
    template_name = 'rp/list-ledgersoa.html'
    path = "rp:list-ledgersoa"



    def get_context_data(self,   **kwargs):
        # The Publisher we're editing:
        cursor = connection.cursor()
        sql = '''
            Select rowno, ledcode,ledarbname, ttarbname,arbdesc,engdesc,transdate,docnumber,tdramount,tcramount,rowtot,obamount from  gl_RPLedgerSOA(
                 '101010010010',
                '',	'','','','','','',
                '2020-01-01',
                '2021-01-31',	
                '', -9999999999, 999999999,	'','', False, false, false, false,1
            );
                    
        '''

        context = super(LedgerSOAListView, self).get_context_data(**kwargs)
        #print(sql)
        cursor.execute(sql)
        row = cursor.fetchall()
        context['ledgersoa']=row
        #context = {'ledgersoa':row}

        #self.object = self.get_object(queryset=data.objects.all())
        return context #  super().get(request, *args, **kwargs)


class DashboardViewerView(LoginRequiredMixin, ListView):
    template_name = "rp/trans/dashboardview.html"
    paramval = None

    def post(self, request, *args, **kwargs):
        global paramval
        paramval = request.POST.getlist

        return HttpResponse('Hello world')

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        dash = self.kwargs
        dash_id = dash['id']


        repinfo = Reports.objects.filter(id=dash_id).values('datasource', 'josndesign')
        josndesign = repinfo[0]['josndesign']
        procname =  repinfo[0]['datasource']
        # print(procname)
        strsql = """
        select json_agg(row)
                            From(
                            Select * from [STOREDPROCEDURENAME]()           
                           ) row;
        
        """
        strsql = strsql.replace('[STOREDPROCEDURENAME]' ,procname)
        print(strsql)
        strcursor = connection.cursor()
        strcursor.execute(strsql)
        row = strcursor.fetchall()


        json_string = json.dumps(row, ensure_ascii=False)

        jstr = json_string
        jstr = jstr.replace(r'\n', ' ').replace(r'\r', '')
        jstr = jstr.replace('null', '""')
        jstr = jstr[2:len(jstr) - 2]
        jstr = """  "datarep" :  """ + jstr

        context = super(DashboardViewerView, self).get_context_data(**kwargs)

        totstr = "{"  + jstr  + "}"
        totstr = totstr.rstrip('\r\n')

        context['josndesign'] = josndesign

        #context['companyhead'] = companyhead

        context['datareport'] = totstr

        return context
