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