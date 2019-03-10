import hashlib
import random
import time

from django.core.cache import cache
from django.shortcuts import render, redirect



from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype, Goods, User


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


# def market(request,categoryid=104749):
def market(request):
    # 分类信息
    foodtypes = Foodtype.objects.all()

    # 商品信息
    # goods_list = Goods.objects.all()[0:100]
    # 默认打开页面（热销榜）
    # 点击左侧分类，即显示对应分类，商品信息[传参数categoryid]
    # goods_list=Goods.objects.filter(categoryid=categoryid)

    #客户端需要记录点击的分类下标[cookies会自动携带]
    # 从cookies中获取index下标
    index=int(request.COOKIES.get('index','0'))
    # 根据index获取对应的分类 ID
    categoryid=foodtypes[index].typeid
    # 根据分类ID获取对应的分类信息
    goods_list = Goods.objects.filter(categoryid=categoryid)

    # 获取子类信息
    childtypenames = foodtypes[index].childtypenames
    # 存储子类信息列表
    childtypelist =[]
    # 将对应的子类拆分出来
    # 遍历获取子类中的每个子元素
    for item in childtypenames.split('#'):
        # item  >>>     全部分类：  0
        # item  >>>    子类名称：  子类id
        # 继续使用：拆分出每个元素
        item_arr = item.split(':')
        temp_dir={
            'childname':item_arr[0],
            'childid':item_arr[1],
        }
        childtypelist.append(temp_dir)

    data1={
        'foodtypes':foodtypes,
        'goods_list':goods_list,
        'childtypelist':childtypelist,
    }

    return render(request,'market/market.html',context=data1)


def cart(request):
    return render(request,'cart/cart.html')


def mine(request):
    # 获取token
    token = request.session.get('token')
    userid = cache.get(token)
    user = None
    if userid:

        user = User.objects.get(pk=userid)

    return render(request, 'mine/mine.html', context={'user':user})



def login(request):
    return render(request,'mine/login.html')


def generate_password(param):
    md5=hashlib.md5()
    md5.update(param.encode('utf-8'))
    return md5.hexdigest()


def generate_token():
    temp = str(time.time()) + str(random.random())
    md5 = hashlib.md5()
    md5.update(temp.encode('utf-8'))
    return md5.hexdigest()

def register(request):
    if request.method =='GET':
        return render(request,'mine/register.html')
    elif request.method =='POST':
        # 获取数据（用于判断数据是否能够获得）
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = generate_password(request.POST.get('password'))
        # print(email,password,name)

        # 将数据存入数据库
        # 首先实例化一个user对象
        user = User()
        user.email = email
        user.password = password
        user.name = name
        user.save()
        
        # 状态保持
        token = generate_token()
        # key-value  >> token:userid
        cache.set(token,user.id,60*60*24*3)

        request.session['token'] = token

        response = redirect('axf:mine')
        return response

def logout(request):
    # 清除退出
    request.session.flush()
    return redirect('axf:mine')