function CMSNewsList() {

}

CMSNewsList.prototype.initDatePicker = function () {
    var startPicker = $("#start-picker");
    var endPicker = $("#end-picker");
    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth() + 1) + '/' + todayDate.getDate();
    var options = {
        'showButtonPanel': true,
        'format': 'yyyy/mm/dd',
        'startDate': '2019/5/20',
        'endDate': todayStr,
        'language': 'zh-CN',
        'todayBtn': 'linked',
        'todayHighlight': true,
        'clearBtn': true,
        'autoclose': true
    };
    startPicker.datepicker(options);
    endPicker.datepicker(options);

};

CMSNewsList.prototype.ListenDeleteNewsEvent = function () {
    var deleteBtn = $(".delete-btn");
    deleteBtn.click(function () {
        var btn = $(this);
        var news_id = btn.attr("data-news-id");
        xfzalert.alertConfirm({
            'title': '您确定要删除该条新闻？ ',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_news/',
                    'data': {
                        "news_id": news_id
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            // 重新加载页面
                            // window.location = window.location.href 兼容性更好
                            //  window.location.reload()因为兼容性不是特别好
                            window.location.reload()
                        } else {
                            xfzalert.close()
                        }
                    }
                })
            }
        })
    });
};

CMSNewsList.prototype.run = function () {
    var self = this;
    self.initDatePicker();
    self.ListenDeleteNewsEvent();
};

$(function () {
    var newsList = new CMSNewsList();
    newsList.run();
});