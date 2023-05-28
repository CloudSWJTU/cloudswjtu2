//改变style文件js
function animate(obj, target, callback) {
    clearInterval(obj.timer);
    obj.timer = setInterval(function() {
        var step = (target - obj.offsetTop) / 10;
        step = step > 0 ? Math.ceil(step) : Math.floor(step);
        if (obj.offsetTop == target) {
            clearInterval(obj.timer);
            callback && callback();
        }
        obj.style.top = obj.offsetTop + step + 'px';

    }, 15);
}