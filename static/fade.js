function alercik() {
    let checkBox = document.getElementById('checkboxik');
    if (checkBox.checked == true) {
        $('.bgtransus').addClass("noone");
        setTimeout(function(){$('.bgtransus').addClass("noone2");},1500);
    }
    else
        alert('Potwierdź swoją pełnoletniość');
}