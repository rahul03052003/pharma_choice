
// ==================== NAME VALIDATION ====================

function validateName(nameField) {
    var name = document.getElementById(nameField).value;
    
    if (!/^[a-zA-Z\s]*$/.test(name)) {
        alert("Name should contain only alphabets and spaces");
        document.getElementById(nameField).value = name.slice(0, -1);
        return false;
    }
    return true;
}

// ==================== EMAIL VALIDATION ====================

function validateEmail(emailField) {
    var email = document.getElementById(emailField).value;
    var pattern = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/;
    
    if (!pattern.test(email)) {
        alert("Please enter a valid email address");
        document.getElementById(emailField).focus();
        return false;
    }
    return true;
}

// Real-time email uniqueness check
function checkEmailExists() {
    var email = document.getElementById("email").value;
    var emailMsg = document.getElementById("emailmsg");
    
    if (email.length > 0) {
        fetch(`/checkemail?email=${email}`)
        .then(response => response.json())
        .then(data => {
            if (data.msg === "Exists") {
                if (emailMsg) {
                    emailMsg.innerHTML = "❌ Email already registered!";
                    emailMsg.style.color = "red";
                }
                document.getElementById("email").value = "";
                document.getElementById("email").focus();
            } else {
                if (emailMsg) {
                    emailMsg.innerHTML = "✓ Email available";
                    emailMsg.style.color = "green";
                }
            }
        })
        .catch(error => console.log("Error:", error));
    } else {
        if (emailMsg) emailMsg.innerHTML = "";
    }
}

// ==================== PHONE NUMBER VALIDATION ====================

let phoneAlerted = false;

function validatePhone(phoneField) {
    var phone = document.getElementById(phoneField).value;
    
    // Remove non-digits
    phone = phone.replace(/[^0-9]/g, '');
    
    // Limit to 10 digits
    if (phone.length > 10) {
        if (!phoneAlerted) {
            alert("Phone number should not exceed 10 digits");
            phoneAlerted = true;
        }
        phone = phone.slice(0, 10);
    } else {
        phoneAlerted = false;
    }
    
    document.getElementById(phoneField).value = phone;
    
    // Check starting digit for 10-digit numbers
    if (phone.length === 10) {
        if (!/^[6-9]/.test(phone)) {
            alert("Phone number must start with 6, 7, 8, or 9");
            document.getElementById(phoneField).value = "";
            document.getElementById(phoneField).focus();
            return false;
        }
    }
    return true;
}

// Real-time phone uniqueness check
function checkPhoneExists() {
    var phone = document.getElementById("phone").value;
    var phoneMsg = document.getElementById("phmsg");
    
    if (phone.length === 10) {
        fetch(`/checkphone?phone=${phone}`)
        .then(response => response.json())
        .then(data => {
            if (data.msg === "Exists") {
                if (phoneMsg) {
                    phoneMsg.innerHTML = "❌ Phone number already registered!";
                    phoneMsg.style.color = "red";
                }
                document.getElementById("phone").value = "";
                document.getElementById("phone").focus();
            } else {
                if (phoneMsg) {
                    phoneMsg.innerHTML = "✓ Phone number available";
                    phoneMsg.style.color = "green";
                }
            }
        })
        .catch(error => console.log("Error:", error));
    } else {
        if (phoneMsg) phoneMsg.innerHTML = "";
    }
}

// ==================== PINCODE VALIDATION ====================

function validatePincode(pincodeField) {
    var pincode = document.getElementById(pincodeField).value;
    
    if (!/^[0-9]{6}$/.test(pincode)) {
        alert("Pincode must be exactly 6 digits");
        document.getElementById(pincodeField).value = "";
        document.getElementById(pincodeField).focus();
        return false;
    }
    return true;
}

// ==================== AGE VALIDATION ====================

function validateAge(ageField) {
    var age = parseInt(document.getElementById(ageField).value);
    
    if (isNaN(age) || age < 1 || age > 120) {
        alert("Please enter a valid age (1-120)");
        document.getElementById(ageField).value = "";
        document.getElementById(ageField).focus();
        return false;
    }
    return true;
}

// ==================== PASSWORD VALIDATION ====================

function validatePassword(passwordField) {
    var password = document.getElementById(passwordField).value;
    var strength = 0;
    
    // Check length
    if (password.length >= 8) strength++;
    
    // Check for numbers
    if (/\d/.test(password)) strength++;
    
    // Check for lowercase
    if (/[a-z]/.test(password)) strength++;
    
    // Check for uppercase
    if (/[A-Z]/.test(password)) strength++;
    
    // Check for special characters
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;
    
    // Display strength message
    var strengthMsg = document.getElementById("passwordStrength");
    if (strengthMsg) {
        if (password.length === 0) {
            strengthMsg.innerHTML = "";
        } else if (strength <= 2) {
            strengthMsg.innerHTML = "Weak password";
            strengthMsg.style.color = "red";
        } else if (strength <= 4) {
            strengthMsg.innerHTML = "Medium password";
            strengthMsg.style.color = "orange";
        } else {
            strengthMsg.innerHTML = "Strong password";
            strengthMsg.style.color = "green";
        }
    }
    
    return true;
}

function validateConfirmPassword(passwordField, confirmField) {
    var password = document.getElementById(passwordField).value;
    var confirm = document.getElementById(confirmField).value;
    var confirmMsg = document.getElementById("confirmMsg");
    
    if (password !== confirm) {
        if (confirmMsg) {
            confirmMsg.innerHTML = "❌ Passwords do not match!";
            confirmMsg.style.color = "red";
        }
        return false;
    } else {
        if (confirmMsg) {
            confirmMsg.innerHTML = "✓ Passwords match";
            confirmMsg.style.color = "green";
        }
        return true;
    }
}

// ==================== ADDRESS VALIDATION ====================

function validateAddress(addressField) {
    var address = document.getElementById(addressField).value;
    
    if (address.trim().length < 10) {
        alert("Please enter a complete address (minimum 10 characters)");
        document.getElementById(addressField).focus();
        return false;
    }
    return true;
}

// ==================== QUANTITY VALIDATION ====================

function validateQuantity(quantityField) {
    var quantity = parseInt(document.getElementById(quantityField).value);
    
    if (isNaN(quantity) || quantity < 1) {
        alert("Quantity must be at least 1");
        document.getElementById(quantityField).value = 1;
        return false;
    }
    return true;
}

// ==================== PRICE VALIDATION (Admin) ====================

function validatePrice(priceField) {
    var price = parseFloat(document.getElementById(priceField).value);
    
    if (isNaN(price) || price <= 0) {
        alert("Price must be greater than 0");
        document.getElementById(priceField).value = "";
        document.getElementById(priceField).focus();
        return false;
    }
    return true;
}

function validateDiscount(discountField) {
    var discount = parseFloat(document.getElementById(discountField).value);
    
    if (isNaN(discount) || discount < 0 || discount > 100) {
        alert("Discount must be between 0 and 100");
        document.getElementById(discountField).value = 0;
        return false;
    }
    return true;
}

function validateStock(stockField) {
    var stock = parseInt(document.getElementById(stockField).value);
    
    if (isNaN(stock) || stock < 0) {
        alert("Stock must be 0 or greater");
        document.getElementById(stockField).value = 0;
        return false;
    }
    return true;
}

// ==================== FORM VALIDATIONS ====================

function validateRegistrationForm() {
    if (!validateName("name")) return false;
    if (!validateEmail("email")) return false;
    
    var phone = document.getElementById("phone").value;
    if (phone.length !== 10) {
        alert("Phone number must be 10 digits");
        document.getElementById("phone").focus();
        return false;
    }
    
    if (!validateAge("age")) return false;
    if (!validatePincode("pincode")) return false;
    if (!validateAddress("address")) return false;
    if (!validatePassword("password")) return false;
    if (!validateConfirmPassword("password", "confirm_password")) return false;
    
    return true;
}

function validateLoginForm() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var userType = document.getElementById("user_type").value;
    
    if (!userType) {
        alert("Please select login type");
        return false;
    }
    
    var emailPattern = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address");
        document.getElementById("email").focus();
        return false;
    }
    
    if (password.length === 0) {
        alert("Please enter your password");
        document.getElementById("password").focus();
        return false;
    }
    
    return true;
}

function validateAddDrugForm() {
    if (!validateName("drug_name")) return false;
    
    var category = document.getElementById("category_id").value;
    if (!category) {
        alert("Please select a category");
        return false;
    }
    
    if (!validatePrice("price")) return false;
    if (!validateDiscount("discount")) return false;
    if (!validateStock("available_stock")) return false;
    
    return true;
}

function validateAddCategoryForm() {
    var categoryName = document.getElementById("category_name").value;
    
    if (categoryName.trim().length === 0) {
        alert("Please enter a category name");
        return false;
    }
    
    if (!/^[a-zA-Z\s]*$/.test(categoryName)) {
        alert("Category name should contain only alphabets and spaces");
        return false;
    }
    
    return true;
}

// ==================== DELETE CONFIRMATION ====================

function confirmDelete(itemName) {
    var result = prompt(`Type "delete" to confirm deletion of ${itemName}`);
    return result === "delete";
}

function confirmOrderCancel() {
    return confirm("Are you sure you want to cancel this order?");
}

// ==================== CART QUANTITY UPDATE ====================

function updateCartQuantity(cartId, currentQty, maxStock) {
    var newQty = prompt("Enter new quantity:", currentQty);
    
    if (newQty && !isNaN(newQty) && newQty > 0) {
        if (newQty > maxStock) {
            alert("Sorry, only " + maxStock + " items available in stock");
            return false;
        }
        window.location.href = `/user/updatecart/${cartId}/${newQty}`;
    }
    return false;
}

// ==================== TOGGLE PASSWORD VISIBILITY ====================

function togglePasswordVisibility(passwordFieldId, toggleIconId) {
    var passwordField = document.getElementById(passwordFieldId);
    var toggleIcon = document.getElementById(toggleIconId);
    
    if (passwordField.type === "password") {
        passwordField.type = "text";
        if (toggleIcon) toggleIcon.innerHTML = "🙈";
    } else {
        passwordField.type = "password";
        if (toggleIcon) toggleIcon.innerHTML = "👁️";
    }
}

// ==================== PRICE CALCULATION ====================

function calculateFinalPrice() {
    var price = parseFloat(document.getElementById("price").value) || 0;
    var discount = parseFloat(document.getElementById("discount").value) || 0;
    var finalPriceSpan = document.getElementById("finalPrice");
    
    if (finalPriceSpan) {
        var finalPrice = price - (price * discount / 100);
        finalPriceSpan.innerHTML = "Final Price: ₹ " + finalPrice.toFixed(2);
    }
}

// ==================== STOCK VALIDATION IN CART ====================

function validateCartQuantity(drugId, requestedQty, availableStock) {
    if (requestedQty > availableStock) {
        alert("Sorry, only " + availableStock + " items available in stock");
        return false;
    }
    return true;
}

// ==================== INITIALIZE EVENT LISTENERS ====================

document.addEventListener("DOMContentLoaded", function() {
    // Name fields
    var nameField = document.getElementById("name");
    if (nameField) {
        nameField.addEventListener("input", function() { validateName("name"); });
    }
    
    // Email field
    var emailField = document.getElementById("email");
    if (emailField) {
        emailField.addEventListener("blur", checkEmailExists);
        emailField.addEventListener("input", function() { 
            var msg = document.getElementById("emailmsg");
            if (msg) msg.innerHTML = "";
        });
    }
    
    // Phone field
    var phoneField = document.getElementById("phone");
    if (phoneField) {
        phoneField.addEventListener("input", function() { validatePhone("phone"); });
        phoneField.addEventListener("blur", checkPhoneExists);
    }
    
    // Password fields
    var passwordField = document.getElementById("password");
    if (passwordField) {
        passwordField.addEventListener("input", function() { validatePassword("password"); });
    }
    
    var confirmField = document.getElementById("confirm_password");
    if (confirmField) {
        confirmField.addEventListener("input", function() { 
            validateConfirmPassword("password", "confirm_password"); 
        });
    }
    
    // Pincode field
    var pincodeField = document.getElementById("pincode");
    if (pincodeField) {
        pincodeField.addEventListener("input", function() { validatePincode("pincode"); });
    }
    
    // Price and discount fields for admin
    var priceField = document.getElementById("price");
    if (priceField) {
        priceField.addEventListener("input", calculateFinalPrice);
    }
    
    var discountField = document.getElementById("discount");
    if (discountField) {
        discountField.addEventListener("input", calculateFinalPrice);
    }
});