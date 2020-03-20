function CourseCategory() {

}

CourseCategory.prototype.listenAddCourseCategoryEvent = function () {
    var addBtn = $('#add-btn');
    addBtn.click(function () {
        xfzalert.alertOneInput({
            'title': '请输入新的课程名称',
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/add_course_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location.reload()
                        } else {
                            xfzalert.close()
                        }
                    }
                })
            }
        })
    })
};

CourseCategory.prototype.listenEditCourseCategoryEvent = function () {
    var editBtn = $(".edit-btn");
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var category_id = tr.attr("data-pk");
        var category_name = tr.attr("data-name");
        xfzalert.alertOneInput({
            'title': '请输入修改后的分类名称',
            'value': category_name,
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/edit_course_category/',
                    'data': {
                        'category_id': category_id,
                        'new_name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location.reload()
                        }
                    }
                })
            }
        })
    })
};

CourseCategory.prototype.listenDelCourseCategoryEvent = function () {
    var delBtn = $(".delete-btn");
    delBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr("data-pk");
        xfzalert.alertConfirm({
            'title': '您确定要删除该课程分类? ',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_course_category/',
                    'data': {
                        'category_id': pk
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location.reload()
                        } else {
                            xfzalert.close();
                        }
                    }
                })
            }
        })
    })
};

CourseCategory.prototype.run = function () {
    var self = this;
    self.listenEditCourseCategoryEvent();
    self.listenAddCourseCategoryEvent();
    self.listenDelCourseCategoryEvent();
};

$(function () {
    var cou_category = new CourseCategory();
    cou_category.run();
});