
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "shopnest-development-secret"

products = [
    {"id": 1, "name": "Wireless Headphones", "price": 1999, "category": "Electronics", "emoji": "🎧"},
    {"id": 2, "name": "Smart Watch", "price": 2499, "category": "Electronics", "emoji": "⌚"},
    {"id": 3, "name": "Running Shoes", "price": 1799, "category": "Fashion", "emoji": "👟"},
    {"id": 4, "name": "Backpack", "price": 999, "category": "Accessories", "emoji": "🎒"},
    {"id": 5, "name": "Bluetooth Speaker", "price": 1499, "category": "Electronics", "emoji": "🔊"},
    {"id": 6, "name": "Sunglasses", "price": 799, "category": "Fashion", "emoji": "🕶️"},
]

orders = []


@app.route("/")
def home():
    search = request.args.get("q", "").strip().lower()

    filtered_products = [
        p for p in products
        if search in p["name"].lower() or search in p["category"].lower()
    ]

    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    return render_template(
        "index.html",
        products=filtered_products,
        cart_count=cart_count,
        cart=cart
    )


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if not any(p["id"] == product_id for p in products):
        return "Product not found", 404

    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    session["cart"] = cart

    return redirect(url_for("home"))


@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    cart_items = []
    total = 0

    for product in products:
        quantity = cart.get(str(product["id"]), 0)

        if quantity > 0:
            subtotal = product["price"] * quantity
            total += subtotal
            cart_items.append({
                **product,
                "quantity": quantity,
                "subtotal": subtotal
            })

    return jsonify({
        "items": cart_items,
        "total": total
    })


@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", {})

    if not cart:
        return jsonify({"error": "Your cart is empty"}), 400

    total = sum(
        p["price"] * cart.get(str(p["id"]), 0)
        for p in products
    )

    order = {
        "order_id": len(orders) + 1,
        "total": total,
        "status": "Confirmed"
    }

    orders.append(order)
    session["cart"] = {}

    return jsonify({
        "message": "Order placed successfully",
        "order": order
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "application": "ShopNest"}), 200


@app.route("/api/products")
def api_products():
    return jsonify(products)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
