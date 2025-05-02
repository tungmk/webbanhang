var updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        const productID = this.dataset.product;
        const action = this.dataset.action;

        // Tìm input số lượng gần nút được nhấn
        const container = this.closest('.col-md-6'); // Hoặc container phù hợp
        const quantityInput = container.querySelector('#quantity');
        const quantity = parseInt(quantityInput.value) || 1 ;

        const noteInput = container.querySelector('#order-note');
        const note = noteInput ? noteInput.value : "";

        if (user === "AnonymousUser") {
            alert("Bạn cần đăng nhập để thêm sản phẩm vào giỏ hàng.");
        } else {
            updateUserOrder(productID, action, quantity, note);
        }
    });
}


function updateUserOrder(productID, action, quantity) {
    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productID': productID,
            'action': action,
            'quantity': quantity
        })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Cập nhật thành công:', data);
        location.reload();  // Cập nhật giỏ hàng sau khi thêm
    });
}
