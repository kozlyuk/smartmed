// init modal and ajax request
export const requestAjaxAdd2Modal = () => {
function add2modal() {
    var form_options = {
        target: '#modal',
    };
    $('#AddToBasketForm').ajaxForm(form_options);
};
};