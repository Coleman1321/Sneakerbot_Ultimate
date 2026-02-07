from src.checkout_manager import process_checkout

def footsites_checkout(sneaker_id, size, payment_info):
    """Automates checkout for FootLocker, Champs, and Eastbay."""
    print(f"🛒 Starting checkout process for {sneaker_id} on Footsites (Size: {size})...")

    success = process_checkout("Footsites", sneaker_id, size, payment_info)

    if success:
        print("✅ Footsites checkout successful!")
    else:
        print("❌ Footsites checkout failed.")
