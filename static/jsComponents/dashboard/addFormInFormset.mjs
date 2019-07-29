//price
function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function () {
        var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({
            'name': name,
            'id': id
        }).val('').removeAttr('checked');
    });
    newElement.find('label').each(function () {
        var forValue = $(this).attr('for');
        if (forValue) {
            forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');
            $(this).attr({
                'for': forValue
            });
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.btn.add-form-row')
        .removeClass('btn-outline-success').addClass('btn-outline-danger')
        .removeClass('add-form-row').addClass('remove-form-row')
        .html('<i class="material-icons">remove</i>');
    return false;
}

function deleteForm(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1) {
        btn.closest('.form-row').remove();
        var forms = $('.form-row');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).find(':input').each(function () {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}

//attr
function updateElementIndexAttr(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMoreAttr(selector, prefix) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function () {
        var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({
            'name': name,
            'id': id
        }).val('').removeAttr('checked');
    });
    newElement.find('label').each(function () {
        var forValue = $(this).attr('for');
        if (forValue) {
            forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');
            $(this).attr({
                'for': forValue
            });
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    var conditionRow = $('.form-row-attr:not(:last)');
    conditionRow.find('.btn.add-form-row-attr')
        .removeClass('btn-outline-success').addClass('btn-outline-danger')
        .removeClass('add-form-row-attr').addClass('remove-form-row-attr')
        .html('<i class="material-icons">remove</i>');
    return false;
}

function deleteFormAttr(prefix, btn) {
    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1) {
        btn.closest('.form-row-attr').remove();
        var forms = $('.form-row-attr');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).find(':input').each(function () {
                updateElementIndexAttr(this, prefix, i);
            });
        }
    }
    return false;
}

export {
    cloneMore,
    deleteForm,
    updateElementIndex,
    cloneMoreAttr,
    deleteFormAttr,
    updateElementIndexAttr,
};