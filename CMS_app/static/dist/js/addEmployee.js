function addEmployee(e) {
    var AddEmployeeForm = $("#add_employee_form");
    $.ajax({
        type: 'POST',
        url: 'employees/add/',
        data: AddEmployeeForm.serialize(),
        success: function(res){
            alert(res['msg'])
        }
    })
}