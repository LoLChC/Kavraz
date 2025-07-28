// Sekme yönetimi
function showSection(event, id) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    const targetSection = document.getElementById(id);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
        link.classList.remove('active');
    });
    
    if (event && event.target) {
        event.target.closest("a").classList.add('active');
    }
    
    localStorage.setItem('activeSection', id);
}

// Address Modal işlemleri
function openAddressModal(action, id = null, title = '', city = '', district = '', addressLine = '', isDefault = false) {
    const modal = document.getElementById('addressModal');
    const form = document.getElementById('addressForm');
    
    if (action === 'add') {
        document.getElementById('modalTitle').innerHTML = '<i class="fas fa-plus-circle"></i> Yeni Adres Ekle';
        document.getElementById('formType').value = 'add_address';
        form.reset();
        document.getElementById('addressId').value = '';
        document.getElementById('setAsDefault').checked = false;
    } else if (action === 'edit') {
        document.getElementById('modalTitle').innerHTML = '<i class="fas fa-edit"></i> Adresi Düzenle';
        document.getElementById('formType').value = 'edit_address';
        document.getElementById('addressId').value = id;
        document.getElementById('addressTitle').value = title;
        document.getElementById('city').value = city;
        document.getElementById('district').value = district;
        document.getElementById('addressLine').value = addressLine;
        document.getElementById('setAsDefault').checked = isDefault;
    }
    
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeAddressModal() {
    document.getElementById('addressModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Password Modal işlemleri
function openPasswordModal() {
    document.getElementById('passwordModal').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closePasswordModal() {
    document.getElementById('passwordModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Şifre güçlülük kontrolü
function checkPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength += 1;
    if (password.match(/[a-z]/)) strength += 1;
    if (password.match(/[A-Z]/)) strength += 1;
    if (password.match(/[0-9]/)) strength += 1;
    if (password.match(/[\W_]/)) strength += 1;
    return strength;
}

// Hata gösterimi
function showError(id, message) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
        document.getElementById(id.replace('-error', '')).classList.add('error-input');
    }
}

function clearError(id) {
    const element = document.getElementById(id);
    if (element) {
        element.style.display = 'none';
        document.getElementById(id.replace('-error', '')).classList.remove('error-input');
    }
}

// Şifre doğrulama
function validatePassword(password) {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
    return regex.test(password);
}

function validatePasswords() {
    const pass1 = document.getElementById('new_password1').value;
    const pass2 = document.getElementById('new_password2').value;
    let isValid = true;

    if (!validatePassword(pass1)) {
        showError('new_password1-error', 'Şifre en az 8 karakter, büyük harf, rakam ve özel karakter içermelidir.');
        isValid = false;
    } else {
        clearError('new_password1-error');
    }

    if (pass1 !== pass2) {
        showError('new_password2-error', 'Şifreler eşleşmiyor');
        isValid = false;
    } else {
        clearError('new_password2-error');
    }

    return isValid;
}

// Sayfa yüklendiğinde
document.addEventListener("DOMContentLoaded", function() {
    // Aktif sekme
    const savedSection = localStorage.getItem('activeSection') || 'profile';
    const link = document.querySelector(`.sidebar-nav a[onclick*="${savedSection}"]`);
    if (link) {
        showSection({ target: link }, savedSection);
    } else {
        showSection(null, 'profile');
    }

    // Form submit işlemleri
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitButtons = this.querySelectorAll('button[type="submit"]');
            submitButtons.forEach(button => {
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> İşleniyor...';
                button.disabled = true;
            });
        });
    });
    
    // Şifre güçlülük çubuğu
    document.getElementById('new_password1')?.addEventListener('input', function() {
        const password = this.value;
        const strengthBar = document.getElementById('passwordStrengthBar');
        if (!strengthBar) return;
        
        const strength = checkPasswordStrength(password);
        let width = strength * 20;
        let color = '#f44336'; // Kırmızı
        
        if (strength >= 4) {
            color = '#4CAF50'; // Yeşil
        } else if (strength >= 3) {
            color = '#FFC107'; // Sarı
        }
        
        strengthBar.style.width = `${width}%`;
        strengthBar.style.backgroundColor = color;
        
        validatePasswords();
    });

    // Yeni şifre tekrarı doğrulama
    document.getElementById('new_password2')?.addEventListener('input', function() {
        validatePasswords();
    });

    // Şifre formu submit işlemi
    const passwordForm = document.getElementById('passwordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            if (!validatePasswords()) {
                e.preventDefault();
                return false;
            }
        });
    }
    
    // Modal dışına tıklandığında kapat
    window.addEventListener('click', function(event) {
        if (event.target === document.getElementById('addressModal')) {
            closeAddressModal();
        }
        if (event.target === document.getElementById('passwordModal')) {
            closePasswordModal();
        }
    });
});