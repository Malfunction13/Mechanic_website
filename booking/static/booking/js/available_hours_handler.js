$(document).ready(function(){
    $("#id_timestamp").on('dp.change', function(){
        $.ajax({
            url: '',
            type: 'GET',
            data: {
                    date: $(this).val(),
            },
            success: function(response){
                $("#id_hour").empty();

                for(let i = 0; i < response.hours.length; i++){
                    let slot = response.hours[i];
                    $("#id_hour").append(`<option value=${slot}>${slot}</option>`);
                }
            }
        });
    });
});