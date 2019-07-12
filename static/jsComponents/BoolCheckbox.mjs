const checkbox = () => {
    var boolElem = document.getElementById("is_active").value;
    if (boolElem != "true") {
        document.getElementById("is_active").checked = true;
    }
}
export {checkbox};