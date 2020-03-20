function News() {
    this.progressGroup = $("#progress-group");
}

News.prototype.initUEditor = function () {
    window.ue = UE.getEditor("editor", {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};

/* 将图片上传到自己的服务器上 */
News.prototype.listenUploadFileEvent = function () {
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            /* 告诉JQuery，这是一个文件，不是一个普通的文本字符串，不需要你再去处理 */
            'processData': false,
            /*默认使用文件的格式*/
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    /* 如果图片上传成功，服务器就要返回图片链接，链接就在data中 */
                    var url = result['data']['url'];
                    var thumbnailInput = $("#thumbnail-form");
                    thumbnailInput.val(url);
                }
            }
        })
    });
};

/* 将图片上传到七牛云中 */
News.prototype.listenQiniuUploadFileEvent = function () {
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    for (var i = 0; i <= file.name.split('.').length; i++) {
                        if (i === file.name.split('.').length) {
                            var key = (new Date()).getTime() + '.' + file.name.split('.')[i];
                        }
                    }
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'video/x-ms-wmv', 'image/jpeg', 'audio/mp3', 'audio/mpeg']
                        // mimeType:null
                    };
                    var config = {
                        /* 是否使用CDN加速 */
                        useCdnDomain: true,
                        /* 如果你当前网络不好，他总共回发送6次请求 */
                        retryCount: 6,
                        /* 上传文件到那个空间,根据后端定位的空间地址 */
                        region: qiniu.region.z2
                    };
                    var observable = qiniu.upload(file, key, token, putExtra, config);
                    observable.subscribe({
                        /* 上传过程中重复调用的函数 */
                        "next": self.updateUploadProgress,
                        /* 上传过程中发生错误，调用下面函数，并且传入一个错误的信息 */
                        "error": self.uploadErrorEvent,
                        /* 文件上传使用的函数 */
                        "complete": self.complateUploadEvent
                    });
                }
            }
        });
    });
};

News.prototype.updateUploadProgress = function (response) {
    var self = this;
    var total = response.total;
    var percent = total.percent;
    var percentText = percent.toFixed(0) + '%';
    var progressGroup = News.progressGroup;
    progressGroup.show();
    var progressBar = $(".progress-bar");
    if (percent === 100) {
        progressBar.removeAttr("style", 1);
        progressBar.removeAttr().val()
    }
    progressBar.css({"width": percentText});
    progressBar.text(percentText);
};

News.prototype.uploadErrorEvent = function (error) {
    window.messageBox.showError(error.message);
    var progressGroup = $("#progress-group");
    progressGroup.hide();
};

News.prototype.complateUploadEvent = function (response) {
    var self = this;
    var filename = response['key'];
    var domain = "http://q2yx3wc2f.bkt.clouddn.com/";
    var thumbnailUrl = domain + filename;
    var thumbnailInput = $("#thumbnail-form");
    thumbnailInput.val(thumbnailUrl);
    var progressGroup = $("#progress-group");
    progressGroup.hide();
};

News.prototype.listensubmitEvent = function () {
    var submitBtn = $("#submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr("data-news-id");
        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();
        var url = '';
        if (pk) {
            url = '/cms/edit_news/';
        } else {
            url = '/cms/news_release/';
        }
        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
                'pk': pk
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    if (pk) {
                        xfzalert.alertSuccess('新闻编辑成功! ', function () {
                            window.location.reload();
                        })
                    } else {
                        xfzalert.alertSuccess('新闻添加成功！ ', function () {
                            window.location.reload();
                        })
                    }
                }
            }
        });
    });

};

News.prototype.run = function () {
    var self = this;
    self.initUEditor();
    self.listensubmitEvent();
    // self.listenQiniuUploadFileEvent();
    self.listenUploadFileEvent();
};

$(function () {
    var news = new News();
    news.run();
    News.progressGroup = $("#progress-group");
});