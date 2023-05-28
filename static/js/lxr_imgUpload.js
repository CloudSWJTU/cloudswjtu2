// 地标部分上传后端插件
function imgUpload(opts) {
    var self = this;
    self.id = opts.id;
    self.imgCount = opts.imgCount||1;
    self.imgList = [];
    if($('#' + self.id).length<0) return;
    $('#' + self.id).addClass("uploadImgGroup");
    var html = ` <input id="` + self.id + `_list" type="text" name="img" style="display:none">`;
    $('#' + self.id).html(html);
    self.creatUploadBtn();
    self.bind();
}
imgUpload.prototype.bind = function () {
    var self = this;
    //上传
    $(document).on("change", ".uploadImg", function () {
        self.upload($(this));
    });
    //删除
    $(document).on("click", ".uploadImgBtn.del .icon-del", function () {
        var length = $("#" + self.id + ">.uploadImgBtn").length;
        var inputNum = $("#" + self.id + " .uploadImgBtn input").length;
        if (length == self.imgCount&&inputNum==0) {
            self.creatUploadBtn();
        }
        $(this).parent().remove();
        self.imgList=self.getList();
    });
}
imgUpload.prototype.creatUploadBtn = function (num) {
    var self = this;
    var html = `
                <div class="uploadImgBtn">
                    <input class="uploadImg" type="file" name="file">
                    <i class="iconfont icon-del"></i>
                </div>
            `;
    $('#' + self.id).append(html);
}
imgUpload.prototype.upload = function (tag) {
    var self = this;
    var formData = new FormData();
    formData.append("file", tag[0].files[0]);
// 本部分内容使用与本学期内容无关，便于下学期加入后端接口，且因为未接入后端接口，图片一定会上传失败
    $.ajax({
        url: "/uploadFile",
        type: "post",
        dataType: "json",
        cache: false,
        data: formData,
        processData: false,// 不处理数据
        contentType: false, // 不设置内容类型
        success: function (data) {
            
            if (data.resultCode != '000000') {
                alert("暂不支持该功能。");
                return false;
            }

            var fileUrl = data.result.url;//后端返回图片存于服务器中的url

            //回显
            tag.parent().css({
                "background-image": "url(" + fileUrl + ")"
            })
                .addClass("del")
                .attr("fileUrl",fileUrl);

            self.imgList=self.getList();

            //移除input
            tag.remove();

            var length = $("#" + self.id + ">.uploadImgBtn").length;
            if (length < self.imgCount) {
                self.creatUploadBtn();
            }
        },
        error: function () {
            alert("暂不支持该功能。");
        }
    });
}
imgUpload.prototype.getList = function (){
    var self = this,
        imgList = [];
    $('#'+self.id+' .uploadImgBtn').each(function(){
        var fileUrl = $(this).attr("fileUrl");
        imgList.push(fileUrl);
    });
    $('#' + self.id + '_list').val(imgList.join(","));
    return imgList;
}
/*
需要后台配合写一个图片以formdata对象格式存储到服务器并返回图片url的接口
*/

      $(document).ready(function () {
        var $imgUpload = new imgUpload({
          id: "file1",
          imgCount: 5
        });
      });