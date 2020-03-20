/*对象（类）*/
function NewCategory() {

}

/*构造函数的run方法*/
NewCategory.prototype.run = function () {
    var self = this;
    self.listenAddCategoryEvent();
    self.listenEditCategoryEvent();
    self.listenDeleteCategory();
};

/*NewCategory的点击事件*/
NewCategory.prototype.listenAddCategoryEvent = function () {
    var addBtn = $('#add-btn');
    addBtn.click(function () {
        xfzalert.alertOneInput({
            'title': '添加新闻分类',
            'placeholder': '请输入新闻分类',
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/add_news_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            console.log(result);
                            window.location.reload();
                        } else {
                            xfzalert.close();
                        }
                    }
                });
            }
        });
    });
};

NewCategory.prototype.listenEditCategoryEvent = function () {
    /*this代表的是NewCategory这个对象*/
    var editBtn = $(".edit-btn");
    editBtn.click(function () {
        /*this代表的是编辑按钮*/
        var currentBtn = $(this);
        /* 编辑按钮的父级元素(td).td的父级元素(tr)*/
        var tr = currentBtn.parent().parent();
        /*attr是代表属性*/
        var pk = tr.attr("data-pk");
        var name = tr.attr("data-name");
        xfzalert.alertOneInput({
            'title': '修改分类的名称',
            'placeholder': '请输入新的分类名称',
            'value': name,
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/edit_news_category/',
                    'data': {
                        'pk': pk,
                        /*填写输入的name,也就是inputValue*/
                        'name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            console.log(result);
                            /*将网页重新加载一次*/
                            window.location.reload();
                        } else {
                            xfzalert.close()
                        }
                    }
                });
            }
        });
    });
};

NewCategory.prototype.listenDeleteCategory = function () {
    var deleteBtn = $(".delete-btn");
    deleteBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr("data-pk");
        xfzalert.alertConfirm({
            'title': '确定要删除该分类吗?',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_news_category/',
                    'data': {
                        'pk': pk
                    },
                    'success': function (result) {
                        if (result[code] === 200) {
                            window.location.reload()
                        } else {
                            xfzalert.close()
                        }
                    }
                });
            }
        });
    });
};

/*构造函数*/
$(function () {
    var category = new NewCategory();
    category.run();
});