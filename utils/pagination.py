import math
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from math import ceil
       
def pagination_class(self,queryset,request):
    try:
        page=1
        items=10
        if "page" in request.query_params:        
            page=request.query_params.get('page')
        if "page" in request.query_params:      
            items=request.query_params.get('item')

        paginator = Paginator(queryset,items)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(1)

        total_pages=math.ceil(int(queryset.count())/int(items))
        total_count= int(queryset.count())
        if total_count==0:
            total_pages=0
        # if total_count
        result={
            "data":data,
            "total_pages":total_pages,
            "total_count":total_count
        }
        return result
    except:
        raise Exception
    
    

def pagination_func(data,request):
    try:
        page=request.query_params.get('page')
        items=request.query_params.get('item')

        paginator = Paginator(data,items)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(1)
        try:
            total_page=ceil(int(data.count())/int(request.query_params.get('item')))

        except :
            total_page=ceil(int(len(data))/int(request.query_params.get('item')))

        return users,total_page
    except:
        raise Exception