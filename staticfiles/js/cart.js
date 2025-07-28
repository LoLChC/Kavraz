document.addEventListener('DOMContentLoaded', function() {

    // Miktar artırma/azaltma işlemleri
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            const itemId = this.dataset.itemId;
            const isIncrease = this.classList.contains('plus');
            const quantityElement = this.parentElement.querySelector('.quantity');
            
            try {
                const response = await fetch(`/products/${isIncrease ? 'increase' : 'decrease'}_quantity/${itemId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin'
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        quantityElement.textContent = data.new_quantity;
                        updateItemTotal(this.closest('.cart-item'), data.item_total);
                        updateCartTotals(data.cart_total);
                        
                        // Başarılı mesajı
                        showToast('Sepet güncellendi', 'success');
                    } else {
                        showToast(data.message || 'Bir hata oluştu', 'error');
                    }
                } else {
                    throw new Error('Network response was not ok');
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('İşlem sırasında bir hata oluştu', 'error');
            }
        });
    });

    // Sepetten ürün kaldırma
    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            const itemId = this.dataset.itemId;
            const cartItem = this.closest('.cart-item');
        
        // Confirm kısmı silindi, direkt işleme devam ediyor.
            try {
                const response = await fetch(`/products/remove_from_cart/${itemId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin'
                });
            
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        cartItem.style.animation = 'fadeOut 0.3s ease';
                        setTimeout(() => {
                            cartItem.remove();
                            updateCartTotals(data.cart_total);
                        
                            if (document.querySelectorAll('.cart-item').length === 0) {
                                showEmptyCart();
                            }
                        
                            showToast('Ürün sepetten kaldırıldı', 'success');
                        }, 300);
                    } else {
                        showToast(data.message || 'Bir hata oluştu', 'error');
                    }
                } else {
                    throw new Error('Network response was not ok');
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('İşlem sırasında bir hata oluştu', 'error');
            }
        });
    });

    // Yardımcı fonksiyonlar
    function updateItemTotal(itemElement, newTotal) {
        itemElement.querySelector('.item-total').textContent = `${newTotal} TL`;
    }

    function updateCartTotals(newTotal) {
        document.querySelectorAll('.subtotal, .grand-total').forEach(el => {
            el.textContent = `${newTotal} TL`;
        });
    }

    function showEmptyCart() {
        const cartContainer = document.querySelector('.cart-container');
        cartContainer.innerHTML = `
            <div class="empty-cart">
                <div class="empty-cart-icon">
                    <i class="fas fa-shopping-basket"></i>
                </div>
                <h3>Sepetiniz Şu An Boş</h3>
                <p>Lezzetli çikolatalarımızı keşfetmek için ürünler sayfamızı ziyaret edin</p>
                <a href="/products" class="btn btn-primary">
                    <i class="fas fa-arrow-right"></i> Ürünlere Göz At
                </a>
            </div>
        `;
    }

    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast-notification ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => {
                    toast.remove();
                }, 300);
            }, 3000);
        }, 100);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// CSS animasyonu için global stil ekleme
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-20px); }
    }
    .toast-notification {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        padding: 12px 24px;
        border-radius: 4px;
        color: white;
        background-color: #333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1000;
    }
    .toast-notification.show {
        opacity: 1;
    }
    .toast-notification.success {
        background-color: #28a745;
    }
    .toast-notification.error {
        background-color: #dc3545;
    }
`;
document.head.appendChild(style);