from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import os

import mysql.connector


# =====================================================
# MYSQL DATABASE CONNECTION
# =====================================================

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="plant",
    port=3306,
    connection_timeout=10
)

cursor = db.cursor()

# =====================================================
# VENDOR DASHBOARD
# =====================================================

def VDashboard(request):

    # -------------------------------------------------
    # VENDOR LOGIN CHECK
    # -------------------------------------------------

    if "vendor" not in request.session:
        return redirect("/login/")

    # -------------------------------------------------
    # VENDOR EMAIL
    # -------------------------------------------------

    vendor_email = request.session["vendor"]

    print("==============================================")
    print("VENDOR DASHBOARD")
    print("LOGGED IN VENDOR:", vendor_email)
    print("==============================================")

    # -------------------------------------------------
    # DEFAULT VALUES
    # -------------------------------------------------

    total_products = 0
    total_orders = 0
    total_sales = 0
    total_reviews = 0

    # -------------------------------------------------
    # TOTAL PRODUCTS
    # -------------------------------------------------

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM product
            WHERE LOWER(TRIM(vendor_email))
                  = LOWER(TRIM(%s))
        """, (vendor_email,))

        row = cursor.fetchone()

        if row:
            total_products = row[0]

    except Exception as e:

        print("Vendor Product Count Error:", e)

    # -------------------------------------------------
    # TOTAL REVIEWS
    # -------------------------------------------------

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM reviews r
            INNER JOIN product p
                ON r.product_id = p.id
            WHERE LOWER(TRIM(p.vendor_email))
                  = LOWER(TRIM(%s))
        """, (vendor_email,))

        row = cursor.fetchone()

        if row:
            total_reviews = row[0]

    except Exception as e:

        print("Vendor Review Count Error:", e)

    # -------------------------------------------------
    # TOTAL ORDERS
    # -------------------------------------------------

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM orders o
            INNER JOIN product p
                ON o.product_id = p.id
            WHERE LOWER(TRIM(p.vendor_email))
                  = LOWER(TRIM(%s))
        """, (vendor_email,))

        row = cursor.fetchone()

        if row:
            total_orders = row[0]

    except Exception as e:

        print("Vendor Order Count Error:", e)

    # -------------------------------------------------
    # TOTAL SALES
    # -------------------------------------------------

    try:

        cursor.execute("""
            SELECT COALESCE(SUM(o.total), 0)
            FROM orders o
            INNER JOIN product p
                ON o.product_id = p.id
            WHERE LOWER(TRIM(p.vendor_email))
                  = LOWER(TRIM(%s))
        """, (vendor_email,))

        row = cursor.fetchone()

        if row:
            total_sales = row[0]

    except Exception as e:

        print("Vendor Sales Error:", e)

    # -------------------------------------------------
    # DEBUG
    # -------------------------------------------------

    print("TOTAL PRODUCTS:", total_products)
    print("TOTAL ORDERS:", total_orders)
    print("TOTAL SALES:", total_sales)
    print("TOTAL REVIEWS:", total_reviews)
    print("==============================================")

    # -------------------------------------------------
    # RENDER
    # -------------------------------------------------

    return render(
        request,
        "store/Vender/VDashboard.html",
        {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_sales": total_sales,
            "total_reviews": total_reviews,
        }
    )


# =====================================================
# VENDOR VIEW PROFILE
# =====================================================

def vviewprofile(request):

    # =================================================
    # VENDOR LOGIN CHECK
    # =================================================

    if "vendor" not in request.session:
        return redirect("/login/")

    # Logged-in vendor email
    email = request.session["vendor"]

    edit_mode = False


    # =================================================
    # POST REQUEST
    # =================================================

    if request.method == "POST":

        action = request.POST.get("action")


        # =============================================
        # EDIT PROFILE
        # =============================================

        if action == "edit":

            edit_mode = True


        # =============================================
        # CANCEL EDIT
        # =============================================

        elif action == "cancel":

            edit_mode = False


        # =============================================
        # SAVE PROFILE
        # =============================================

        elif action == "save":

            name = request.POST.get(
                "name",
                ""
            ).strip()

            new_email = request.POST.get(
                "email",
                ""
            ).strip()


            # =========================================
            # EMPTY CHECK
            # =========================================

            if name == "" or new_email == "":

                messages.error(
                    request,
                    "Name and Email cannot be empty."
                )

                edit_mode = True


            else:

                # =====================================
                # CHECK DUPLICATE EMAIL
                # =====================================

                check_query = """
                    SELECT email
                    FROM register
                    WHERE email = %s
                    AND email != %s
                """

                cursor.execute(
                    check_query,
                    (
                        new_email,
                        email
                    )
                )

                existing = cursor.fetchone()


                if existing:

                    messages.error(
                        request,
                        "This email is already registered."
                    )

                    edit_mode = True


                else:

                    # =================================
                    # UPDATE REGISTER TABLE
                    # =================================

                    update_query = """
                        UPDATE register
                        SET name = %s,
                            email = %s
                        WHERE email = %s
                    """

                    cursor.execute(
                        update_query,
                        (
                            name,
                            new_email,
                            email
                        )
                    )

                    db.commit()


                    # =================================
                    # UPDATE LOGIN TABLE
                    # =================================

                    login_update_query = """
                        UPDATE login
                        SET email = %s
                        WHERE email = %s
                        AND role = 'vendor'
                    """

                    cursor.execute(
                        login_update_query,
                        (
                            new_email,
                            email
                        )
                    )

                    db.commit()


                    # =================================
                    # UPDATE VENDOR SESSION
                    # =================================

                    request.session["vendor"] = new_email


                    messages.success(
                        request,
                        "Vendor profile updated successfully."
                    )


                    return redirect(
                        "/Vender/vviewprofile/"
                    )


    # =================================================
    # GET VENDOR DATA
    # =================================================

    query = """
        SELECT name, email
        FROM register
        WHERE email = %s
    """

    cursor.execute(
        query,
        (
            request.session["vendor"],
        )
    )

    data = cursor.fetchone()


    # =================================================
    # RETURN PROFILE PAGE
    # =================================================

    return render(
        request,
        "store/Vender/vviewprofile.html",
        {
            "vendor_data": data,
            "edit_mode": edit_mode
        }
    )


# =====================================================
# CHANGE PASSWORD
# =====================================================

def vcpassword(request):

    # Vendor login check
    if "vendor" not in request.session:
        return redirect("/login/")


    # IMPORTANT
    # Vendor email session se lena hai
    email = request.session["vendor"]


    # =================================================
    # POST REQUEST
    # =================================================

    if request.method == "POST":

        old_password = request.POST.get(
            "old_password",
            ""
        ).strip()


        new_password = request.POST.get(
            "new_password",
            ""
        ).strip()


        confirm_password = request.POST.get(
            "confirm_password",
            ""
        ).strip()


        # =============================================
        # CHECK EMPTY FIELDS
        # =============================================

        if (
            old_password == ""
            or new_password == ""
            or confirm_password == ""
        ):

            messages.error(
                request,
                "All password fields are required."
            )

            return render(
                request,
                "store/Vender/vcpassword.html"
            )


        # =============================================
        # GET CURRENT PASSWORD
        # =============================================

        query = """
            SELECT password
            FROM register
            WHERE email = %s
        """

        cursor.execute(
            query,
            (
                email,
            )
        )

        user_data = cursor.fetchone()


        # =============================================
        # USER NOT FOUND
        # =============================================

        if not user_data:

            messages.error(
                request,
                "Vendor account not found."
            )

            return render(
                request,
                "store/Vender/vcpassword.html"
            )


        current_password = user_data[0]


        # =============================================
        # CHECK OLD PASSWORD
        # =============================================

        if old_password != current_password:

            messages.error(
                request,
                "Current password is incorrect."
            )

            return render(
                request,
                "store/Vender/vcpassword.html"
            )


        # =============================================
        # CHECK NEW PASSWORD
        # =============================================

        if new_password != confirm_password:

            messages.error(
                request,
                "New password and confirm password do not match."
            )

            return render(
                request,
                "store/Vender/vcpassword.html"
            )


        # =============================================
        # PASSWORD LENGTH
        # =============================================

        if len(new_password) < 6:

            messages.error(
                request,
                "Password must be at least 6 characters."
            )

            return render(
                request,
                "store/Vender/vcpassword.html"
            )


        # =============================================
        # OLD & NEW SAME
        # =============================================

        if old_password == new_password:

            messages.error(
                request,
                "New password must be different from old password."
            )

            return render(
                request,
                "store/Vender/vcpassword.html"
            )


        # =============================================
        # UPDATE PASSWORD IN REGISTER
        # =============================================

        update_query = """
            UPDATE register
            SET password = %s
            WHERE email = %s
        """

        cursor.execute(
            update_query,
            (
                new_password,
                email
            )
        )

        db.commit()


        # =============================================
        # UPDATE PASSWORD IN LOGIN
        # =============================================

        login_password_query = """
            UPDATE login
            SET password = %s
            WHERE email = %s
            AND role = 'vendor'
        """

        cursor.execute(
            login_password_query,
            (
                new_password,
                email
            )
        )

        db.commit()


        # =============================================
        # SUCCESS
        # =============================================

        messages.success(
            request,
            "Password changed successfully."
        )


        return redirect(
            "/Vender/vcpassword/"
        )


    # =================================================
    # GET REQUEST
    # =================================================

    return render(
        request,
        "store/Vender/vcpassword.html"
    )


# =====================================================
# ADD PRODUCT
# =====================================================
def AddProduct(request):

    # Vendor login check
    if "vendor" not in request.session:
        return redirect("/login/")

    vendor_email = request.session["vendor"]

    # =====================================================
    # GET CATEGORIES
    # =====================================================

    cursor.execute("""
        SELECT
            id,
            category_name
        FROM category
        WHERE LOWER(TRIM(status)) = 'active'
        ORDER BY id ASC
    """)

    category_rows = cursor.fetchall()

    categories = []

    for row in category_rows:

        category_name = row[1]

        # =================================================
        # CATEGORY NAME MAPPING
        # =================================================

        if category_name == "Indoor Plants":
            product_category = "Indoor Plant"

        elif category_name == "Outdoor Plants":
            product_category = "Outdoor Plant"

        elif category_name == "Flower Plants":
            product_category = "Flower Plant"

        else:
            product_category = category_name

        categories.append({
            "id": row[0],
            "category_name": product_category
        })

    # =====================================================
    # GET COLLECTIONS
    # =====================================================

    cursor.execute("""
        SELECT
            id,
            collection_name
        FROM collection
        WHERE LOWER(TRIM(status)) = 'active'
        ORDER BY id ASC
    """)

    collection_rows = cursor.fetchall()

    collections = []

    for row in collection_rows:

        collections.append({
            "id": row[0],
            "collection_name": row[1]
        })

    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        category = request.POST.get(
            "category",
            ""
        ).strip()

        subcategory = request.POST.get(
            "subcategory",
            ""
        ).strip()

        collection_id = request.POST.get(
            "collection_id",
            ""
        ).strip()

        price = request.POST.get(
            "price",
            ""
        ).strip()

        old_price = request.POST.get(
            "old_price",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        stock = request.POST.get(
            "stock",
            "0"
        ).strip()

        image = request.FILES.get("image")

        # =================================================
        # VALIDATION
        # =================================================

        if name == "":
            messages.error(
                request,
                "Product name is required."
            )
            return redirect("/Vender/AddProduct/")

        if category == "":
            messages.error(
                request,
                "Please select category."
            )
            return redirect("/Vender/AddProduct/")

        if subcategory == "":
            messages.error(
                request,
                "Please enter subcategory."
            )
            return redirect("/Vender/AddProduct/")

        if collection_id == "":
            messages.error(
                request,
                "Please select collection."
            )
            return redirect("/Vender/AddProduct/")

        if price == "":
            messages.error(
                request,
                "Price is required."
            )
            return redirect("/Vender/AddProduct/")

        if image is None:
            messages.error(
                request,
                "Please select product image."
            )
            return redirect("/Vender/AddProduct/")

        if old_price == "":
            old_price = None

        if stock == "":
            stock = 0

        # =================================================
        # SAVE IMAGE
        # =================================================

        product_folder = os.path.join(
            settings.BASE_DIR,
            "static",
            "product_images"
        )

        os.makedirs(
            product_folder,
            exist_ok=True
        )

        image_name = image.name

        image_path = os.path.join(
            product_folder,
            image_name
        )

        with open(
            image_path,
            "wb+"
        ) as destination:

            for chunk in image.chunks():
                destination.write(chunk)

        # =================================================
        # INSERT PRODUCT
        # =================================================

        query = """
            INSERT INTO product
            (
                vendor_email,
                name,
                category,
                subcategory,
                collection_id,
                price,
                old_price,
                image,
                description,
                stock,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        values = (
            vendor_email,
            name,
            category,
            subcategory,
            collection_id,
            price,
            old_price,
            image_name,
            description,
            stock,
            "active"
        )

        cursor.execute(
            query,
            values
        )

        db.commit()

        messages.success(
            request,
            "Product added successfully."
        )

        return redirect(
            "/Vender/MyProducts/"
        )

    # =====================================================
    # PAGE
    # =====================================================

    return render(
        request,
        "store/Vender/AddProduct.html",
        {
            "categories": categories,
            "collections": collections
        }
    )

# =====================================================
# MY PRODUCTS
# =====================================================
def vproducts(request):

    # =====================================================
    # VENDOR LOGIN CHECK
    # =====================================================

    if "vendor" not in request.session:
        return redirect("/login/")

    vendor_email = request.session.get("vendor")

    print("==============================================")
    print("LOGGED IN VENDOR:", vendor_email)
    print("==============================================")


    # =====================================================
    # GET VENDOR PRODUCTS
    # =====================================================

    query = """
        SELECT
            id,
            name,
            category,
            subcategory,
            price,
            old_price,
            image,
            description,
            stock,
            status
        FROM product
        WHERE LOWER(TRIM(vendor_email)) = LOWER(TRIM(%s))
        ORDER BY id DESC
    """

    cursor.execute(query, (vendor_email,))

    product_rows = cursor.fetchall()


    # =====================================================
    # CONVERT DATA
    # =====================================================

    products = []

    for item in product_rows:

        products.append({
            "id": item[0],
            "name": item[1],
            "category": item[2] if item[2] else "No Category",
            "subcategory": item[3] if item[3] else "No Subcategory",
            "price": item[4],
            "old_price": item[5],
            "image": item[6],
            "description": item[7],
            "stock": item[8],
            "status": item[9],

            "image_url":
                "/static/product_images/" + item[6]
                if item[6]
                else ""
        })


    print("TOTAL PRODUCTS:", len(products))

    for product in products:
        print(
            "PRODUCT:",
            product["id"],
            product["name"],
            product["category"],
            product["subcategory"]
        )


    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "store/Vender/vproducts.html",
        {
            "products": products,
            "total_products": len(products)
        }
    )
# =====================================================
# DELETE PRODUCT
# =====================================================

def DeleteProduct(request, id):

    # Vendor login check
    if "vendor" not in request.session:
        return redirect("/login/")

    # Logged-in vendor email
    vendor_email = request.session["vendor"]


    # =================================================
    # GET PRODUCT IMAGE
    # =================================================

    select_query = """
        SELECT image
        FROM product
        WHERE id = %s
        AND vendor_email = %s
    """

    cursor.execute(
        select_query,
        (
            id,
            vendor_email
        )
    )

    product = cursor.fetchone()


    # =================================================
    # PRODUCT NOT FOUND
    # =================================================

    if not product:

        messages.error(
            request,
            "Product not found."
        )

        return redirect("/Vender/MyProducts/")


    image_name = product[0]


    # =================================================
    # DELETE PRODUCT
    # =================================================

    delete_query = """
        DELETE FROM product
        WHERE id = %s
        AND vendor_email = %s
    """

    cursor.execute(
        delete_query,
        (
            id,
            vendor_email
        )
    )

    db.commit()


    # =================================================
    # DELETE IMAGE FROM STATIC FOLDER
    # =================================================

    if image_name:

        image_path = os.path.join(
            settings.BASE_DIR,
            "static",
            "product_images",
            image_name
        )

        if os.path.exists(image_path):

            os.remove(image_path)


    # =================================================
    # SUCCESS MESSAGE
    # =================================================

    messages.success(
        request,
        "Product deleted successfully."
    )


    # =================================================
    # BACK TO MY PRODUCTS
    # =================================================

    return redirect("/Vender/MyProducts/")

def vorders(request):

    if "vendor" not in request.session:
        return redirect("/login/")

    vendor_email = request.session["vendor"]

    orders = []

    try:

        cursor.execute("""
            SELECT
                o.id,
                o.user_email,
                COALESCE(
                    NULLIF(TRIM(o.vendor_email), ''),
                    p.vendor_email
                ) AS vendor_email,
                o.product_id,
                o.product_name,
                o.price,
                o.image,
                o.quantity,
                o.total,
                o.status,
                o.cancel_reason,
                o.payment_method,
                o.created_at,

                r.name,
                r.email,
                r.mobile,

                COALESCE(
                    NULLIF(r.address, ''),
                    ua.address,
                    ''
                ) AS address,

                COALESCE(
                    NULLIF(r.city, ''),
                    ua.city,
                    ''
                ) AS city,

                COALESCE(
                    NULLIF(r.state, ''),
                    ua.state,
                    ''
                ) AS state,

                COALESCE(
                    NULLIF(r.pincode, ''),
                    ua.pincode,
                    ''
                ) AS pincode

            FROM orders o

            LEFT JOIN product p
                ON p.id = o.product_id

            LEFT JOIN register r
                ON r.email = o.user_email

            LEFT JOIN user_address ua
                ON ua.email = o.user_email

            WHERE LOWER(TRIM(
                COALESCE(
                    NULLIF(TRIM(o.vendor_email), ''),
                    p.vendor_email
                )
            )) = LOWER(TRIM(%s))

            ORDER BY o.id DESC
        """, (vendor_email,))

        rows = cursor.fetchall()

        for row in rows:

            orders.append({
                "id": row[0],
                "user_email": row[1],
                "vendor_email": row[2],
                "product_id": row[3],
                "product_name": row[4],
                "price": row[5],
                "image": row[6],
                "quantity": row[7],
                "total": row[8],
                "status": row[9],
                "cancel_reason": row[10],
                "payment_method": row[11],
                "created_at": row[12],

                # USER DETAILS
                "customer_name": row[13],
                "customer_email": row[14],
                "mobile": row[15],
                "address": row[16],
                "city": row[17],
                "state": row[18],
                "pincode": row[19],

                "image_url": (
                    "/static/product_images/" + row[6]
                    if row[6]
                    else ""
                )
            })

    except Exception as e:

        print("VORDERS ERROR:", e)

    context = {
        "orders": orders,
        "total_orders": len(orders)
    }

    return render(
        request,
        "store/Vender/vorders.html",
        context
    )
# =====================================================
# APPROVE ORDER
# =====================================================

def ApproveOrder(request, order_id):

    if "vendor" not in request.session:
        return redirect("/login/")

    vendor_email = request.session["vendor"]

    try:

        cursor.execute("""
            UPDATE orders
            SET status = 'Approved'
            WHERE id = %s
              AND LOWER(TRIM(vendor_email))
                  = LOWER(TRIM(%s))
              AND status = 'Pending'
        """, (
            order_id,
            vendor_email
        ))

        db.commit()

        if cursor.rowcount > 0:
            messages.success(
                request,
                "Order approved successfully."
            )
        else:
            messages.error(
                request,
                "Order not found or already processed."
            )

    except Exception as e:

        print("APPROVE ORDER ERROR:", e)

        db.rollback()

        messages.error(
            request,
            "Unable to approve order."
        )

    return redirect("/Vender/vorders/")


# =====================================================
# SHIP ORDER
# =====================================================

def ShipOrder(request, order_id):

    if "vendor" not in request.session:
        return redirect("/login/")

    vendor_email = request.session["vendor"]

    try:

        cursor.execute("""
            UPDATE orders
            SET status = 'Shipped'
            WHERE id = %s
              AND LOWER(TRIM(vendor_email))
                  = LOWER(TRIM(%s))
              AND status = 'Approved'
        """, (
            order_id,
            vendor_email
        ))

        db.commit()

        if cursor.rowcount > 0:
            messages.success(
                request,
                "Order marked as shipped."
            )
        else:
            messages.error(
                request,
                "Order cannot be shipped."
            )

    except Exception as e:

        print("SHIP ORDER ERROR:", e)

        db.rollback()

        messages.error(
            request,
            "Unable to update order."
        )

    return redirect("/Vender/vorders/")


# =====================================================
# DELIVER ORDER
# =====================================================

def DeliverOrder(request, order_id):

    if "vendor" not in request.session:
        return redirect("/login/")

    vendor_email = request.session["vendor"]

    try:

        cursor.execute("""
            UPDATE orders
            SET status = 'Delivered'
            WHERE id = %s
              AND LOWER(TRIM(vendor_email))
                  = LOWER(TRIM(%s))
              AND status = 'Shipped'
        """, (
            order_id,
            vendor_email
        ))

        db.commit()

        if cursor.rowcount > 0:
            messages.success(
                request,
                "Order marked as delivered."
            )
        else:
            messages.error(
                request,
                "Order cannot be marked as delivered."
            )

    except Exception as e:

        print("DELIVER ORDER ERROR:", e)

        db.rollback()

        messages.error(
            request,
            "Unable to update order."
        )

    return redirect("/Vender/vorders/")

# =====================================================
# VENDOR SALES
# =====================================================

def vsales(request):

    if "vendor" not in request.session:
        return redirect("/login/")


    return render(
        request,
        "store/Vender/vsales.html"
    )


# =====================================================
# VENDOR LOGOUT
# =====================================================

def logout(request):

    # Session completely clear
    request.session.flush()


    # Login page par bhejo
    return redirect("/login/")
# =====================================================
# VENDOR SALES REPORT
# =====================================================

def SalesReport(request):

    # Check vendor login
    if "vendor" not in request.session:
        return redirect("login")

    # Logged-in vendor email
    vendor_email = request.session["vendor"]

    # Get vendor sales
    cmd = """
        SELECT
            o.id,
            o.user_email,
            o.product_id,
            o.product_name,
            o.price,
            o.quantity,
            o.total,
            o.status,
            o.created_at
        FROM orders o
        INNER JOIN product p
            ON o.product_id = p.id
        WHERE p.vendor_email = %s
        ORDER BY o.id DESC
    """

    cursor.execute(cmd, (vendor_email,))
    sales = cursor.fetchall()

    # Total Orders
    total_orders = len(sales)

    # Total Products Sold
    products_sold = 0

    # Total Sales
    total_sales = 0

    for sale in sales:
        products_sold += sale[5]
        total_sales += float(sale[6])

    context = {
        "sales": sales,
        "total_orders": total_orders,
        "products_sold": products_sold,
        "total_sales": total_sales,
    }

    return render(
        request,
        "store/Vender/SalesReport.html",
        context
    )

def VendorReviews(request):

    if "vendor" not in request.session:
        return redirect("/login/")

    vendor_email = request.session["vendor"]

    print("====================================")
    print("VENDOR EMAIL:", vendor_email)
    print("====================================")

    reviews = []

    try:

        # -------------------------------------------------
        # STEP 1: CURRENT VENDOR KE PRODUCTS
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                id,
                name,
                vendor_email
            FROM product
            WHERE LOWER(TRIM(vendor_email))
                  = LOWER(TRIM(%s))
            ORDER BY id DESC
        """, (vendor_email,))

        vendor_products = cursor.fetchall()

        print("VENDOR PRODUCTS:")
        print(vendor_products)


        # -------------------------------------------------
        # STEP 2: REVIEWS OF THESE PRODUCTS
        # -------------------------------------------------

        cursor.execute("""
            SELECT
                r.id,
                r.product_id,
                r.user_name,
                r.user_email,
                r.rating,
                r.review_text,
                r.created_at,
                p.name
            FROM reviews r
            INNER JOIN product p
                ON r.product_id = p.id
            WHERE LOWER(TRIM(p.vendor_email))
                  = LOWER(TRIM(%s))
            ORDER BY r.created_at DESC
        """, (vendor_email,))

        review_rows = cursor.fetchall()

        print("VENDOR REVIEWS:")
        print(review_rows)


        # -------------------------------------------------
        # STEP 3: CONVERT DATA
        # -------------------------------------------------

        for row in review_rows:

            reviews.append({

                "id": row[0],

                "product_id": row[1],

                "user_name": row[2],

                "user_email": row[3],

                "rating": row[4],

                "review_text": row[5],

                "created_at": row[6],

                "product_name": row[7]

            })


    except Exception as e:

        print("VENDOR REVIEWS ERROR:", e)


    return render(
        request,
        "store/Vender/VendorReviews.html",
        {
            "reviews": reviews,
            "total_reviews": len(reviews)
        }
    )
# =====================================================
# CANCEL ORDER
# =====================================================

def CancelOrder(request, order_id):

    if "vendor" not in request.session:
        return redirect("/login/")

    vendor_email = request.session["vendor"]

    try:

        cursor.execute("""
            UPDATE orders
            SET status = 'Cancelled'
            WHERE id = %s
              AND LOWER(TRIM(vendor_email))
                  = LOWER(TRIM(%s))
              AND status IN ('Pending', 'Approved')
        """, (
            order_id,
            vendor_email
        ))

        db.commit()

        if cursor.rowcount > 0:

            messages.success(
                request,
                "Order cancelled successfully."
            )

        else:

            messages.error(
                request,
                "Order cannot be cancelled."
            )

    except Exception as e:

        print("CANCEL ORDER ERROR:", e)

        db.rollback()

        messages.error(
            request,
            "Unable to cancel order."
        )

    return redirect("/Vender/vorders/")