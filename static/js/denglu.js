 //登录页面js
 const signInBtn = document.getElementById("signIn");
  const signUpBtn = document.getElementById("signUp");
  const fistForm = document.getElementById("form1");
  const secondForm = document.getElementById("form2");
  const container = document.querySelector(".container");
  var true_code="-1"
  //移除signInBtn事件句柄
  signInBtn.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
  });
  //向signUpBtn添加事件句柄
  signUpBtn.addEventListener("click", () => {
    container.classList.add("right-panel-active");
  });


  function loginMow(){

   var email=$(".email").val()
   var password=$(".password").val()
   if (email==""||password==""){
       alert('账号或密码错误')
    return
   }
    $.post("/account/login?type=login",{"email":email,"password":password}, function (data) {
    if (data.code===0){
     alert('账号或密码错误')
    }else{
     if (data.role==1){
           window.location.href="/admin/league/list"

      return

     }
     window.location.href="/history/list"
    }

  })
  }
  function signUpNow() {
      var r_name=$(".r_name").val()
   var r_password=$(".r_password").val()
   var r_email=$(".r_email").val()
   var m_code=$(".m_code").val()
   if (m_code!=true_code){
    alert("验证码错误")
    return
   }
   var instes=[]
   $(".intersert:checked").each(function() {
    var checkboxValue = $(this).val();
    console.log(checkboxValue)
    instes.push(checkboxValue)
});
      console.log(instes)
   $.post("/account/login?type=signup",{"username":r_name,"password":r_password,"email":r_email,"interest":instes}, function (data) {
    if (data.code===0) {
     alert("该账号已经注册过了");
    }
     else{
     alert("注册成功");
     }

   })
  }

  function sendemail(){
   $.get("/account/send?email="+$(".r_email").val(), function (data) {
    if (data.code===0) {
     alert("发送失败，请稍后重试");
    }
     else{
     alert("发送成功");
     true_code=data.data
     }

   })
  }
