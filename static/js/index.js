
var hamburger=document.getElementById("hamburger");
var navopen=document.getElementsByClassName("nav")[0];
var hamline=document.getElementsByClassName("line");
hamburger.addEventListener("click",function(){
    navopen.classList.toggle("open");
    hamline[0].classList.toggle("open");
    hamline[1].classList.toggle("open");
    hamline[2].classList.toggle("open");
    
});


var pracitcedropdown=document.getElementById("pracitcedropdown");
var pracitceul=document.getElementsByClassName("pracitce-ul");
pracitcedropdown.addEventListener("click",function(){
    pracitceul[0].classList.toggle("open");
    console.log("hi");
});
var coursediv=document.getElementsByClassName("course");
coursediv[0].addEventListener("mouseover",function(){
    
});
