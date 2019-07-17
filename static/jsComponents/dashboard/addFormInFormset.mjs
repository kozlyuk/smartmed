function addFormInFormset () {
    addNewRow();
};

function addNewRow () {
    let targetFormRow = document.querySelector('#attributeList');
    let clone = targetFormRow.cloneNode(true);

    changeLastHiddenInputForDelete(clone);

    document.getElementById("attributeListAll").appendChild(clone);
}

function changeLastHiddenInputForDelete (element) {
    //get ALL existing inputs
    let hiddenInput = document.querySelectorAll("#deleteCheckboxes>input");
    //get last input from existing inputs
    let lastHiddenInput = hiddenInput[hiddenInput.length- 1]
    //remove all symbol before number
    let getAttribute = lastHiddenInput.getAttribute("name").replace(/attribute_set-/g, ' ');
    
    //convert str to int
    let inputId = parseInt(getAttribute, 10);  //get id from hidden input
    let getParentDivCheckbox = element.lastElementChild;
    let getCheckbox = getParentDivCheckbox.lastElementChild;
    //create attribute
    let attributeId = "id_attribute_set-" + (inputId +1) + "-DELETE";
    let attributeName = "attribute_set-" + (inputId +1) + "-DELETE";

    //remove id and name attributes
    getCheckbox.removeAttribute("id");
    getCheckbox.removeAttribute("name");
    //put new attribute
    getCheckbox.setAttribute("id", attributeId);
    getCheckbox.setAttribute("name", attributeName);
}

function checkDeleteCheckboxes () {

}


export {addFormInFormset};

// * * * * * * * * *
//  jquery syntax 
// * * * * * * * * *

// $(function() {
//     setTimeout(function() {
//     $('span.select2-container.select2-container--bootstrap').width('auto');
//     }, 100);
//     $('#ExecutorsTable tbody').formset({
//         prefix: '{{ executors_formset.prefix }}',
//         formCssClass: 'dynamic-formset1',
//         addText: 'Додати Виконавця',
//         deleteText: 'Видалити Виконавця',
//         'added': function(row){
//             //find the fields with the calendar widget
//             $(row).find('.vDateField').each(function(i){
//                 //remove the cloned spam element: it links to an incorrect calendar
//                 $(this).parent().find('span').remove();
//                 //DateTimeShortcuts is in the django admin widgets
//                 DateTimeShortcuts.addCalendar(this);
//             })
//             $(row).find('.django-select2').djangoSelect2();
//         }
//     });
//     $('#CostsTable tbody').formset({
//         prefix: '{{ costs_formset.prefix }}',
//         formCssClass: 'dynamic-formset2',
//         addText: 'Додати Підрядника',
//         deleteText: 'Видалити Підрядника',
//         'added': function(row){
//             $(row).find('.vDateField').each(function(i){
//                 $(this).parent().find('span').remove();
//                 DateTimeShortcuts.addCalendar(this);
//                 });
//             $(row).find('.django-select2').djangoSelect2();
//         }
//     });
//     $('#SendingTable tbody').formset({
//         prefix: '{{ sending_formset.prefix }}',
//         formCssClass: 'dynamic-formset3',
//         addText: 'Додати Відправку',
//         deleteText: 'Видалити Відправку',
//         'added': function(row){
//             $(row).find('.vDateField').each(function(i){
//                 $(this).parent().find('span').remove();
//                 DateTimeShortcuts.addCalendar(this);
//                 });
//             $(row).find('.django-select2').djangoSelect2();
//         }
//     });
// })