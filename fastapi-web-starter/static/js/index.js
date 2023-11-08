$("#TestButton").click(function(){
        $.ajax({
                url : '/model',
                dataType : 'json',
                contentType:"application/json",
                method : 'get',
                success: function(obj){

                       to_append = ``
                       to_append += `
                        <div class="col">
                            <button id="TestButton" type="button" class="btn btn-success">
                                ${obj["data"]}
                            </button>
                        </div>
                       `
                       $("#chatbox").append(to_append)
                    }
              });

});


$("#TestButton2").click(function(){

    $("#TestButton2").css("background-color", "yellow")
    $(".custom_button").css("background-color", "yellow")
});