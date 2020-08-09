
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
    console.log(notificationbar.length);
    notificationbar[0].classList.toggle("open");
});



