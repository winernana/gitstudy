$(function () {

    // jQuery.cookie() 的用法
    // 设置
    // $.cookie(key,value,options)

    // 获取
    // value=$.cookie(key)

    // 删除
    // $.cookie(key,null)

    // 解决方法，记录点击分类的下标，页面刷新后重新添加样式
    // var index=localStorage.getItem('index')
    // 获取值
    var index = $.cookie('index')
    console.log(index)
    if (index){ //有点击有下标
        $('.type-slider li').eq(index).addClass('active')
    } else {
        $('.type-slider li:first').addClass('active')
    }


    // 侧边栏分类  点击操作
    //点击后的效果显示是可以的，但是由于a标签的原因，点击后的样式由于重新加载页面，导致样式被清除掉
    $('.type-slider li').click(function () {
    // $(this)  代表当前点击的对象

        // $(this).addClass('active')
        // 点击后记录下标
        // localStorage.setItem('index', $(this).index())
        $.cookie('index', $(this).index(), {expires: 3, path: '/'})
    })


    // 子类
    var  categoryshow = false
    $('#category-bt').click(function(){
        // console.log(categoryshow)
        // if(categoryshow){ //隐藏
        //     // 逻辑隐藏时点击变为显示
        // categoryshow = false
        // $('.bounce-view ').hide()
        // }else{ //显示
        //     // 逻辑显示时点击变为隐藏
        // categoryshow = true
        // $('.bounce-view ').show()
        // }

        // 取反
        categoryshow = !categoryshow
        categoryshow ? categoryviewshow():categoryviewhide()
    })
        function categoryviewshow(){
        $('.category-view').show()
        $('#category-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
        }
        function categoryviewhide() {
        $('.category-view').hide()
        $('#category-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        }

    // 排序
    var sortshow = false
    $('#sort-bt').click(function () {
        sortshow = !sortshow
        sortshow ? sortviewshow():sortviewhide()
    })
        function sortviewshow(){
        $('.sort-view').show()
        $('#sort-bt i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
        }
        function sortviewhide() {
        $('.sort-view').hide()
        $('#sort-bt i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        }
})