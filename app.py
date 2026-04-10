from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from dbtransaction import Dbtransactions

app = Flask(__name__)
app.secret_key = "pharma_choice_secret_key"


# ==================== DECORATORS ====================

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper
#home world
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'admin':
            flash("Admin access required", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

def user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'user':
            flash("User access required", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        age = request.form['age']
        pincode = request.form['pincode']
        address = request.form['address']
        password = request.form['password']
        
        Dbtransactions().registerUser(name, email, phone, gender, age, pincode, address, password, 'user')
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))
    
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        user = Dbtransactions().validateLogin(email, password, user_type)
        
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_type'] = user['user_type']
            
            flash(f"Welcome {user['name']}!", "success")
            
            if user['user_type'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash("Invalid credentials!", "error")
            return redirect(url_for('login'))
    
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))


# ==================== API ROUTES FOR DASHBOARD ====================

@app.route('/api/drugs/count')
def api_drugs_count():
    try:
        drugs = Dbtransactions().getAllDrugs()
        return jsonify({"count": len(drugs)})
    except Exception as e:
        print(f"Error in api_drugs_count: {e}")
        return jsonify({"count": 0})

@app.route('/api/orders/count')
@login_required
def api_orders_count():
    try:
        if session.get('user_type') == 'user':
            orders = Dbtransactions().getUserOrders(session['user_id'])
        else:
            orders = Dbtransactions().getAllOrders()
        return jsonify({"count": len(orders)})
    except Exception as e:
        print(f"Error in api_orders_count: {e}")
        return jsonify({"count": 0})

@app.route('/api/cart/count')
@login_required
def api_cart_count():
    try:
        if session.get('user_type') == 'user':
            cart_items, total = Dbtransactions().getCart(session['user_id'])
            return jsonify({"count": len(cart_items)})
        else:
            return jsonify({"count": 0})
    except Exception as e:
        print(f"Error in api_cart_count: {e}")
        return jsonify({"count": 0})


# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    stats = Dbtransactions().getDashboardStats()
    low_stock = Dbtransactions().getLowStockDrugs(10)
    return render_template("admin_dashboard.html", stats=stats, low_stock=low_stock)

@app.route('/admin/addcategory', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        
        if Dbtransactions().addCategory(category_name):
            flash("Category added successfully!", "success")
        else:
            flash("Category already exists!", "error")
        
        return redirect(url_for('view_category'))
    
    return render_template("add_category.html")

@app.route('/admin/viewcategory')
@login_required
@admin_required
def view_category():
    categories = Dbtransactions().getAllCategories()
    return render_template("view_category.html", categories=categories)

@app.route('/admin/deletecategory/<int:category_id>')
@login_required
@admin_required
def delete_category(category_id):
    Dbtransactions().deleteCategory(category_id)
    flash("Category deleted successfully!", "success")
    return redirect(url_for('view_category'))

@app.route('/admin/adddrug', methods=['GET', 'POST'])
@login_required
@admin_required
def add_drug():
    if request.method == 'POST':
        drug_name = request.form['drug_name']
        category_id = request.form['category_id']
        price = request.form['price']
        discount = request.form.get('discount', 0)
        available_stock = request.form['available_stock']
        
        Dbtransactions().addDrug(drug_name, category_id, price, discount, available_stock)
        flash("Drug added successfully!", "success")
        return redirect(url_for('view_drugs'))
    
    categories = Dbtransactions().getAllCategories()
    return render_template("add_drug.html", categories=categories)

@app.route('/admin/viewdrugs')
@login_required
@admin_required
def view_drugs():
    category = request.args.get('category')
    search = request.args.get('search')
    sort = request.args.get('sort')
    
    drugs = Dbtransactions().getAllDrugs(category, search, sort)
    categories = Dbtransactions().getAllCategories()
    return render_template("view_drugs.html", drugs=drugs, categories=categories)

@app.route('/admin/updatedrug/<int:drug_id>', methods=['POST'])
@login_required
@admin_required
def update_drug(drug_id):
    price = request.form['price']
    discount = request.form['discount']
    available_stock = request.form['available_stock']
    
    Dbtransactions().updateDrug(drug_id, price, discount, available_stock)
    flash("Drug updated successfully!", "success")
    return redirect(url_for('view_drugs'))

@app.route('/admin/deletedrug/<int:drug_id>')
@login_required
@admin_required
def delete_drug(drug_id):
    Dbtransactions().deleteDrug(drug_id)
    flash("Drug deleted successfully!", "success")
    return redirect(url_for('view_drugs'))

@app.route('/admin/vieworders')
@login_required
@admin_required
def view_orders():
    orders = Dbtransactions().getAllOrders()
    return render_template("view_orders.html", orders=orders)

@app.route('/admin/updateorderstatus/<int:order_id>/<status>')
@login_required
@admin_required
def update_order_status(order_id, status):
    Dbtransactions().updateOrderStatus(order_id, status)
    flash(f"Order status updated to {status}!", "success")
    return redirect(url_for('view_orders'))


# ==================== USER ROUTES ====================

@app.route('/user/dashboard')
@login_required
@user_required
def user_dashboard():
    return render_template("user_dashboard.html")

@app.route('/user/drugs')
@login_required
@user_required
def user_drugs():
    category = request.args.get('category')
    search = request.args.get('search')
    sort = request.args.get('sort')
    
    drugs = Dbtransactions().getAllDrugs(category, search, sort)
    categories = Dbtransactions().getAllCategories()
    return render_template("user_view_drugs.html", drugs=drugs, categories=categories)

@app.route('/user/addtocart/<int:drug_id>', methods=['POST'])
@login_required
@user_required
def add_to_cart(drug_id):
    try:
        quantity = int(request.form['quantity'])
        if quantity <= 0:
            flash("Quantity must be at least 1", "error")
            return redirect(url_for('user_drugs'))
        
        Dbtransactions().addToCart(session['user_id'], drug_id, quantity)
        flash("Item added to cart!", "success")
    except Exception as e:
        print(f"Error adding to cart: {e}")
        flash("Error adding to cart", "error")
    
    return redirect(url_for('user_drugs'))

@app.route('/user/cart')
@login_required
@user_required
def view_cart():
    cart_items, total = Dbtransactions().getCart(session['user_id'])
    return render_template("cart.html", cart_items=cart_items, total=total)

@app.route('/user/removefromcart/<int:cart_id>', methods=['POST'])
@login_required
@user_required
def remove_from_cart(cart_id):
    try:
        Dbtransactions().removeFromCart(cart_id)
        return jsonify({"success": True, "message": "Item removed from cart!"})
    except Exception as e:
        return jsonify({"success": False, "message": "Error removing item"})

@app.route('/user/checkout', methods=['POST'])
@login_required
@user_required
def checkout():
    try:
        data = request.get_json()
        payment_method = data.get('payment_method', 'Unknown')
        
        if Dbtransactions().placeOrder(session['user_id']):
            return jsonify({"success": True, "message": f"Order placed successfully! Paid via {payment_method}"})
        else:
            return jsonify({"success": False, "message": "Your cart is empty!"})
    except Exception as e:
        print(f"Checkout error: {e}")
        return jsonify({"success": False, "message": "Error placing order"})

@app.route('/user/myorders')
@login_required
@user_required
def my_orders():
    orders = Dbtransactions().getUserOrders(session['user_id'])
    return render_template("my_orders.html", orders=orders)


# ==================== AJAX ROUTES ====================

@app.route('/get_drug_details/<int:drug_id>')
def get_drug_details(drug_id):
    try:
        drugs = Dbtransactions().getAllDrugs()
        for drug in drugs:
            if drug['id'] == drug_id:
                return jsonify({"drug": drug})
        return jsonify({"drug": None})
    except Exception as e:
        print(f"Error getting drug details: {e}")
        return jsonify({"drug": None})
@app.route('/user/cart/data')
@login_required
@user_required
def cart_data():
    cart_items, total = Dbtransactions().getCart(session['user_id'])
    return jsonify({"cart_items": cart_items, "total": total})

if __name__ == "__main__":
    app.run(debug=True)