var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productID = this.dataset.product;
        var action = this.dataset.action;
        var quantity = parseInt(this.closest('.product-container').querySelector('.quantity').value) || 1;  // Lấy số lượng từ input tương ứng

        console.log('productID:', productID, 'action:', action, 'quantity:', quantity);
        console.log('user:', user);

        if (user == "AnonymousUser") {
            console.log('User is not logged in.');
        } else {
            updateUserOrder(productID, action, quantity);
        }
    });
}

function updateUserOrder(productID, action, quantity) {
    console.log('User is logged in.');
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
        console.log('data:', data);
        // Cập nhật giỏ hàng trên giao diện người dùng mà không reload trang
        document.getElementById('cart-total').innerText = data.cart_total;  // Giả sử dữ liệu trả về có thông tin giỏ hàng
    });
}
