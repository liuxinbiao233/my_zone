import datetime
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.shortcuts import  get_object_or_404, render
from django.utils import timezone

from comment.forms import CommentForm
from comment.models import Comment
from .models import Blog, Blog_Type
from read_statistics.utils import read_statistics_once_read, get_yesterday_days_date
from read_statistics.utils import  get_seven_days_date

def blog_with_comment(request,blog_all_list):
    paginator = Paginator(blog_all_list, 5)  # 每四个商品为一夜
    page_num = request.GET.get('page', 1)  # 获取页码参数，get请求
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 1:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 1:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    #获取日期对应的数量

    blog_dates=Blog.objects.dates('create_time', 'day', order='DESC')
    blog_dates_dic={}
    for blog_date in blog_dates:
        blog_count=Blog.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month,create_time__day=blog_date.day).count()
        blog_dates_dic[blog_date]=blog_count

    context={}
    context['blog_type_sum'] = Blog_Type.objects.annotate(blog_count=Count('blog'))
    context['blogs'] = Blog.objects.all()  # 获取全部博客数量
    context['page_of_blogs'] = page_of_blogs  # 获取这一页的博客数量
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dic
    return context

# Create your views here.
def blog_list(request):
    blog_all_list_=Blog.objects.all()
    context = blog_with_comment(request, blog_all_list_)
    return render(request,'blog_list.html',context)

def blog_detail(request,blog_pk,):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookies_key=read_statistics_once_read(request,blog)
    blog_content_type=ContentType.objects.get_for_model(blog)
    comments=Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk)

    context={}
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()  # 当前博客创建时间，随后进行比较
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['blog']=blog
    response=render(request,'blog_deatil.html',context)
    response.set_cookie(read_cookies_key, 'true')
    return response


def blog_type(request,blog_type_pk):
    blog_type = get_object_or_404(Blog_Type, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context=blog_with_comment(request,blog_all_list)
    context['blog_type']=blog_type

    return render(request,'blog_type.html', context)

def blog_date(request,year,month,day):
    blog_all_list=Blog.objects.filter(create_time__year=year,create_time__month=month,create_time__day=day)
    blog_dates_list='%s年%s月%s日' % (year, month, day)
    context=blog_with_comment(request,blog_all_list)
    context['blog_dates_list']=blog_dates_list
    return render(request,'blog_date.html', context)



#下面是关于阅读日期

def get_7_days_hot_blogs():
    today=timezone.now().date()
    date=today-datetime.timedelta(days=7)
    blogs=Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date).values('id','title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')#read_details 中的read_num
    return blogs[0:2]

def get_yesterday_hot_data():
    today=timezone.now().date()
    yesterday=today - datetime.timedelta(days=1 )
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=yesterday) \
        .values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[0:3]

def get_today_hot_date():
    today=timezone.now().date()
    blogs=Blog.objects.filter(read_details__date__lte=today,read_details__date__gte=today).values('id','title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')#read_details 中的read_num
    return blogs[:5]


def home(request):
    blog_content_type=ContentType.objects.get_for_model(Blog)
    dates,read_nums_sevent=get_seven_days_date(blog_content_type)
    date, get_yesterday_hot = get_yesterday_days_date(blog_content_type)

    #引用缓存 获取七天热门博客
    get_7_days_hot=cache.get('get_7_days_hot_blogs')
    if get_7_days_hot is None:
        get_7_days_hot=get_7_days_hot_blogs()
        cache.set('get_7_days_hot_blogs',get_7_days_hot_blogs,3600)



    context={}
    context['dates']=dates
    context['read_nums_sevent'] = read_nums_sevent

    context['get_yesterday_hot'] = get_yesterday_hot

    context['get_today_hot_date'] = get_today_hot_date()
    context['get_yesterday_hot_data']=get_yesterday_hot_data()
    context['get_7_days_hot_blogs']=get_7_days_hot_blogs()
    return render(request,'home_blog.html', context)