import pandas as pd
import random

# Sample data patterns for generating the dataset
names = ["Rajesh Kumar", "Priya Sharma", "Suresh Gupta", "Meera Joshi", "Deepak Verma", 
         "Kavita Nair", "Arjun Reddy", "Preeti Malhotra", "Neha Sharma", "Ravi Gupta"]

masked_names = ["Michael Brown", "Jennifer Wilson", "David Miller", "Sarah Johnson", 
                "Lisa Brown", "Michael Johnson", "Jennifer Davis", "David Wilson"]

companies = ["Amazon", "Flipkart", "eBay", "Walmart", "Nike", "Dell", "HP"]
masked_companies = ["TechStore", "OnlineShop", "MarketPlace", "RetailStore", "SportsBrand"]

# Dataset entries
dataset = []

# Commerce & E-commerce entries
commerce_patterns = [
    ("Customer name {name}, order ID {order_id}, track my package", 
     "Customer name {name}, order ID {order_id}, track my package", 
     "Both customer identity and order needed for tracking"),
    
    ("Buyer {name}, seller {company}, what's the weather today?", 
     "Buyer {masked_name}, seller {masked_company}, what's the weather today?", 
     "Neither identity needed for weather query"),
    
    ("My name is {name}, purchased from {company}, count letters in my name", 
     "My name is {name}, purchased from {masked_company}, count letters in my name", 
     "Customer name needed for counting, seller not functional"),
    
    ("User {name}, product {product}, calculate shipping to my address", 
     "User {name}, product {product}, calculate shipping to my address", 
     "User identity needed for shipping calculation"),
    
    ("Account holder {name}, store {company}, explain machine learning", 
     "Account holder {masked_name}, store {masked_company}, explain machine learning", 
     "Neither identity needed for technical explanation")
]

# Generate 1000 commerce entries
for i in range(1000):
    pattern = random.choice(commerce_patterns)
    name = random.choice(names)
    masked_name = random.choice(masked_names)
    company = random.choice(companies)
    masked_company = random.choice(masked_companies)
    
    input_text = pattern[0].format(
        name=name, 
        company=company, 
        order_id=f"ORD{random.randint(10000,99999)}",
        product=f"Product{random.randint(1,100)}"
    )
    
    masked_text = pattern[1].format(
        name=name if "{name}" in pattern[1] else masked_name,
        masked_name=masked_name,
        company=company if "{company}" in pattern[1] else masked_company,
        masked_company=masked_company,
        order_id=f"ORD{random.randint(10000,99999)}",
        product=f"Product{random.randint(1,100)}"
    )
    
    dataset.append({
        'Section': 'Commerce & E-commerce',
        'Subsection': 'Online Shopping',
        'Input': input_text,
        'Masked': masked_text,
        'Reason': pattern[2],
        'Functional_Dependency': 'High' if pattern[0] == pattern[1] else 'Low'
    })

# Retail & POS entries
retail_patterns = [
    ("Cashier {name1}, customer {name2}, process return",
     "Cashier {name1}, customer {name2}, process return",
     "Both identities needed for return transaction"),
    
    ("Store manager {name}, receipt {receipt_id}, what's artificial intelligence?",
     "Store manager {masked_name}, receipt {masked_receipt}, what's artificial intelligence?",
     "Neither identity needed for AI explanation"),
    
    ("Sales associate {name}, transaction {txn_id}, count vowels in associate's name",
     "Sales associate {name}, transaction {masked_txn}, count vowels in associate's name",
     "Associate name needed for vowel count, transaction ID not functional")
]

# Generate 1000 retail entries
for i in range(1000):
    pattern = random.choice(retail_patterns)
    name = random.choice(names)
    name1 = random.choice(names)
    name2 = random.choice(names)
    masked_name = random.choice(masked_names)
    
    input_text = pattern[0].format(
        name=name,
        name1=name1,
        name2=name2,
        receipt_id=f"REC{random.randint(100,999)}",
        txn_id=f"TXN{random.randint(100,999)}"
    )
    
    masked_text = pattern[1].format(
        name=name if "{name}" in pattern[1] else masked_name,
        name1=name1,
        name2=name2,
        masked_name=masked_name,
        masked_receipt=f"REC{random.randint(100,999)}",
        masked_txn=f"TXN{random.randint(100,999)}"
    )
    
    dataset.append({
        'Section': 'Commerce & E-commerce',
        'Subsection': 'Retail & Point of Sale',
        'Input': input_text,
        'Masked': masked_text,
        'Reason': pattern[2],
        'Functional_Dependency': 'High' if pattern[0] == pattern[1] else 'Low'
    })

# Supply Chain entries
supply_patterns = [
    ("Driver {name}, truck {truck_id}, deliver package to address",
     "Driver {name}, truck {truck_id}, deliver package to address",
     "Driver identity and truck needed for delivery"),
    
    ("Warehouse manager {name}, facility {facility}, what's machine learning?",
     "Warehouse manager {masked_name}, facility {masked_facility}, what's machine learning?",
     "Neither identity needed for technical explanation"),
    
    ("Logistics coordinator {name}, shipment {shipment_id}, count letters in coordinator's first name",
     "Logistics coordinator {name}, shipment {masked_shipment}, count letters in coordinator's first name",
     "Coordinator name needed for counting, shipment ID not functional")
]

# Generate 1000 supply chain entries
for i in range(1000):
    pattern = random.choice(supply_patterns)
    name = random.choice(names)
    masked_name = random.choice(masked_names)
    
    input_text = pattern[0].format(
        name=name,
        truck_id=f"TR{random.randint(100,999)}",
        facility=f"WH-{random.choice(['North', 'South', 'East', 'West'])}",
        shipment_id=f"SH{random.randint(100,999)}"
    )
    
    masked_text = pattern[1].format(
        name=name if "{name}" in pattern[1] else masked_name,
        masked_name=masked_name,
        truck_id=f"TR{random.randint(100,999)}",
        masked_facility=f"WH-{random.choice(['North', 'South', 'East', 'West'])}",
        masked_shipment=f"SH{random.randint(100,999)}"
    )
    
    dataset.append({
        'Section': 'Commerce & E-commerce',
        'Subsection': 'Supply Chain & Logistics',
        'Input': input_text,
        'Masked': masked_text,
        'Reason': pattern[2],
        'Functional_Dependency': 'High' if pattern[0] == pattern[1] else 'Low'
    })

# Create DataFrame and save to Excel
df = pd.DataFrame(dataset)
df.to_excel('functional_dependency_dataset.xlsx', index=False)
print(f"Generated {len(dataset)} entries and saved to functional_dependency_dataset.xlsx")