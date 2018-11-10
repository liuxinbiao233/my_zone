from django.shortcuts import get_object_or_404,HttpResponse,render_to_response
from django.core.paginator import Paginator
from product.models import Product_List,Category_of_goods
from django.db.models import Count

# Create your views here.

def get_comment(request,product_all_list):
    paginator = Paginator(product_all_list, 2)  # 每四个商品为一夜
    page_num = request.GET.get('page', 1)  # 获取页码参数，get请求
    page_of_products = paginator.get_page(page_num)
    current_page_num = page_of_products.number
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

    blog_dates=Product_List.objects.dates('create_time', 'day', order='DESC')
    blog_dates_dic={}
    for blog_date in blog_dates:
        blog_count=Product_List.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month,create_time__day=blog_date.day).count()
        blog_dates_dic[blog_date]=blog_count

    context={}
    context['products_category'] = Category_of_goods.objects.annotate(blog_count=Count('product_list'))
    context['products'] = Product_List.objects.all()  # 获取全部博客数量
    context['page_of_products'] = page_of_products  # 获取这一页的博客数量
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dic
    return context



def product_list(request):
    product_all_list=Product_List.objects.all()
    context=get_comment(request,product_all_list)
    return render_to_response('product_list.html',context)

def product_detail(request,product_pk):
    context={}
    product=get_object_or_404(Product_List,pk=product_pk)
    context['previous_blog']=Product_List.objects.filter(create_time__gt=product.create_time).last()#当前博客创建时间，随后进行比较
    context['next_blog'] = Product_List.objects.filter(create_time__lt=product.create_time).first()
    context['product']=product

    return render_to_response('product_detail.html',context)

def Category(request,Category_pk):
    Category=get_object_or_404(Category_of_goods,pk=Category_pk)
    product_all_list = Product_List.objects.filter(Category=Category)
    context=get_comment(request,product_all_list)
    context['Category'] = Category
    return render_to_response('product_category.html', context)

def product_date(request,year,month,day):
    product_all_list=Product_List.objects.filter(create_time__year=year,create_time__month=month,create_time__day=day)
    product_date_category = '%s年%s月%s日' % (year, month, day)
    context = get_comment(request,product_all_list)
    context['product_date_category']=product_date_category
    return render_to_response('product_date.html',context)


