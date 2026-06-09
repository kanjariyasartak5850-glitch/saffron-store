# Saffron Store - Setup & Configuration Guide

## 📋 Project Overview

Your Django-based e-commerce store for selling premium Kashmiri saffron is now configured with:

- ✅ Product management system with variants (different weights/prices)
- ✅ Shopping cart functionality (session-based)
- ✅ Order management system
- ✅ Admin dashboard for managing products and orders
- ✅ Responsive UI with Bootstrap 5
- ✅ Razorpay payment integration (configured, awaiting API keys)
- ✅ Cloudinary image storage (configured, awaiting API keys)

---

## 🔧 Environment Configuration

### 1. Fill in your `.env` file

Update `c:\Users\kanja\OneDrive\Desktop\saffron-store\.env` with your actual credentials:

```env
SECRET_KEY=your-actual-secret-key-here
DEBUG=True
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
DATABASE_URL=sqlite:///db.sqlite3
```

### 2. Generate a Secure SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy this value to your `.env` file.

---

## 📦 Required API Keys

### Razorpay Setup (Payment Gateway)
1. Go to https://razorpay.com
2. Sign up and create an account
3. Get your Key ID and Key Secret from Dashboard → Settings → API Keys
4. Add them to `.env`

### Cloudinary Setup (Image Storage)
1. Go to https://cloudinary.com
2. Sign up for free account
3. Get your Cloud Name, API Key, and API Secret from Dashboard
4. Add them to `.env`

---

## 🚀 Getting Started

### 1. Activate Virtual Environment

```bash
# Navigate to project
cd c:\Users\kanja\OneDrive\Desktop\saffron-store

# Activate virtual environment
env\Scripts\activate
```

### 2. Install Dependencies

All required packages are already in your environment. To verify:

```bash
pip list
```

Key packages:
- Django 6.0.6
- Pillow 12.2.0 (Image handling)
- Razorpay 2.0.1 (Payment)
- Cloudinary 1.44.2 (Image storage)
- psycopg2 (PostgreSQL support)

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 5. Start Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 👨‍💼 Admin Dashboard Access

1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. You'll see:
   - **Products**: Add saffron products with multiple weight variants
   - **Product Variants**: Manage pricing and stock for each weight
   - **Orders**: Track customer orders
   - **Order Items**: View items in each order

---

## 📝 Managing Products

### Adding a Product

1. Go to Admin → Products → Add Product
2. Fill in details:
   - **Name**: e.g., "Premium Kashmiri Saffron"
   - **Slug**: Auto-generated URL identifier
   - **Description**: Product details
   - **Origin**: e.g., "Kashmir, India"
   - **Image**: Upload product photo (uploaded to Cloudinary)
   - **Is Active**: Check to make it visible

3. Add Variants (different weights):
   - Go to Product Variants section
   - Add each weight option with price and stock
   - Example:
     - 1g - ₹50
     - 5g - ₹240
     - 10g - ₹450

---

## 🛍️ Frontend Routes

Your storefront is now live with these routes:

| Route | Purpose |
|-------|---------|
| `/` | Product listing page |
| `/product/<slug>/` | Product details page |
| `/cart/add/<variant_id>/` | Add to cart (POST) |
| `/cart/` | View shopping cart |
| `/cart/remove/<variant_id>/` | Remove from cart (POST) |
| `/cart/update/<variant_id>/` | Update quantity (POST) |
| `/checkout/` | Checkout page |
| `/order/<order_id>/success/` | Order confirmation |
| `/admin/` | Admin dashboard |

---

## 🛒 Shopping Cart Features

- **Session-based**: Uses Django sessions to store cart
- **Persistent**: Cart remains until checkout or manual clearing
- **Add to Cart**: Users can select weight variant and quantity
- **Update Quantity**: Adjust quantities before checkout
- **Remove Items**: Delete products from cart

---

## 💳 Payment Integration (Next Steps)

### Setup Razorpay Integration

You'll need to create an API endpoint to handle payments. Here's what needs to be done:

1. **Create a payment view** in `orders/views.py`:
   - Get cart items from session
   - Create Razorpay order
   - Return order details to frontend

2. **Handle payment callback** from Razorpay:
   - Verify payment signature
   - Create Order and OrderItem objects
   - Clear session cart
   - Send confirmation email

3. **Update checkout template** to trigger Razorpay payment modal

**Note**: Payment implementation is more complex and requires additional setup.

---

## 📧 Email Notifications (Optional)

Configure email settings in `core/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@saffronstore.com'
```

---

## 🗄️ Database Information

Currently using SQLite (`db.sqlite3`). For production, consider:

- **PostgreSQL** (recommended)
- **MySQL**
- **MariaDB**

Update `DATABASES` in `core/settings.py` to switch.

---

## 📁 Project Structure

```
saffron-store/
├── core/                 # Django project settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # Main URL routing
│   ├── wsgi.py          # Production deployment
│   └── asgi.py          # Async support
├── shop/                # E-commerce app
│   ├── models.py        # Product & ProductVariant
│   ├── views.py         # Frontend views
│   ├── admin.py         # Admin configuration
│   └── urls.py          # Shop routes
├── orders/              # Order management app
│   ├── models.py        # Order & OrderItem
│   ├── admin.py         # Admin configuration
│   └── urls.py          # Order routes
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   └── shop/            # Shop-specific templates
├── static/              # CSS, JS, images
│   ├── css/style.css    # Custom styling
│   └── js/main.js       # Frontend JavaScript
├── db.sqlite3           # Database
├── manage.py            # Django management
└── .env                 # Environment variables (secret)
```

---

## 🔐 Security Checklist

Before going to production:

- [ ] Change `DEBUG = False` in settings.py
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Use strong `SECRET_KEY`
- [ ] Configure HTTPS
- [ ] Set up proper database (not SQLite)
- [ ] Configure CSRF settings
- [ ] Set up security headers
- [ ] Test payment flow thoroughly

---

## 📱 Responsive Design

Your store is mobile-friendly with:
- Bootstrap 5 responsive grid
- Mobile-optimized navigation
- Touch-friendly buttons
- Responsive tables

---

## 🎨 Customization Guide

### Change Store Colors

Edit `static/css/style.css`:

```css
:root {
    --saffron-color: #D4A574;    /* Main theme color */
    --dark-color: #1a1a1a;
    --success-color: #28a745;
}
```

### Add Custom Logo

1. Place logo image in `static/img/`
2. Update `templates/base.html`:
   ```html
   <img src="{% static 'img/logo.png' %}" alt="Logo" class="logo">
   ```

### Modify Footer

Edit footer section in `templates/base.html`

---

## 🆘 Troubleshooting

### Issue: Images not uploading
- Check Cloudinary credentials in `.env`
- Verify API key and secret are correct
- Check Cloudinary account permissions

### Issue: Cart not persisting
- Ensure sessions middleware is enabled in `settings.py`
- Check browser cookies are enabled
- Clear browser cache

### Issue: Static files not loading
- Run: `python manage.py collectstatic`
- Check `STATIC_URL` and `STATICFILES_DIRS` in settings

---

## 📚 Next Steps

1. ✅ Configure `.env` with real API keys
2. ✅ Create products in admin panel
3. ✅ Test shopping flow
4. ✅ Implement payment integration
5. ✅ Set up email notifications
6. ✅ Deploy to production server
7. ✅ Set up domain and SSL certificate

---

## 💡 Tips

- Use the admin panel to manage inventory
- Monitor orders in real-time
- Test checkout process with Razorpay sandbox first
- Keep backups of your database
- Monitor server performance

---

## 📞 Support Resources

- Django Documentation: https://docs.djangoproject.com/
- Razorpay Documentation: https://razorpay.com/docs/
- Cloudinary Documentation: https://cloudinary.com/documentation
- Bootstrap Documentation: https://getbootstrap.com/docs/

---

**Happy selling! 🎉**

For questions or issues, refer to the official documentation of each service.
