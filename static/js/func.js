//------------javaScript--------------------------------
//подключение к текстовому полю
document.querySelector('#phone').onkeydown = function(e){
    inputphone(e,document.querySelector('#phone'))
}
//-- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --
     
//Функция маски формат +7 (
function inputphone(e, phone){
    function stop(evt) {
        evt.preventDefault();
    }
    let key = e.key, v = phone.value; not = key.replace(/([0-9])/, 1)
    
    if(not == 1 || 'Backspace' === not){
        if('Backspace' != not){ 
            if(v.length < 3 || v ===''){phone.value= '+7('}
            if(v.length === 6){phone.value= v +')'}
            if(v.length === 10){phone.value= v +'-'}
            if(v.length === 13){phone.value= v +'-'}
        }
    }else{
        stop(e)
    }  
}

var a = document.querySelector('#phone');

function inputnum(num, input){
    let v = input.value
    
    if(input.id == 'phone' && num != 'C'){
        if(v.length < 3 || v ===''){input.value= '+7('}
        if(v.length === 6){input.value= v +')'}
        if(v.length === 10){input.value= v +'-'}
        if(v.length === 13){input.value= v +'-'}
        if(input.value.length < 16){
            input.value = input.value + num
        }
    }
    if(input.id == 'pincode' && num != 'C'){
        if(input.value.length < 6){
            input.value = input.value + num
        }
    }
    if(num === 'C' && input.value.length > 0){
        input.value = input.value.replace(/.$/, '');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $('#pin_create').click(function(){
        $('#usernamemsg').remove()
        $('#pincodemsg').remove()
        $('#phone').removeClass('is-invalid').removeClass('is-valid');
        $('#pincode').removeClass('is-invalid').removeClass('is-valid');
        $.ajax({
            url: 'pin_create/',
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin', // Do not send CSR
            dataType: 'json',
            data: {
                phone: document.querySelector('#phone').value,
            },
            success: function(response){
                if (response.username != undefined) {
                    $('#phone').removeClass('is-invalid').addClass('is-valid');
                    $('#phone').after('<div class="valid-feedback d-block" id="usernamemsg">' + response.username + '</div>')
                    $('#pincode').removeClass('is-invalid').addClass('is-valid');
                    $('#pincodebtn').after('<div class="valid-feedback d-block" id="pincodemsg">' + response.pincode + '</div>')
                }
                if (response.error != undefined) {
                    $('#phone').removeClass('is-valid').addClass('is-invalid');
                    $('#phone').after('<div class="invalid-feedback d-block" id="usernamemsg">' + response.error + '</div>')
                }
            },
            error: function(response){
                console.log(response.responseJSON.errors)
            }
        });
    });

    $('#enterbtn').click(function(){
        $('#usernamemsg').remove()
        $('#pincodemsg').remove()
        $('#phone').removeClass('is-invalid').removeClass('is-valid');
        $('#pincode').removeClass('is-invalid').removeClass('is-valid');
        if(document.querySelector('#phone').value === '' || document.querySelector('#phone').value.length < 16){
            $('#phone').removeClass('is-valid').addClass('is-invalid');
            $('#phone').after('<div class="invalid-feedback d-block" id="usernamemsg">Введите корректный номер телефона</div>')
            a = document.querySelector('#phone');
        } else {
            if(document.querySelector('#pincode').value === '' || document.querySelector('#pincode').value.length < 6){
                $('#pincode').removeClass('is-valid').addClass('is-invalid');
                $('#pincodebtn').after('<div class="invalid-feedback d-block" id="pincodemsg">Введите корректный ПИН-Код</div>')
                a = document.querySelector('#pincode');
            } else {
                $.ajax({
                    url: '.',
                    type: 'POST',
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    mode: 'same-origin', // Do not send CSR
                    dataType: 'json',
                    data: {
                        phone: document.querySelector('#phone').value,
                        pincode: document.querySelector('#pincode').value,
                    },
                    success: function(response){
                        $('#orderAuth').modal('hide')
                        $('#addbtn').remove()
                        $('#content').remove()
                        $('#logodiv').after('<div class="row p-3" id="addbtn"><div class="col p-2"><a href="/" class="btn btn-outline-light btn-block btn-lg">Новый заказ</a></div></div>')
                        $('#navbar').after(
                            '<div id="content" class="p-4 p-md-5">' +
                                '<div class="album py-5">' +
                                    '<div class="container">' +
                                        '<div class="row" style="margin-top: 6%">' +
                                            '<div class="col-md-8 col-md-offset-2">' +
                                                '<h3 class="page-header">Приятного аппетита, ' + response.username + '!</h3>' +
                                                '<p>Ваш заказ оформлен. Номер заказа <strong>' + response.orderid + '</strong>.</p>' +
                                                '<p>Ваш рейтинг <strong>' + response.userrating + '</strong>.</p>' +
                                                '<p>QR код для оплаты:</p>' +
                                                '<img src="/media/qr/' + response.orderid + '.png">' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                            '</div>'
                        )
                    },
                    error: function(response){
                        console.log(response.responseJSON.errors)
                    }
                });
            }
        }
    });
});