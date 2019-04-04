var csrftoken = $("input[name='csrfmiddlewaretoken']").attr("value")

// Autocomplete
$(".search-field").autocomplete({
    _resizeMenu: function () {
        var ul = this.menu.element;
        ul.outerWidth(this.element.outerWidth());
    },
    autofocus: true,
    source : function (request, response) {
        $.post({
            beforeSend: function(request) {
                    request.setRequestHeader("X-CSRFToken", csrftoken);
                },
            url: "/",
            dataType: "json",
            data: JSON.stringify(request),            
            contentType: "application/json",
            success: function(data){
                response($.map(data,                 
                    function(product){
                    return product.name 
                    }
                  )
                );
            }
        });
    }
});

// Ajax request for saving substitute
$(document).ready(function() {
    originalId = $("#original").attr("data-id")
    $(".substitute").click(function(e) {
        e.preventDefault();
        var link = $(this)
        substituteId = link.attr("data-id")
        var data = {"original": originalId, "substitute": substituteId}
        $.post({
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: "/save-substitute/",
            dataType: "json",
            data: {"data": JSON.stringify(data)},
            success: function(data) {
                console.log(data.title)
                $(".modal-title").text(data.title);
                $(".modal-body").text(data.message);
                $("#ajaxModal").modal("show");
            }
        });
    });
});