var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productID = this.dataset.product;
        var action = this.dataset.action;
        var quantity = parseInt(this.closest('.product-container').querySelector('.quantity').value) || 1;

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
        document.getElementById('cart-total').innerText = data.cart_total;
    });
}

// Xử lý nút "Xóa tất cả sản phẩm"
document.getElementById('clear-cart-btn').addEventListener('click', function () {
    const cartTableBody = document.querySelector('tbody');
    cartTableBody.innerHTML = '';

    // Đặt lại tổng số lượng và tổng tiền
    document.querySelector('body').querySelectorAll('div')[1].innerText = '0';
    document.querySelector('body').querySelectorAll('div')[2].innerText = '0 VNĐ';

    // Xóa giỏ hàng trong localStorage (nếu có)
    localStorage.removeItem('cart');

    // Gửi request tới server (nếu cần)
    /*
    fetch('/clear-cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    }).then(response => {
        if (response.ok) {
            // Xử lý khi xóa thành công
        }
    });
    */
});
