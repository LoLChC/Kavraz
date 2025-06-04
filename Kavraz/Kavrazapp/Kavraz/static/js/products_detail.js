document.addEventListener('DOMContentLoaded', function() {
    // Miktar seçici fonksiyonları
    const minusBtn = document.querySelector('.minus');
    const plusBtn = document.querySelector('.plus');
    const quantityInput = document.querySelector('.quantity-input');
    
    minusBtn.addEventListener('click', function() {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });
    
    plusBtn.addEventListener('click', function() {
        let currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });
    
    // Sepete ekle butonu
    const addToCartBtn = document.querySelector('.add-to-cart');
    
    addToCartBtn.addEventListener('click', function() {
        const productId = window.location.pathname.split('/').pop();
        const quantity = parseInt(quantityInput.value);
        
        // Burada AJAX çağrısı yapılabilir
        console.log(`Ürün ID: ${productId}, Miktar: ${quantity} sepete eklendi`);
        
        // Kullanıcıya bildirim göster
        showNotification('Ürün sepete eklendi!');
    });
    
    // Bildirim fonksiyonu
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Ürün kartlarına hover efekti
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 15px 30px rgba(243, 190, 110, 0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.2)';
        });
    });
});