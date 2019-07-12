const checkbox = () => {
    var boolElem = document.getElementById("bool_check").value;
    if (boolElem != "true") {
        document.getElementById("bool_check").checked = true;
    }
}
export {checkbox};