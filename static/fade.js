function alercik() {
    let checkBox = document.getElementById('checkboxik');
    if (checkBox.checked == true) {
        $('#existingdiv').html('<class="invisible">');
    }
    else
        alert('Potwierdź swoją pełnoletniość');
}