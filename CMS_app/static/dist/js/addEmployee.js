#addEmployee.js
function addEmployee {
    var addNewEmployee = $("#add_employee_form");
    $.ajax({
        type: 'POST',
        url: '/employees/new/',
        data: addNewEmployee.serialize(),
        success: function(res){
            alert(res['msg'])
        }
    })
}
