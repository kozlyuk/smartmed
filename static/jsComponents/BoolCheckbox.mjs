const checkbox = () => {
    var boolElem = document.getElementById("id_is_active").value;
    if (boolElem != "true") {
        document.getElementById("id_is_active").checked = true;
    }
}
export {checkbox};