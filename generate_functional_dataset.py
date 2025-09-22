#!/usr/bin/env python3
import random
import json

class FunctionalDependencyDatasetGenerator:
    def __init__(self):
        self.names = [
            "Rajesh Kumar", "Priya Sharma", "Suresh Gupta", "Meera Joshi", "Deepak Verma",
            "Kavita Nair", "Arjun Reddy", "Preeti Malhotra", "Neha Sharma", "Ravi Gupta",
            "Amit Agarwal", "Pooja Krishnan", "Ajay Malhotra", "Kiran Rao", "Sachin Tendulkar"
        ]
        
        self.replacement_names = [
            "Jennifer Wilson", "Michael Brown", "David Miller", "Sarah Johnson", "Lisa Davis",
            "Michael Johnson", "Jennifer Davis", "David Wilson", "Sarah Miller", "Lisa Brown"
        ]
        
        self.companies = ["Amazon", "Flipkart", "eBay", "Walmart", "Nike"]
        self.replacement_companies = ["TechStore", "OnlineShop", "MarketPlace", "RetailStore", "SportsBrand"]
        
        self.ids = ["ORD12345", "CART789", "INV001", "TXN123", "WL123"]
        self.replacement_ids = ["ORD67890", "CART456", "INV002", "TXN456", "WL456"]

    def generate_commerce_dataset(self, count=1000):
        dataset = []
        
        # Name analysis queries (keep name, mask others)
        name_queries = [
            "count letters in {name}'s name",
            "find vowels in {name}'s first name", 
            "check if {name}'s name starts with '{letter}'",
            "count syllables in {name}'s name",
            "arrange {name}'s name letters alphabetically",
            "count consonants in {name}'s name",
            "find palindromes in {name}'s name",
            "does {name}'s surname contain '{substring}'?",
            "check if {name}'s first name ends with '{letter}'",
            "find longest word in {name}'s name"
        ]
        
        # General knowledge queries (mask all entities)
        general_queries = [
            "what's the weather today?",
            "explain machine learning",
            "what's photosynthesis?", 
            "what's artificial intelligence?",
            "what's cooking recipes?",
            "what's meditation techniques?",
            "what's quantum physics?",
            "explain democracy",
            "what's cooking techniques?",
            "what's meditation benefits?"
        ]
        
        # Comparison queries (keep both entities)
        comparison_queries = [
            "which name is longer - {name1} or {name2}?",
            "calculate total letters in both names",
            "find common digits between {name} and {id}",
            "compare {name}'s first name length with {company} name"
        ]
        
        # Functional queries (keep functional entities)
        functional_queries = [
            "track my package", # needs customer + order
            "process return", # needs both parties
            "deliver package to address", # needs driver + truck
            "calculate shipping to my address" # needs user identity
        ]
        
        for i in range(count):
            name = random.choice(self.names)
            company = random.choice(self.companies)
            order_id = random.choice(self.ids)
            
            query_type = random.choice(['name', 'general', 'comparison', 'functional'])
            
            if query_type == 'name':
                query_template = random.choice(name_queries)
                letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                substring = random.choice(['kar', 'sha', 'raj', 'pra'])
                
                query = query_template.format(name=name, letter=letter, substring=substring)
                input_text = f"Customer {name}, order ID {order_id}, {query}"
                
                # Keep name (functional), mask order ID (not functional)
                masked_id = random.choice(self.replacement_ids)
                masked_text = f"Customer {name}, order ID {masked_id}, {query}"
                reason = f"Customer name needed for {query.split()[0]} analysis, order ID not functional"
                
            elif query_type == 'general':
                query = random.choice(general_queries)
                input_text = f"Buyer {name}, seller {company}, {query}"
                
                # Mask both (neither functional)
                masked_name = random.choice(self.replacement_names)
                masked_company = random.choice(self.replacement_companies)
                masked_text = f"Buyer {masked_name}, seller {masked_company}, {query}"
                reason = "Neither identity needed for general knowledge query"
                
            elif query_type == 'comparison':
                name2 = random.choice(self.names)
                query_template = random.choice(comparison_queries)
                
                if 'name1' in query_template:
                    query = query_template.format(name1=name, name2=name2)
                    input_text = f"Buyer {name}, seller {name2}, {query}"
                    masked_text = input_text  # Keep both for comparison
                    reason = "Both names needed for comparison"
                else:
                    query = query_template.format(name=name, id=order_id, company=company)
                    input_text = f"Customer {name}, company {company}, order {order_id}, {query}"
                    masked_text = input_text  # Keep all for comparison
                    reason = "All entities needed for comparison"
                    
            else:  # functional
                query = random.choice(functional_queries)
                input_text = f"Customer {name}, order ID {order_id}, {query}"
                masked_text = input_text  # Keep all for functional operation
                reason = "Both customer identity and order needed for operation"
            
            dataset.append({
                "input": input_text,
                "masked": masked_text, 
                "reason": reason
            })
        
        return dataset

    def generate_retail_dataset(self, count=1000):
        dataset = []
        
        roles = ["Cashier", "Store manager", "Sales associate", "Customer", "Clerk"]
        locations = ["Store-A", "Till-5", "Dock-3", "Department Electronics", "Region North"]
        
        for i in range(count):
            role = random.choice(roles)
            name = random.choice(self.names)
            location = random.choice(locations)
            
            # Similar pattern as commerce
            query_type = random.choice(['name_analysis', 'general', 'functional'])
            
            if query_type == 'name_analysis':
                queries = [
                    f"count vowels in {role.lower()}'s name",
                    f"check if {role.lower()}'s first name ends with 'r'",
                    f"find consonants in {role.lower()}'s surname"
                ]
                query = random.choice(queries)
                input_text = f"{role} {name}, location {location}, {query}"
                
                # Keep name, mask location
                masked_location = random.choice(locations)
                masked_text = f"{role} {name}, location {masked_location}, {query}"
                reason = f"{role} name needed for analysis, location not functional"
                
            elif query_type == 'general':
                queries = ["what's artificial intelligence?", "explain democracy", "what's cooking techniques?"]
                query = random.choice(queries)
                input_text = f"{role} {name}, location {location}, {query}"
                
                # Mask both
                masked_name = random.choice(self.replacement_names)
                masked_location = random.choice(locations)
                masked_text = f"{role} {masked_name}, location {masked_location}, {query}"
                reason = "Neither identity needed for general knowledge"
                
            else:  # functional
                queries = ["process return", "handle customer complaint", "authorize transaction"]
                query = random.choice(queries)
                input_text = f"{role} {name}, customer interaction, {query}"
                masked_text = input_text  # Keep for functional operation
                reason = f"{role} identity needed for {query}"
            
            dataset.append({
                "input": input_text,
                "masked": masked_text,
                "reason": reason
            })
        
        return dataset

    def generate_full_dataset(self):
        print("Generating Functional Dependency Privacy Masking Dataset...")
        
        dataset = {
            "metadata": {
                "title": "50,000 Functional Dependency Privacy Masking Dataset",
                "description": "Dataset where entities are masked only if NOT functionally required for answering the query"
            },
            "sections": {}
        }
        
        # Commerce & E-commerce (5,000 entries)
        print("Generating Commerce section...")
        commerce_data = self.generate_commerce_dataset(2500)
        retail_data = self.generate_retail_dataset(2500)
        
        dataset["sections"]["commerce"] = {
            "title": "Commerce & E-commerce (5,000 entries)",
            "subsections": {
                "online_shopping": {
                    "title": "Online Shopping (2,500 entries)", 
                    "data": commerce_data
                },
                "retail_pos": {
                    "title": "Retail & Point of Sale (2,500 entries)",
                    "data": retail_data
                }
            }
        }
        
        return dataset

    def save_dataset(self, filename="functional_dependency_dataset.json"):
        dataset = self.generate_full_dataset()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        print(f"Dataset saved to {filename}")
        
        # Also save in text format like your example
        text_filename = filename.replace('.json', '.txt')
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write("50,000 Functional Dependency Privacy Masking Dataset\n")
            f.write("=" * 60 + "\n\n")
            
            for section_key, section in dataset["sections"].items():
                f.write(f"Section: {section['title']}\n")
                f.write("-" * 40 + "\n")
                
                for subsection_key, subsection in section["subsections"].items():
                    f.write(f"\nSubsection: {subsection['title']}\n")
                    
                    for i, entry in enumerate(subsection["data"][:20]):  # Show first 20
                        f.write(f"Input: {entry['input']}\n")
                        f.write(f"Masked: {entry['masked']}\n") 
                        f.write(f"Reason: {entry['reason']}\n\n")
                        
        print(f"Text format saved to {text_filename}")

if __name__ == "__main__":
    generator = FunctionalDependencyDatasetGenerator()
    generator.save_dataset()