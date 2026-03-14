from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from functools import wraps
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import os

# chatbot functions
from .chatbot import predict_disease, chatbot_response

main = Blueprint('main', __name__)

# ----------------------------
# Login Required Decorator
# ----------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# Home
# ----------------------------
@main.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# Shop
# ----------------------------
@main.route("/shop")
def shop():
    db = current_app.db
    products = list(db.products.find())
    return render_template("shop.html", products=products)


# ----------------------------
# Add Product
# ----------------------------
@main.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():

    db = current_app.db

    if request.method == "POST":

        name = request.form.get("name")
        price = int(request.form.get("price"))
        description = request.form.get("description")

        image = request.files.get("image")

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
        else:
            filename = "default.png"

        db.products.insert_one({
            "name": name,
            "price": price,
            "description": description,
            "image": filename
        })

        return redirect(url_for("main.shop"))

    return render_template("add_product.html")


# ----------------------------
# Add to Cart
# ----------------------------
@main.route("/add-to-cart/<product_id>")
@login_required
def add_to_cart(product_id):

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(product_id)
    session["cart_count"] = len(session["cart"])
    session.modified = True

    return redirect(url_for("main.cart"))


# ----------------------------
# Cart Page
# ----------------------------
@main.route("/cart")
@login_required
def cart():

    db = current_app.db
    cart_items = []
    total = 0

    if "cart" in session:
        for item_id in session["cart"]:
            product = db.products.find_one({"_id": ObjectId(item_id)})

            if product:
                cart_items.append(product)
                total += product["price"]

    return render_template("cart.html", cart_items=cart_items, total=total)


# ----------------------------
# Remove Item from Cart
# ----------------------------
@main.route("/remove/<product_id>")
@login_required
def remove_from_cart(product_id):

    if "cart" in session and product_id in session["cart"]:
        session["cart"].remove(product_id)
        session["cart_count"] = len(session["cart"])
        session.modified = True

    return redirect(url_for("main.cart"))


# ----------------------------
# SMART CHATBOT (TEXT + IMAGE)
# ----------------------------
@main.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    reply = None
    disease = None
    medicine = None

    if request.method == "POST":

        message = request.form.get("message")
        image = request.files.get("image")

        # TEXT CHATBOT
        if message:
            reply = chatbot_response(message)

        # IMAGE DISEASE DETECTION
        if image and image.filename != "":

            filename = secure_filename(image.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)

            disease, medicine = predict_disease(filepath)

    return render_template(
        "chatbot.html",
        reply=reply,
        disease=disease,
        medicine=medicine
    )


# ----------------------------
# Login
# ----------------------------
@main.route("/login", methods=["GET", "POST"])
def login():

    db = current_app.db

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = db.users.find_one({
            "username": username,
            "password": password
        })

        if user:
            session["user"] = username
            session["cart"] = []
            session["cart_count"] = 0
            return redirect(url_for("main.home"))

        return "Invalid Credentials!"

    return render_template("login.html")


# ----------------------------
# Register
# ----------------------------
@main.route("/register", methods=["GET", "POST"])
def register():

    db = current_app.db

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if db.users.find_one({"username": username}):
            return "User already exists!"

        db.users.insert_one({
            "username": username,
            "password": password
        })

        return redirect(url_for("main.login"))

    return render_template("register.html")


# ----------------------------
# Logout
# ----------------------------
@main.route("/logout")
def logout():

    session.pop("user", None)
    session.pop("cart", None)
    session.pop("cart_count", None)

    return redirect(url_for("main.home"))