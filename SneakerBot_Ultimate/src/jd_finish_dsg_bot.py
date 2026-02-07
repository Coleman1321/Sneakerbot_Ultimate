from src.checkout_manager import process_checkout

def jd_finish_dsg_checkout(sneaker_id, size, payment_info):
    """Automates checkout for JD Sports, Finish Line, and Dick's Sporting Goods (DSG)."""
    print(f"🛒 Attempting checkout for {sneaker_id} on JD/FinishLine/DSG (Size: {size})...")

    success = process_checkout("JD Sports / Finish Line / DSG", sneaker_id, size, payment_info)

    if success:
        print("✅ JD Sports / Finish Line / DSG checkout successful!")
    else:
        print("❌ Checkout failed for JD / Finish Line / DSG.")
