// calculate quantity in add2basket modal
export const calcQuantity = () => {
    window.oninput = function calcQuantityAdd2Basket() {
        var quantityProduct = document.getElementById('id_quantity').value;
        var price = document.getElementById('price').innerHTML;
        var priceNum = Number.parseFloat(price);
        var sumQuantity = quantityProduct * priceNum;
        var value = document.getElementById('countResult').innerHTML.replace(/[0-9, .]/g, '')
        var sumQuantity = sumQuantity.toFixed(2) + " " + value;
        document.getElementById('countResult').innerHTML = sumQuantity;
    };
};