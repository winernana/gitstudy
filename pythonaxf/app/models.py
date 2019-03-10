from django.db import models

class BaseModel(models.Model):
    img=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    trackid=models.CharField(max_length=20)

    class Meta:
        # 抽象类
        abstract = True

# 轮播图 模型类
class Wheel(BaseModel):
    class Meta:
        db_table = 'axf_wheel'

# 导航 模型类
class Nav(BaseModel):
    class Meta:
        db_table = 'axf_nav'

# 每日必购
class Mustbuy(BaseModel):
    class Meta:
        db_table='axf_mustbuy'


#部分商品
class Shop(BaseModel):
    class Meta:
        db_table='axf_shop'

# 商品列表，模型类
class Mainshow(BaseModel):
    trackid = models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    img=models.CharField(max_length=100)
    categoryid=models.CharField(max_length=20)
    brandname=models.CharField(max_length=100)

    img1=models.CharField(max_length=100)
    childcid1=models.CharField(max_length=100)
    productid1=models.CharField(max_length=20)
    longname1=models.CharField(max_length=100)
    price1=models.CharField(max_length=20)
    marketprice1=models.CharField(max_length=100)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=100)
    productid2 = models.CharField(max_length=20)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=20)
    marketprice2 = models.CharField(max_length=100)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=100)
    productid3 = models.CharField(max_length=20)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=20)
    marketprice3 = models.CharField(max_length=100)

    class Meta:
        db_table='axf_mainshow'

    def __str__(self):
        return self.name

# insert into axf_foodtypes(typeid,typename,childtypenames,typesort)
class Foodtype(models.Model):
    # 分类id
    typeid=models.CharField(max_length=20)
    # 分类名称
    typename=models.CharField(max_length=100)
    # 子类（多个）
    childtypenames=models.CharField(max_length=255)
    # 分类排序
    typesort=models.IntegerField()

    class Meta:
        db_table='axf_foodtypes'

# 商品模型
class Goods(models.Model):
    # 商品id
    productid=models.CharField(max_length=10)
    # 商品图片
    productimg=models.CharField(max_length=200)
    # 商品名称
    productname=models.CharField(max_length=100)
    # 商品长名字
    productlongname=models.CharField(max_length=200)
    # 精选
    isxf = models.BooleanField(default=False)
    # 是否买一送一
    pmdesc = models.BooleanField(default=False)
    # 商品规格
    specifics = models.CharField(max_length=100)
    # 商品价格
    price = models.DecimalField(max_digits=6,decimal_places=2)
    # 超市价格
    marketprice = models.FloatField()
    # 分类ID
    categoryid = models.CharField(max_length=10)
    # 子类ID
    childcid = models.CharField(max_length=10)
    # 子类名字
    childcidname = models.CharField(max_length=50)
    # 详情页id
    dealerid = models.CharField(max_length=10)
    # 库存量
    storenums = models.IntegerField()
    # 销售量
    productnum = models.IntegerField()

    class Meta:
        db_table='axf_goods'

class User(models.Model):
    #邮箱
    email = models.CharField(max_length=40,unique=True)
    # 密码
    password=models.CharField(max_length=255)
    # 昵称
    name=models.CharField(max_length=100)
    # 头像
    img=models.CharField(max_length=40,default='tx.jpeg')
    # 等级
    rank=models.IntegerField(default=1)

    class Meta:
        db_table='axf_user'