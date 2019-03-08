from django.shortcuts import render

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype


def home(request):
    # 轮播图数据
    wheels=Wheel.objects.all()

    #获取导航
    navs = Nav.objects.all()

    #每日必购
    mustbuys = Mustbuy.objects.all()

    #商品部分
    shops = Shop.objects.all()

    shead = shops[0]
    stab = shops[1:3]
    sclass = shops[3:7]
    scommend = shops[7:]

    # 商品列表
    mainshows=Mainshow.objects.all()

    data={
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shead':shead,
        'stab':stab,
        'sclass':sclass,
        'scommend':scommend,
        'mainshows':mainshows,
    }

    return render(request,'home/home.html',context=data)


def market(request):
    foodtypes = Foodtype.objects.all()

    data1={
        'foodtypes':foodtypes,
    }
    return render(request,'market/market.html',context=data1)


def cart(request):
    return render(request,'cart/cart.html')


def mine(request):
    return render(request,'mine/mine.html')