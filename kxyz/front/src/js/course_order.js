function CourseToken() {

}

CourseToken.prototype.listenCourseOrderSubmitEvent = function () {
    var submitBtn = $("#submit-btn");
    var price = $("input[name='price']");
    var notify_url = $("input[name='notify_url']").val();
    var return_url = $("input[name='return_url']").val();
    /* checked 用户选择的值 */
    var istype = $("input[name='istype']:checked").val();
    var orderid = $("input[name='orderid']").val();
    var goodsname = $("input[name='goodsname']").val();
    submitBtn.click(function (event) {
        event.preventDefault();
        xfzajax.post({
            'url': '/course/course_order_key/',
            'data': {
                'price': price,
                'notify_url': notify_url,
                'return_url': return_url,
                'istype': istype,
                'orderid': orderid,
                'goodsname': goodsname
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var key = result['data']['key'];
                    var keyInput = $("input[name='key']");
                    keyInput.val(key);
                    $("#pay-form").submit();
                }
            }
        })
    })
};


CourseToken.prototype.run = function () {
    var self = this;
    self.listenCourseOrderSubmitEvent();
};


$(function () {
    var courseToken = new CourseToken();
    courseToken.run();
});