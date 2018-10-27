from django.shortcuts import get_object_or_404,HttpResponse,render_to_response
from product.models import Product_List,Category_of_goods


# Create your views here.


def product_list(request):
    context={}
    context['products_category']=Category_of_goods.objects.all()
    context['products']=Product_List.objects.all()
    return render_to_response('product_list.html',context)

def product_detail(request,product_pk):
    context={}
    context['product']=get_object_or_404(Product_List,pk=product_pk)
    return render_to_response('product_detail.html',context)

def Category(request,Category_pk):
    context={}
    Category=get_object_or_404(Category_of_goods,pk=Category_pk)
    context['products']=Product_List.objects.filter(Category=Category)
    context['Category']=Category
    context['products_category'] = Category_of_goods.objects.all()
    return render_to_response('product_category.html', context)