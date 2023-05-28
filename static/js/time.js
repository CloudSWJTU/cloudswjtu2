//显示时间
function show_time() {
    var time = new Date();
    var year = time.getFullYear();
    var month = time.getMonth() + 1;
    var day = time.getDate();
    var hour = time.getHours();
    var min = time.getMinutes();
    var sec = time.getSeconds();
    document.getElementById("timeblock").innerHTML = year + "-" + month + "-" + day + "&nbsp;&nbsp;" + hour +
        ":" + min + ":" + sec;
        document.getElementById("timeblock").style.fontSize="15px";
        document.getElementById("timeblock").style.color="white";
}
//serInterval:以相同的时间间隔执行某个操作
setInterval("show_time()", 1000);

