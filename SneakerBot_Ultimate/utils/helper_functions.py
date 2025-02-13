import random
import string

def generate_random_email():
    """Generates a random email for sneaker raffle entries."""
    domain = ["gmail.com", "yahoo.com", "outlook.com"]
    name = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"{name}@{random.choice(domain)}"
    return email

