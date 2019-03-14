import hashlib
import random
import time
from urllib.parse import parse_qs

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app.alipay import alipay
from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype, Goods, User, Cart, Order, OrderGoods


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
def market(request,childid='0',sortid='0'):

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
    # goods_list = Goods.objects.filter(categoryid=categoryid)

    # 子类
    if childid == '0':
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)

    # 排序
    # 0默认综合排序   1销量排序     2价格最低   3价格最高
    if sortid == '1':
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '2':
        goods_list = goods_list.order_by('price')
    elif sortid == '3':
        goods_list = goods_list.order_by('-price')

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
        'childid':childid,

    }

    # 获取购物车信息
    token = request.session.get('token')
    userid = cache.get(token)
    if userid:
        user = User.objects.get(pk=userid)
        carts = user.cart_set.all()
        data1['carts'] = carts

    return render(request,'market/market.html',context=data1)


def cart(request):
    token = request.session.get('token')
    userid = cache.get(token)
    if userid:  # 有登录才显示
        user = User.objects.get(pk=userid)
        carts = user.cart_set.filter(number__gt=0)

        isall = True
        for cart in carts:
            if not cart.isselect:
                isall = False

        return render(request, 'cart/cart.html', context={'carts': carts, 'isall': isall})
    else:  # 未登录不显示
        return render(request, 'cart/no-login.html')


def mine(request):
    # 获取token
    token = request.session.get('token')
    userid = cache.get(token)


    response_data = {
        'user': None
    }

    if userid:
        user = User.objects.get(pk=userid)
        response_data['user'] = user

        orders = user.order_set.all()
        # 待付款
        response_data['waitpay'] = orders.filter(status=0).count()
        # 待发货
        response_data['paydone'] = orders.filter(status=1).count()

    return render(request, 'mine/mine.html', context=response_data)


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        # 重定向位置
        back = request.COOKIES.get('back')

        users = User.objects.filter(email=email)
        if users.exists():  # 用户存在
            user = users.first()
            if user.password == generate_password(password):    # 密码验证通过
                # 更新token
                token = generate_token()

                # 状态保持
                cache.set(token, user.id, 60*60*24*3)

                # 数据传递客户端
                request.session['token'] = token

                # 根据back
                if back == 'mine':
                    return redirect('axf:mine')
                else:
                    return redirect('axf:marketbase')
            else:   # 密码错误
                return render(request, 'mine/login.html', context={'ps_err': '密码错误'})
        else:   # 不存在
            return render(request, 'mine/login.html', context={'user_err':'用户不存在'})



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


def checkemail(request):
    email = request.GET.get('email')

    # 去数据库中查找
    users = User.objects.filter(email=email)
    if users.exists():  # 账号被占用
        response_data = {
            'status': 0,  # 1可用， 0不可用
            'msg': '账号被占用!'
        }
    else:  # 账号可用
        response_data = {
            'status': 1,  # 1可用， 0不可用
            'msg': '账号可用!'
        }

    # 返回JSON数据
    return JsonResponse(response_data)


def addcart(request):
    # 获取token
    token = request.session.get('token')

    # 响应数据
    response_data={}

    # 从缓存获取userid
    if token:
        userid = cache.get(token)

        if userid:  #已经登陆
            user = User.objects.get(pk=userid)
            goodsid = request.GET.get('goodsid')
            goods = Goods.objects.get(pk=goodsid)

            #商品不存在：添加新的记录

            # 商品存在: 修改number
            carts = Cart.objects.filter(user=user).filter(goods=goods)
            if carts.exists():
                cart = carts.first()
                cart.number = cart.number + 1
                cart.save()
            else:
                cart = Cart()
                cart.user = user
                cart.goods = goods
                cart.number = 1
                cart.save()
            response_data['status'] = 1
            response_data['number'] = cart.number
            response_data['msg'] = '添加 {} 购物车成功: {}'.format(cart.goods.productlongname, cart.number)

            return JsonResponse(response_data)

    # 未登录
    # 因为是ajax操作，所以重定向是不可以的!
    # return redirect('axf:login')

    response_data['status'] = -1
    response_data['msg'] = '请登录后操作'

    return JsonResponse(response_data)


def subcart(request):
    # 商品
    goodsid = request.GET.get('goodsid')
    goods = Goods.objects.get(pk=goodsid)

    # 用户
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    # 获取对应的购物车信息
    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number - 1
    cart.save()

    response_data = {
        'msg': '删减商品成功',
        'status': 1,
        'number': cart.number
    }

    return JsonResponse(response_data)


def changecartselect(request):
    cartid = request.GET.get('cartid')

    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    response_data = {
        'msg': '状态修改成功',
        'status': 1,
        'isselect': cart.isselect
    }

    return JsonResponse(response_data)


def changecartall(request):
    isall = request.GET.get('isall')

    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)
    carts = user.cart_set.all()

    if isall == 'true':
        isall = True
    else:
        isall = False

    for cart in carts:
        cart.isselect = isall
        cart.save()

    response_data = {
        'msg': '全选/取消全选 成功',
        'status': 1
    }

    return JsonResponse(response_data)


def generate_identifier():
    temp = str(time.time()) +str(random.randrange(1000,10000))
    return temp

def generateorder(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    # 订单
    order = Order()
    order.user = user
    order.identifier = generate_identifier()
    order.save()

    # 订单商品(购物车中选中)
    carts = user.cart_set.filter(isselect=True)
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.order = order
        orderGoods.goods = cart.goods
        orderGoods.number = cart.number
        orderGoods.save()

        # 购物车中移除
        cart.delete()

    # response_data = {
    #     'msg': '生成订单',
    #     'status': 1,
    #     'identifier': order.identifier
    # }
    #
    # return JsonResponse(response_data)

    return render(request, 'order/orderdetail.html', context={'order': order})


def orderlist(request):
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    orders = user.order_set.all()

    # status_list = ['未付款', '待发货', '待收货', '待评价', '已评价']

    return render(request, 'order/orderlist.html', context={'orders': orders})


def orderdetail(request,identifier):
    order = Order.objects.filter(identifier=identifier).first()

    return render(request, 'order/orderdetail.html', context={'order': order})


def pay(request):
    orderid = request.GET.get('orderid')
    order = Order.objects.get(pk=orderid)

    sum = 0
    for orderGoods in order.ordergoods_set.all():
        sum += orderGoods.goods.price * orderGoods.number

    #支付地址信息
    data = alipay.direct_pay(
        subject='歼-10战斗机', #显示标题
        out_trade_no=order.identifier,  #项目订单号
        total_amount=str(sum),   #支付金额
        return_url= "http://47.112.199.172/axf/returnurl/"
    )
    #支付地址
    alipay_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=data)
    response_data = {
        'msg':'调用支付接口',
        'alipayurl':alipay_url,
        'status':1
    }

    return JsonResponse(response_data)


def returnurl(request):
    return redirect('axf:mine')


@csrf_exempt
def appnotifyurl(request):
    if request.method =='POST':

        # 获取到参数
        body_str = request.body.decode('utf-8')

        # 通过parse_qs函数
        post_data = parse_qs(body_str)

        # 转换为字典
        post_dic = {}
        for k, v in post_data.items():
            post_dic[k] = v[0]

        # 获取订单号
        out_trade_no = post_dic['out_trade_no']

        # 更新状态
        Order.objects.filter(identifier=out_trade_no).update(status=1)

    return JsonResponse({'msg': 'success'})