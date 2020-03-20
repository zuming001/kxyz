function VideoPlayer() {

}

VideoPlayer.prototype.listenVideoPlayEvent = function () {
    var videoGroup = $("#video-info");
    var videoUrl = videoGroup.attr("data-video-url");
    var coverUrl = videoGroup.attr("data-cover-url");
    var courseId = videoGroup.attr("data-course-id");
    var player = cyberplayer("playercontainer").setup({
        width: '100%',
        height: '100%',
        file: videoUrl,
        image: coverUrl,
        autostart: false,
        stretching: "uniform",
        repeat: false,
        volume: 100,
        controls: true,
        tokenEncrypt: "true",
        /* AccessKey */
        ak: 'a5c18a9a51904766a2bf19669b4bfe0b'
    });
    player.on('beforePlay', function (e) {
        if (!/m3u8/.test(e.file)) {
            return;
        }
        xfzajax.get({
            'url': '/course/course_token/',
            'data': {
                'video': videoUrl,
                'course_id': courseId
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    player.setToken(e.file, token);
                } else {
                    window.messageBox.showInfo(result['message']);
                    player.stop();
                }
            },
            'fail': function (error) {
                console.log(error)
            }
        })
    })
};


VideoPlayer.prototype.run = function () {
    var self = this;
    self.listenVideoPlayEvent()
};

$(function () {
    var videoPlayer = new VideoPlayer();
    videoPlayer.run()
});