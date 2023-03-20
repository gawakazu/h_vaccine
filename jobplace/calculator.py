
import calendar
from .models import DateModel,RegisterModel
def previous_month(current_month):
    date = current_month.split('/')
    if int(date[1])==1:
        date[1]="12"
        date[0]=str(int(date[0][:4])-1)
        date=date[0]+'-'+date[1]
    else:
        date=date[0]+'-'+str(int(date[1])-1)
    return date

def next_month(current_month):
    date = current_month.split('/')
    if int(date[1])==12:
        date[1]="1"
        date[0]=str(int(date[0][:4])+1)
        date=date[0]+'-'+date[1]
    else:
        date=date[0]+'-'+str(int(date[1])+1)
    return date

def date_cal(initial_date,locate):
    date = initial_date.split('/')#2022/6 --> [2022,6]
    cal_data = calendar.monthrange(int(date[0]),int(date[1]))#cal_data[0]:1日の曜日、cal_data[1]:当月の日数
    date_list = ['-' for i in range(cal_data[0]+1) if i<cal_data[0]+1]# 1日の前に'-'を追加。cal_date[0]は月曜が0のため、日曜からのｶﾚﾝﾀﾞｰでは１をﾌﾟﾗｽ。
    select = DateModel.objects.filter(date__icontains=initial_date)
    select = [i.date for i in select]
    select_full,select_half,select_empty = [],[],[]
    for i in select:
        if locate == "---":#会場が設定されていない場合、2会場の空きを表示する（double：2）
            select_num = RegisterModel.objects.filter(date__date=i).count()
            double = 2
        else:
            select_num = RegisterModel.objects.filter(place__place=locate,date__date=i).count()
            double = 1
        if select_num < 4*double :# 1会場なら3までが空きあり’〇’　2会場はdoubleで'6'
            select_empty.append(i)
        elif select_num >= 4*double and select_num < 8*double :
            select_half.append(i)
        else:
            select_full.append(i)
    select_empty = [int(i[i.find('/',5)+1:]) + cal_data[0]+1 for i in select_empty] # 2022/7/1 7以降の'/'を見つけ、次の値'1'を抽出
    select_half = [int(i[i.find('/',5)+1:]) + cal_data[0]+1 for i in select_half] 
    select_full = [int(i[i.find('/',5)+1:]) + cal_data[0]+1  for i in select_full]        
    for i in range(1,cal_data[1]+1):
        date_list.append(i)
    return date_list,select_empty,select_half,select_full