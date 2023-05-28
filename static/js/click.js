//主页功能区块开关
function deleteminipart(){
   document.getElementById("minipart").style.display="none";
   document.getElementById("tackbackbutton").style.display="block";
}
function takebackminipart(){
    document.getElementById("minipart").style.display="block";
    document.getElementById("tackbackbutton").style.display="none";
}
function minipartchangecolor1(){
    document.getElementById("minipart").style.backgroundColor="#2196F3";
}
function minipartchangecolor2(){
    document.getElementById("minipart").style.backgroundColor="rgba(0, 137, 249, 0.5)";
}