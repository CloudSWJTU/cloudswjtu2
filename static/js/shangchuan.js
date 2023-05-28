var container = document.getElementsByClassName('container')[0]
// 被隐藏的" 文件选择按钮 "
var uploadInput = document.getElementById('upload-input')
// 上传框
var uploadDragger = document.getElementsByClassName('upload-dragger')[0]

// 上传框点击触发"文件选择按钮"的点击
uploadDragger.addEventListener('click', function(e) {
    uploadInput.click()
})
// 选中文件时
uploadInput.addEventListener('change', function(e) {
    console.log(e.target.files)
    // 图片显示
    uploadPicture(e.target.files)
})

// 在 uploadDragger 内部有拖拽行为时
uploadDragger.addEventListener('dragover', function(e) {
    // dragover 事件一定要清楚默认事件, 不然会无法触发后面的drop事件
    e.preventDefault()
    // console.log("over")
})

// 拖拽进入 uploadDragger 时
uploadDragger.addEventListener('dragenter', function(e) {
    uploadDragger.classList.add('drag')
})

// 拖拽离开 uploadDragger 时
uploadDragger.addEventListener('dragleave', function(e) {
    uploadDragger.classList.remove('drag')
})

// 拖拽松开时
uploadDragger.addEventListener('drop', function(e) {
    // 禁止默认行为 (有些浏览器会在新页面预览图片) 
    e.preventDefault()
    console.log(e.dataTransfer.files)
    uploadDragger.classList.remove('drag')
    // 图片显示
    uploadPicture(e.dataTransfer.files)
})

function uploadPicture(files) {  
    for (let index = 0; index < files.length; index++) {
        // 检查是否为图片
        if( !/\.(png|jpg|jpeg|gif|PNG|JPG|JPEG|GIF)$/.test(files[index].name) ) {
            alert('文件 ' + files[index].name + ' 上传错误, 文件格式必须为png|jpg|jpeg|gif')
            continue
        }
        /**
         * 上传操作(接口) 可以写在这里
         */

        //  创建 img 元素
        var newimg = document.createElement('img')
        newimg.src = window.URL.createObjectURL(files[index])
        newimg.className = 'picture'
        // 在 container 的子元素 uploadDragger 前面插入 newimg 元素
        container.insertBefore(newimg, uploadDragger)
    }
}