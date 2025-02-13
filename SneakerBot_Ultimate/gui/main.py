import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.adidas_bot import adidas_checkout
from src.nike_bot import nike_login, enter_snkrs_draw
from src.shopify_bot import monitor_shopify_stock, checkout_shopify


def run_adidas():
    """Executes full Adidas automation: login → search sneaker → checkout"""
    email = email_entry.get()
    password = password_entry.get()
    sneaker = sneaker_entry.get()

    if not email or not password or not sneaker:
        messagebox.showerror("Error", "Please enter email, password, and sneaker name.")
        return

    messagebox.showinfo("Status", f"Starting Adidas bot for {sneaker}...")

    with open("log.txt", "a") as log_file:
        log_file.write(f"Running Adidas bot for {sneaker}...\n")

    success = adidas_checkout(email, password, sneaker)

    if success:
        messagebox.showinfo("Success", f"Successfully purchased {sneaker}!")
    else:
        messagebox.showerror("Failed", f"Could not complete checkout for {sneaker}.")


def run_nike():
    from src.nike_bot import nike_login, enter_snkrs_draw
    email = email_entry.get()
    password = password_entry.get()
    nike_login(email, password)
    enter_snkrs_draw("nike-travis-scott", "10")

def run_shopify():
    from src.shopify_bot import monitor_shopify_stock, checkout_shopify
    sneaker_id = monitor_shopify_stock("kith.com", ["Jordan", "Nike"])
    if sneaker_id:
        checkout_shopify("kith.com", sneaker_id, "10.5")

# Create GUI
root = tk.Tk()
root.title("SneakerBot Ultimate")
root.geometry("400x300")

tk.Label(root, text="Email:").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Label(root, text="Sneaker Name:").pack()
sneaker_entry = tk.Entry(root)
sneaker_entry.pack()

nike_button = tk.Button(root, text="Run Nike Bot", command=run_nike)
nike_button.pack()

adidas_button = tk.Button(root, text="Run Adidas Bot", command=run_adidas)
adidas_button.pack()

shopify_button = tk.Button(root, text="Run Shopify Monitor", command=run_shopify)
shopify_button.pack()

root.mainloop()
