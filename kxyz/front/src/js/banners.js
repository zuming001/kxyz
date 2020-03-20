function Banners() {

}

/* 轮播图展示函数 */
Banners.prototype.loadData = function () {
    var self = this;
    xfzajax.get({
        'url': '/cms/banner_list/',
        'success': function (result) {
            if (result['code'] === 200) {
                var banners = result['data'];
                for (var i = 0; i < banners.length; i++) {
                    var banner = banners[i];
                    self.createBannerEvent(banner)
                }
            }
        }
    })
};

/* 这是给轮播图做的功能函数,
    1.如果是添加轮播图,就一直出现在最上面,
    2.如果是展示轮播图,就按照顺序,最先添加的展示在最上面,最近添加的展示在最下方 */
Banners.prototype.createBannerEvent = function (banner) {
    var self = this;
    var tpl = template("banner-item", {"banner": banner});
    var bannerListGroup = $('.banner-list-group');
    var bannerItem = null;
    if (banner) {
        bannerListGroup.append(tpl);
        bannerItem = bannerListGroup.find('.banner-item:last');
    } else {
        bannerListGroup.prepend(tpl);
        bannerItem = bannerListGroup.find('.banner-item:first');
    }
    self.addImageSelectEvent(bannerItem);
    self.addRemoveEvent(bannerItem);
    self.addSaveBannerEvent(bannerItem);
};

/* 添加轮播图 */
Banners.prototype.listenAddBannersEvent = function () {
    var self = this;
    var addBtn = $("#add-banner-btn");
    addBtn.click(function () {
        var bannerListGroup = $('.banner-list-group');
        var len = bannerListGroup.children().length;
        if (len >= 6) {
            window.messageBox.showInfo('最多只能添加6张轮播图!!!');
            return;
        }
        self.createBannerEvent()
    });
};

/* 轮播图中添加图片的函数 */
Banners.prototype.addImageSelectEvent = function (bannerItem) {
    var image = bannerItem.find('.thumbnail');
    /* imageInput 也可以通过bannerItem来选择,因为listenAddBannersEvent中确定每次只能选择最上面的对象 */
    var imageInput = bannerItem.find('.image-input');
    image.click(function () {
        /* 因为img标签没有打开文件的能力,只有input标签可以,
        当用户点击图片,然后js代码执行点击input标签的事件 */
        // var that = $(this);
        /* 因为有很多个轮播图片,并且都用class进行标注,会导致冲突,
        所以需要使用到,当你选择某个图片时,你的兄弟标签input执行点击事件 */
        // var imageInput = that.siblings('.image-input');
        imageInput.click();
    });

    /* 因为打开文件夹中,选择某个文件或图片是属于change事件 */
    imageInput.change(function () {
        /* 代表选择的文件(图片) */
        var file = this.files[0];
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
                    var url = result['data']['url'];
                    image.attr('src', url);
                }
            }
        });
    });
};

/* 轮播图中关闭按钮的函数 */
Banners.prototype.addRemoveEvent = function (bannerItem) {
    var closeBtn = bannerItem.find("#close-btn");
    closeBtn.click(function () {
        var bannerId = bannerItem.attr('data-banner-id');
        if (bannerId) {
            xfzalert.alertConfirm({
                'text': '您确定要删除这个轮播图吗? ',
                'confirmCallback': function () {
                    xfzajax.post({
                        'url': '/cms/delete_banner/',
                        'data': {
                            'banner_id': bannerId
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                bannerItem.remove();
                                window.messageBox.showSuccess("轮播图删除成功! ")
                            }
                        }
                    })
                }
            })
        } else {
            bannerItem.remove();
        }
    });
};

/* 轮播图中保存轮播图的函数 */
Banners.prototype.addSaveBannerEvent = function (bannerItem) {
    var saveBtn = bannerItem.find('.save-btn');
    var imageTag = bannerItem.find('.thumbnail');
    var priorityTag = bannerItem.find('input[name="priority"]');
    var linktoTag = bannerItem.find('input[name="link-to"]');
    var prioritySpan = bannerItem.find('span[class="priority"]');
    var bannerId = bannerItem.attr('data-banner-id');
    var url = '';
    if (bannerId) {
        url = '/cms/edit_banner/'
    }
    {
        url = '/cms/add_banner/'
    }
    saveBtn.click(function () {
        var image_url = imageTag.attr("src");
        var priority = priorityTag.val();
        var link_to = linktoTag.val();
        xfzajax.post({
            'url': url,
            'data': {
                'image_url': image_url,
                'priority': priority,
                'link_to': link_to,
                'pk': bannerId
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    if (bannerId) {
                        window.messageBox.showSuccess("轮播图修改成功! ")
                    } else {
                        bannerId = result['data']['banner_id'];
                        bannerItem.attr('data-banner-id', bannerId);
                        window.messageBox.showSuccess('轮播图添加完成! ')
                    }
                    /* 无论是新增还是修改都要去更改优先级 */
                    prioritySpan.text("优先级: " + priority);
                }
            }
        })
    });
};

Banners.prototype.run = function () {
    var self = this;
    self.listenAddBannersEvent();
    self.loadData();
};

$(function () {
    var banners = new Banners();
    banners.run();
});