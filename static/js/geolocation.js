// 目前使用效果不好，先搁置
  // 获取显示元素(h1) / 反馈元素(span) 
  var span = document.getElementById('feedback')
  var h1 = document.getElementById('display')

  // 判断浏览器是否支持定位
  function getLocation() {
    if(navigator.geolocation){//true
      navigator.geolocation.getCurrentPosition(showPosition)
      span.innerHTML = `恭喜您，您的浏览器支持定位！`
      h1.innerHTML = `≡(▔﹏▔)≡正在努力获取中...`//给出等待反馈
    }else{//false
      span.innerHTML = `很遗憾，您的浏览器不支持定位！`      
    }
  }

  // 获取位置
  function showPosition(position){
    h1.innerHTML = `纬度：${position.coords.latitude}经度：${position.coords.longitude}`
  }

