from django.shortcuts import render,redirect
from django.views.generic import ListView,TemplateView,RedirectView
from django.views import View
from django.contrib.auth import login,logout,authenticate,views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from .models import PlaceModel,DateModel,TimeModel,CustomUser,RegisterModel
from .forms import LoginForm
from . import models
import datetime
import calendar
from . import calculator

class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    form_class = LoginForm

class LogoutView(LoginRequiredMixin,LogoutView):
    template_name = 'logout.html'

class MainView(LoginRequiredMixin,TemplateView):
    template_name = 'main.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user_count = RegisterModel.objects.filter(user=self.request.user).count()#loginﾕｰｻﾞの登録有無を判断し、警告。confirmでは登録禁止。
        if user_count > 0 :
            exit = "exit"
        else :
            exit = "non"
        context['ppp'] = '---'
        context['exit'] = exit
        return context

class PlaceView(LoginRequiredMixin,ListView):
    template_name = 'place.html'
    model = PlaceModel
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        date_num = DateModel.objects.all().count()
        time_num = TimeModel.objects.all().count()
        place_list = [i.place for i in PlaceModel.objects.all()]
        place_empty,place_half,place_full = [],[],[]
        for i in place_list:
            place_num = RegisterModel.objects.filter(place__place=i).count()
            if place_num < date_num * time_num / 2 :#　設定総数（設定日＊設定時間）の半分より小さいと、empty：”〇”
                place_empty.append(i)
            elif place_num >= date_num * time_num /2 and place_num < date_num * time_num:#総数の半分以上、総数以下は、half：”△”
                place_half.append(i)
            else:
                place_full.append(i)#その他は、full：”×”
        context['place_empty'] = place_empty
        context['place_half'] = place_half
        context['place_full'] = place_full
        context['place_list'] = place_list
        return context 

class DateView(LoginRequiredMixin,ListView):
    template_name = 'date.html'
    model = DateModel
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        initial_date = str(datetime.datetime.now().year) + '/' + str(datetime.datetime.now().month)#今の年月をinitialに設定。固定なら、initial_date = "2022/6"
        locate = self.kwargs['i']
        context['place'] = str(self.kwargs['i'] + '_' + initial_date.replace('/','-') + '-')#　”/”は、View間の転送ができない。正規表現が適用される？　そのための変換。
        date_list,select_empty,select_half,select_full = calculator.date_cal(initial_date,locate)
        previous_month = calculator.previous_month(initial_date)
        next_month = calculator.next_month(initial_date)
        context['select_empty'] = select_empty
        context['select_half'] = select_half
        context['select_full'] = select_full
        context['date_list'] = date_list
        context['seven'] = [7,14,21,28]#カレンダー表示の改行のためのデータ
        context['previous_month'] = previous_month
        context['next_month'] =next_month
        return context

class Date2View(LoginRequiredMixin,ListView):
    template_name = 'date2.html'
    model = DateModel
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)       
        all = self.kwargs['place'] + self.kwargs['previous_month']# 片倉_2022-7-2022-8 会場-当月-移動月
        all_parts = all.split('_')
        place_part = all_parts[0]
        initial_date = all_parts[1].split('-')[2] + '/' + all_parts[1].split('-')[3]#split('-')[2]+split('-')[3] 移動年月(2022/6)
        date_list,select_empty,select_half,select_full = calculator.date_cal(initial_date,all_parts[0])
        previous_month = calculator.previous_month(initial_date)
        next_month = calculator.next_month(initial_date)
        context['place'] = place_part + '_' + initial_date.replace('/','-') + '-'#html移動字は、"/"から"-"へ  
        context['select_empty'] = select_empty
        context['select_half'] = select_half
        context['select_full'] = select_full
        context['date_list'] = date_list
        context['seven'] = [7,14,21,28]
        context['previous_month'] = previous_month
        context['next_month'] =next_month
        return context

class TimeView(LoginRequiredMixin,ListView):
    template_name = 'time.html'
    model = TimeModel
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        place = self.kwargs['place'] + self.kwargs['i'] +'_'
        locate = place.split('_')[0]
        date = place.split('_')[1].replace('-','/')
        time = TimeModel.objects.all()
        time_list = [i.time for i in time]
        number_empty,number_half,number_full = [],[],[]
        for i in time_list:
            if place[:3]=='---':
                context['ret_place'] ='---'
                double = 2
                num = RegisterModel.objects.filter(date__date=date,time__time=i).count()
            else:
                double = 1
                num = RegisterModel.objects.filter(place__place=locate,date__date=date,time__time=i).count()
            if num < 1*double :
                number_empty.append(i)
            elif num >= 1*double and num < 2*double :
                number_half.append(i)
            else:
                number_full.append(i) 
        context['time_list'] = time_list
        context['number_empty'] = number_empty
        context['number_half'] = number_half
        context['number_full'] = number_full
        context['select'] = place        
        return context

class ConfirmView(LoginRequiredMixin,TemplateView):
    template_name = 'confirm.html'
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(**kwargs)
        select = self.kwargs['select']
        i = self.kwargs['i']
        final = self.kwargs['select'] + self.kwargs['i']
        context['final'] = final
        user_count = RegisterModel.objects.filter(user=self.request.user).count()
        if user_count > 0 :
            exit = "exit"
        else:
            exit = "non"
        context['exit'] = exit
        return context
    def post(self,request,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        final = request.POST['final']
        member = final.split('_')
        member = [i.replace('-','/') if '-' in i else i for i in member ]
        place = PlaceModel.objects.get(place=member[0])
        date = DateModel.objects.get(date=member[1])
        time= TimeModel.objects.get(time=member[2])
        RegisterModel.objects.create(user=self.request.user,place=place,date=date,time=time)
        return redirect('main')

class Place2View(LoginRequiredMixin,ListView):
    template_name = 'place2.html'
    model = PlaceModel
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(**kwargs)
        all = self.kwargs['select'] + self.kwargs['i']
        select = all[3:]
        date = select.split('_')[1].replace('-','/')
        time = select.split('_')[2]
        place = PlaceModel.objects.all()
        place_list = [i.place for i in place]
        place_empty,place_half,place_full = [],[],[]
        for i in place_list:
            num = RegisterModel.objects.filter(place__place=i,date__date=date,time__time=time).count()
            if num == 0 :
                place_empty.append(i)
            elif num < 2 :
                place_half.append(i)
            else:
                place_full.append(i)
        i = all[all.find(':')-2:]
        context['place_list'] = place_list
        context['select'] = select     
        context['place_empty'] = place_empty
        context['place_half'] = place_half
        context['place_full'] = place_full
        return context

