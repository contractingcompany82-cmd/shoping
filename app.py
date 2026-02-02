import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="My Online Shop", layout="wide")

# --- Dummy Product Data ---
products = [
    {"id": 1, "name": "Laptop", "price": 80000, "category": "Electronics"},
    {"id": 2, "name": "Headphones", "price": 5000, "category": "Electronics"},
    {"id": 3, "name": "Coffee Mug", "price": 500, "category": "Home"},
    {"id": 4, "name": "Backpack", "price": 2500, "category": "Fashion"},
]

# --- Session State for Cart ---
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- UI Sidebar ---
st.sidebar.title("🛒 Shopping Cart")
if not st.session_state.cart:
    st.sidebar.write("Cart khali hai.")
else:
    total = 0
    for item in st.session_state.cart:
        st.sidebar.write(f"{item['name']} - ₹{item['price']}")
        total += item['price']
    st.sidebar.divider()
    st.sidebar.subheader(f"Total: ₹{total}")
    if st.sidebar.button("Checkout Done"):
        st.success("Order Place Ho Gaya!")
        st.session_state.cart = []

# --- Main Page UI ---
st.title("🛍️ Python Cloud Shop")
st.write("Welcome! Apne manpasand products chuniye.")

cols = st.columns(len(products))

for i, product in enumerate(products):
    with cols[i]:
        st.subheader(product["name"])
        st.write(f"Price: ₹{product['price']}")
        if st.button(f"Add to Cart", key=product["id"]):
            st.session_state.cart.append(product)
            st.toast(f"{product['name']} add ho gaya!")
