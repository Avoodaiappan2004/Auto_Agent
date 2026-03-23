const addToCartButtons = document.querySelectorAll('.add-to-cart');
const cartList = document.getElementById('cart-list');
const totalPrice = document.getElementById('total-price');
const checkoutButton = document.getElementById('checkout');
let cart = [];

addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
        const productId = button.dataset.id;
        const product = {
            id: productId,
            price: parseFloat(button.parentElement.querySelector('p').textContent.replace('$', ''))
        };
        cart.push(product);
        updateCart();
    });
});

function updateCart() {
    cartList.innerHTML = '';
    let totalPriceValue = 0;
    cart.forEach(product => {
        const li = document.createElement('li');
        li.textContent = `Product ${product.id}: $${product.price} x 1 = $${product.price}`;
        cartList.appendChild(li);
        totalPriceValue += product.price;
    });
    totalPrice.textContent = `Total Price: $${totalPriceValue}`;
    checkoutButton.disabled = cart.length === 0;
}

checkoutButton.addEventListener('click', () => {
    alert(`Checkout successful! Total price: $${cart.reduce((acc, product) => acc + product.price, 0)}`);
    cart = [];
    updateCart();
});