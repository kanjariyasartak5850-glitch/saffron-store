<<<<<<< HEAD
# 🌾 Saffron Store - Premium E-Commerce Platform

A fully-featured Django e-commerce platform for selling premium Kashmiri saffron with a responsive frontend, shopping cart, and payment integration.

## ✨ Features

### 🛍️ Shopping Experience
- Product catalog with detailed descriptions
- Multiple variants (different weights and prices)
- Shopping cart with session persistence
- Add/remove/update cart items
- Responsive mobile-friendly design

### 👨‍💼 Admin Dashboard
- Manage products and variants
- Track orders in real-time
- Inventory management
- Order status tracking

### 💳 Payment Integration
- Razorpay payment gateway integration
- Support for credit/debit cards and UPI
- Order confirmation system

### 📷 Image Management
- Cloudinary integration for image storage
- Automatic image optimization
- CDN delivery for fast loading

### 📱 Responsive Design
- Bootstrap 5 UI framework
- Mobile-optimized interface
- Touch-friendly navigation

---

## 🚀 Quick Start

### 1. Activate Environment
```bash
cd c:\Users\kanja\OneDrive\Desktop\saffron-store
env\Scripts\activate
```

### 2. Configure Environment Variables
Edit `.env` file with your API keys:
```env
SECRET_KEY=your-secret-key
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Admin Account
```bash
python manage.py createsuperuser
```

### 5. Start Server
```bash
python manage.py runserver
```

### 6. Access
- **Frontend**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
saffron-store/
├── core/                 # Django settings
├── shop/                 # Products app
├── orders/               # Orders app
├── templates/            # HTML templates
├── static/               # CSS, JS
├── .env                  # Environment variables
└── SETUP_GUIDE.md        # Detailed setup guide
```

---

## 🎯 Routes

| URL | Purpose |
|-----|---------|
| `/` | Product listing |
| `/product/<slug>/` | Product details |
| `/cart/` | Shopping cart |
| `/checkout/` | Checkout page |
| `/admin/` | Admin dashboard |

---

## 📦 Dependencies

- Django 6.0.6
- Pillow 12.2.0
- Razorpay 2.0.1
- Cloudinary 1.44.2
- python-dotenv 1.2.2
- psycopg2 2.9.12

---

## 🔐 Security

- Environment variables for sensitive data
- CSRF protection enabled
- Secure password validators
- Session-based cart (no local storage)

---

## 📖 Documentation

See `SETUP_GUIDE.md` for detailed:
- Environment configuration
- API key setup (Razorpay, Cloudinary)
- Product management
- Admin dashboard usage
- Customization guide
- Troubleshooting

---

## 🎨 Customization

Easily customize:
- Store colors in `static/css/style.css`
- Footer and header in `templates/base.html`
- Product display in templates
- Admin interface

---

## 🚢 Production Deployment

Before deploying:
1. Set `DEBUG = False`
2. Configure `ALLOWED_HOSTS`
3. Switch to PostgreSQL database
4. Set up SSL/HTTPS
5. Configure static files serving
6. Set up email backend

---

## 💡 Next Steps

1. Add test products via admin
2. Configure Razorpay test mode
3. Test complete checkout flow
4. Deploy to production server
5. Monitor orders and inventory

---

## 📞 Support

- Django: https://docs.djangoproject.com/
- Razorpay: https://razorpay.com/docs/
- Cloudinary: https://cloudinary.com/documentation/

---

## 📄 License

Personal use license - Use for your own business

---

**Ready to start selling premium saffron! 🌾✨**
=======
