export function login () {
    $(document).on('submit','#login', function(e){
        e.preventDefault();

        $.ajax({
            type:'POST',
            url:'{% url "login" %}',
            data:{
                email:$('#username-modal').val(),
                password:$('#password-modal').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            sucess:function(){

            }
        })
    })
}