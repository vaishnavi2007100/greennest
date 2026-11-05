GreenNest – Plant E-Commerce Website
About Project

GreenNest is a plant e-commerce website developed using Python and Django. It allows users to explore different types of plants, view product details, add products to their cart and wishlist, and place orders.

The website provides four separate modules: Admin, Manager, Vendor, and User.

Technologies Used
Frontend: HTML, CSS, Bootstrap, JavaScript

Backend: Python, Django

Database: MySQL

Database Connectivity: MySQL Connector

Version Control: Git and GitHub

Main Features

1. Admin Module

Admin Dashboard

Manage Users

Manage Managers and Vendors

Manage Categories and Subcategories

Manage Products

Manage Orders

View Reports and Reviews

2. Manager Module

Manager Dashboard

Manage Categories and Subcategories

Manage Collections

View Products

Manage Orders

Manage Customer Messages

View Reports

3. Vendor Module

Vendor Dashboard

Add and Manage Products

Upload Product Images

Manage Product Stock

View Customer Orders

View Sales Reports

View Product Reviews

4. User Module

User Registration and Login

Browse Plants

View Product Details

Add to Cart

Add to Wishlist

Place Orders

Manage Profile and Address

View Order History

Submit Product Reviews

Project Structure

GreenNest/
│
├── plantcare/
├── store/
│   ├── templates/
│   ├── static/
│   ├── AdminView.py
│   ├── Managerview.py
│   ├── UserView.py
│   ├── Venderview.py
│   ├── views.py
│   └── urls.py
│
├── static/
├── manage.py
├── requirements.txt
└── .gitignore

Installation and Setup
1. Clone Repository

git clone https://github.com/vaishnavi2007100/greennest.git

2. Open Project Folder

cd greennest

3. Create Virtual Environment

py -3.13 -m venv venv

4. Activate Virtual Environment

venv\Scripts\activate

5. Install Required Packages

pip install -r requirements.txt

6. Configure Environment Variables

Create a .env file in the project root and add your own settings:

DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

7. Configure MySQL Database

Start MySQL Server.

Create a database named plant.

Configure MySQL connection details in the project.

Create or import the required database tables.

8. Run the Project

py -3.13 manage.py check

py -3.13 manage.py runserver

Open in browser:

http://127.0.0.1:8000/

Developer

GitHub: vaishnavi2007100

Project Purpose

This project was developed to gain practical experience in full-stack web development using Python, Django, MySQL, HTML, CSS, Bootstrap, and JavaScript.