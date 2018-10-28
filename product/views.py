from django.shortcuts import get_object_or_404,HttpResponse,render_to_response
from django.core.paginator import Paginator
from product.models import Product_List,Category_of_goods


# Create your views here.

def get_comment(request,product_all_list):
    paginator = Paginator(product_all_list, 2)  # 每四个商品为一夜
    page_num = request.GET.get('page', 1)  # 获取页码参数，get请求
    page_of_products = paginator.get_page(page_num)
    current_page_num = page_of_products.number
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加入首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    # 加入。。。
    if page_range[0] - 1 >= 1:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 1:
        page_range.append('...')

    context={}
    context['products_category'] = Category_of_goods.objects.all()
    context['products'] = Product_List.objects.all()  # 获取全部博客数量
    context['page_of_products'] = page_of_products  # 获取这一页的博客数量
    context['page_range'] = page_range

    return context



def product_list(request):
    product_all_list=Product_List.objects.all()
    context=get_comment(request,product_all_list)
    return render_to_response('product_list.html',context)

def product_detail(request,product_pk):
    context={}
    context['product']=get_object_or_404(Product_List,pk=product_pk)
    return render_to_response('product_detail.html',context)

def Category(request,Category_pk):
    Category=get_object_or_404(Category_of_goods,pk=Category_pk)
    product_all_list = Product_List.objects.filter(Category=Category)
    context=get_comment(request,product_all_list)
    context['Category'] = Category
    return render_to_response('product_category.html', context)