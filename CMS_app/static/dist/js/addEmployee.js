#addEmployee.js
function addEmployee(e) {
    var addNewEmployee = $("#add_new_product_form");
    $.ajax({
        type: 'POST',
        url: '/employees/new/',
        data: addNewEmployee.serialize(),
        success: function(res){
            alert(res['msg'])
        }
    })
}
