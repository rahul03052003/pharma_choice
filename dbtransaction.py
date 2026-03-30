from dbconnection import Database

class Dbtransactions:

    # ==================== USER MANAGEMENT ====================
    
    def registerUser(self, name, email, phone, gender, age, pincode, address, password, user_type='user'):
        con = Database().dbconnection()
        db = con.cursor()
        
        query = """
        INSERT INTO users(name, email, phone, gender, age, pincode, address, password, user_type)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        db.execute(query, (name, email, phone, gender, age, pincode, address, password, user_type))
        
        user_id = db.lastrowid
        con.commit()
        con.close()
        
        return user_id

    def validateLogin(self, email, password, user_type):
        con = Database().dbconnection()
        db = con.cursor()
        
        query = """
        SELECT id, name, user_type FROM users 
        WHERE email = %s AND password = %s AND user_type = %s
        """
        db.execute(query, (email, password, user_type))
        rs = db.fetchone()
        con.close()
        
        if rs:
            return {"id": rs[0], "name": rs[1], "user_type": rs[2]}
        return None

    def getUserById(self, user_id):
        con = Database().dbconnection()
        db = con.cursor()
        
        db.execute("SELECT id, name, email, phone, address FROM users WHERE id = %s", (user_id,))
        rs = db.fetchone()
        con.close()
        
        if rs:
            return {"id": rs[0], "name": rs[1], "email": rs[2], "phone": rs[3], "address": rs[4]}
        return None

    # ==================== CATEGORY MANAGEMENT ====================
    
    def addCategory(self, category_name):
        con = Database().dbconnection()
        db = con.cursor()
        
        try:
            db.execute("INSERT INTO categories(category_name) VALUES(%s)", (category_name,))
            con.commit()
            con.close()
            return True
        except:
            con.close()
            return False

    def getAllCategories(self):
        con = Database().dbconnection()
        db = con.cursor()
        
        db.execute("SELECT id, category_name, created_at FROM categories ORDER BY category_name")
        rs = db.fetchall()
        con.close()
        
        categories = []
        for row in rs:
            categories.append({
                "id": row[0],
                "category_name": row[1],
                "created_at": row[2]
            })
        return categories

    def deleteCategory(self, category_id):
        con = Database().dbconnection()
        db = con.cursor()
        
        db.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        con.commit()
        con.close()

    # ==================== DRUG MANAGEMENT ====================
    
    def addDrug(self, drug_name, category_id, price, discount, available_stock):
        con = Database().dbconnection()
        db = con.cursor()
        
        # Ensure positive values
        price = abs(float(price))
        discount = abs(float(discount))
        if discount > 100:
            discount = 100
        
        query = """
        INSERT INTO drugs(drug_name, category_id, price, discount, available_stock)
        VALUES(%s, %s, %s, %s, %s)
        """
        db.execute(query, (drug_name, category_id, price, discount, available_stock))
        
        drug_id = db.lastrowid
        con.commit()
        con.close()
        
        return drug_id

    def getAllDrugs(self, category_filter=None, search=None, sort=None):
        con = Database().dbconnection()
        db = con.cursor()
        
        query = """
        SELECT d.id, d.drug_name, c.category_name, d.price, d.discount, 
               d.available_stock, d.last_updated, c.id as category_id
        FROM drugs d
        JOIN categories c ON d.category_id = c.id
        WHERE 1=1
        """
        params = []
        
        if category_filter and category_filter != 'All Categories':
            query += " AND c.category_name = %s"
            params.append(category_filter)
        
        if search:
            query += " AND d.drug_name LIKE %s"
            params.append(f"%{search}%")
        
        if sort == 'A-Z':
            query += " ORDER BY d.drug_name ASC"
        elif sort == 'Z-A':
            query += " ORDER BY d.drug_name DESC"
        elif sort == 'Price Low to High':
            query += " ORDER BY (d.price - (d.price * d.discount/100)) ASC"
        elif sort == 'Price High to Low':
            query += " ORDER BY (d.price - (d.price * d.discount/100)) DESC"
        else:
            query += " ORDER BY d.id DESC"
        
        db.execute(query, params)
        rs = db.fetchall()
        con.close()
        
        drugs = []
        for row in rs:
            price = float(row[3]) if row[3] else 0
            discount = float(row[4]) if row[4] else 0
            
            # Ensure discount doesn't exceed 100%
            if discount > 100:
                discount = 100
            if discount < 0:
                discount = 0
                
            final_price = price - (price * discount / 100)
            
            # Ensure final price is not negative
            if final_price < 0:
                final_price = 0
                
            drugs.append({
                "id": row[0],
                "drug_name": row[1],
                "category": row[2],
                "category_id": row[7],
                "price": round(price, 2),
                "discount": round(discount, 2),
                "final_price": round(final_price, 2),
                "available_stock": row[5],
                "last_updated": row[6]
            })
        return drugs

    def updateDrug(self, drug_id, price, discount, available_stock):
        con = Database().dbconnection()
        db = con.cursor()
        
        # Ensure positive values
        price = abs(float(price))
        discount = abs(float(discount))
        if discount > 100:
            discount = 100
        
        query = """
        UPDATE drugs 
        SET price = %s, discount = %s, available_stock = %s, last_updated = NOW()
        WHERE id = %s
        """
        db.execute(query, (price, discount, available_stock, drug_id))
        con.commit()
        con.close()

    def deleteDrug(self, drug_id):
        con = Database().dbconnection()
        db = con.cursor()
        
        db.execute("DELETE FROM drugs WHERE id = %s", (drug_id,))
        con.commit()
        con.close()

    def getLowStockDrugs(self, threshold=10):
        con = Database().dbconnection()
        db = con.cursor()
        
        query = """
        SELECT d.id, d.drug_name, d.available_stock, d.last_updated
        FROM drugs d
        WHERE d.available_stock < %s
        ORDER BY d.available_stock ASC
        """
        db.execute(query, (threshold,))
        rs = db.fetchall()
        con.close()
        
        drugs = []
        for row in rs:
            drugs.append({
                "id": row[0],
                "drug_name": row[1],
                "available_stock": row[2],
                "last_updated": row[3]
            })
        return drugs

    # ==================== CART MANAGEMENT ====================
    
    def addToCart(self, user_id, drug_id, quantity):
        con = Database().dbconnection()
        db = con.cursor()
        
        # Check if already in cart
        db.execute("SELECT id, quantity FROM cart WHERE user_id = %s AND drug_id = %s", (user_id, drug_id))
        existing = db.fetchone()
        
        if existing:
            db.execute("UPDATE cart SET quantity = quantity + %s WHERE id = %s", (quantity, existing[0]))
        else:
            db.execute("INSERT INTO cart(user_id, drug_id, quantity) VALUES(%s, %s, %s)", (user_id, drug_id, quantity))
        
        con.commit()
        con.close()

    def getCart(self, user_id):
        con = Database().dbconnection()
        db = con.cursor()
        
        query = """
        SELECT c.id, c.drug_id, d.drug_name, cat.category_name, c.quantity, 
               d.price, d.discount
        FROM cart c
        JOIN drugs d ON c.drug_id = d.id
        JOIN categories cat ON d.category_id = cat.id
        WHERE c.user_id = %s
        """
        db.execute(query, (user_id,))
        rs = db.fetchall()
        con.close()
        
        cart_items = []
        total = 0
        
        for row in rs:
            # Extract values safely
            cart_id = row[0]
            drug_id = row[1]
            drug_name = row[2]
            category = row[3]
            quantity = row[4] if row[4] else 0
            
            # Convert price and discount to float
            price = float(row[5]) if row[5] else 0
            discount = float(row[6]) if row[6] else 0
            
            # Validate discount
            if discount > 100:
                discount = 100
            if discount < 0:
                discount = 0
            
            # Calculate final price (ensure not negative)
            final_price = price - (price * discount / 100)
            if final_price < 0:
                final_price = 0
            
            # Calculate item total
            item_total = final_price * quantity
            
            # Add to grand total
            total += item_total
            
            cart_items.append({
                "cart_id": cart_id,
                "drug_id": drug_id,
                "drug_name": drug_name,
                "category": category,
                "quantity": quantity,
                "price": round(price, 2),
                "discount": round(discount, 2),
                "final_price": round(final_price, 2),
                "item_total": round(item_total, 2)
            })
        
        return cart_items, round(total, 2)

    def removeFromCart(self, cart_id):
        con = Database().dbconnection()
        db = con.cursor()
        
        db.execute("DELETE FROM cart WHERE id = %s", (cart_id,))
        con.commit()
        con.close()

    def clearCart(self, user_id):
        con = Database().dbconnection()
        db = con.cursor()
        
        db.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        con.commit()
        con.close()

    # ==================== ORDER MANAGEMENT ====================
    
    def placeOrder(self, user_id):
        con = Database().dbconnection()
        db = con.cursor()
        
        # Get cart items
        cart_items, total = self.getCart(user_id)
        
        if not cart_items:
            return False
        
        # Create order for each cart item
        for item in cart_items:
            query = """
            INSERT INTO orders(user_id, drug_id, quantity, price, total_amount, status)
            VALUES(%s, %s, %s, %s, %s, 'Order Placed')
            """
            db.execute(query, (user_id, item['drug_id'], item['quantity'], 
                              item['final_price'], item['item_total']))
            
            # Update stock
            db.execute("""
                UPDATE drugs SET available_stock = available_stock - %s 
                WHERE id = %s AND available_stock >= %s
            """, (item['quantity'], item['drug_id'], item['quantity']))
        
        # Clear cart
        db.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        
        con.commit()
        con.close()
        return True

    def getUserOrders(self, user_id):
        con = Database().dbconnection()
        db = con.cursor()
        
        query = """
        SELECT o.id, d.drug_name, c.category_name, o.quantity, o.price, o.total_amount, 
               o.order_date, o.status
        FROM orders o
        JOIN drugs d ON o.drug_id = d.id
        JOIN categories c ON d.category_id = c.id
        WHERE o.user_id = %s
        ORDER BY o.order_date DESC
        """
        db.execute(query, (user_id,))
        rs = db.fetchall()
        con.close()
        
        orders = []
        for row in rs:
            orders.append({
                "id": row[0],
                "drug_name": row[1],
                "category": row[2],
                "quantity": row[3],
                "price": float(row[4]),
                "total_amount": float(row[5]),
                "order_date": row[6],
                "status": row[7]
            })
        return orders

    def getAllOrders(self):
        con = Database().dbconnection()
        db = con.cursor()
        
        query = """
        SELECT o.id, u.name, u.email, u.phone, u.address, d.drug_name, c.category_name, 
               o.quantity, o.price, o.total_amount, o.order_date, o.status
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN drugs d ON o.drug_id = d.id
        JOIN categories c ON d.category_id = c.id
        ORDER BY o.order_date DESC
        """
        db.execute(query)
        rs = db.fetchall()
        con.close()
        
        orders = []
        for row in rs:
            orders.append({
                "id": row[0],
                "user_name": row[1],
                "user_email": row[2],
                "user_phone": row[3],
                "user_address": row[4],
                "drug_name": row[5],
                "category": row[6],
                "quantity": row[7],
                "price": float(row[8]),
                "total_amount": float(row[9]),
                "order_date": row[10],
                "status": row[11]
            })
        return orders

    def updateOrderStatus(self, order_id, status):
        con = Database().dbconnection()
        db = con.cursor()
        
        db.execute("UPDATE orders SET status = %s WHERE id = %s", (status, order_id))
        con.commit()
        con.close()

    # ==================== STATISTICS ====================
    
    def getDashboardStats(self):
        con = Database().dbconnection()
        db = con.cursor()
        
        # Total users
        db.execute("SELECT COUNT(*) FROM users WHERE user_type = 'user'")
        total_users = db.fetchone()[0]
        
        # Total categories
        db.execute("SELECT COUNT(*) FROM categories")
        total_categories = db.fetchone()[0]
        
        # Total drugs
        db.execute("SELECT COUNT(*) FROM drugs")
        total_drugs = db.fetchone()[0]
        
        # Total orders
        db.execute("SELECT COUNT(*) FROM orders")
        total_orders = db.fetchone()[0]
        
        # Total revenue
        db.execute("SELECT SUM(total_amount) FROM orders")
        total_revenue = db.fetchone()[0] or 0
        
        con.close()
        
        return {
            "total_users": total_users,
            "total_categories": total_categories,
            "total_drugs": total_drugs,
            "total_orders": total_orders,
            "total_revenue": float(total_revenue)
        }