import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import pandas as pd
from faker import Faker
from src.core.pii_system import PIIPrivacySystem


class PIIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('PII Privacy Protection System — v2')
        self.root.geometry('1100x700')
        tb.Style('solar')

        # Top controls
        top = tb.Frame(self.root, padding=10)
        top.pack(fill='x')
        tb.Button(top, text='Load Fake Data CSV', bootstyle='secondary', command=self.load_fake_data_csv).pack(side='left', padx=5)
        tb.Button(top, text='Generate Sample Input', bootstyle='info', command=self.generate_sample_input).pack(side='left', padx=5)
        tb.Button(top, text='Test CSV Data', bootstyle='warning', command=self.test_csv_data).pack(side='left', padx=5)
        tb.Button(top, text='Process Input', bootstyle='primary', command=self.process_input).pack(side='left', padx=15)

        # Main pane
        pan = tb.PanedWindow(self.root, orient='horizontal')
        pan.pack(fill='both', expand=True, padx=10, pady=10)

        # Left - Input
        left = tb.Frame(pan, padding=10)
        pan.add(left, weight=1)
        tb.Label(left, text='Input (Enter your text here)').pack(anchor='w')
        self.input_text = scrolledtext.ScrolledText(left, height=20)
        self.input_text.pack(fill='both', expand=True)

        # Middle - Anonymized
        mid = tb.Frame(pan, padding=10)
        pan.add(mid, weight=1)
        tb.Label(mid, text='Changed Data (Anonymized)').pack(anchor='w')
        self.anon_text = scrolledtext.ScrolledText(mid, height=20, state='normal')
        self.anon_text.pack(fill='both', expand=True)

        # Right - Output & Reconstructed
        right = tb.Frame(pan, padding=10)
        pan.add(right, weight=1)
        tb.Label(right, text='Output (LLM response)').pack(anchor='w')
        self.llm_text = scrolledtext.ScrolledText(right, height=8, state='normal')
        self.llm_text.pack(fill='both', expand=True)
        tb.Separator(right).pack(fill='x', pady=5)
        tb.Label(right, text='Reconstructed (original details restored)').pack(anchor='w')
        self.recon_text = scrolledtext.ScrolledText(right, height=5, state='normal')
        self.recon_text.pack(fill='both', expand=True)
        tb.Separator(right).pack(fill='x', pady=5)
        tb.Label(right, text='Data Sources Used').pack(anchor='w')
        self.sources_text = scrolledtext.ScrolledText(right, height=3, state='normal')
        self.sources_text.pack(fill='both', expand=True)

        # Status
        self.status = tb.StringVar(value='Ready - Enter your text and click Process Input')
        tb.Label(self.root, textvariable=self.status, bootstyle='dark').pack(fill='x', side='bottom')

        # System
        self.sys = PIIPrivacySystem()
        self.fake_data_df = None

    def test_csv_data(self):
        """Test CSV data functionality"""
        try:
            # Check if CSV data is loaded in the anonymizer
            if hasattr(self.sys, 'anonymizer') and hasattr(self.sys.anonymizer, '_has_csv_data') and self.sys.anonymizer._has_csv_data:
                categories = self.sys.anonymizer.get_csv_categories()
                csv_info = f"CSV data loaded successfully!\nAvailable categories: {', '.join(categories)}"
                
                # Test sample replacements
                test_results = []
                if 'name' in categories:
                    test_name = self.sys.anonymizer._get_replacement_data('name', 'John Doe')
                    test_results.append(f"Name test: {test_name[0]} (source: {test_name[1]})")
                
                if 'organization' in categories:
                    test_org = self.sys.anonymizer._get_replacement_data('organization', 'Acme Corp')
                    test_results.append(f"Organization test: {test_org[0]} (source: {test_org[1]})")
                
                if 'location' in categories:
                    test_loc = self.sys.anonymizer._get_replacement_data('location', 'New York')
                    test_results.append(f"Location test: {test_loc[0]} (source: {test_loc[1]})")
                
                if test_results:
                    csv_info += "\n\nSample replacements:\n" + "\n".join(test_results)
                
                messagebox.showinfo("CSV Data Test", csv_info)
            
            elif self.fake_data_df is not None:
                # CSV is loaded in GUI but not configured in anonymizer
                csv_info = f"CSV loaded in GUI: {len(self.fake_data_df)} rows\n"
                csv_info += f"Columns: {', '.join(self.fake_data_df.columns)}\n\n"
                csv_info += "Note: CSV data is loaded but not yet integrated with the anonymizer.\n"
                csv_info += "The anonymizer is still using Faker for replacements."
                messagebox.showinfo("CSV Data Status", csv_info)
            
            else:
                messagebox.showwarning("CSV Data Test", 
                                     "No CSV data loaded.\n\nTo use CSV data:\n"
                                     "1. Click 'Load Fake Data CSV' to load a CSV file\n"
                                     "2. The system will use CSV data first, Faker as fallback\n"
                                     "3. Click this button again to test the loaded data")
        
        except Exception as e:
            messagebox.showerror("CSV Data Test Error", f"Error testing CSV data: {str(e)}")

    def load_fake_data_csv(self):
        """Load CSV file containing fake data for PII replacement during anonymization"""
        path = filedialog.askopenfilename(
            title="Select Fake Data CSV for PII Replacement",
            filetypes=[('CSV Files', '*.csv')]
        )
        if not path:
            return
        
        try:
            self.fake_data_df = pd.read_csv(path)
            file_name = Path(path).name
            
            # Convert DataFrame to dictionary format for anonymizer
            csv_data = {}
            for column in self.fake_data_df.columns:
                # Clean column name and map to anonymizer categories
                clean_column = column.lower().strip()
                values = [str(val).strip() for val in self.fake_data_df[column].dropna() if str(val).strip()]
                
                # Map CSV columns to anonymizer categories
                if 'name' in clean_column:
                    csv_data['name'] = values
                elif 'email' in clean_column:
                    csv_data['email'] = values
                elif 'phone' in clean_column:
                    csv_data['phone'] = values
                elif 'organization' in clean_column or 'company' in clean_column:
                    csv_data['organization'] = values
                elif 'address' in clean_column or 'location' in clean_column or 'city' in clean_column:
                    csv_data['location'] = values
                elif 'ssn' in clean_column or 'national_id' in clean_column:
                    csv_data['ssn'] = values
                elif 'credit_card' in clean_column or 'card' in clean_column:
                    csv_data['credit_card'] = values
                elif 'ip' in clean_column:
                    csv_data['ip_address'] = values
                elif 'date' in clean_column:
                    csv_data['date'] = values
                else:
                    # Keep original column name for unrecognized columns
                    csv_data[clean_column] = values
            
            # Set CSV data in the anonymizer
            if hasattr(self.sys, 'anonymizer'):
                self.sys.anonymizer.set_csv_data(csv_data)
                categories = list(csv_data.keys())
                
                status_msg = f'Loaded CSV: {file_name} ({len(self.fake_data_df)} rows)'
                if categories:
                    status_msg += f' - Categories: {", ".join(categories)}'
                
                self.status.set(status_msg)
                messagebox.showinfo("CSV Loaded", 
                                  f"Successfully loaded CSV data!\n\n"
                                  f"File: {file_name}\n"
                                  f"Rows: {len(self.fake_data_df)}\n"
                                  f"Categories mapped: {', '.join(categories)}\n\n"
                                  f"The anonymizer will now use this data for replacements.")
            else:
                self.status.set(f'CSV loaded but anonymizer not available')
                messagebox.showwarning("Warning", "CSV loaded but could not configure anonymizer")
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load fake data CSV: {e}')
            self.status.set('Error loading CSV')

    def _analyze_csv_data(self):
        """Analyze CSV columns to determine what types of PII data are available"""
        if self.fake_data_df is None:
            return {}
            
        data_info = {
            'available_fields': [],
            'column_mapping': {},
            'total_rows': len(self.fake_data_df)
        }
        
        # Mapping based on your specific CSV structure
        column_mappings = {
            'name': 'Name',
            'email': 'Email', 
            'phone': 'Phone',
            'address': 'Address',
            'date_of_birth': 'Date_of_Birth',
            'credit_card': 'Credit_Card',
            'ip_address': 'IP_Address',
            'ssn': 'National_ID',  # Your National_ID appears to be SSN format
            'organization': 'Organization',
            'company': 'Organization'  # Alias for organization
        }
        
        # Check which columns exist in your CSV
        available_columns = self.fake_data_df.columns.tolist()
        
        for field_type, column_name in column_mappings.items():
            if column_name in available_columns:
                data_info['available_fields'].append(field_type)
                data_info['column_mapping'][field_type] = column_name
        
        return data_info

    def _get_random_csv_data(self, field_type=None, num_rows=1):
        """Get random data from CSV, optionally filtered by field type"""
        if self.fake_data_df is None or self.fake_data_df.empty:
            return None
            
        random_rows = self.fake_data_df.sample(n=min(num_rows, len(self.fake_data_df)))
        
        if field_type and hasattr(self.sys, '_csv_data_info'):
            column_mapping = self.sys._csv_data_info.get('column_mapping', {})
            if field_type in column_mapping:
                column = column_mapping[field_type]
                return random_rows[column].iloc[0] if num_rows == 1 else random_rows[column].tolist()
        
        return random_rows

    def _get_replacement_data(self, pii_type, original_value=None):
        """
        Smart replacement: try CSV first, fallback to Faker if not available
        Returns tuple: (replacement_value, source_info)
        """
        if self.fake_data_df is not None and hasattr(self.sys, '_csv_data_info'):
            csv_data_info = self.sys._csv_data_info
            
            # Try to get replacement from CSV
            if pii_type in csv_data_info.get('available_fields', []):
                column = csv_data_info['column_mapping'][pii_type]
                random_row = self.fake_data_df.sample(n=1)
                replacement_value = random_row[column].iloc[0]
                row_num = random_row.index[0] + 1  # 1-indexed for user display
                
                # Format the replacement value properly
                if pii_type == 'credit_card':
                    # Handle scientific notation in credit card numbers
                    replacement = f"{int(float(replacement_value)):016d}" if pd.notna(replacement_value) else "[INVALID_CC]"
                elif pii_type == 'date_of_birth':
                    # Keep date format as is
                    replacement = str(replacement_value)
                else:
                    replacement = str(replacement_value)
                    
                return replacement, f"CSV row {row_num}, column '{column}'"
        
        # Fallback to Faker
        fake = Faker()
        faker_mapping = {
            'name': fake.name,
            'email': fake.email,
            'phone': fake.phone_number,
            'address': fake.address,
            'city': fake.city,
            'state': fake.state,
            'zipcode': fake.zipcode,
            'ssn': fake.ssn,
            'date_of_birth': lambda: fake.date_of_birth().strftime('%d-%m-%Y'),
            'date': lambda: fake.date_of_birth().strftime('%d-%m-%Y'),
            'organization': fake.company,
            'company': fake.company,
            'credit_card': fake.credit_card_number,
            'ip_address': fake.ipv4,
            'job': fake.job,
            'country': fake.country
        }
        
        if pii_type in faker_mapping:
            replacement = faker_mapping[pii_type]()
            return str(replacement), "Faker (not in CSV)"
        
        # Default fallback
        return f"[REDACTED_{pii_type.upper()}]", "Default redaction"

    def _configure_pii_system_with_fake_data(self):
        """Configure the PII system to use the CSV data for PII replacements with smart fallback"""
        if self.fake_data_df is not None and not self.fake_data_df.empty:
            try:
                # Analyze what data types are available in the CSV
                csv_data_info = self._analyze_csv_data()
                
                # Pass the fake data and analysis to the PII system
                if hasattr(self.sys, 'set_fake_data_source'):
                    self.sys.set_fake_data_source(self.fake_data_df, csv_data_info)
                elif hasattr(self.sys, 'set_replacement_data'):
                    self.sys.set_replacement_data(self.fake_data_df, csv_data_info)
                elif hasattr(self.sys, 'configure_data_sources'):
                    self.sys.configure_data_sources(csv_data=self.fake_data_df, data_info=csv_data_info)
                else:
                    # Store data and helper methods for the PII system to use
                    self.sys._fake_data_df = self.fake_data_df
                    self.sys._csv_data_info = csv_data_info
                    self.sys._get_random_csv_data = self._get_random_csv_data
                    self.sys._get_replacement_data = self._get_replacement_data
                    print("Configured PII system with CSV data and smart fallback")
                    
            except Exception as e:
                print(f"Warning: Could not configure PII system with fake data: {e}")

    def get_random_fake_data(self, num_items=1):
        """Get random fake data items from the loaded CSV"""
        if self.fake_data_df is not None and not self.fake_data_df.empty:
            num_items = min(num_items, len(self.fake_data_df))
            return self.fake_data_df.sample(n=num_items)
        return None

    def generate_sample_input(self):
        """Generate sample input using random rows from fake data CSV or Faker"""
        try:
            if self.fake_data_df is not None and not self.fake_data_df.empty:
                # Use multiple random rows from fake data CSV
                num_rows = min(3, len(self.fake_data_df))  # Use up to 3 random rows
                random_rows = self.fake_data_df.sample(n=num_rows)
                
                # Combine data from multiple rows
                sample_parts = []
                for _, row in random_rows.iterrows():
                    row_text = " ".join(str(v) for v in row.values() if pd.notna(v))
                    if row_text.strip():
                        sample_parts.append(row_text.strip())
                
                sample_text = ". ".join(sample_parts)
            else:
                # Use Faker as fallback
                fake = Faker()
                sample_text = f"My name is {fake.name()}, I live at {fake.address()}, you can contact me at {fake.phone_number()} or email me at {fake.email()}."
            
            self.input_text.delete('1.0', 'end')
            self.input_text.insert('1.0', sample_text)
            
            source = f"CSV data ({num_rows} random rows)" if self.fake_data_df is not None else "Faker"
            self.status.set(f'Generated sample input using {source}')
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to generate sample input: {e}')

    def process_input(self):
        """Process the user input text"""
        text = self.input_text.get('1.0', 'end').strip()
        
        if not text:
            messagebox.showwarning('No Input', 'Please enter some text to process or use "Generate Sample Input".')
            return
        
        threading.Thread(target=self._process_worker, args=(text,), daemon=True).start()

    def _process_worker(self, text):
        """Worker thread for processing input"""
        try:
            self.status.set('Processing...')
            
            # Ensure PII system has the latest fake data for replacements
            if self.fake_data_df is not None:
                self._configure_pii_system_with_fake_data()
                
                # Initialize replacement tracking
                if not hasattr(self.sys, '_replacement_sources'):
                    self.sys._replacement_sources = {}
            
            # Process the input text - PII system will use CSV data for replacements if available
            res = self.sys.process(text, include_llm=True)
            
            # Get sources information
            sources_info = self._get_sources_info(text, res.anonymized_text)
            
            self._update_display(res.anonymized_text, res.llm_response, res.reconstructed_text, sources_info)
            
            # Update status based on what was used
            if hasattr(self.sys, 'anonymizer') and hasattr(self.sys.anonymizer, '_has_csv_data') and self.sys.anonymizer._has_csv_data:
                csv_usage = "CSV data + Faker fallback"
            elif self.fake_data_df is not None:
                csv_usage = "GUI CSV + Faker fallback"
            else:
                csv_usage = "Faker only"
            
            self.status.set(f'Done — anonymized using {csv_usage}')
            
        except Exception as e:
            self.status.set(f'Error: {e}')

    def _get_sources_info(self, original_text, anonymized_text):
        """Generate sources information based on available data"""
        sources_info = ""
        
        # Method 1: Check if anonymizer tracked sources
        if hasattr(self.sys, 'anonymizer') and hasattr(self.sys.anonymizer, 'get_replacement_sources'):
            sources = self.sys.anonymizer.get_replacement_sources()
            if sources:
                sources_list = [f"• {field}: {source}" for field, source in sources.items()]
                return "Anonymizer Sources:\n" + "\n".join(sources_list)
        
        # Method 2: Check if PII system tracked sources
        if hasattr(self.sys, '_replacement_sources') and self.sys._replacement_sources:
            sources_list = [f"• {field}: {source}" for field, source in self.sys._replacement_sources.items()]
            return "PII System Sources:\n" + "\n".join(sources_list)
        
        # Method 3: Show what CSV data is available for use
        if hasattr(self.sys, 'anonymizer') and hasattr(self.sys.anonymizer, '_has_csv_data') and self.sys.anonymizer._has_csv_data:
            categories = self.sys.anonymizer.get_csv_categories()
            sources_info = "CSV Data Available:\n"
            for category in categories:
                sources_info += f"• {category}: CSV data loaded\n"
            sources_info += "\nNote: Processing completed successfully using available data sources."
            return sources_info
        
        # Method 4: Show GUI CSV info
        if self.fake_data_df is not None:
            return f"CSV loaded in GUI: {len(self.fake_data_df)} rows\nColumns: {', '.join(self.fake_data_df.columns)}\n\nNote: Processing completed using available data."
        
        # Method 5: Basic fallback info
        return "No CSV data loaded - using Faker for any replacements.\n\nTip: Load a CSV file to use specific fake data for replacements."

    def get_csv_replacement(self, pii_type, original_value=None):
        """Public method for PII system to get smart replacements"""
        replacement, source = self._get_replacement_data(pii_type, original_value)
        
        # Track the replacement
        if not hasattr(self.sys, '_replacement_sources'):
            self.sys._replacement_sources = {}
        self.sys._replacement_sources[pii_type] = source
        
        return replacement

    def demo_replacement_tracking(self):
        """Demo method to show how replacement tracking works"""
        if self.fake_data_df is None:
            return "No CSV loaded"
            
        demo_info = "Demo - Available Replacements:\n\n"
        if hasattr(self.sys, '_csv_data_info'):
            csv_data_info = self.sys._csv_data_info
            available_fields = csv_data_info.get('available_fields', [])
            
            for field in available_fields[:5]:  # Show first 5 for demo
                replacement, source = self._get_replacement_data(field)
                demo_info += f"• {field}: {replacement}\n  Source: {source}\n\n"
                
        return demo_info

    def _update_display(self, anon, llm, recon, sources_info=None):
        """Update the display panels with processed results"""
        self.anon_text.delete('1.0', 'end')
        self.anon_text.insert('1.0', anon)
        self.llm_text.delete('1.0', 'end')
        self.llm_text.insert('1.0', llm)
        self.recon_text.delete('1.0', 'end')
        self.recon_text.insert('1.0', recon)
        
        # Update data sources information
        self.sources_text.delete('1.0', 'end')
        if sources_info:
            self.sources_text.insert('1.0', sources_info)
        else:
            default_info = "No source tracking available.\n\nTo enable detailed tracking, your PII system needs to:\n1. Use the provided _get_replacement_data() method\n2. Store results in self._replacement_sources\n\nCurrently showing that processing completed successfully."
            self.sources_text.insert('1.0', default_info)


def main():
    root = tb.Window(themename='solar')
    app = PIIGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()