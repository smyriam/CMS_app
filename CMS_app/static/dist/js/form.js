function addEmployee(e) {
    var AddEmployeeForm = $("#add_employee_form");
    $.ajax({
        type: 'POST',
        url: 'employees/add/',
        data: AddEmployeeForm.serialize(),
        success: function(res){
            $('#addNewEmployee').modal('hide');
            window.location.reload();
        }
    })
}


function addCourse(e) {
    var AddCourseForm = $("#add_course_form");
    $.ajax({
        type: 'POST',
        url: 'courses/add/',
        data: AddCourseForm.serialize(),
        success: function(res){
            $('#addNewCourse').modal('hide');
            window.location.reload();
        }
    })
}