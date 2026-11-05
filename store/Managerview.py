from django.shortcuts import render, redirect
from django.contrib import messages
import os
from django.conf import settings
import mysql.connector


# ========================================================
# DATABASE CONNECTION
# ========================================================

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="plant",
    port=3306,
    connection_timeout=10
)

cursor = db.cursor()



# ========================================================
# MANAGER DASHBOARD
# ========================================================

def MDashboard(request):

    # ====================================================
    # MANAGER LOGIN CHECK
    # ====================================================

    if "manager" not in request.session:
        return redirect("/login/")

    email = request.session["manager"]


    # ====================================================
    # TOTAL USERS
    # ====================================================

    cmd = """
        SELECT COUNT(*)
        FROM register
    """

    cursor.execute(cmd)

    user_count = cursor.fetchone()[0]


    # ====================================================
    # TOTAL VENDORS
    # ====================================================

    cmd = """
        SELECT COUNT(*)
        FROM login
        WHERE LOWER(TRIM(role)) = 'vendor'
    """

    cursor.execute(cmd)

    vendor_count = cursor.fetchone()[0]


    # ====================================================
    # TOTAL CATEGORIES
    # ====================================================

    cmd = """
        SELECT COUNT(*)
        FROM category
    """

    cursor.execute(cmd)

    category_count = cursor.fetchone()[0]


    # ====================================================
    # TOTAL SUBCATEGORIES
    # ====================================================

    cmd = """
        SELECT COUNT(*)
        FROM subcategory
    """

    cursor.execute(cmd)

    subcategory_count = cursor.fetchone()[0]


    # ====================================================
    # TOTAL COLLECTIONS
    # ====================================================

    cmd = """
        SELECT COUNT(*)
        FROM collection
    """

    cursor.execute(cmd)

    collection_count = cursor.fetchone()[0]


    # ====================================================
    # DASHBOARD CONTEXT
    # ====================================================

    context = {

        "manager_email": email,

        "user_count": user_count,

        "vendor_count": vendor_count,

        "category_count": category_count,

        "subcategory_count": subcategory_count,

        "collection_count": collection_count

    }


    # ====================================================
    # RENDER DASHBOARD
    # ====================================================

    return render(
        request,
        "store/Manager/MDashboard.html",
        context
    )


# ========================================================
# MANAGER PROFILE
# ========================================================
# ========================================================
# MANAGER PROFILE
# ========================================================

def mviewprofile(request):

    # ====================================================
    # MANAGER LOGIN CHECK
    # ====================================================

    if "manager" not in request.session:
        return redirect("/login/")

    email = request.session["manager"]

    # ====================================================
    # EDIT PROFILE
    # ====================================================

    if request.method == "POST" and request.POST.get("action") == "edit":

        cmd = """
            SELECT
                name,
                email,
                mobile
            FROM register
            WHERE email = %s
            LIMIT 1
        """

        cursor.execute(
            cmd,
            (email,)
        )

        row = cursor.fetchone()

        # ------------------------------------------------
        # MANAGER REGISTER TABLE MEIN NA HO
        # ------------------------------------------------

        if row:

            manager = {
                "name": row[0] or "",
                "email": row[1] or email,
                "mobile": row[2] or ""
            }

        else:

            # Login table se email lo
            manager = {
                "name": "Manager",
                "email": email,
                "mobile": ""
            }

        return render(
            request,
            "store/Manager/mviewprofile.html",
            {
                "manager": manager,
                "edit_mode": True
            }
        )
        

    # ====================================================
    # SAVE PROFILE
    # ====================================================

    if request.method == "POST" and request.POST.get("action") == "save":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        new_email = request.POST.get(
            "email",
            ""
        ).strip()

        mobile = request.POST.get(
            "mobile",
            ""
        ).strip()

        manager = {
            "name": name,
            "email": new_email,
            "mobile": mobile
        }

        # =================================================
        # VALIDATION
        # =================================================

        if name == "" or new_email == "":

            return render(
                request,
                "store/Manager/mviewprofile.html",
                {
                    "manager": manager,
                    "edit_mode": True,
                    "error": "Name and Email are required."
                }
            )

        # =================================================
        # CHECK EMAIL IN LOGIN TABLE
        # =================================================

        cmd = """
            SELECT email
            FROM login
            WHERE email = %s
            AND email != %s
            LIMIT 1
        """

        cursor.execute(
            cmd,
            (
                new_email,
                email
            )
        )

        existing_email = cursor.fetchone()

        if existing_email:

            return render(
                request,
                "store/Manager/mviewprofile.html",
                {
                    "manager": manager,
                    "edit_mode": True,
                    "error": "This email is already registered."
                }
            )

        # =================================================
        # CHECK REGISTER RECORD
        # =================================================

        cmd = """
            SELECT id
            FROM register
            WHERE email = %s
            LIMIT 1
        """

        cursor.execute(
            cmd,
            (email,)
        )

        register_row = cursor.fetchone()

        # =================================================
        # UPDATE REGISTER IF EXISTS
        # =================================================

        if register_row:

            cmd = """
                UPDATE register
                SET
                    name = %s,
                    email = %s,
                    mobile = %s
                WHERE email = %s
            """

            cursor.execute(
                cmd,
                (
                    name,
                    new_email,
                    mobile,
                    email
                )
            )

        # =================================================
        # UPDATE LOGIN TABLE
        # =================================================

        cmd = """
            UPDATE login
            SET
                email = %s
            WHERE email = %s
            AND LOWER(TRIM(role)) = 'manager'
        """

        cursor.execute(
            cmd,
            (
                new_email,
                email
            )
        )

        db.commit()

        # =================================================
        # UPDATE MANAGER SESSION
        # =================================================

        request.session["manager"] = new_email

        request.session.save()

        return redirect(
            "/Manager/mviewprofile/"
        )

    # ====================================================
    # CANCEL EDIT
    # ====================================================

    if request.method == "POST" and request.POST.get("action") == "cancel":

        return redirect(
            "/Manager/mviewprofile/"
        )

    # ====================================================
    # VIEW PROFILE
    # ====================================================

    cmd = """
        SELECT
            name,
            email,
            mobile
        FROM register
        WHERE email = %s
        LIMIT 1
    """

    cursor.execute(
        cmd,
        (email,)
    )

    row = cursor.fetchone()

    # ====================================================
    # REGISTER TABLE MEIN MANAGER MIL GAYA
    # ====================================================

    if row:

        manager = {
            "name": row[0] or "",
            "email": row[1] or email,
            "mobile": row[2] or ""
        }

    # ====================================================
    # REGISTER TABLE MEIN MANAGER NAHI HAI
    # ====================================================

    else:

        manager = {
            "name": "Manager",
            "email": email,
            "mobile": ""
        }

    # ====================================================
    # RENDER PROFILE
    # ====================================================

    return render(
        request,
        "store/Manager/mviewprofile.html",
        {
            "manager": manager,
            "edit_mode": False
        }
    )

# ============================================================
# MANAGER REPORTS
# ============================================================
def Mreports(request):

    # =========================================================
    # MANAGER LOGIN CHECK
    # =========================================================

    if "manager" not in request.session:
        return redirect("/login/")


    # =========================================================
    # DEFAULT VALUES
    # =========================================================

    user_count = 0
    vendor_count = 0
    category_count = 0
    subcategory_count = 0
    collection_count = 0
    product_count = 0
    order_count = 0


    # =========================================================
    # TOTAL USERS
    # =========================================================

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM register
        """)

        user_count = cursor.fetchone()[0]

    except Exception as e:

        print("Report User Count Error:", e)


    # =========================================================
    # TOTAL VENDORS
    # =========================================================

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM login
            WHERE LOWER(TRIM(role)) = 'vendor'
        """)

        vendor_count = cursor.fetchone()[0]

    except Exception as e:

        print("Report Vendor Count Error:", e)


    # =========================================================
    # TOTAL CATEGORIES
    # =========================================================

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM category
        """)

        category_count = cursor.fetchone()[0]

    except Exception as e:

        print("Report Category Count Error:", e)


    # =========================================================
    # TOTAL SUBCATEGORIES
    # =========================================================

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM subcategory
        """)

        subcategory_count = cursor.fetchone()[0]

    except Exception as e:

        print("Report Subcategory Count Error:", e)


    # =========================================================
    # TOTAL COLLECTIONS
    # =========================================================

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM collection
        """)

        collection_count = cursor.fetchone()[0]

    except Exception as e:

        print("Report Collection Count Error:", e)


    # =========================================================
    # TOTAL PRODUCTS
    # =========================================================

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM product
        """)

        product_count = cursor.fetchone()[0]

    except Exception as e:

        print("Report Product Count Error:", e)


    # =========================================================
    # TOTAL ORDERS
    # =========================================================

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM orders
        """)

        order_count = cursor.fetchone()[0]

    except Exception as e:

        print("Report Order Count Error:", e)


    # =========================================================
    # CONTEXT
    # =========================================================

    context = {

        "user_count": user_count,

        "vendor_count": vendor_count,

        "category_count": category_count,

        "subcategory_count": subcategory_count,

        "collection_count": collection_count,

        "product_count": product_count,

        "order_count": order_count,

    }


    # =========================================================
    # RENDER
    # =========================================================

    return render(
        request,
        "store/Manager/Mreports.html",
        context
    )

# =========================================================
# MANAGER ORDER LIST
# =========================================================

def Orderlist(request):

    # =====================================================
    # MANAGER LOGIN CHECK
    # =====================================================

    if "manager" not in request.session:
        return redirect("/login/")


    orders = []


    try:

        # =================================================
        # GET ORDERS
        # =================================================
        #
        # orders
        #     ↓
        # product
        #     ↓
        # register
        #     ↓
        # user_address
        #
        # Isse manager ko customer + product + vendor
        # ki details milengi.
        # =================================================

        cursor.execute(
            """
            SELECT

                o.id,
                o.user_email,
                o.product_id,
                o.product_name,
                o.price,
                o.image,
                o.quantity,
                o.total,
                o.status,
                o.created_at,

                /* CUSTOMER DETAILS */

                r.name,
                r.email,
                r.mobile,

                /* ADDRESS */

                ua.address,
                ua.city,
                ua.state,
                ua.pincode,

                /* VENDOR */

                p.vendor_email,

                /* CANCEL REASON */

                o.cancel_reason

            FROM orders o

            LEFT JOIN register r
                ON LOWER(TRIM(o.user_email))
                   =
                   LOWER(TRIM(r.email))

            LEFT JOIN user_address ua
                ON LOWER(TRIM(o.user_email))
                   =
                   LOWER(TRIM(ua.email))

            LEFT JOIN product p
                ON o.product_id = p.id

            ORDER BY
                o.created_at DESC,
                o.id DESC
            """
        )


        rows = cursor.fetchall()


        # =================================================
        # CREATE ORDER DICTIONARY
        # =================================================

        for row in rows:

            orders.append({

                # =========================================
                # ORDER DETAILS
                # =========================================

                "id":
                    row[0],

                "user_email":
                    row[1],

                "product_id":
                    row[2],

                "product_name":
                    row[3],

                "price":
                    row[4],

                "image":
                    row[5],

                "quantity":
                    row[6],

                "total":
                    row[7],

                "status":
                    row[8],

                "created_at":
                    row[9],


                # =========================================
                # CUSTOMER DETAILS
                # =========================================

                "customer_name":
                    row[10] or "",

                "customer_email":
                    row[11] or row[1],

                "mobile":
                    row[12] or "",


                # =========================================
                # DELIVERY ADDRESS
                # =========================================

                "address":
                    row[13] or "",

                "city":
                    row[14] or "",

                "state":
                    row[15] or "",

                "pincode":
                    row[16] or "",


                # =========================================
                # VENDOR DETAILS
                # =========================================

                "vendor_email":
                    row[17] or "",

                "vendor_email_display":
                    row[17] or "",

                # Vendor name abhi database me
                # order ke saath available nahi hai.
                # Isliye blank rakha hai.

                "vendor_name":
                    "",


                # =========================================
                # PAYMENT
                # =========================================

                # Current orders INSERT code me
                # payment_method save nahi ho raha.
                # Isliye abhi blank.

                "payment_method":
                    "",


                # =========================================
                # CANCEL REASON
                # =========================================

                "cancel_reason":
                    row[18] or ""

            })


    except Exception as e:

        print(
            "Manager Order List Error:",
            e
        )


    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "store/Manager/Orderlist.html",
        {
            "orders": orders
        }
    )
# ========================================================
# CHANGE PASSWORD
# ========================================================

def cpassword(request):

    if "manager" not in request.session:
        return redirect("/login/")

    email = request.session["manager"]

    message = ""

    # ====================================================
    # POST
    # ====================================================

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

        # =================================================
        # EMPTY FIELD CHECK
        # =================================================

        if (
            old_password == ""
            or new_password == ""
            or confirm_password == ""
        ):

            message = "All password fields are required."

            return render(
                request,
                "store/Manager/cpassword.html",
                {
                    "message": message
                }
            )

        # =================================================
        # CHECK NEW PASSWORD
        # =================================================

        if new_password != confirm_password:

            message = (
                "New password and confirm password "
                "do not match."
            )

            return render(
                request,
                "store/Manager/cpassword.html",
                {
                    "message": message
                }
            )

        # =================================================
        # PASSWORD LENGTH
        # =================================================

        if len(new_password) < 6:

            message = (
                "Password must be at least 6 characters."
            )

            return render(
                request,
                "store/Manager/cpassword.html",
                {
                    "message": message
                }
            )

        # =================================================
        # GET OLD PASSWORD
        # =================================================

        cmd = """
            SELECT password
            FROM login
            WHERE email = %s
            AND role = 'manager'
        """

        cursor.execute(
            cmd,
            (email,)
        )

        row = cursor.fetchone()

        if not row:

            message = "Manager account not found."

            return render(
                request,
                "store/Manager/cpassword.html",
                {
                    "message": message
                }
            )

        # =================================================
        # CHECK OLD PASSWORD
        # =================================================

        if row[0] != old_password:

            message = "Old password is incorrect."

            return render(
                request,
                "store/Manager/cpassword.html",
                {
                    "message": message
                }
            )

        # =================================================
        # CHECK SAME PASSWORD
        # =================================================

        if old_password == new_password:

            message = (
                "New password must be different "
                "from old password."
            )

            return render(
                request,
                "store/Manager/cpassword.html",
                {
                    "message": message
                }
            )

        # =================================================
        # UPDATE LOGIN PASSWORD
        # =================================================

        cmd = """
            UPDATE login
            SET password = %s
            WHERE email = %s
            AND role = 'manager'
        """

        cursor.execute(
            cmd,
            (
                new_password,
                email
            )
        )

        # =================================================
        # UPDATE REGISTER PASSWORD
        # =================================================

        cmd = """
            UPDATE register
            SET password = %s
            WHERE email = %s
        """

        cursor.execute(
            cmd,
            (
                new_password,
                email
            )
        )

        db.commit()

        message = "Password changed successfully."

    # ====================================================
    # PAGE
    # ====================================================

    return render(
        request,
        "store/Manager/cpassword.html",
        {
            "message": message
        }
    )


# ========================================================
# ADD CATEGORY
# ========================================================

def Addcategory(request):

    if "manager" not in request.session:
        return redirect("/login/")

    if request.method == "POST":

        category_name = request.POST.get(
            "category_name",
            ""
        ).strip()

        category_type = request.POST.get(
            "category_type",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            ""
        ).strip()

        if status == "":
            status = "Active"

        cmd = """
            INSERT INTO category
            (
                category_name,
                category_type,
                description,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """

        cursor.execute(
            cmd,
            (
                category_name,
                category_type,
                description,
                status
            )
        )

        db.commit()

        messages.success(
            request,
            "Category added successfully."
        )

        return redirect(
            "/Manager/Categorylist/"
        )

    return render(
        request,
        "store/Manager/Addcategory.html"
    )


# ========================================================
# CATEGORY LIST
# ========================================================

def Categorylist(request):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        SELECT
            id,
            category_name,
            category_type,
            description,
            status
        FROM category
        ORDER BY id DESC
    """

    cursor.execute(cmd)

    rows = cursor.fetchall()

    categories = []

    for row in rows:

        categories.append({
            "id": row[0],
            "category_name": row[1],
            "category_type": row[2],
            "description": row[3],
            "status": row[4]
        })

    return render(
        request,
        "store/Manager/Categorylist.html",
        {
            "categories": categories
        }
    )


# ========================================================
# EDIT CATEGORY
# ========================================================
def Editcategorylist(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    # =========================================================
    # POST - UPDATE CATEGORY
    # =========================================================

    if request.method == "POST":

        category_name = request.POST.get(
            "category_name",
            ""
        ).strip()

        category_type = request.POST.get(
            "category_type",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            ""
        ).strip()

        if status == "":
            status = "Active"

        cmd = """
            UPDATE category
            SET
                category_name = %s,
                category_type = %s,
                description = %s,
                status = %s
            WHERE id = %s
        """

        cursor.execute(
            cmd,
            (
                category_name,
                category_type,
                description,
                status,
                id
            )
        )

        db.commit()

        messages.success(
            request,
            "Category updated successfully."
        )

        # =====================================================
        # IMPORTANT:
        # After update go to Category List
        # =====================================================

        return redirect(
            "/Manager/Categorylist/"
        )


    # =========================================================
    # GET - LOAD CATEGORY
    # =========================================================

    cmd = """
        SELECT
            id,
            category_name,
            category_type,
            description,
            status
        FROM category
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    row = cursor.fetchone()


    # =========================================================
    # CATEGORY NOT FOUND
    # =========================================================

    if not row:

        messages.error(
            request,
            "Category not found."
        )

        return redirect(
            "/Manager/Categorylist/"
        )


    # =========================================================
    # CONVERT TUPLE TO DICTIONARY
    # =========================================================

    category = {
        "id": row[0],
        "category_name": row[1],
        "category_type": row[2],
        "description": row[3],
        "status": row[4]
    }


    return render(
        request,
        "store/Manager/Editcategorylist.html",
        {
            "category": category
        }
    )


# ========================================================
# DELETE CATEGORY
# ========================================================

def Deletecategory(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # CHECK SUBCATEGORIES
    # ====================================================

    cmd = """
        SELECT COUNT(*)
        FROM subcategory
        WHERE category_id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    subcategory_count = cursor.fetchone()[0]

    if subcategory_count > 0:

        messages.error(
            request,
            "This category cannot be deleted because it has subcategories."
        )

        return redirect(
            "/Manager/Categorylist/"
        )

    # ====================================================
    # DELETE
    # ====================================================

    cmd = """
        DELETE FROM category
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    db.commit()

    messages.success(
        request,
        "Category deleted successfully."
    )

    return redirect(
        "/Manager/Categorylist/"
    )


# ========================================================
# ADD SUBCATEGORY
# ========================================================

def Addsubcategory(request):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # GET CATEGORIES
    # ====================================================

    cmd = """
        SELECT
            id,
            category_name
        FROM category
        WHERE LOWER(TRIM(status)) = 'active'
        ORDER BY category_name ASC
    """

    cursor.execute(cmd)

    category_rows = cursor.fetchall()

    categories = []

    for row in category_rows:

        categories.append({
            "id": row[0],
            "category_name": row[1]
        })

    # ====================================================
    # INSERT SUBCATEGORY
    # ====================================================

    if request.method == "POST":

        category_id = request.POST.get(
            "category_id",
            ""
        ).strip()

        subcategory_name = request.POST.get(
            "subcategory_name",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            ""
        ).strip()

        if category_id == "":
            return render(
                request,
                "store/Manager/Addsubcategory.html",
                {
                    "categories": categories,
                    "error": "Please select category."
                }
            )

        if subcategory_name == "":
            return render(
                request,
                "store/Manager/Addsubcategory.html",
                {
                    "categories": categories,
                    "error": "Subcategory name is required."
                }
            )

        if status == "":
            status = "Active"

        cmd = """
            INSERT INTO subcategory
            (
                category_id,
                subcategory_name,
                description,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """

        cursor.execute(
            cmd,
            (
                category_id,
                subcategory_name,
                description,
                status
            )
        )

        db.commit()

        messages.success(
            request,
            "Subcategory added successfully."
        )

        return redirect(
            "/Manager/Subcategorylist/"
        )

    return render(
        request,
        "store/Manager/Addsubcategory.html",
        {
            "categories": categories
        }
    )


# ========================================================
# SUBCATEGORY LIST
# ========================================================

def Subcategorylist(request):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        SELECT
            s.id,
            s.category_id,
            c.category_name,
            s.subcategory_name,
            s.description,
            s.status
        FROM subcategory s
        LEFT JOIN category c
        ON s.category_id = c.id
        ORDER BY s.id DESC
    """

    cursor.execute(cmd)

    rows = cursor.fetchall()

    subcategories = []

    for row in rows:

        subcategories.append({
            "id": row[0],
            "category_id": row[1],
            "category_name": row[2],
            "subcategory_name": row[3],
            "description": row[4],
            "status": row[5]
        })

    return render(
        request,
        "store/Manager/Subcategorylist.html",
        {
            "subcategories": subcategories
        }
    )


# ========================================================
# EDIT SUBCATEGORY
# ========================================================

def Editsubcategory(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # GET CATEGORIES
    # ====================================================

    cmd = """
        SELECT
            id,
            category_name
        FROM category
        ORDER BY category_name ASC
    """

    cursor.execute(cmd)

    category_rows = cursor.fetchall()

    categories = []

    for row in category_rows:

        categories.append({
            "id": row[0],
            "category_name": row[1]
        })

    # ====================================================
    # UPDATE
    # ====================================================

    if request.method == "POST":

        category_id = request.POST.get(
            "category_id",
            ""
        ).strip()

        subcategory_name = request.POST.get(
            "subcategory_name",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            ""
        ).strip()

        if category_id == "":
            return render(
                request,
                "store/Manager/Editsubcategory.html",
                {
                    "subcategory": {
                        "id": id,
                        "category_id": category_id,
                        "subcategory_name": subcategory_name,
                        "description": description,
                        "status": status
                    },
                    "categories": categories,
                    "error": "Please select category."
                }
            )

        if subcategory_name == "":
            return render(
                request,
                "store/Manager/Editsubcategory.html",
                {
                    "subcategory": {
                        "id": id,
                        "category_id": category_id,
                        "subcategory_name": subcategory_name,
                        "description": description,
                        "status": status
                    },
                    "categories": categories,
                    "error": "Subcategory name is required."
                }
            )

        if status == "":
            status = "Active"

        cmd = """
            UPDATE subcategory
            SET
                category_id = %s,
                subcategory_name = %s,
                description = %s,
                status = %s
            WHERE id = %s
        """

        cursor.execute(
            cmd,
            (
                category_id,
                subcategory_name,
                description,
                status,
                id
            )
        )

        db.commit()

        messages.success(
            request,
            "Subcategory updated successfully."
        )

        return redirect(
            "/Manager/Subcategorylist/"
        )

    # ====================================================
    # GET SUBCATEGORY
    # ====================================================

    cmd = """
        SELECT
            id,
            category_id,
            subcategory_name,
            description,
            status
        FROM subcategory
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    row = cursor.fetchone()

    if not row:

        messages.error(
            request,
            "Subcategory not found."
        )

        return redirect(
            "/Manager/Subcategorylist/"
        )

    subcategory = {
        "id": row[0],
        "category_id": row[1],
        "subcategory_name": row[2],
        "description": row[3],
        "status": row[4]
    }

    return render(
        request,
        "store/Manager/Editsubcategory.html",
        {
            "subcategory": subcategory,
            "categories": categories
        }
    )


# ========================================================
# DELETE SUBCATEGORY
# ========================================================

def Deletesubcategory(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        DELETE FROM subcategory
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    db.commit()

    messages.success(
        request,
        "Subcategory deleted successfully."
    )

    return redirect(
        "/Manager/Subcategorylist/"
    )


# ========================================================
# ADD COLLECTION
# ========================================================

def Addcollection(request):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # GET PARENT COLLECTIONS
    # ====================================================

    cmd = """
        SELECT
            id,
            collection_name
        FROM collection
        WHERE parent_id IS NULL
        AND LOWER(TRIM(status)) = 'active'
        ORDER BY collection_name ASC
    """

    cursor.execute(cmd)

    rows = cursor.fetchall()

    parent_collections = []

    for row in rows:

        parent_collections.append({
            "id": row[0],
            "collection_name": row[1]
        })

    # ====================================================
    # SAVE COLLECTION
    # ====================================================

    if request.method == "POST":

        collection_name = request.POST.get(
            "collection_name",
            ""
        ).strip()

        parent_id = request.POST.get(
            "parent_id",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            ""
        ).strip()

        # =================================================
        # VALIDATION
        # =================================================

        if collection_name == "":

            return render(
                request,
                "store/Manager/Addcollection.html",
                {
                    "parent_collections": parent_collections,
                    "error": "Collection name is required."
                }
            )

        # =================================================
        # PARENT ID
        # =================================================

        if parent_id == "":
            parent_id = None

        # =================================================
        # DEFAULT STATUS
        # =================================================

        if status == "":
            status = "Active"

        # =================================================
        # INSERT
        # =================================================

        cmd = """
            INSERT INTO collection
            (
                collection_name,
                parent_id,
                description,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """

        cursor.execute(
            cmd,
            (
                collection_name,
                parent_id,
                description,
                status
            )
        )

        db.commit()

        messages.success(
            request,
            "Collection added successfully."
        )

        return redirect(
            "/Manager/Collectionlist/"
        )

    return render(
        request,
        "store/Manager/Addcollection.html",
        {
            "parent_collections": parent_collections
        }
    )


# ========================================================
# COLLECTION LIST
# ========================================================

def Collectionlist(request):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        SELECT
            c.id,
            c.collection_name,
            c.parent_id,
            p.collection_name,
            c.description,
            c.status
        FROM collection c
        LEFT JOIN collection p
        ON c.parent_id = p.id
        ORDER BY c.id DESC
    """

    cursor.execute(cmd)

    rows = cursor.fetchall()

    collections = []

    for row in rows:

        collections.append({
            "id": row[0],
            "collection_name": row[1],
            "parent_id": row[2],
            "parent_name": row[3],
            "description": row[4],
            "status": row[5]
        })

    return render(
        request,
        "store/Manager/Collectionlist.html",
        {
            "collections": collections
        }
    )


# ========================================================
# EDIT COLLECTION
# ========================================================

def Editcollection(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # GET PARENT COLLECTIONS
    # ====================================================

    cmd = """
        SELECT
            id,
            collection_name
        FROM collection
        WHERE parent_id IS NULL
        AND id != %s
        AND LOWER(TRIM(status)) = 'active'
        ORDER BY collection_name ASC
    """

    cursor.execute(
        cmd,
        (id,)
    )

    rows = cursor.fetchall()

    parent_collections = []

    for row in rows:

        parent_collections.append({
            "id": row[0],
            "collection_name": row[1]
        })

    # ====================================================
    # UPDATE COLLECTION
    # ====================================================

    if request.method == "POST":

        collection_name = request.POST.get(
            "collection_name",
            ""
        ).strip()

        parent_id = request.POST.get(
            "parent_id",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            ""
        ).strip()

        # =================================================
        # VALIDATION
        # =================================================

        if collection_name == "":

            collection = {
                "id": id,
                "collection_name": collection_name,
                "parent_id": parent_id,
                "description": description,
                "status": status
            }

            return render(
                request,
                "store/Manager/Editcollection.html",
                {
                    "collection": collection,
                    "parent_collections": parent_collections,
                    "error": "Collection name is required."
                }
            )

        # =================================================
        # EMPTY PARENT
        # =================================================

        if parent_id == "":
            parent_id = None

        # =================================================
        # DEFAULT STATUS
        # =================================================

        if status == "":
            status = "Active"

        # =================================================
        # PREVENT SELF PARENT
        # =================================================

        if (
            parent_id is not None
            and str(parent_id) == str(id)
        ):

            collection = {
                "id": id,
                "collection_name": collection_name,
                "parent_id": parent_id,
                "description": description,
                "status": status
            }

            return render(
                request,
                "store/Manager/Editcollection.html",
                {
                    "collection": collection,
                    "parent_collections": parent_collections,
                    "error": "A collection cannot be its own parent."
                }
            )

        # =================================================
        # UPDATE
        # =================================================

        cmd = """
            UPDATE collection
            SET
                collection_name = %s,
                parent_id = %s,
                description = %s,
                status = %s
            WHERE id = %s
        """

        cursor.execute(
            cmd,
            (
                collection_name,
                parent_id,
                description,
                status,
                id
            )
        )

        db.commit()

        messages.success(
            request,
            "Collection updated successfully."
        )

        return redirect(
            "/Manager/Collectionlist/"
        )

    # ====================================================
    # GET COLLECTION
    # ====================================================

    cmd = """
        SELECT
            id,
            collection_name,
            parent_id,
            description,
            status
        FROM collection
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    row = cursor.fetchone()

    if not row:

        messages.error(
            request,
            "Collection not found."
        )

        return redirect(
            "/Manager/Collectionlist/"
        )

    collection = {
        "id": row[0],
        "collection_name": row[1],
        "parent_id": row[2],
        "description": row[3],
        "status": row[4]
    }

    return render(
        request,
        "store/Manager/Editcollection.html",
        {
            "collection": collection,
            "parent_collections": parent_collections
        }
    )


# ========================================================
# DELETE COLLECTION
# ========================================================

def Deletecollection(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # CHECK CHILD COLLECTIONS
    # ====================================================

    cmd = """
        SELECT COUNT(*)
        FROM collection
        WHERE parent_id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    child_count = cursor.fetchone()[0]

    if child_count > 0:

        messages.error(
            request,
            "This collection has subcollections. Delete them first."
        )

        return redirect(
            "/Manager/Collectionlist/"
        )

    # ====================================================
    # DELETE
    # ====================================================

    cmd = """
        DELETE FROM collection
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    db.commit()

    messages.success(
        request,
        "Collection deleted successfully."
    )

    return redirect(
        "/Manager/Collectionlist/"
    )


# ========================================================
# USER LIST
# ========================================================

# ========================================================
# USER LIST
# ========================================================

def Userlist(request):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # GET USERS
    # ====================================================

    cmd = """
        SELECT
            id,
            name,
            email,
            mobile,
            status
        FROM register
        ORDER BY id DESC
    """

    cursor.execute(cmd)

    rows = cursor.fetchall()

    users = []

    # ====================================================
    # GET ADDRESS
    # ====================================================

    for row in rows:

        user_id = row[0]
        name = row[1]
        email = row[2]
        mobile = row[3]
        status = row[4]

        address = ""
        city = ""
        state = ""
        pincode = ""

        cmd = """
            SELECT
                address,
                city,
                state,
                pincode
            FROM user_address
            WHERE email = %s
            LIMIT 1
        """

        cursor.execute(
            cmd,
            (email,)
        )

        address_row = cursor.fetchone()

        if address_row:

            address = address_row[0] or ""
            city = address_row[1] or ""
            state = address_row[2] or ""
            pincode = address_row[3] or ""

        users.append({
            "id": user_id,
            "name": name,
            "email": email,
            "mobile": mobile or "",
            "phone": mobile or "",
            "address": address,
            "city": city,
            "state": state,
            "pincode": pincode,
            "status": status or "Active"
        })

    return render(
        request,
        "store/Manager/Userlist.html",
        {
            "users": users
        }
    )


# ========================================================
# BLOCK USER
# ========================================================

def BlockUser(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        UPDATE register
        SET status = 'Blocked'
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    db.commit()

    messages.success(
        request,
        "User blocked successfully."
    )

    return redirect(
        "/Manager/Userlist/"
    )


# ========================================================
# UNBLOCK USER
# ========================================================

def UnblockUser(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        UPDATE register
        SET status = 'Active'
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    db.commit()

    messages.success(
        request,
        "User unblocked successfully."
    )

    return redirect(
        "/Manager/Userlist/"
    )


# ========================================================
# USER DETAIL
# ========================================================

def Userdetail(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # GET USER
    # ====================================================

    cmd = """
        SELECT
            id,
            name,
            email,
            mobile
        FROM register
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    row = cursor.fetchone()

    if not row:

        return redirect(
            "/Manager/Userlist/"
        )

    user_id = row[0]
    name = row[1]
    email = row[2]
    mobile = row[3]

    # ====================================================
    # DEFAULT ADDRESS
    # ====================================================

    address = ""
    city = ""
    state = ""
    pincode = ""

    # ====================================================
    # GET ADDRESS
    # ====================================================

    cmd = """
        SELECT
            address,
            city,
            state,
            pincode
        FROM user_address
        WHERE email = %s
        LIMIT 1
    """

    cursor.execute(
        cmd,
        (email,)
    )

    address_row = cursor.fetchone()

    if address_row:

        address = address_row[0] or ""
        city = address_row[1] or ""
        state = address_row[2] or ""
        pincode = address_row[3] or ""

    # ====================================================
    # USER DICTIONARY
    # ====================================================

    user = {
        "id": user_id,
        "name": name,
        "email": email,
        "mobile": mobile or "",
        "phone": mobile or "",
        "address": address,
        "city": city,
        "state": state,
        "pincode": pincode
    }

    return render(
        request,
        "store/Manager/Userdetail.html",
        {
            "user": user
        }
    )

# ========================================================
# VENDOR LIST
# ========================================================
# ========================================================
# VENDOR LIST
# ========================================================

def Venderlist(request):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        SELECT
            id,
            email,
            role
        FROM login
        WHERE LOWER(TRIM(role)) = 'vendor'
        ORDER BY id DESC
    """

    cursor.execute(cmd)

    rows = cursor.fetchall()

    print("====================================")
    print("VENDOR ROWS:", rows)
    print("====================================")

    vendors = []

    for row in rows:

        vendors.append({
            "id": row[0],
            "email": row[1],
            "role": row[2],
            "name": "Vendor",
            "mobile": ""
        })

    return render(
        request,
        "store/Manager/Venderlist.html",
        {
            "vendors": vendors
        }
    )


# ========================================================
# VENDOR DETAILS
# ========================================================
# ========================================================
# VENDOR DETAILS
# ========================================================

def Venderdetails(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    try:

        cmd = """
            SELECT
                id,
                email,
                role
            FROM login
            WHERE id = %s
            AND LOWER(TRIM(role)) = 'vendor'
        """

        cursor.execute(
            cmd,
            (id,)
        )

        row = cursor.fetchone()

        if not row:

            messages.error(
                request,
                "Vendor not found."
            )

            return redirect(
                "Venderlist"
            )


        vendor_id = row[0]
        email = row[1]
        role = row[2]


        # =================================================
        # GET VENDOR PROFILE
        # =================================================

        cmd2 = """
            SELECT
                COALESCE(NULLIF(TRIM(name), ''), 'Vendor'),
                COALESCE(mobile, '')
            FROM register
            WHERE email = %s
            LIMIT 1
        """

        cursor.execute(
            cmd2,
            (email,)
        )

        register_row = cursor.fetchone()


        if register_row:

            name = register_row[0]
            mobile = register_row[1]

        else:

            name = "Vendor"
            mobile = ""


        vendor = {

            "id": vendor_id,

            "name": name,

            "email": email,

            "mobile": mobile,

            "phone": mobile,

            "role": role

        }


        return render(
            request,
            "store/Manager/Venderdetails.html",
            {
                "vendor": vendor
            }
        )


    except Exception as e:

        print("VENDOR DETAILS ERROR:", e)

        messages.error(
            request,
            "Unable to load vendor details."
        )

        return redirect(
            "Venderlist"
        )

# ========================================================
# MANAGER PRODUCT LIST
# ========================================================

def Productlist(request):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        SELECT
            id,
            vendor_email,
            name,
            category,
            subcategory,
            price,
            old_price,
            image,
            description,
            stock,
            status,
            created_at
        FROM product
        ORDER BY id DESC
    """

    cursor.execute(cmd)

    rows = cursor.fetchall()

    products = []

    for row in rows:

        products.append({
            "id": row[0],
            "vendor_email": row[1],
            "name": row[2],
            "category": row[3],
            "subcategory": row[4],
            "price": row[5],
            "old_price": row[6],
            "image": row[7],
            "description": row[8],
            "stock": row[9],
            "status": row[10],
            "created_at": row[11]
        })

    return render(
        request,
        "store/Manager/Productlist.html",
        {
            "products": products
        }
    )


# ========================================================
# PRODUCT DETAIL
# ========================================================

def Productdetail(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        SELECT
            id,
            vendor_email,
            name,
            category,
            subcategory,
            price,
            old_price,
            image,
            description,
            stock,
            status,
            created_at
        FROM product
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    row = cursor.fetchone()

    if row is None:

        messages.error(
            request,
            "Product not found."
        )

        return redirect(
            "/Manager/Productlist/"
        )

    product = {
        "id": row[0],
        "vendor_email": row[1],
        "name": row[2],
        "category": row[3],
        "subcategory": row[4],
        "price": row[5],
        "old_price": row[6],
        "image": row[7],
        "description": row[8],
        "stock": row[9],
        "status": row[10],
        "created_at": row[11]
    }

    return render(
        request,
        "store/Manager/Productdetail.html",
        {
            "product": product
        }
    )


# ========================================================
# EDIT PRODUCT
# ========================================================

def EditProduct(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # GET CATEGORIES
    # ====================================================

    cmd = """
        SELECT
            id,
            category_name
        FROM category
        WHERE LOWER(TRIM(status)) = 'active'
        ORDER BY category_name ASC
    """

    cursor.execute(cmd)

    category_rows = cursor.fetchall()

    categories = []

    for row in category_rows:

        categories.append({
            "id": row[0],
            "category_name": row[1]
        })

    # ====================================================
    # GET SUBCATEGORIES
    # ====================================================

    cmd = """
        SELECT
            id,
            category_id,
            subcategory_name
        FROM subcategory
        WHERE LOWER(TRIM(status)) = 'active'
        ORDER BY subcategory_name ASC
    """

    cursor.execute(cmd)

    subcategory_rows = cursor.fetchall()

    subcategories = []

    for row in subcategory_rows:

        subcategories.append({
            "id": row[0],
            "category_id": row[1],
            "subcategory_name": row[2]
        })

    # ====================================================
    # GET CURRENT PRODUCT
    # ====================================================

    cmd = """
        SELECT
            id,
            vendor_email,
            name,
            category,
            subcategory,
            price,
            old_price,
            image,
            description,
            stock,
            status,
            created_at
        FROM product
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    row = cursor.fetchone()

    if not row:

        messages.error(
            request,
            "Product not found."
        )

        return redirect(
            "/Manager/Productlist/"
        )

    product = {
        "id": row[0],
        "vendor_email": row[1],
        "name": row[2],
        "category": row[3],
        "subcategory": row[4],
        "price": row[5],
        "old_price": row[6],
        "image": row[7],
        "description": row[8],
        "stock": row[9],
        "status": row[10],
        "created_at": row[11]
    }

    # ====================================================
    # UPDATE PRODUCT
    # ====================================================

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
            ""
        ).strip()

        status = request.POST.get(
            "status",
            ""
        ).strip()

        image = request.FILES.get("image")

        # =================================================
        # VALIDATION
        # =================================================

        if name == "":

            product["name"] = name
            product["category"] = category
            product["subcategory"] = subcategory
            product["price"] = price
            product["old_price"] = old_price
            product["description"] = description
            product["stock"] = stock
            product["status"] = status

            return render(
                request,
                "store/Manager/EditProduct.html",
                {
                    "product": product,
                    "categories": categories,
                    "subcategories": subcategories,
                    "error": "Product name is required."
                }
            )

        # =================================================
        # CATEGORY VALIDATION
        # =================================================

        if category == "":

            product["name"] = name
            product["category"] = category
            product["subcategory"] = subcategory
            product["price"] = price
            product["old_price"] = old_price
            product["description"] = description
            product["stock"] = stock
            product["status"] = status

            return render(
                request,
                "store/Manager/EditProduct.html",
                {
                    "product": product,
                    "categories": categories,
                    "subcategories": subcategories,
                    "error": "Please select category."
                }
            )

        # =================================================
        # PRICE VALIDATION
        # =================================================

        if price == "":

            product["name"] = name
            product["category"] = category
            product["subcategory"] = subcategory
            product["price"] = price
            product["old_price"] = old_price
            product["description"] = description
            product["stock"] = stock
            product["status"] = status

            return render(
                request,
                "store/Manager/EditProduct.html",
                {
                    "product": product,
                    "categories": categories,
                    "subcategories": subcategories,
                    "error": "Price is required."
                }
            )

        # =================================================
        # DEFAULT STOCK
        # =================================================

        if stock == "":
            stock = 0

        # =================================================
        # DEFAULT OLD PRICE
        # =================================================

        if old_price == "":
            old_price = None

        # =================================================
        # IMAGE UPDATE
        # =================================================

        if image:

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

            cmd = """
                UPDATE product
                SET
                    name = %s,
                    category = %s,
                    subcategory = %s,
                    price = %s,
                    old_price = %s,
                    image = %s,
                    description = %s,
                    stock = %s,
                    status = %s
                WHERE id = %s
            """

            cursor.execute(
                cmd,
                (
                    name,
                    category,
                    subcategory,
                    price,
                    old_price,
                    image_name,
                    description,
                    stock,
                    status,
                    id
                )
            )

        else:

            cmd = """
                UPDATE product
                SET
                    name = %s,
                    category = %s,
                    subcategory = %s,
                    price = %s,
                    old_price = %s,
                    description = %s,
                    stock = %s,
                    status = %s
                WHERE id = %s
            """

            cursor.execute(
                cmd,
                (
                    name,
                    category,
                    subcategory,
                    price,
                    old_price,
                    description,
                    stock,
                    status,
                    id
                )
            )

        # =================================================
        # COMMIT
        # =================================================

        db.commit()

        messages.success(
            request,
            "Product updated successfully."
        )

        return redirect(
            "/Manager/Productlist/"
        )

    # ====================================================
    # RENDER EDIT PAGE
    # ====================================================

    return render(
        request,
        "store/Manager/EditProduct.html",
        {
            "product": product,
            "categories": categories,
            "subcategories": subcategories
        }
    )


# ========================================================
# DELETE PRODUCT
# ========================================================

def DeleteProduct(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # GET PRODUCT IMAGE
    # ====================================================

    cmd = """
        SELECT image
        FROM product
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    row = cursor.fetchone()

    if not row:

        messages.error(
            request,
            "Product not found."
        )

        return redirect(
            "/Manager/Productlist/"
        )

    image_name = row[0]

    # ====================================================
    # DELETE PRODUCT
    # ====================================================

    cmd = """
        DELETE FROM product
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    db.commit()

    # ====================================================
    # DELETE IMAGE FILE
    # ====================================================

    if image_name:

        image_path = os.path.join(
            settings.BASE_DIR,
            "static",
            "product_images",
            image_name
        )

        if os.path.exists(image_path):

            os.remove(image_path)

    messages.success(
        request,
        "Product deleted successfully."
    )

    return redirect(
        "/Manager/Productlist/"
    )


# ========================================================
# MANAGER CONTACT MESSAGES
# ========================================================

def ContactMessages(request):

    if "manager" not in request.session:
        return redirect("/login/")

    cmd = """
        SELECT
            id,
            name,
            email,
            phone,
            subject,
            message,
            created_at,
            response,
            response_by,
            response_date,
            status
        FROM contact
        ORDER BY id DESC
    """

    cursor.execute(cmd)

    rows = cursor.fetchall()

    contacts = []

    for row in rows:

        contacts.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "subject": row[4],
            "message": row[5],
            "created_at": row[6],
            "response": row[7],
            "response_by": row[8],
            "response_date": row[9],
            "status": row[10]
        })

    return render(
        request,
        "store/Manager/ContactMessages.html",
        {
            "contacts": contacts
        }
    )


# ========================================================
# MANAGER CONTACT MESSAGE VIEW / REPLY
# ========================================================

def ContactReply(request, id):

    if "manager" not in request.session:
        return redirect("/login/")

    # ====================================================
    # GET CONTACT MESSAGE
    # ====================================================

    cmd = """
        SELECT
            id,
            name,
            email,
            phone,
            subject,
            message,
            created_at,
            response,
            response_by,
            response_date,
            status
        FROM contact
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (id,)
    )

    row = cursor.fetchone()

    # ====================================================
    # MESSAGE NOT FOUND
    # ====================================================

    if row is None:

        messages.error(
            request,
            "Contact message not found."
        )

        return redirect(
            "/Manager/ContactMessages/"
        )

    # ====================================================
    # CONTACT DATA
    # ====================================================

    contact = {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "phone": row[3],
        "subject": row[4],
        "message": row[5],
        "created_at": row[6],
        "response": row[7],
        "response_by": row[8],
        "response_date": row[9],
        "status": row[10]
    }

    # ====================================================
    # REPLY SUBMIT
    # ====================================================

    if request.method == "POST":

        response = request.POST.get(
            "response",
            ""
        ).strip()

        # =================================================
        # EMPTY REPLY
        # =================================================

        if response == "":

            messages.error(
                request,
                "Please enter your reply."
            )

            return render(
                request,
                "store/Manager/ContactReply.html",
                {
                    "contact": contact
                }
            )

        # =================================================
        # MANAGER EMAIL
        # =================================================

        manager_email = request.session["manager"]

        # =================================================
        # UPDATE CONTACT
        # =================================================

        update_cmd = """
            UPDATE contact
            SET
                response = %s,
                response_by = %s,
                response_date = NOW(),
                status = 'Replied'
            WHERE id = %s
        """

        update_values = (
            response,
            manager_email,
            id
        )

        cursor.execute(
            update_cmd,
            update_values
        )

        db.commit()

        messages.success(
            request,
            "Reply sent successfully."
        )

        return redirect(
            "/Manager/ContactMessages/"
        )

    # ====================================================
    # PAGE
    # ====================================================

    return render(
        request,
        "store/Manager/ContactReply.html",
        {
            "contact": contact
        }
    )