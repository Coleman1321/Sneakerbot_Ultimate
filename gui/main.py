"""
SneakerBot Ultimate - Enhanced GUI
With account management and manual CAPTCHA option
"""
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sys
import os
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.nike_bot import NikeBot
from src.adidas_bot import AdidasBot
from src.account_manager import AccountManager
from config.settings import CAPTCHA_CONFIG

class AccountManagerWindow:
    """Account management window"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Account Manager")
        self.window.geometry("600x400")
        
        self.am = AccountManager()
        self.create_widgets()
        self.load_accounts()
    
    def create_widgets(self):
        """Create account management UI"""
        # Header
        header = tk.Label(self.window, text="Stored Accounts", font=("Arial", 14, "bold"))
        header.pack(pady=10)
        
        # Account list
        list_frame = tk.Frame(self.window)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create treeview
        columns = ("ID", "Platform", "Email", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Account", command=self.add_account, 
                 bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Delete Selected", command=self.delete_account,
                 bg="#f44336", fg="white", width=15).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Refresh", command=self.load_accounts,
                 bg="#2196F3", fg="white", width=15).pack(side="left", padx=5)
    
    def load_accounts(self):
        """Load accounts from database"""
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load from database
        try:
            conn = sqlite3.connect("database/userdata.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, platform, email, status FROM accounts")
            accounts = cursor.fetchall()
            conn.close()
            
            for account in accounts:
                self.tree.insert("", "end", values=account)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accounts: {e}")
    
    def add_account(self):
        """Add new account"""
        # Create add account dialog
        dialog = tk.Toplevel(self.window)
        dialog.title("Add Account")
        dialog.geometry("400x250")
        
        tk.Label(dialog, text="Platform:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        platform_var = tk.StringVar(value="Nike")
        platform_menu = ttk.Combobox(dialog, textvariable=platform_var, 
                                     values=["Nike", "Adidas", "Shopify", "Supreme", "Footsites"],
                                     state="readonly", width=25)
        platform_menu.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Email:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        email_entry = tk.Entry(dialog, width=27)
        email_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Password:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        password_entry = tk.Entry(dialog, show="*", width=27)
        password_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="First Name:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        fname_entry = tk.Entry(dialog, width=27)
        fname_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Last Name:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        lname_entry = tk.Entry(dialog, width=27)
        lname_entry.grid(row=4, column=1, padx=10, pady=5)
        
        def save_account():
            platform = platform_var.get()
            email = email_entry.get()
            password = password_entry.get()
            first_name = fname_entry.get()
            last_name = lname_entry.get()
            
            if not email or not password:
                messagebox.showerror("Error", "Email and password required")
                return
            
            try:
                conn = sqlite3.connect("database/userdata.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO accounts (platform, email, password, first_name, last_name)
                    VALUES (?, ?, ?, ?, ?)
                """, (platform, email, password, first_name, last_name))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"Account added: {email}")
                dialog.destroy()
                self.load_accounts()
                
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Account already exists")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add account: {e}")
        
        tk.Button(dialog, text="Save", command=save_account, 
                 bg="#4CAF50", fg="white", width=15).grid(row=5, column=0, columnspan=2, pady=20)
    
    def delete_account(self):
        """Delete selected account"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an account to delete")
            return
        
        item = self.tree.item(selection[0])
        account_id = item["values"][0]
        email = item["values"][2]
        
        if messagebox.askyesno("Confirm", f"Delete account {email}?"):
            try:
                conn = sqlite3.connect("database/userdata.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Account deleted")
                self.load_accounts()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")


class SneakerBotGUI:
    """Enhanced main GUI with account management"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SneakerBot Ultimate - Security Research")
        self.root.geometry("700x650")
        
        self.manual_captcha_var = tk.BooleanVar(value=True)  # Manual CAPTCHA by default
        self.use_proxy_var = tk.BooleanVar(value=False)
        self.selected_account = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create enhanced GUI"""
        # Title
        title_frame = tk.Frame(self.root, bg="#1976D2", pady=15)
        title_frame.pack(fill="x")
        
        title = tk.Label(title_frame, text="SneakerBot Ultimate", 
                        font=("Arial", 20, "bold"), bg="#1976D2", fg="white")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Security Research Project - For Educational Use Only",
                           font=("Arial", 9), bg="#1976D2", fg="white")
        subtitle.pack()
        
        # Account Management Section
        account_frame = tk.LabelFrame(self.root, text="Account Management", 
                                     font=("Arial", 11, "bold"), padx=10, pady=10)
        account_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Button(account_frame, text="📋 Manage Stored Accounts", 
                 command=self.open_account_manager,
                 bg="#4CAF50", fg="white", width=25, height=2).pack(side="left", padx=5)
        
        tk.Button(account_frame, text="🔄 Load Account", 
                 command=self.load_saved_account,
                 bg="#2196F3", fg="white", width=25, height=2).pack(side="left", padx=5)
        
        # Manual Entry Section
        cred_frame = tk.LabelFrame(self.root, text="Manual Entry (or load account above)",
                                  padx=10, pady=10)
        cred_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Label(cred_frame, text="Email:").grid(row=0, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(cred_frame, width=45)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(cred_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(cred_frame, show="*", width=45)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Product Details
        product_frame = tk.LabelFrame(self.root, text="Product Details", padx=10, pady=10)
        product_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Label(product_frame, text="Sneaker Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.sneaker_entry = tk.Entry(product_frame, width=45)
        self.sneaker_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(product_frame, text="Size:").grid(row=1, column=0, sticky="w", pady=5)
        self.size_entry = tk.Entry(product_frame, width=45)
        self.size_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Platform Selection
        platform_frame = tk.LabelFrame(self.root, text="Select Platform", padx=10, pady=10)
        platform_frame.pack(padx=20, pady=10, fill="x")
        
        self.platform_var = tk.StringVar(value="Nike")
        platforms = [
            ("Nike/SNKRS", "Nike"),
            ("Adidas", "Adidas"),
            ("Shopify Stores", "Shopify"),
            ("Supreme", "Supreme"),
            ("Footsites", "Footsites")
        ]
        
        col = 0
        for text, value in platforms:
            tk.Radiobutton(platform_frame, text=text, variable=self.platform_var,
                          value=value).grid(row=0, column=col, padx=10, sticky="w")
            col += 1
        
        # Options
        options_frame = tk.LabelFrame(self.root, text="Options", padx=10, pady=10)
        options_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Checkbutton(options_frame, text="✋ Manual CAPTCHA (Recommended - No API cost!)",
                      variable=self.manual_captcha_var,
                      font=("Arial", 10, "bold")).pack(anchor="w")
        
        tk.Label(options_frame, text="   ℹ️  When checked, bot will pause and let you solve CAPTCHAs manually",
                fg="gray", font=("Arial", 9)).pack(anchor="w")
        
        tk.Checkbutton(options_frame, text="Use Proxies (requires proxy list)",
                      variable=self.use_proxy_var).pack(anchor="w", pady=(10,0))
        
        # Action Buttons
        button_frame = tk.Frame(self.root, pady=15)
        button_frame.pack()
        
        tk.Button(button_frame, text="🚀 Run Bot", command=self.run_bot,
                 bg="#4CAF50", fg="white", width=20, height=2,
                 font=("Arial", 11, "bold")).pack(side="left", padx=10)
        
        tk.Button(button_frame, text="📊 Monitor Stock", command=self.monitor_stock,
                 bg="#FF9800", fg="white", width=20, height=2,
                 font=("Arial", 11, "bold")).pack(side="left", padx=10)
        
        # Status Bar
        self.status_label = tk.Label(self.root, text="Ready", 
                                     relief=tk.SUNKEN, anchor="w")
        self.status_label.pack(fill="x", side="bottom")
    
    def open_account_manager(self):
        """Open account management window"""
        AccountManagerWindow(self.root)
    
    def load_saved_account(self):
        """Load account from database"""
        try:
            conn = sqlite3.connect("database/userdata.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, platform, email, password FROM accounts WHERE status='active'")
            accounts = cursor.fetchall()
            conn.close()
            
            if not accounts:
                messagebox.showinfo("No Accounts", 
                    "No saved accounts found.\nClick 'Manage Stored Accounts' to add one.")
                return
            
            # Create selection dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Select Account")
            dialog.geometry("400x300")
            
            tk.Label(dialog, text="Select an account to load:", 
                    font=("Arial", 11, "bold")).pack(pady=10)
            
            listbox = tk.Listbox(dialog, width=50, height=10)
            listbox.pack(padx=20, pady=10)
            
            for acc in accounts:
                listbox.insert(tk.END, f"{acc[1]} - {acc[2]}")
            
            def load_selected():
                selection = listbox.curselection()
                if selection:
                    idx = selection[0]
                    account = accounts[idx]
                    
                    self.email_entry.delete(0, tk.END)
                    self.email_entry.insert(0, account[2])
                    
                    self.password_entry.delete(0, tk.END)
                    self.password_entry.insert(0, account[3])
                    
                    self.platform_var.set(account[1])
                    
                    messagebox.showinfo("Success", f"Loaded account: {account[2]}")
                    dialog.destroy()
            
            tk.Button(dialog, text="Load Selected", command=load_selected,
                     bg="#4CAF50", fg="white", width=20).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accounts: {e}")
    
    def run_bot(self):
        """Run bot with selected settings"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        sneaker = self.sneaker_entry.get()
        size = self.size_entry.get()
        platform = self.platform_var.get()
        use_manual_captcha = self.manual_captcha_var.get()
        use_proxy = self.use_proxy_var.get()
        
        if not all([email, password, sneaker, size]):
            messagebox.showerror("Error", "Please fill in all fields\nor load a saved account")
            return
        
        self.status_label.config(text=f"Running {platform} bot...")
        self.root.update()
        
        try:
            # Update CAPTCHA config for this session
            CAPTCHA_CONFIG["auto_solve"] = not use_manual_captcha
            
            if platform == "Nike":
                # Show info about manual CAPTCHA
                if use_manual_captcha:
                    messagebox.showinfo("Manual CAPTCHA Mode",
                        "Bot will pause when CAPTCHA appears.\n" +
                        "Solve it manually, then press Enter in terminal to continue.")
                
                bot = NikeBot(email, password, use_proxy)
                bot.setup_browser()
                
                try:
                    if bot.login():
                        success = bot.complete_purchase(sneaker, size)
                        if success:
                            messagebox.showinfo("Success", 
                                f"Nike purchase process completed!\n" +
                                f"Sneaker: {sneaker}\nSize: {size}")
                        else:
                            messagebox.showerror("Failed", "Purchase process failed")
                    else:
                        messagebox.showerror("Failed", "Login failed")
                finally:
                    bot.cleanup()
                    
            elif platform == "Adidas":
                if use_manual_captcha:
                    messagebox.showinfo("Manual CAPTCHA Mode", 
                        "Bot will pause for manual CAPTCHA solving")
                
                bot = AdidasBot(email, password, use_proxy)
                bot.setup_browser()
                
                try:
                    success = bot.complete_purchase(sneaker, size)
                    if success:
                        messagebox.showinfo("Success", "Adidas purchase completed!")
                    else:
                        messagebox.showerror("Failed", "Purchase failed")
                finally:
                    bot.cleanup()
            
            else:
                messagebox.showinfo("Info", 
                    f"{platform} bot demo mode\n" +
                    "Full implementation available in code")
                
        except Exception as e:
            messagebox.showerror("Error", f"Bot error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.status_label.config(text="Ready")
    
    def monitor_stock(self):
        """Stock monitoring"""
        messagebox.showinfo("Stock Monitor",
            "Stock monitoring runs in background\n" +
            "See stock_monitor.py for full implementation")


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Check if database exists
    if not os.path.exists("database/userdata.db"):
        response = messagebox.askyesno("Database Not Found",
            "Database not initialized.\n" +
            "Run setup wizard first?\n\n" +
            "Click Yes to run setup, No to exit")
        
        if response:
            import subprocess
            subprocess.run([sys.executable, "setup_wizard.py"])
        root.destroy()
        return
    
    app = SneakerBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
