window.onload = function(){
    var target = document.getElementsByTagName('p')[0];
    target.addEventListener('mouseover', function(){
        target.style.color = "yellow";
    });
 
    target.addEventListener('mouseout', function(){
        target.style.color = "black";
    });
};