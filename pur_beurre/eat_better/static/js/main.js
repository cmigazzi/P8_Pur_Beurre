var searchField = $("#search-field")
var form = $("form")
var csrftoken = $("input[name='csrfmiddlewaretoken']").attr("value")

var liste = [
    "Draggable",
    "Droppable",
    "Resizable",
    "Selectable",
    "Sortable"

];

$("#search-field").autocomplete({
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
                    return product.name + " " + product.brand 
                    }
                  )
                );
            }
        });
    }
});
