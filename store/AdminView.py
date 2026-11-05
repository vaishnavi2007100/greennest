from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import mysql.connector


# ============================================================
# DATABASE CONNECTION
# ============================================================

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="plant",
    port=3306
)

cursor = db.cursor(dictionary=True)


# ============================================================
# ADMIN LOGIN CHECK
# ============================================================

def admin_login_required(request):

    if "admin" not in request.session:
        return redirect("/login/")

    return None


# ============================================================
# ADMIN DASHBOARD
# ============================================================
def ADashboard(request):

    # --------------------------------------------------------
    # ADMIN LOGIN CHECK
    # --------------------------------------------------------

    check = admin_login_required(request)

    if check:
        return check


    # --------------------------------------------------------
    # TOTAL USERS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total_users
        FROM register
    """)

    user_data = cursor.fetchone()

    total_users = user_data["total_users"]


    # --------------------------------------------------------
    # TOTAL MANAGERS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total_managers
        FROM login
        WHERE LOWER(TRIM(role)) = 'manager'
    """)

    manager_data = cursor.fetchone()

    total_managers = manager_data["total_managers"]


    # --------------------------------------------------------
    # TOTAL VENDORS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total_vendors
        FROM login
        WHERE LOWER(TRIM(role)) = 'vendor'
    """)

    vendor_data = cursor.fetchone()

    total_vendors = vendor_data["total_vendors"]


    # --------------------------------------------------------
    # TOTAL PRODUCTS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total_products
        FROM product
    """)

    product_data = cursor.fetchone()

    total_products = product_data["total_products"]


    # --------------------------------------------------------
    # TOTAL CATEGORIES
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total_categories
        FROM category
    """)

    category_data = cursor.fetchone()

    total_categories = category_data["total_categories"]


    # --------------------------------------------------------
    # TOTAL ORDERS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total_orders
        FROM orders
    """)

    order_data = cursor.fetchone()

    total_orders = order_data["total_orders"]


    # --------------------------------------------------------
    # TOTAL REVIEWS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total_reviews
        FROM reviews
    """)

    review_data = cursor.fetchone()

    total_reviews = review_data["total_reviews"]


    # --------------------------------------------------------
    # TOTAL CONTACT MESSAGES
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total_messages
        FROM contact
    """)

    message_data = cursor.fetchone()

    total_messages = message_data["total_messages"]


    # --------------------------------------------------------
    # DASHBOARD DATA
    # --------------------------------------------------------

    context = {

        "total_users": total_users,

        "total_managers": total_managers,

        "total_vendors": total_vendors,

        "total_products": total_products,

        "total_categories": total_categories,

        "total_orders": total_orders,

        "total_reviews": total_reviews,

        "total_messages": total_messages,

    }


    # --------------------------------------------------------
    # RENDER ADMIN DASHBOARD
    # --------------------------------------------------------

    return render(
        request,
        "store/Admin/ADashboard.html",
        context
    )
# =====================================================
# BLOCK USER
# =====================================================

def AdminBlockUser(request, id):

    if "admin" not in request.session:
        return redirect("/login/")

    cursor.execute(
        """
        UPDATE register
        SET status = 'Blocked'
        WHERE id = %s
        """,
        (id,)
    )

    db.commit()

    messages.success(
        request,
        "User blocked successfully."
    )

    return redirect(
        "/Admin/UserList/"
    )


# =====================================================
# UNBLOCK USER
# =====================================================

def AdminUnblockUser(request, id):

    if "admin" not in request.session:
        return redirect("/login/")

    cursor.execute(
        """
        UPDATE register
        SET status = 'Active'
        WHERE id = %s
        """,
        (id,)
    )

    db.commit()

    messages.success(
        request,
        "User unblocked successfully."
    )

    return redirect(
        "/Admin/UserList/"
    )

# ============================================================
# MANAGER MANAGEMENT
# ============================================================


# ============================================================
# ADMIN - ADD MANAGER
# ============================================================

def AddManager(request):

    check = admin_login_required(request)

    if check:
        return check


    # --------------------------------------------------------
    # POST REQUEST
    # --------------------------------------------------------

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")


        # ----------------------------------------------------
        # REMOVE EXTRA SPACES
        # ----------------------------------------------------

        email = email.strip() if email else ""
        password = password.strip() if password else ""


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not email or not password:

            messages.error(
                request,
                "Email and password are required."
            )

            return redirect("AddManager")


        # ----------------------------------------------------
        # CHECK EMAIL ALREADY EXISTS
        # ----------------------------------------------------

        cmd = """
            SELECT id
            FROM login
            WHERE email = %s
        """

        cursor.execute(
            cmd,
            (email,)
        )

        existing_manager = cursor.fetchone()


        if existing_manager:

            messages.error(
                request,
                "This email already exists."
            )

            return redirect("AddManager")


        # ----------------------------------------------------
        # INSERT MANAGER
        # ----------------------------------------------------

        cmd = """
            INSERT INTO login
            (email, password, role)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            cmd,
            (
                email,
                password,
                "manager"
            )
        )

        db.commit()


        # ----------------------------------------------------
        # SUCCESS MESSAGE
        # ----------------------------------------------------

        messages.success(
            request,
            "Manager added successfully."
        )


        return redirect("Managerlist")


    # --------------------------------------------------------
    # GET REQUEST
    # --------------------------------------------------------

    return render(
        request,
        "store/Admin/AddManager.html"
    )


# ============================================================
# ADMIN - MANAGER LIST
# ============================================================

def Managerlist(request):

    check = admin_login_required(request)

    if check:
        return check


    cmd = """
        SELECT id, email, role
        FROM login
        WHERE role = 'manager'
        ORDER BY id DESC
    """

    cursor.execute(cmd)

    managers = cursor.fetchall()


    return render(
        request,
        "store/Admin/Managerlist.html",
        {
            "managers": managers
        }
    )


# ============================================================
# ADMIN - EDIT MANAGER
# ============================================================

def EditManager(request, id):

    check = admin_login_required(request)

    if check:
        return check


    cmd = """
        SELECT id, email, password, role
        FROM login
        WHERE id = %s
        AND role = 'manager'
    """

    cursor.execute(
        cmd,
        (id,)
    )

    manager = cursor.fetchone()


    if not manager:

        messages.error(
            request,
            "Manager not found."
        )

        return redirect("Managerlist")


    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        email = email.strip() if email else ""
        password = password.strip() if password else ""


        if not email:

            messages.error(
                request,
                "Email is required."
            )

            return redirect(
                "EditManager",
                id=id
            )


        # ----------------------------------------------------
        # CHECK DUPLICATE EMAIL
        # ----------------------------------------------------

        cmd = """
            SELECT id
            FROM login
            WHERE email = %s
            AND id != %s
        """

        cursor.execute(
            cmd,
            (email, id)
        )

        existing = cursor.fetchone()


        if existing:

            messages.error(
                request,
                "This email is already used."
            )

            return redirect(
                "EditManager",
                id=id
            )


        # ----------------------------------------------------
        # UPDATE WITH PASSWORD
        # ----------------------------------------------------

        if password:

            cmd = """
                UPDATE login
                SET
                    email = %s,
                    password = %s
                WHERE id = %s
                AND role = 'manager'
            """

            cursor.execute(
                cmd,
                (
                    email,
                    password,
                    id
                )
            )


        # ----------------------------------------------------
        # UPDATE WITHOUT PASSWORD
        # ----------------------------------------------------

        else:

            cmd = """
                UPDATE login
                SET
                    email = %s
                WHERE id = %s
                AND role = 'manager'
            """

            cursor.execute(
                cmd,
                (
                    email,
                    id
                )
            )


        db.commit()


        messages.success(
            request,
            "Manager updated successfully."
        )


        return redirect("Managerlist")


    return render(
        request,
        "store/Admin/EditManager.html",
        {
            "manager": manager
        }
    )


# ============================================================
# ADMIN - DELETE MANAGER
# ============================================================

def DeleteManager(request, id):

    check = admin_login_required(request)

    if check:
        return check


    cmd = """
        SELECT id
        FROM login
        WHERE id = %s
        AND role = 'manager'
    """

    cursor.execute(
        cmd,
        (id,)
    )

    manager = cursor.fetchone()


    if not manager:

        messages.error(
            request,
            "Manager not found."
        )

        return redirect("Managerlist")


    cmd = """
        DELETE FROM login
        WHERE id = %s
        AND role = 'manager'
    """

    cursor.execute(
        cmd,
        (id,)
    )

    db.commit()


    messages.success(
        request,
        "Manager deleted successfully."
    )


    return redirect("Managerlist")


# ============================================================
# VENDOR MANAGEMENT
# ============================================================

def Addvender(request):

    check = admin_login_required(request)

    if check:
        return check


    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()


        if not name or not email or not password or not phone:

            messages.error(
                request,
                "Please fill all vendor fields."
            )

            return render(
                request,
                "store/Admin/AddVendor.html"
            )


        try:

            cursor.execute(
                """
                INSERT INTO vender
                (
                    name,
                    email,
                    password,
                    phone
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    name,
                    email,
                    password,
                    phone
                )
            )

            db.commit()


            messages.success(
                request,
                "Vendor added successfully."
            )


            return redirect(
                "/Admin/Vendorlist/"
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to add vendor."
            )

            print(
                "Add Vendor Error:",
                e
            )


    return render(
        request,
        "store/Admin/AddVender.html"
    )


# ============================================================
# ============================================================
# VENDOR LIST
# ============================================================
# ============================================================
# VENDOR LIST
# ============================================================

def Vendorlist(request):

    check = admin_login_required(request)

    if check:
        return check

    vendors = []

    try:

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

        for row in rows:

            vendors.append({
                "id": row["id"],
                "name": row["email"].split("@")[0],
                "email": row["email"],
                "mobile": "",
                "role": row["role"]
            })

    except Exception as e:

        print("Vendor List Error:", e)

    return render(
        request,
        "store/Admin/VendorList.html",
        {
            "vendors": vendors
        }
    )
# ============================================================

def EditVendor(request, id):

    check = admin_login_required(request)

    if check:
        return check


    vendor = None


    try:

        cursor.execute(
            """
            SELECT *
            FROM vender
            WHERE id = %s
            """,
            (id,)
        )

        vendor = cursor.fetchone()


    except Exception as e:

        print(
            "Edit Vendor Error:",
            e
        )


    if not vendor:

        messages.error(
            request,
            "Vendor not found."
        )

        return redirect(
            "/Admin/Vendorlist/"
        )


    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()


        if not name or not email or not phone:

            messages.error(
                request,
                "Please fill all vendor fields."
            )

            return render(
                request,
                "store/Admin/EditVendor.html",
                {
                    "vendor": vendor
                }
            )


        try:

            cursor.execute(
                """
                UPDATE vender
                SET
                    name = %s,
                    email = %s,
                    phone = %s
                WHERE id = %s
                """,
                (
                    name,
                    email,
                    phone,
                    id
                )
            )

            db.commit()


            messages.success(
                request,
                "Vendor updated successfully."
            )


            return redirect(
                "/Admin/Vendorlist/"
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to update vendor."
            )

            print(
                "Update Vendor Error:",
                e
            )


    return render(
        request,
        "store/Admin/EditVendor.html",
        {
            "vendor": vendor
        }
    )


# ============================================================

def DeleteVendor(request, id):

    check = admin_login_required(request)

    if check:
        return check


    try:

        cursor.execute(
            "DELETE FROM vender WHERE id = %s",
            (id,)
        )

        db.commit()


        messages.success(
            request,
            "Vendor deleted successfully."
        )


    except Exception as e:

        db.rollback()

        messages.error(
            request,
            "Unable to delete vendor."
        )

        print(
            "Delete Vendor Error:",
            e
        )


    return redirect(
        "/Admin/Vendorlist/"
    )

# ============================================================
# USER MANAGEMENT
# ============================================================

def UserList(request):

    # =========================================================
    # ADMIN LOGIN CHECK
    # =========================================================

    check = admin_login_required(request)

    if check:
        return check


    # =========================================================
    # USER LIST
    # =========================================================

    users = []


    try:

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                status
            FROM register
            ORDER BY id DESC
            """
        )

        users = cursor.fetchall()

        print(
            "USER LIST DATA:",
            users
        )


    except Exception as e:

        print(
            "User List Error:",
            e
        )


    # =========================================================
    # RENDER
    # =========================================================

    return render(
        request,
        "store/Admin/UserList.html",
        {
            "users": users
        }
    )




# ============================================================

def AUserdetail(request, id):

    check = admin_login_required(request)

    if check:
        return check

    user = None

    try:

        cursor.execute(
            """
            SELECT
                r.id,
                r.name,
                r.email,
                r.mobile,
                ua.address,
                ua.city,
                ua.state,
                ua.pincode

            FROM register r

            LEFT JOIN user_address ua
                ON r.email = ua.email

            WHERE r.id = %s
            """,
            (id,)
        )

        user = cursor.fetchone()

        print("USER DETAIL DATA:", user)

    except Exception as e:

        print(
            "User Detail Error:",
            e
        )

    if not user:

        messages.error(
            request,
            "User not found."
        )

        return redirect(
            "/Admin/UserList/"
        )

    return render(
        request,
        "store/Admin/AUserdetail.html",
        {
            "user": user
        }
    )

# ============================================================

def DeleteUser(request, id):

    check = admin_login_required(request)

    if check:
        return check


    try:

        cursor.execute(
            "DELETE FROM register WHERE id = %s",
            (id,)
        )

        db.commit()


        messages.success(
            request,
            "User deleted successfully."
        )


    except Exception as e:

        db.rollback()

        messages.error(
            request,
            "Unable to delete user."
        )

        print(
            "Delete User Error:",
            e
        )


    return redirect(
        "/Admin/UserList/"
    )


# ============================================================
# CATEGORY MANAGEMENT
# ============================================================

def AdminAddcategory(request):

    check = admin_login_required(request)

    if check:
        return check


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
            "Active"
        ).strip()


        if not status:
            status = "Active"


        if not category_name:

            messages.error(
                request,
                "Category name is required."
            )

            return render(
                request,
                "store/Admin/AdminAddcategory.html"
            )


        try:

            cursor.execute(
                """
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
                """,
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
                "/Admin/AdminCategorylist/"
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to add category."
            )

            print(
                "Add Category Error:",
                e
            )


    return render(
        request,
        "store/Admin/AdminAddcategory.html"
    )


# ============================================================

def AdminCategorylist(request):

    check = admin_login_required(request)

    if check:
        return check


    categories = []


    try:

        cursor.execute(
            """
            SELECT
                id,
                category_name,
                category_type,
                description,
                status
            FROM category
            ORDER BY id DESC
            """
        )

        categories = cursor.fetchall()


    except Exception as e:

        print(
            "Category List Error:",
            e
        )


    return render(
        request,
        "store/Admin/AdminCategorylist.html",
        {
            "categories": categories
        }
    )


# ============================================================

def AdminEditcategory(request, id):

    check = admin_login_required(request)

    if check:
        return check


    category = None


    try:

        cursor.execute(
            """
            SELECT *
            FROM category
            WHERE id = %s
            """,
            (id,)
        )

        category = cursor.fetchone()


    except Exception as e:

        print(
            "Edit Category Error:",
            e
        )


    if not category:

        messages.error(
            request,
            "Category not found."
        )

        return redirect(
            "/Admin/AdminCategorylist/"
        )


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
            "Active"
        ).strip()


        if not status:
            status = "Active"


        if not category_name:

            messages.error(
                request,
                "Category name is required."
            )

            return render(
                request,
                "store/Admin/AdminEditcategory.html",
                {
                    "category": category
                }
            )


        try:

            cursor.execute(
                """
                UPDATE category
                SET
                    category_name = %s,
                    category_type = %s,
                    description = %s,
                    status = %s
                WHERE id = %s
                """,
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


            return redirect(
                "/Admin/AdminCategorylist/"
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to update category."
            )

            print(
                "Update Category Error:",
                e
            )


    return render(
        request,
        "store/Admin/AdminEditcategory.html",
        {
            "category": category
        }
    )


# ============================================================

def Deletecategory(request, id):

    check = admin_login_required(request)

    if check:
        return check


    try:

        cursor.execute(
            "DELETE FROM category WHERE id = %s",
            (id,)
        )

        db.commit()


        messages.success(
            request,
            "Category deleted successfully."
        )


    except Exception as e:

        db.rollback()

        messages.error(
            request,
            "Unable to delete category."
        )

        print(
            "Delete Category Error:",
            e
        )


    return redirect(
        "/Admin/AdminCategorylist/"
    )


# ============================================================
# SUBCATEGORY MANAGEMENT
# ============================================================

def AdminAddsubcategory(request):

    check = admin_login_required(request)

    if check:
        return check


    categories = []


    try:

        cursor.execute(
            """
            SELECT
                id,
                category_name
            FROM category
            ORDER BY category_name
            """
        )

        categories = cursor.fetchall()


    except Exception as e:

        print(
            "Category Fetch Error:",
            e
        )


    if request.method == "POST":

        category_id = request.POST.get(
            "category_id"
        )

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
            "Active"
        ).strip()


        if not status:
            status = "Active"


        if not category_id or not subcategory_name:

            messages.error(
                request,
                "Category and subcategory name are required."
            )

            return render(
                request,
                "store/Admin/AdminAddsubcategory.html",
                {
                    "categories": categories
                }
            )


        try:

            cursor.execute(
                """
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
                """,
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
                "/Admin/AdminSubcategorylist/"
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to add subcategory."
            )

            print(
                "Add Subcategory Error:",
                e
            )


    return render(
        request,
        "store/Admin/AdminAddsubcategory.html",
        {
            "categories": categories
        }
    )


# ============================================================

def AdminSubcategorylist(request):

    check = admin_login_required(request)

    if check:
        return check


    subcategories = []


    try:

        cursor.execute(
            """
            SELECT
                s.id,
                s.category_id,
                s.subcategory_name,
                s.description,
                s.status,
                c.category_name
            FROM subcategory s
            LEFT JOIN category c
                ON s.category_id = c.id
            ORDER BY s.id DESC
            """
        )

        subcategories = cursor.fetchall()


    except Exception as e:

        print(
            "Subcategory List Error:",
            e
        )


    return render(
        request,
        "store/Admin/AdminSubcategorylist.html",
        {
            "subcategories": subcategories
        }
    )


# ============================================================

def Editsubcategory(request, id):

    check = admin_login_required(request)

    if check:
        return check


    subcategory = None
    categories = []


    try:

        cursor.execute(
            """
            SELECT *
            FROM subcategory
            WHERE id = %s
            """,
            (id,)
        )

        subcategory = cursor.fetchone()


        cursor.execute(
            """
            SELECT
                id,
                category_name
            FROM category
            ORDER BY category_name
            """
        )

        categories = cursor.fetchall()


    except Exception as e:

        print(
            "Edit Subcategory Error:",
            e
        )


    if not subcategory:

        messages.error(
            request,
            "Subcategory not found."
        )

        return redirect(
            "/Admin/AdminSubcategorylist/"
        )


    if request.method == "POST":

        category_id = request.POST.get(
            "category_id"
        )

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
            "Active"
        ).strip()


        if not status:
            status = "Active"


        if not category_id or not subcategory_name:

            messages.error(
                request,
                "Category and subcategory name are required."
            )

            return render(
                request,
                "store/Admin/Editsubcategory.html",
                {
                    "subcategory": subcategory,
                    "categories": categories
                }
            )


        try:

            cursor.execute(
                """
                UPDATE subcategory
                SET
                    category_id = %s,
                    subcategory_name = %s,
                    description = %s,
                    status = %s
                WHERE id = %s
                """,
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
                "/Admin/AdminSubcategorylist/"
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to update subcategory."
            )

            print(
                "Update Subcategory Error:",
                e
            )


    return render(
        request,
        "store/Admin/Editsubcategory.html",
        {
            "subcategory": subcategory,
            "categories": categories
        }
    )


# ============================================================

def deletesubcategory(request, id):

    check = admin_login_required(request)

    if check:
        return check


    try:

        cursor.execute(
            "DELETE FROM subcategory WHERE id = %s",
            (id,)
        )

        db.commit()


        messages.success(
            request,
            "Subcategory deleted successfully."
        )


    except Exception as e:

        db.rollback()

        messages.error(
            request,
            "Unable to delete subcategory."
        )

        print(
            "Delete Subcategory Error:",
            e
        )


    return redirect(
        "/Admin/AdminSubcategorylist/"
    )


# ============================================================
# PRODUCT MANAGEMENT
# ============================================================

def AdminProductlist(request):

    check = admin_login_required(request)

    if check:
        return check


    products = []


    try:

        cursor.execute(
            """
            SELECT *
            FROM product
            ORDER BY id DESC
            """
        )

        products = cursor.fetchall()


    except Exception as e:

        print(
            "Product List Error:",
            e
        )


    return render(
        request,
        "store/Admin/AdminProductList.html",
        {
            "products": products
        }
    )


# ============================================================

def AdminProductdetail(request, id):

    check = admin_login_required(request)

    if check:
        return check


    product = None


    try:

        cursor.execute(
            """
            SELECT *
            FROM product
            WHERE id = %s
            """,
            (id,)
        )

        product = cursor.fetchone()


    except Exception as e:

        print(
            "Product Detail Error:",
            e
        )


    if not product:

        messages.error(
            request,
            "Product not found."
        )

        return redirect(
            "/Admin/AdminProductlist/"
        )


    return render(
        request,
        "store/Admin/AdminProductdetail.html",
        {
            "product": product
        }
    )


# ============================================================

def AdminEditProduct(request, id):

    check = admin_login_required(request)

    if check:
        return check


    product = None
    categories = []
    subcategories = []


    try:

        cursor.execute(
            """
            SELECT *
            FROM product
            WHERE id = %s
            """,
            (id,)
        )

        product = cursor.fetchone()


        cursor.execute(
            """
            SELECT
                id,
                category_name
            FROM category
            ORDER BY category_name
            """
        )

        categories = cursor.fetchall()


        cursor.execute(
            """
            SELECT
                id,
                category_id,
                subcategory_name
            FROM subcategory
            ORDER BY subcategory_name
            """
        )

        subcategories = cursor.fetchall()


    except Exception as e:

        print(
            "Product Edit Error:",
            e
        )


    if not product:

        messages.error(
            request,
            "Product not found."
        )

        return redirect(
            "/Admin/AdminEditProduct/"
        )


    if request.method == "POST":

        product_name = request.POST.get(
            "product_name",
            ""
        ).strip()

        category_id = request.POST.get(
            "category_id"
        )

        subcategory_id = request.POST.get(
            "subcategory_id"
        )

        description = request.POST.get(
            "description",
            ""
        ).strip()

        price = request.POST.get(
            "price",
            ""
        ).strip()

        quantity = request.POST.get(
            "quantity",
            ""
        ).strip()

        status = request.POST.get(
            "status",
            ""
        ).strip()


        if not product_name:

            messages.error(
                request,
                "Product name is required."
            )

            return render(
                request,
                "store/Admin/AdminEditProduct.html",
                {
                    "product": product,
                    "categories": categories,
                    "subcategories": subcategories
                }
            )


        try:

            cursor.execute(
                """
                UPDATE product
                SET
                    product_name = %s,
                    category_id = %s,
                    subcategory_id = %s,
                    description = %s,
                    price = %s,
                    quantity = %s,
                    status = %s
                WHERE id = %s
                """,
                (
                    product_name,
                    category_id,
                    subcategory_id,
                    description,
                    price,
                    quantity,
                    status,
                    id
                )
            )

            db.commit()


            messages.success(
                request,
                "Product updated successfully."
            )


            return redirect(
                "/Admin/AdminProductlist/"
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to update product."
            )

            print(
                "Product Update Error:",
                e
            )


    return render(
        request,
        "store/Admin/AdminEditProduct.html",
        {
            "product": product,
            "categories": categories,
            "subcategories": subcategories
        }
    )


# ============================================================

def AdminDeleteProduct(request, id):

    check = admin_login_required(request)

    if check:
        return check


    try:

        cursor.execute(
            "DELETE FROM product WHERE id = %s",
            (id,)
        )

        db.commit()


        messages.success(
            request,
            "Product deleted successfully."
        )


    except Exception as e:

        db.rollback()

        messages.error(
            request,
            "Unable to delete product."
        )

        print(
            "Product Delete Error:",
            e
        )


    return redirect(
        "/Admin/AdminProductlist/"
    )


# ============================================================
# ORDER MANAGEMENT
# ============================================================

def AdminOrderlist(request):

    check = admin_login_required(request)

    if check:
        return check


    orders = []


    try:

        cursor.execute(
            """
            SELECT *
            FROM orders
            ORDER BY id DESC
            """
        )

        orders = cursor.fetchall()


    except Exception as e:

        print(
            "Order List Error:",
            e
        )


    return render(
        request,
        "store/Admin/AdminOrderList.html",
        {
            "orders": orders
        }
    )


# ============================================================

def AdminOrderdetail(request, id):

    check = admin_login_required(request)

    if check:
        return check


    order = None


    try:

        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE id = %s
            """,
            (id,)
        )

        order = cursor.fetchone()


    except Exception as e:

        print(
            "Order Detail Error:",
            e
        )


    if not order:

        messages.error(
            request,
            "Order not found."
        )

        return redirect(
            "/Admin/AdminOrderlist/"
        )


    return render(
        request,
        "store/Admin/AdminOrderDetail.html",
        {
            "order": order
        }
    )


# ============================================================

def AdminOrderstatus(request, id):

    check = admin_login_required(request)

    if check:
        return check


    if request.method == "POST":

        status = request.POST.get(
            "status",
            ""
        ).strip()


        if not status:

            messages.error(
                request,
                "Please select an order status."
            )

            return redirect(
                "/Admin/AdminOrderlist/"
            )


        try:

            cursor.execute(
                """
                UPDATE orders
                SET
                    status = %s
                WHERE id = %s
                """,
                (
                    status,
                    id
                )
            )

            db.commit()


            messages.success(
                request,
                "Order status updated successfully."
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to update order status."
            )

            print(
                "Order Status Error:",
                e
            )


    return redirect(
        "/Admin/Orderlist/"
    )


# ============================================================
# CUSTOMER REVIEWS
# ============================================================

def AdminReviews(request):

    check = admin_login_required(request)

    if check:
        return check


    reviews = []


    try:

        cursor.execute(
            """
            SELECT
                id,
                product_id,
                user_name,
                user_email,
                rating,
                review_text,
                created_at
            FROM reviews
            ORDER BY created_at DESC
            """
        )

        reviews = cursor.fetchall()


    except Exception as e:

        print(
            "Reviews Error:",
            e
        )


    return render(
        request,
        "store/Admin/AdminReviews.html",
        {
            "reviews": reviews,
            "total_reviews": len(reviews)
        }
    )


# ============================================================

def AdminDeleteReview(request, id):

    check = admin_login_required(request)

    if check:
        return check


    try:

        cursor.execute(
            "DELETE FROM reviews WHERE id = %s",
            (id,)
        )

        db.commit()


        messages.success(
            request,
            "Customer review deleted successfully."
        )


    except Exception as e:

        db.rollback()

        messages.error(
            request,
            "Unable to delete review."
        )

        print(
            "Delete Review Error:",
            e
        )


    return redirect(
        "/Admin/AdminReviews/"
    )


# ============================================================
# CUSTOMER FEEDBACK
# ============================================================

def AdminFeedback(request):

    check = admin_login_required(request)

    if check:
        return check


    feedbacks = []


    try:

        cursor.execute(
            """
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
        )

        feedbacks = cursor.fetchall()


    except Exception as e:

        print(
            "Feedback Error:",
            e
        )


    return render(
        request,
        "store/Admin/AdminFeedback.html",
        {
            "feedbacks": feedbacks,
            "total_feedbacks": len(feedbacks)
        }
    )


# ============================================================

def AdminFeedbackReply(request, id):

    check = admin_login_required(request)

    if check:
        return check


    feedback = None


    try:

        cursor.execute(
            """
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
            """,
            (id,)
        )

        feedback = cursor.fetchone()


    except Exception as e:

        print(
            "Feedback Detail Error:",
            e
        )


    if not feedback:

        messages.error(
            request,
            "Feedback not found."
        )

        return redirect(
            "/Admin/AdminFeedback/"
        )


    if request.method == "POST":

        response_text = request.POST.get(
            "response",
            ""
        ).strip()


        if not response_text:

            messages.error(
                request,
                "Please enter a response."
            )

            return render(
                request,
                "store/Admin/AdminFeedbackReply.html",
                {
                    "feedback": feedback
                }
            )


        admin_email = request.session.get(
            "admin"
        )


        try:

            cursor.execute(
                """
                UPDATE contact
                SET
                    response = %s,
                    response_by = %s,
                    response_date = NOW(),
                    status = 'Replied'
                WHERE id = %s
                """,
                (
                    response_text,
                    admin_email,
                    id
                )
            )

            db.commit()


            messages.success(
                request,
                "Feedback reply saved successfully."
            )


            return redirect(
                "/Admin/AdminFeedback/"
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to save feedback reply."
            )

            print(
                "Feedback Reply Error:",
                e
            )


    return render(
        request,
        "store/Admin/AdminFeedbackReply.html",
        {
            "feedback": feedback
        }
    )


# ============================================================
# REPORTS MAIN PAGE
# ============================================================
def Reports(request):

    check = admin_login_required(request)

    if check:
        return check


    # ----------------------------------------------------
    # DEFAULT VALUES
    # ----------------------------------------------------

    total_sales = 0
    total_orders = 0
    total_users = 0
    total_products = 0
    total_reviews = 0


    try:

        # ----------------------------------------------------
        # TOTAL ORDERS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM orders
            """
        )

        row = cursor.fetchone()

        if row:
            total_orders = row["total"]


        # ----------------------------------------------------
        # TOTAL USERS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM register
            """
        )

        row = cursor.fetchone()

        if row:
            total_users = row["total"]


        # ----------------------------------------------------
        # TOTAL PRODUCTS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM product
            """
        )

        row = cursor.fetchone()

        if row:
            total_products = row["total"]


        # ----------------------------------------------------
        # TOTAL REVIEWS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM reviews
            """
        )

        row = cursor.fetchone()

        if row:
            total_reviews = row["total"]


        # ----------------------------------------------------
        # TOTAL SALES
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                COALESCE(
                    SUM(total),
                    0
                ) AS total
            FROM orders
            """
        )

        row = cursor.fetchone()

        if row:
            total_sales = row["total"]


    except Exception as e:

        print(
            "Reports Error:",
            e
        )


    # ----------------------------------------------------
    # SEND DATA TO TEMPLATE
    # ----------------------------------------------------

    return render(
        request,
        "store/Admin/Reports.html",
        {
            "total_sales": total_sales,
            "total_orders": total_orders,
            "total_users": total_users,
            "total_products": total_products,
            "total_reviews": total_reviews
        }
    )


def AdminSalesReport(request):

    check = admin_login_required(request)

    if check:
        return check


    sales_orders = []

    total_orders = 0
    delivered_orders = 0
    total_sales = 0


    try:

        # ====================================================
        # ALL ORDERS
        # ====================================================

        cursor.execute(
            """
            SELECT *
            FROM orders
            ORDER BY id DESC
            """
        )

        sales_orders = cursor.fetchall()


        # ====================================================
        # TOTAL ORDERS
        # ====================================================

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM orders
            """
        )

        row = cursor.fetchone()

        if row:
            total_orders = row["total"]


        # ====================================================
        # DELIVERED ORDERS
        # ====================================================

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM orders
            WHERE LOWER(TRIM(status)) = 'delivered'
            """
        )

        row = cursor.fetchone()

        if row:
            delivered_orders = row["total"]


        # ====================================================
        # TOTAL SALES / REVENUE
        # ====================================================

        cursor.execute(
            """
            SELECT
                COALESCE(SUM(total), 0) AS total
            FROM orders
            """
        )

        row = cursor.fetchone()

        if row:
            total_sales = row["total"]


    except Exception as e:

        print(
            "Sales Report Error:",
            e
        )


    return render(
        request,
        "store/Admin/AdminSalesReport.html",
        {
            "sales_orders": sales_orders,
            "total_orders": total_orders,
            "delivered_orders": delivered_orders,
            "total_sales": total_sales
        }
    )

# ============================================================
# USER REPORT
# ============================================================

def AdminUserReport(request):

    check = admin_login_required(request)

    if check:
        return check


    users = []


    try:

        cursor.execute(
            """
            SELECT
                id,
                name,
                email
            FROM register
            ORDER BY id DESC
            """
        )

        users = cursor.fetchall()


    except Exception as e:

        print(
            "User Report Error:",
            e
        )


    return render(
        request,
        "store/Admin/AdminUserReport.html",
        {
            "users": users
        }
    )


# ============================================================
# PRODUCT REPORT
# ============================================================

def AdminProductReport(request):

    check = admin_login_required(request)

    if check:
        return check


    products = []


    try:

        cursor.execute(
            """
            SELECT *
            FROM product
            ORDER BY id DESC
            """
        )

        products = cursor.fetchall()


    except Exception as e:

        print(
            "Product Report Error:",
            e
        )


    return render(
        request,
        "store/Admin/AdminProductReport.html",
        {
            "products": products
        }
    )


# ============================================================
# ADMIN PROFILE
# ============================================================
def AdminProfile(request):

    check = admin_login_required(request)

    if check:
        return check

    email = request.session.get("admin")

    admin = None

    try:

        cursor.execute(
            """
            SELECT *
            FROM login
            WHERE email = %s
            """,
            (email,)
        )

        admin = cursor.fetchone()

    except Exception as e:

        print(
            "Admin Profile Error:",
            e
        )

    if not admin:

        messages.error(
            request,
            "Admin account not found."
        )

    return render(
        request,
        "store/Admin/AdminProfile.html",
        {
            "admin": admin
        }
    )
# ============================================================
# ADMIN CHANGE PASSWORD
# ============================================================

def AdminChangePassword(request):

    check = admin_login_required(request)

    if check:
        return check


    if request.method == "POST":

        old_password = request.POST.get(
            "old_password",
            ""
        )

        new_password = request.POST.get(
            "new_password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )


        email = request.session.get(
            "admin"
        )


        if not old_password:

            messages.error(
                request,
                "Please enter your current password."
            )

            return render(
                request,
                "store/Admin/AdminChangePassword.html"
            )


        if not new_password:

            messages.error(
                request,
                "Please enter a new password."
            )

            return render(
                request,
                "store/Admin/AdminChangePassword.html"
            )


        if new_password != confirm_password:

            messages.error(
                request,
                "New password and confirm password do not match."
            )

            return render(
                request,
                "store/Admin/AdminChangePassword.html"
            )


        try:

            cursor.execute(
                """
                SELECT password
                FROM login
                WHERE email = %s
                """,
                (email,)
            )

            admin = cursor.fetchone()


            if not admin:

                messages.error(
                    request,
                    "Admin account not found."
                )

                return render(
                    request,
                    "store/Admin/AdminChangePassword.html"
                )


            if admin["password"] != old_password:

                messages.error(
                    request,
                    "Current password is incorrect."
                )

                return render(
                    request,
                    "store/Admin/AdminChangePassword.html"
                )


            cursor.execute(
                """
                UPDATE login
                SET
                    password = %s
                WHERE email = %s
                """,
                (
                    new_password,
                    email
                )
            )

            db.commit()


            messages.success(
                request,
                "Password changed successfully."
            )


            return redirect(
                "/Admin/AdminProfile/"
            )


        except Exception as e:

            db.rollback()

            messages.error(
                request,
                "Unable to change password."
            )

            print(
                "Admin Password Error:",
                e
            )


    return render(
        request,
        "store/Admin/AdminChangePassword.html"
    )


# ============================================================
# ADMIN LOGOUT
# ============================================================

def AdminLogout(request):

    request.session.flush()

    return redirect(
        "/login/"
    )