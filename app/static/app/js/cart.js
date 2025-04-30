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

document.getElementById('clear-cart-btn').addEventListener('click', function () {
    // Xóa toàn bộ nội dung giỏ hàng
    const cartTableBody = document.querySelector('tbody'); // body của bảng sản phẩm
    cartTableBody.innerHTML = ''; // xoá toàn bộ hàng sản phẩm

    // Cập nhật tổng số lượng và tổng tiền
    document.querySelector('body').querySelectorAll('div')[1].innerText = '0'; // Tổng số sản phẩm
    document.querySelector('body').querySelectorAll('div')[2].innerText = '0 VNĐ'; // Tổng tiền

    // Nếu bạn lưu giỏ hàng bằng localStorage
    localStorage.removeItem('cart');

    // Nếu cần gửi yêu cầu tới server để xóa trên database
    /*
    fetch('/clear-cart', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({})
    }).then(response => {
        if (response.ok) {
            // Xóa thành công trên server
        }
    });
    */
});
