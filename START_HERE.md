# 🚀 START HERE - First Time Setup

## **Step 1: Run the Setup Wizard**

```bash
python setup_wizard.py
```

The wizard will:
- ✅ Check Python version
- ✅ Install all dependencies automatically
- ✅ Install browsers
- ✅ Create database
- ✅ Create desktop shortcut
- ✅ Set up configuration

**This takes 5 minutes and does everything for you!**

---

## **Step 2: Launch the Bot**

After setup completes, you can launch in 3 ways:

### **Option A: Double-click the shortcut**
- Look for `START_HERE.bat` (Windows) or `START_HERE.sh` (Mac/Linux)
- Double-click it

### **Option B: Desktop icon**
- Setup creates a desktop shortcut
- Double-click it

### **Option C: Command line**
```bash
python run_bot.py
```

---

## **Step 3: Add Your Accounts**

When the GUI opens:

1. Click **"📋 Manage Stored Accounts"**
2. Click **"Add Account"**
3. Fill in:
   - Platform: Nike, Adidas, etc.
   - Email: your@email.com
   - Password: yourpassword
   - Name (optional)
4. Click **"Save"**

Now your accounts are stored securely in the database!

---

## **Step 4: Use the Bot**

### **For Actual Purchases:**

1. Click **"🔄 Load Account"** to load saved credentials
2. Fill in:
   - **Sneaker Name**: "Air Jordan 1"
   - **Size**: "10.5"
3. **Check** "✋ Manual CAPTCHA" (avoid paying for service!)
4. Select **Platform**: Nike, Adidas, etc.
5. Click **"🚀 Run Bot"**

### **Manual CAPTCHA Mode (Recommended!)**

When **"✋ Manual CAPTCHA"** is checked:
- Bot runs normally
- When CAPTCHA appears, **bot pauses**
- **You solve it manually** in the browser
- **Press Enter** in the terminal
- Bot continues!

**No API costs! No subscription needed!**

---

## **What Works Right Now:**

✅ **Account Management** - Store unlimited accounts  
✅ **Manual CAPTCHA** - No paid service needed  
✅ **Nike Bot** - Complete login & purchase flow  
✅ **Adidas Bot** - With queue handling  
✅ **Stock Monitor** - Track restocks  
✅ **Database** - All your data saved  

---

## **Important Notes:**

### **For Your Presentation:**
This project is for **security research** to show companies how bots work. Focus on:
- The **security analysis** (`docs/SECURITY_ANALYSIS.md`)
- The **code quality** and techniques demonstrated
- The **defensive recommendations** for companies

### **For Actual Use:**
- ⚠️ Requires real accounts with saved payment
- ⚠️ Success rate varies by site defenses
- ⚠️ Use for authorized testing only
- ✅ Manual CAPTCHA mode = free!

---

## **Troubleshooting:**

### **"ModuleNotFoundError"**
```bash
python setup_wizard.py
```
The wizard installs everything.

### **"Database not found"**
```bash
python database/init_db.py
```

### **"Browser not found"**
```bash
playwright install chromium
```

### **GUI won't open**
```bash
# Install tkinter (usually pre-installed)
# Windows/Mac: Already included
# Linux: sudo apt-get install python3-tk
```

---

## **Quick Commands:**

```bash
# Setup (first time only)
python setup_wizard.py

# Launch GUI
python run_bot.py

# Or double-click
START_HERE.bat  # Windows
START_HERE.sh   # Mac/Linux

# Check database
sqlite3 database/userdata.db "SELECT * FROM accounts;"

# View logs
cat bot.log
```

---

## **Files You Need to Know:**

- **`setup_wizard.py`** - Run this first!
- **`run_bot.py`** - Launches the GUI
- **`database/userdata.db`** - Your accounts stored here
- **`config/settings.py`** - All settings
- **`docs/SECURITY_ANALYSIS.md`** - For presentation
- **`bot.log`** - All activity logged here

---

## **Next Steps:**

1. ✅ Run setup wizard
2. ✅ Launch GUI
3. ✅ Add your accounts
4. ✅ Try a test run with manual CAPTCHA
5. ✅ Review security analysis for presentation

---

**That's it! You're ready to go!** 🎉

For detailed documentation, see `README.md` and `QUICK_START.md`.
