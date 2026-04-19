import os
import random
import json
import pandas as pd
from faker import Faker

fake = Faker()

# ----------------------------
# Setup directories
# ----------------------------
BASE_DIR = "data/raw"
BANK_DIR = os.path.join(BASE_DIR, "bank_transactions")
INVOICE_DIR = os.path.join(BASE_DIR, "invoices")
ERP_DIR = os.path.join(BASE_DIR, "erp")

os.makedirs(BANK_DIR, exist_ok=True)
os.makedirs(INVOICE_DIR, exist_ok=True)
os.makedirs(ERP_DIR, exist_ok=True)

# ----------------------------
# Vendor normalization chaos
# ----------------------------
VENDOR_ALIASES = {
    "Amazon": ["Amazon", "AMZN", "Amazon India Pvt Ltd"],
    "TCS": ["TCS Ltd", "Tata Consultancy Services", "TCS"],
    "Swiggy": ["Swiggy", "Swiggy India", "SWIGGY"],
    "Uber": ["Uber", "Uber India", "UBER TRIP"]
}

VENDORS = list(VENDOR_ALIASES.keys())

# ----------------------------
# Generate Bank Transactions
# ----------------------------
def generate_transactions(n=300):
    """Generates messy bank transaction data with duplicates, mismatches, and missing fields."""
    data = []
    
    for i in range(n):
        vendor_key = random.choice(VENDORS)
        vendor_name = random.choice(VENDOR_ALIASES[vendor_key])
        
        amount = random.randint(200, 10000)
        is_credit = random.random() > 0.5
        
        if not is_credit:
            amount = -amount
        
        # Introduce slight mismatch
        if random.random() < 0.2:
            amount += random.randint(-50, 50)
        
        row = {
            "date": fake.date_this_year().strftime("%Y-%m-%d"),
            "amount": amount,
            "description": f"{vendor_name} {fake.word()} {random.randint(100,999)}",
            "reference": random.choice([None, f"REF{random.randint(1000,9999)}"]),
            "balance": random.randint(10000, 100000)
        }
        
        data.append(row)
        
        # Inject duplicates
        if random.random() < 0.1:
            data.append(row.copy())
    
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(BANK_DIR, "bank_01.csv"), index=False)


# ----------------------------
# Generate Invoices
# ----------------------------
def generate_invoices(n=100):
    invoices = []
    
    for i in range(n):
        vendor_key = random.choice(VENDORS)
        vendor_name = random.choice(VENDOR_ALIASES[vendor_key])
        
        amount = random.randint(200, 10000)
        
        invoice = {
            "invoice_id": f"INV-{i+1:03d}",
            "vendor": vendor_name,
            "amount": amount,
            "due_date": fake.date_this_year().strftime("%Y-%m-%d"),
            "status": random.choice(["paid", "unpaid"])
        }
        
        # Inject missing fields
        if random.random() < 0.15:
            invoice["due_date"] = None
        
        # Inject mismatched amount
        if random.random() < 0.2:
            invoice["amount"] += random.randint(-100, 100)
        
        invoices.append(invoice)
    
    with open(os.path.join(INVOICE_DIR, "invoice_01.json"), "w") as f:
        json.dump(invoices, f, indent=2)

# ----------------------------
# Generate ERP Ledger
# ----------------------------
def generate_erp(n=100):
    data = []
    
    for i in range(n):
        vendor_key = random.choice(VENDORS)
        
        row = {
            "entry_id": i + 1,
            "party": random.choice(VENDOR_ALIASES[vendor_key]),
            "type": random.choice(["payable", "receivable"]),
            "amount": random.randint(200, 10000),
            "date": fake.date_this_year().strftime("%Y-%m-%d")
        }
        
        data.append(row)
    
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(ERP_DIR, "ledger.csv"), index=False)

# ----------------------------
# Run everything
# ----------------------------
if __name__ == "__main__":
    print("Generating messy financial data...")
    
    generate_transactions()
    generate_invoices()
    generate_erp()
    
    print("Done. Your data is ready.")