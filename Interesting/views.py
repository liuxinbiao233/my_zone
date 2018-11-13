from django.shortcuts import render, get_object_or_404
from .models import Type,Interesting
# Create your views here.
def insteresting_list(request):
    blogs=Interesting.objects.all()
    context={}
    context['blogs']=blogs
    return render(request,'interesting_list.html', context)

def things_detail(request,things_pk):
    thing = get_object_or_404(Interesting, pk=things_pk)
    context = {}
    context['thing']=thing
    return render(request,'interesting_detail.html',context)