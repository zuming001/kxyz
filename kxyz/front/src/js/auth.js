//点击登录弹出模态对话框
// $(function () {
//     $("#btn").click(function () {
//         $(".mask-wrapper").show();
//     });
//
//     $(".close-btn").click(function () {
//         $(".mask-wrapper").hide();
//     });
// });
// $(function () {
//     $(".switch").click(function () {
//         var scrollWrapper = $(".scroll-wrapper");
//         var currentLeft = scrollWrapper.css("left");
//         // currentLeft是含有px的字符串,所以需要转换为整数,判断其正负性
//         currentLeft = parseInt(currentLeft);
//         if (currentLeft < 0) {
//             scrollWrapper.animate({'left': '0'})
//         } else {
//             scrollWrapper.animate({'left': '-400px'});
//         }
//     });
// });

function Auth() {
    var self = this;
    self.scrollWrapper = $('.scroll-wrapper');
    self.maskWrapper = $('.mask-wrapper');
}

Auth.prototype.run = function () {
    var self = this;
    self.listenShowHideEvent();
    self.listenSwitchEvent();
    self.listenSigninEvent();
};

Auth.prototype.showEvent = function () {
    var self = this;
    self.maskWrapper.show();
};

Auth.prototype.hideEvent = function () {
    var self = this;
    self.maskWrapper.hide();
};

Auth.prototype.listenShowHideEvent = function () {
    var self = this;
    var signinBtn = $('#signin-btn');
    var signupBtn = $('#signup-btn');
    var closeBtn = $('.close-btn');
    signinBtn.click(function () {
        self.showEvent();
        self.scrollWrapper.css({'left': 0})
    });

    signupBtn.click(function () {
        self.showEvent();
        self.scrollWrapper.css({'left': -400})
    });

    closeBtn.click(function () {
        self.hideEvent();
    });

};

Auth.prototype.listenSwitchEvent = function () {
    var self = this;
    var switcher = $(".switch");
    switcher.click(function () {
        var currentLeft = self.scrollWrapper.css("left");
        // currentLeft是含有px的字符串,所以需要转换为整数,判断其正负性
        currentLeft = parseInt(currentLeft);
        if (currentLeft < 0) {
            self.scrollWrapper.animate({'left': '0'})
        } else {
            self.scrollWrapper.animate({'left': '-400px'});
        }
    });
};

Auth.prototype.listenSigninEvent = function () {
    var self = this;
    var signinGroup = $('.signin-group');
    var telephoneIput = signinGroup.find('input[name="telephone"]');
    var passwordIput = signinGroup.find('input[name="password"]');
    var rememberIput = signinGroup.find('input[name="remember"]');

    var submitBtn = signinGroup.find(".submit-btn");
    submitBtn.click(function () {
        var telephone = telephoneIput.val();
        var password = passwordIput.val();
        var remember = rememberIput.prop("checked");

        xfzajax.post({
            'url': '/account/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                //三目运算符
                'remember': remember?1:0,
            },
            'success':function (result) {
                self.hideEvent();
                window.location.reload();
            },
            'fail':function (error) {
                console.log('服务器内部错误！');
            }
        });
    });

};

$(function () {
    var auth = new Auth();
    auth.run();
});