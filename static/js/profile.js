var hamburger= document.getElementsByClassName("hamburger")[0];
var profilelinks=document.getElementsByClassName("profile-links")[0];
var hamburgerlines=document.getElementsByClassName("line");

hamburger.addEventListener("click",function(){
    profilelinks.classList.toggle("open");
    hamburgerlines[0].classList.toggle("open");
    hamburgerlines[1].classList.toggle("open");
    hamburgerlines[2].classList.toggle("open");
});

var notificationbell=document.getElementsByClassName("fa fa-bell")[0];
var notificationbar=document.getElementsByClassName("notification-bar-div");
notificationbell.addEventListener("click",function(){
    notificationbar[0].classList.toggle("open");
});

var userdatacontainer =document.getElementsByClassName("user-data-container")[0];

userdatacontainer.addEventListener("click",function(){
    profilelinks.classList.remove("open");
    hamburgerlines[0].classList.remove("open");
    hamburgerlines[1].classList.remove("open");
    hamburgerlines[2].classList.remove("open");
    notificationbar[0].classList.remove("open");
    notificationbar[0].classList.remove("open");
});

