# 🌾 Saffron Store - Business Setup Guide

Complete guide to set up your saffron store for personal business.

---

## 📋 Phase 1: Local Development Setup (TODAY)

### ✅ 1. Update .env File

Replace all placeholder values with actual credentials:

```env
SECRET_KEY=n^v!q^4b8-gm$o57(ktlye9=91xw9-kwdn70^*#y5ps^=(wlfg
DEBUG=True
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-secret
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
DATABASE_URL=sqlite:///db.sqlite3
```

**Where to get each:**
- `SECRET_KEY`: ✅ Use the one above
- `RAZORPAY_KEY_ID` & `SECRET`: See **Phase 2** below
- `CLOUDINARY_*`: See **Phase 3** below

### ✅ 2. Create Initial Admin Account

```bash
cd c:\Users\kanja\OneDrive\Desktop\saffron-store
env\Scripts\activate
python manage.py createsuperuser
```

Follow prompts to create your admin username, email, and password.

### ✅ 3. Start Development Server

```bash
python manage.py runserver
```

Access:
- **Store**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin/

---

## 💳 Phase 2: Setup Razorpay (Payment Gateway)

Razorpay allows customers to pay via credit/debit cards, UPI, wallets, etc.

### Step 1: Create Razorpay Account

1. Go to **https://razorpay.com**
2. Click **"Sign Up"**
3. Fill in business details:
   - Business Name: Your Saffron Business Name
   - Email: Your business email
   - Phone: Your phone number
4. Verify email and phone
5. Set up your business info

### Step 2: Get API Keys

1. Go to **Dashboard** → **Settings** → **API Keys**
2. You'll see two keys:
   - **Key ID** (Publishable) → `RAZORPAY_KEY_ID`
   - **Key Secret** (Secret) → `RAZORPAY_KEY_SECRET`
3. Copy both and add to `.env` file

### Step 3: Test Mode

Razorpay provides test credentials for safe testing:

**Test Card Numbers:**
- Visa: `4111111111111111` (any expiry, any CVV)
- Mastercard: `5555555555554444`

### Step 4: Enable Live Mode

Once verified:
1. Submit KYC documents to Razorpay
2. After approval → Switch to **Live Mode**
3. Use live API keys in `.env`

### Creating Payment Integration (Later)

You'll need to:
1. Create a payment view in `orders/views.py`
2. Handle Razorpay webhook callbacks
3. Verify payment signatures

---

## 📷 Phase 3: Setup Cloudinary (Image Storage - Optional)

Cloudinary hosts your product images on a CDN for fast loading.

### Step 1: Create Cloudinary Account

1. Go to **https://cloudinary.com**
2. Click **Sign up for free**
3. Fill in details
4. Verify email

### Step 2: Get API Keys

1. Go to **Dashboard**
2. Look for:
   - **Cloud Name** → `CLOUDINARY_CLOUD_NAME`
   - **API Key** → `CLOUDINARY_API_KEY`
   - **API Secret** → `CLOUDINARY_API_SECRET`
3. Copy and add to `.env`

### Step 3: Enable in Django

Once you have credentials, uncomment in `core/settings.py`:

```python
# Uncomment these lines:
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

Then restart server. Images will upload to Cloudinary!

**For now:** Images are saved locally in `/media/products/`

---

## 📱 Phase 4: Add Your Products

### Via Django Admin:

1. Go to **http://127.0.0.1:8000/admin/**
2. Login with your superuser credentials
3. Click **Products** → **Add Product**

**Fill in:**
- **Name**: e.g., "Premium Kashmiri Saffron"
- **Slug**: Auto-generated (URL identifier)
- **Description**: Product details
- **Origin**: "Kashmir, India"
- **Image**: Upload product photo
- **Is Active**: Check this box

**Add Variants** (click "Add another Product Variant"):
- **Weight (grams)**: 1, 5, 10, etc.
- **Price (₹)**: 50, 240, 450, etc.
- **Stock**: How many in stock

**Example Setup:**
```
Product: Premium Kashmiri Saffron
├─ 1g @ ₹50 (stock: 100)
├─ 5g @ ₹240 (stock: 50)
├─ 10g @ ₹450 (stock: 25)
└─ 50g @ ₹2500 (stock: 10)
```

### View on Frontend:

After saving, visit **http://127.0.0.1:8000/** to see your products!

---

## 🌐 Phase 5: Get Your Own Domain (Optional)

### Buy a Domain:

Popular domain registrars:
- **Namecheap**: https://namecheap.com (~₹100-300/year)
- **GoDaddy**: https://godaddy.com
- **Domain.com**: https://domain.com
- **Hostinger**: https://hostinger.com

**Good domain names:**
- saffronstore.com
- premiumsaffron.in
- indansaffron.com
- kashmirysaffron.shop

---

## 🚀 Phase 6: Deployment (Later)

Once ready to go live, you can deploy to:

### Option 1: PythonAnywhere (Easiest for Beginners)
- Simple setup
- Free tier available
- No server management needed
- https://pythonanywhere.com

### Option 2: Heroku
- Fully managed platform
- Good documentation
- Free tier available (though limited)
- https://heroku.com

### Option 3: DigitalOcean
- Affordable VPS
- Full control
- Requires some server knowledge
- https://digitalocean.com

### Option 4: Keep Running Locally
- Your computer acts as server
- Good for testing
- Limited to when computer is on

---

## 📧 Phase 7: Email Setup (Optional)

Configure email for order confirmations and notifications.

Update `core/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use Gmail App Password
DEFAULT_FROM_EMAIL = 'noreply@yourbusiness.com'
```

**To get Gmail App Password:**
1. Enable 2-factor authentication on Gmail
2. Go to Google Account → Security → App Passwords
3. Create new app password for Django
4. Use that password above

---

## 📊 Business Settings Checklist

- [ ] Created `.env` with SECRET_KEY
- [ ] Created superuser admin account
- [ ] Tested checkout flow locally
- [ ] Set up Razorpay account & got API keys
- [ ] Added first set of products
- [ ] Tested adding to cart & checkout
- [ ] Set up Cloudinary (optional)
- [ ] Purchased domain name (optional)

---

## 🎯 Common Tasks

### Add Multiple Products:

Via admin or bulk import. For each:
1. Product details (name, description, origin)
2. Add variants (weight options with prices)
3. Upload image
4. Set stock quantity

### Update Stock:

When you sell something:
1. Go to Admin → Products → Product Variants
2. Update stock number
3. System auto-prevents overselling

### View Orders:

1. Go to Admin → Orders
2. See customer info, items, total amount
3. Update order status (pending → shipped → delivered)

### Track Payments:

1. Go to Razorpay Dashboard
2. See all transactions
3. Monitor revenue

---

## 🔐 Important Security Notes

Before going live:

1. **Change `DEBUG = False`** in settings.py
2. **Add your domain** to `ALLOWED_HOSTS`
3. **Use strong SECRET_KEY** (already done ✅)
4. **Enable HTTPS** (SSL certificate)
5. **Use PostgreSQL** instead of SQLite
6. **Set up proper logging**
7. **Regular backups** of database

---

## 📞 Getting Help

- **Django Issues**: https://docs.djangoproject.com/
- **Razorpay Issues**: https://razorpay.com/support/
- **Cloudinary Issues**: https://cloudinary.com/support/
- **General Web Hosting**: Your hosting provider's support

---

## 🎉 Next Immediate Actions

1. ✅ Update `.env` file with SECRET_KEY (provided above)
2. 📧 Sign up for Razorpay (https://razorpay.com)
3. 📷 Add at least 3 saffron products via admin
4. 🧪 Test checkout with Razorpay test card
5. 📱 Optionally sign up for Cloudinary

---

**Your saffron store is ready for business!** 🌾✨
