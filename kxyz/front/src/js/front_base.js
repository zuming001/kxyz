// 用来处理导航条
function FrontBase() {

}

FrontBase.prototype.run = function () {
    var self = this;
    self.ListenAuthBoxHover();
};

FrontBase.prototype.ListenAuthBoxHover = function () {
    var authBox = $(".auth-box");
    var userMoreBox = $(".user-more-box");
    authBox.hover(function () {
        userMoreBox.show();
    }, function () {
        userMoreBox.hide();
    });
};

//用来处理登录和注册
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
    self.listenImgCaptchaEvent();
    self.listenSmsCaptcha();
    self.listenSignupEvent();
};

Auth.prototype.showEvent = function () {
    var self = this;
    self.maskWrapper.show();
};

Auth.prototype.hideEvent = function () {
    var self = this;
    self.maskWrapper.hide();
};

Auth.prototype.listenSmsCaptcha = function () {
    var smsCaptcha = $(".sms-captcha-btn");
    var telephpneIput = $(".signup-group input[name='telephone']");
    smsCaptcha.click(function () {
        var telephone = telephpneIput.val();
        if (!telephone) {
            messageBox.showInfo('请输入手机号码！ ');
        }
        xfzajax.get({
            'url': '/account/sms_captcha/',
            'data': {
                'telephone': telephone,
            },
            'success': function (result) {
                if (result['code'] == 200) {
                    messageBox.showSuccess('短信验证码发送成功！ ');
                    smsCaptcha.addClass('disabled');
                    var count = 60;
                    smsCaptcha.unbind('click');
                    //定时器函数setInterval
                    var timer = setInterval(function () {
                        smsCaptcha.text(count + 's');
                        // count-- 等于 count -=1
                        count--;
                        if (count <= 0) {
                            clearInterval(timer);
                            smsCaptcha.removeClass("disabled");
                            smsCaptcha.text("发送验证码");
                        }
                    }, 1000);
                }
            },
            'fail': function (error) {
                console.log(error)
            }
        });
    });
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

Auth.prototype.listenImgCaptchaEvent = function () {
    var imgCaptcha = $(".img-captcha");
    imgCaptcha.click(function () {
        ///account/img_captcha/?random=3
        imgCaptcha.attr("src", "/account/img_captcha/" + "?random=" + Math.random());
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
    var telephoneInput = signinGroup.find('input[name="telephone"]');
    var passwordInput = signinGroup.find('input[name="password"]');
    var rememberInput = signinGroup.find('input[name="remember"]');

    var submitBtn = signinGroup.find(".submit-btn");
    submitBtn.click(function (event) {
        event.preventDefault();
        var telephone = telephoneInput.val();
        var password = passwordInput.val();
        var remember = rememberInput.prop("checked");

        xfzajax.post({
            'url': '/account/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                //三目运算符
                'remember': remember ? 1 : 0,
            },
            'success': function (result) {
                self.hideEvent();
                window.location.reload();
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
};

Auth.prototype.listenSignupEvent = function () {
    var self = this;
    var signupGroup = $('.signup-group');
    var telephoneInput = signupGroup.find("input[name='telephone']");
    var usernameInput = signupGroup.find("input[name='username']");
    var imgCaptchaInput = signupGroup.find("input[name='img_captcha']");
    var password1Input = signupGroup.find("input[name='password1']");
    var password2Input = signupGroup.find("input[name='password2']");
    var smsCaptchaInput = signupGroup.find("input[name='sms_captcha']");

    var submitBtn = signupGroup.find(".submit-btn");
    submitBtn.click(function (event) {
        //为了阻止form的默认行为
        event.preventDefault();
        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var img_captcha = imgCaptchaInput.val();
        var password1 = password1Input.val();
        var password2 = password2Input.val();
        var sms_captcha = smsCaptchaInput.val();

        xfzajax.post({
            'url': '/account/register/',
            'data': {
                'telephone': telephone,
                'username': username,
                'img_captcha': img_captcha,
                'password1': password1,
                'password2': password2,
                'sms_captcha': sms_captcha
            },
            // 监听事件
            'success': function (result) {
                //重新加载页面
                self.hideEvent();
                window.location.reload();
            },
            'fail': function (error) {
                window.messageBox.showError('服务器内部错误！')
            }
        });
    });
};

$(function () {
    var auth = new Auth();
    auth.run();
});

$(function () {
    var frontBase = new FrontBase();
    frontBase.run();
});

$(function () {
    if (window.template) {
        template.defaults.imports.timeSince = function (DateValue) {
            var date = new Date(DateValue);
            var datets = date.getDate(); //得到的是毫秒
            var nowts = (new Date()).getTime(); //得到的是当前时间的时间戳
            var timestamp = (nowts - datets) / 1000; //得到的是秒数
            if (timestamp < 60) {
                return '刚刚';
            } else if (timestamp >= 60 && timestamp < 60 * 60) {
                minutes = parseInt(timestamp / 60);
                return minutes + '%分钟前';
            } else if (timestamp >= 60 * 60 && timestamp < 60 * 60 * 24) {
                hours = parseInt(timestamp / 60 / 60);
                return hours + '%小时前';
            } else if (timestamp >= 60 * 60 * 24 && timestamp < 60 * 60 * 24 * 30) {
                days = parseInt(timestamp / 60 / 60 / 24);
                return days + '%天前';
            } else {
                var year = date.getFullYear();
                var mouth = date.getMonth();
                var day = date.getDay();
                var hour = date.getHours();
                var minute = date.getMinutes();
                return year + '年' + mouth + '月' + day + '日 ' + hour + ':' + minute
            }
        }
    }
});