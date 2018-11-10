import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone

from .models import ReadNum, ReadDetail


def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)

    key="%s_%s_read" %(ct.model,obj.pk)
    if not request.COOKIES.get(key):
        readnum,created=ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        #阅读排行

        date=timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk,date=date)
        readDetail.read_num+=1
        readDetail.save()

    return key


def get_seven_days_date(content_type):
    today = timezone.now().date()
    dates = []
    read_nums_sevent = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums_sevent.append(result['read_num_sum'] or 0)
    return dates, read_nums_sevent

def get_yesterday_days_date(content_type):
    today = timezone.now().date()
    dates = []
    get_yesterday_hot = []
    date = today - datetime.timedelta(days=1)
    dates.append(date.strftime('%m/%d'))
    read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
    result = read_details.aggregate(read_num_sum=Sum('read_num'))
    get_yesterday_hot.append(result['read_num_sum'] or 0)
    return dates, get_yesterday_hot
