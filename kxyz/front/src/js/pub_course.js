function PubCourse() {

}

PubCourse.prototype.initUEditor = function () {
    window.ue = UE.getEditor("editor", {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};

PubCourse.prototype.listenSubmitEvent = function () {
    var addBtn = $("#submit-btn");
    addBtn.click(function () {
        var title = $("#title-form").val();
        var category = $("#category-form").val();
        var lecturer = $("#lecturer-form").val();
        var videoUrl = $("#videoUrl-form").val();
        var coverUrl = $("#coverUrl-form").val();
        var price = $("#price-form").val();
        var duration = $("#duration-from").val();
        var profile = window.ue.getContent();
        xfzajax.post({
            'url': '/cms/pub_course/',
            'data': {
                'title': title,
                'category_id': category,
                'lecturer_id': lecturer,
                'video_url': videoUrl,
                'cover_url': coverUrl,
                'price': price,
                'duration': duration,
                'profile': profile
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    xfzalert.alertSuccess('课程发布成功', function () {
                        window.location.reload()
                    });
                }
            }
        })
    })
};

PubCourse.prototype.run = function () {
    var self = this;
    self.initUEditor();
    self.listenSubmitEvent();
};

$(function () {
    var course = new PubCourse();
    course.run();
});
