/**
* 获取滚动条位置
*/
function getScrollTop() {
    var scrollPos;
    if (window.pageYOffset)
    {
        scrollPos = window.pageYOffset;
    }
    else if (document.compatMode && document.compatMode != 'BackCompat')
    {
        scrollPos = document.documentElement.scrollTop;
    }
    else if (document.body)
    {
        scrollPos = document.body.scrollTop;
    }
    return scrollPos;
 }
/**
 * 监听滚动条 逻辑根据自己需求来哦
 */
 window.onscroll = function () {
    let scrollPos = getScrollTop();
    console.log("scrollPos:",scrollPos);
    if (scrollPos == 0) {
        alert("页面已到顶部")
    }
}
 