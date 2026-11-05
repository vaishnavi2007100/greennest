from django.shortcuts import render, redirect
import mysql.connector
import datetime


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
# DATE
# =====================================================

dt = datetime.date.today()


# =====================================================
# NAVBAR DATA
# =====================================================

def navbar_context(request):

    cart_count = 0
    wishlist_count = 0

    # =================================================
    # CART + WISHLIST
    # =================================================

    if "user" in request.session:

        user_email = request.session["user"]

        # ---------------------------------------------
        # CART COUNT
        # ---------------------------------------------

        cursor.execute("""
            SELECT COALESCE(SUM(quantity), 0)
            FROM cart
            WHERE user_email = %s
        """, (user_email,))

        result = cursor.fetchone()

        if result:
            cart_count = int(result[0] or 0)

        # ---------------------------------------------
        # WISHLIST COUNT
        # ---------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM wishlist
            WHERE user_email = %s
        """, (user_email,))

        result = cursor.fetchone()

        if result:
            wishlist_count = int(result[0] or 0)

    # =================================================
    # CATEGORY DATA
    # =================================================

    navbar_categories = []

    try:

        cursor.execute("""
            SELECT
                id,
                category_name
            FROM category
            WHERE LOWER(TRIM(status)) = 'active'
            ORDER BY id ASC
        """)

        category_rows = cursor.fetchall()

        for row in category_rows:

            navbar_categories.append({
                "id": row[0],
                "category_name": row[1]
            })

        print(
            "NAVBAR CATEGORIES:",
            navbar_categories
        )

    except Exception as e:

        print(
            "Navbar Category Error:",
            e
        )

    # =================================================
    # RETURN NAVBAR DATA
    # =================================================

    return {

        "cart_count":
            cart_count,

        "wishlist_count":
            wishlist_count,

        "navbar_categories":
            navbar_categories,
    }


# =====================================================
# COMMON PRODUCT DICTIONARY
# =====================================================

def make_product(row):

    return {

        "id": row[0],

        "vendor_email": row[1],

        "name": row[2],

        "category": row[3],

        "subcategory": row[4],

        "collection_id": row[5],

        "price": row[6],

        "old_price": row[7],

        "image": row[8],

        "description": row[9],

        "stock": row[10],

        "status": row[11],

        "created_at": row[12],

        "rating": 4.8,

        "image_url":
            "/static/product_images/"
            + str(row[8])
            if row[8]
            else ""
    }


# =====================================================
# HOME
# =====================================================

def home(request):

    home_products = []

    try:

        cursor.execute("""
            SELECT
                id,
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
                status,
                created_at
            FROM product
            WHERE LOWER(TRIM(status)) = 'active'
            GROUP BY name
            ORDER BY created_at DESC, id DESC
            LIMIT 8
        """)

        product_rows = cursor.fetchall()

        for row in product_rows:

            home_products.append(
                make_product(row)
            )

        print(
            "HOME PRODUCTS:",
            len(home_products)
        )

    except Exception as e:

        print(
            "Home Products Error:",
            e
        )

    # =====================================================
    # REVIEWS
    # =====================================================

    reviews = []

    try:

        cursor.execute("""
            SELECT
                id,
                user_name,
                user_email,
                rating,
                review_text,
                created_at
            FROM reviews
            WHERE rating IS NOT NULL
            ORDER BY created_at DESC
            LIMIT 6
        """)

        review_rows = cursor.fetchall()

        for review in review_rows:

            rating = int(
                review[3] or 0
            )

            reviews.append({

                "id": review[0],

                "user_name": review[1],

                "user_email": review[2],

                "rating": rating,

                "review_text": review[4],

                "created_at": review[5],

                "stars": range(rating)

            })

    except Exception as e:

        print(
            "Home Reviews Error:",
            e
        )

    # =====================================================
    # NAVBAR DATA
    # =====================================================

    context = navbar_context(request)

    # =====================================================
    # HOME DATA
    # =====================================================

    context["home_products"] = home_products

    context["product_count"] = len(
        home_products
    )

    context["reviews"] = reviews

    # =====================================================
    # RENDER HOME
    # =====================================================

    return render(
        request,
        "store/home.html",
        context
    )


# =====================================================
# ABOUT
# =====================================================

def about(request):

    context = navbar_context(request)

    return render(
        request,
        "store/about.html",
        context
    )


# =====================================================
# CONTACT
# =====================================================

def contact(request):

    msg = ""

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

        subject = request.POST.get(
            "subject",
            ""
        ).strip()

        message = request.POST.get(
            "message",
            ""
        ).strip()

        cursor.execute(
            """
            INSERT INTO contact
            (
                name,
                email,
                phone,
                subject,
                message
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                name,
                email,
                phone,
                subject,
                message
            )
        )

        db.commit()

        msg = "Your message has been sent successfully!"

    context = navbar_context(request)

    context["Msg"] = msg

    return render(
        request,
        "store/contact.html",
        context
    )


# =====================================================
# PLANT / PRODUCT PAGE
# =====================================================

def plant(request):

    category = request.GET.get(
        "category",
        ""
    ).strip()

    subcategory = request.GET.get(
        "subcategory",
        ""
    ).strip()

    print("==============================================")
    print("PLANT PAGE CALLED")
    print("CATEGORY:", category)
    print("SUBCATEGORY:", subcategory)
    print("==============================================")

    cmd = """
        SELECT
            id,
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
            status,
            created_at
        FROM product
        WHERE LOWER(TRIM(status)) = 'active'
        ORDER BY id DESC
    """

    cursor.execute(cmd)

    product_rows = cursor.fetchall()

    products = []

    for row in product_rows:

        product = make_product(row)

        products.append(product)

    # =========================================================
    # REVIEWS
    # =========================================================

    review_cmd = """
        SELECT
            id,
            product_id,
            user_name,
            user_email,
            rating,
            review_text,
            created_at
        FROM reviews
        ORDER BY id DESC
    """

    cursor.execute(review_cmd)

    review_rows = cursor.fetchall()

    reviews = []

    for row in review_rows:

        review = {
            "id": row[0],
            "product_id": row[1],
            "user_name": row[2],
            "user_email": row[3],
            "rating": row[4],
            "review_text": row[5],
            "created_at": row[6],
        }

        try:

            rating = int(
                review["rating"] or 0
            )

        except (TypeError, ValueError):

            rating = 0

        rating = max(
            0,
            min(rating, 5)
        )

        review["stars"] = range(5)

        review["rating_value"] = rating

        reviews.append(review)

    # =========================================================
    # CONTEXT
    # =========================================================

    context = navbar_context(request)

    context["products"] = products

    context["reviews"] = reviews

    context["category"] = category

    context["subcategory"] = subcategory

    return render(
        request,
        "store/plant.html",
        context
    )


# =====================================================
# PLANT CATEGORY
# =====================================================

def plantc(request):

    context = navbar_context(request)

    return render(
        request,
        "store/plantc.html",
        context
    )


# =====================================================
# INDOOR PLANTS
# =====================================================

def indoorp(request):

    indoor_products = []

    try:

        cursor.execute("""
            SELECT
                id,
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
                status,
                created_at
            FROM product
            WHERE LOWER(TRIM(category)) = 'indoor plant'
              AND LOWER(TRIM(status)) = 'active'
            ORDER BY created_at DESC, id DESC
        """)

        product_rows = cursor.fetchall()

        for row in product_rows:

            indoor_products.append(
                make_product(row)
            )

        print(
            "INDOOR PRODUCTS:",
            len(indoor_products)
        )

    except Exception as e:

        print(
            "Indoor Products Error:",
            e
        )

    context = navbar_context(request)

    context["indoor_products"] = indoor_products

    context["indoor_product_count"] = len(
        indoor_products
    )

    return render(
        request,
        "store/indoorp.html",
        context
    )


# =====================================================
# OUTDOOR PLANTS
# =====================================================

def outdoorp(request):

    outdoor_products = []

    try:

        cursor.execute("""
            SELECT
                id,
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
                status,
                created_at
            FROM product
            WHERE LOWER(TRIM(category)) = 'outdoor plant'
              AND LOWER(TRIM(status)) = 'active'
            ORDER BY created_at DESC, id DESC
        """)

        product_rows = cursor.fetchall()

        for row in product_rows:

            outdoor_products.append(
                make_product(row)
            )

        print(
            "OUTDOOR PRODUCTS:",
            len(outdoor_products)
        )

    except Exception as e:

        print(
            "Outdoor Products Error:",
            e
        )

    context = navbar_context(request)

    context["outdoor_products"] = outdoor_products

    context["outdoor_product_count"] = len(
        outdoor_products
    )

    return render(
        request,
        "store/outdoorp.html",
        context
    )


# =====================================================
# FLOWER PLANTS
# =====================================================

def flowerp(request):

    flower_products = []

    try:

        cursor.execute("""
            SELECT
                id,
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
                status,
                created_at
            FROM product
            WHERE LOWER(TRIM(category)) = 'flower plant'
              AND LOWER(TRIM(status)) = 'active'
            ORDER BY created_at DESC, id DESC
        """)

        product_rows = cursor.fetchall()

        for row in product_rows:

            flower_products.append(
                make_product(row)
            )

    except Exception as e:

        print(
            "Flower Products Error:",
            e
        )

    context = navbar_context(request)

    context["flower_products"] = flower_products

    context["flower_product_count"] = len(
        flower_products
    )

    return render(
        request,
        "store/flowerp.html",
        context
    )


# =====================================================
# TABLE PLANTS
# =====================================================

def tablep(request):

    table_products = []

    try:

        cursor.execute("""
            SELECT
                id,
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
                status,
                created_at
            FROM product
            WHERE LOWER(TRIM(category)) = 'table plant'
              AND LOWER(TRIM(status)) = 'active'
            ORDER BY created_at DESC, id DESC
        """)

        product_rows = cursor.fetchall()

        for row in product_rows:

            table_products.append(
                make_product(row)
            )

        print(
            "TABLE PRODUCTS:",
            len(table_products)
        )

    except Exception as e:

        print(
            "Table Products Error:",
            e
        )

    context = navbar_context(request)

    context["table_products"] = table_products

    context["table_product_count"] = len(
        table_products
    )

    return render(
        request,
        "store/tablep.html",
        context
    )


# =====================================================
# PLANT POTS
# =====================================================

def plantp(request):

    context = navbar_context(request)

    return render(
        request,
        "store/plantp.html",
        context
    )


# =====================================================
# PLANT CARE
# =====================================================

def plantcare(request):

    context = navbar_context(request)

    return render(
        request,
        "store/plantcare.html",
        context
    )


# =====================================================
# HOME DECOR
# =====================================================

def homedecore(request):

    context = navbar_context(request)

    return render(
        request,
        "store/homedecore.html",
        context
    )


# =====================================================
# COLLECTION MAIN PAGE
# =====================================================

def collection(request):

    context = navbar_context(request)

    collection_id = request.GET.get(
        "collection_id",
        ""
    ).strip()

    collection_name_param = request.GET.get(
        "collection",
        ""
    ).strip()

    cursor.execute("""
        SELECT
            id,
            collection_name,
            parent_id,
            description,
            status
        FROM collection
        WHERE LOWER(TRIM(status)) = 'active'
        ORDER BY
            CASE
                WHEN parent_id IS NULL THEN 0
                ELSE 1
            END,
            id ASC
    """)

    collection_rows = cursor.fetchall()

    collections = []

    for row in collection_rows:

        collections.append({
            "id": row[0],
            "collection_name": row[1],
            "parent_id": row[2],
            "description": row[3],
            "status": row[4],
            "children": []
        })

    for child in collections:

        if child["parent_id"] is not None:

            for parent in collections:

                if child["parent_id"] == parent["id"]:

                    parent["children"].append(child)

                    break

    main_collections = []

    for item in collections:

        if item["parent_id"] is None:

            main_collections.append(item)

    if not collection_id and collection_name_param:

        for item in collections:

            if (
                item["collection_name"].strip().lower()
                == collection_name_param.lower()
            ):

                collection_id = str(item["id"])

                break

    if collection_id:

        selected_collection = None

        for item in collections:

            if str(item["id"]) == str(collection_id):

                selected_collection = item

                break

        if selected_collection:

            child_ids = []

            for child in selected_collection["children"]:

                child_ids.append(child["id"])

            if child_ids:

                placeholders = ",".join(
                    ["%s"] * (len(child_ids) + 1)
                )

                collection_ids = (
                    [selected_collection["id"]]
                    + child_ids
                )

                cursor.execute(
                    f"""
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
                    WHERE LOWER(TRIM(status)) = 'active'
                    AND collection_id IN ({placeholders})
                    ORDER BY id DESC
                    """,
                    tuple(collection_ids)
                )

            else:

                cursor.execute("""
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
                    WHERE LOWER(TRIM(status)) = 'active'
                    AND collection_id = %s
                    ORDER BY id DESC
                """, (collection_id,))

        else:

            cursor.execute("""
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
                WHERE LOWER(TRIM(status)) = 'active'
                ORDER BY id DESC
            """)

    else:

        cursor.execute("""
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
            WHERE LOWER(TRIM(status)) = 'active'
            ORDER BY id DESC
        """)

    product_rows = cursor.fetchall()

    products = []

    for row in product_rows:

        products.append({
            "id": row[0],
            "name": row[1],
            "category": row[2] if row[2] else "No Category",
            "subcategory": row[3] if row[3] else "No Subcategory",
            "price": row[4],
            "old_price": row[5],
            "image": row[6],
            "description": row[7],
            "stock": row[8],
            "status": row[9]
        })

    selected_collection_name = ""

    if collection_id:

        for item in collections:

            if str(item["id"]) == str(collection_id):

                selected_collection_name = (
                    item["collection_name"]
                )

                break

    context["collections"] = collections

    context["main_collections"] = main_collections

    context["products"] = products

    context["selected_collection_id"] = collection_id

    context["selected_collection_name"] = (
        selected_collection_name
    )

    return render(
        request,
        "store/collection.html",
        context
    )


# =====================================================
# PLANT ACCESSORIES
# =====================================================

def planta(request):

    context = navbar_context(request)

    return render(
        request,
        "store/planta.html",
        context
    )


# =====================================================
# NEW ARRIVALS
# =====================================================

def newarrivals(request):

    context = navbar_context(request)

    cursor.execute("""
        SELECT
            id,
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
            status,
            created_at
        FROM product
        WHERE LOWER(TRIM(status)) = 'active'
        ORDER BY created_at DESC, id DESC
        LIMIT 8
    """)

    product_rows = cursor.fetchall()

    products = []

    for row in product_rows:

        products.append(
            make_product(row)
        )

    new_arrival = {

        "collection_name":
            "New Arrivals",

        "description":
            "Discover the latest plants and products added to GreenNest.",

        "status":
            "Active"
    }

    context["new_arrival"] = new_arrival

    context["products"] = products

    context["product_count"] = len(products)

    print("==============================================")
    print("NEW ARRIVALS")
    print("PRODUCT COUNT:", len(products))
    print("==============================================")

    return render(
        request,
        "store/newarrivals.html",
        context
    )


# =====================================================
# COMMON COLLECTION PRODUCT FUNCTION
# =====================================================

def collection_products(request, collection_id):

    context = navbar_context(request)

    cursor.execute(
        """
        SELECT
            id,
            collection_name,
            parent_id,
            description,
            status
        FROM collection
        WHERE id = %s
        AND LOWER(TRIM(status)) = 'active'
        """,
        (
            collection_id,
        )
    )

    collection_row = cursor.fetchone()

    if not collection_row:

        print("==============================================")
        print("COLLECTION NOT FOUND")
        print("COLLECTION ID:", collection_id)
        print("==============================================")

        return redirect(
            "/collection/"
        )

    collection_name = str(
        collection_row[1]
    ).strip()

    selected_collection = {

        "id":
            collection_row[0],

        "collection_name":
            collection_row[1],

        "parent_id":
            collection_row[2],

        "description":
            collection_row[3],

        "status":
            collection_row[4]
    }

    product_query = """
        SELECT
            id,
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
            status,
            created_at
        FROM product
        WHERE collection_id = %s
        AND LOWER(TRIM(status)) = 'active'
        ORDER BY id DESC
        LIMIT 8
    """

    cursor.execute(
        product_query,
        (
            collection_id,
        )
    )

    product_rows = cursor.fetchall()

    print(
        "DIRECT PRODUCTS FOUND:",
        len(product_rows)
    )

    if int(collection_id) == 6:

        cursor.execute(
            """
            SELECT
                id,
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
                status,
                created_at
            FROM product
            WHERE collection_id IN (7, 8, 9, 10)
            AND LOWER(TRIM(status)) = 'active'
            ORDER BY id DESC
            LIMIT 8
            """
        )

        seasonal_rows = cursor.fetchall()

        if seasonal_rows:

            product_rows = seasonal_rows

        print(
            "SEASONAL PRODUCTS FOUND:",
            len(product_rows)
        )

    products = []

    for row in product_rows:

        products.append(
            make_product(row)
        )

    if len(products) == 0:

        print("==============================================")
        print("NO PRODUCTS IN SELECTED COLLECTION")
        print("RUNNING FALLBACK QUERY")
        print("==============================================")

        cursor.execute(
            """
            SELECT
                id,
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
                status,
                created_at
            FROM product
            WHERE LOWER(TRIM(status)) = 'active'
            ORDER BY created_at DESC, id DESC
            LIMIT 8
            """
        )

        fallback_rows = cursor.fetchall()

        for row in fallback_rows:

            products.append(
                make_product(row)
            )

        print(
            "FALLBACK PRODUCTS FOUND:",
            len(products)
        )

    context["selected_collection"] = selected_collection

    context["products"] = products

    context["product_count"] = len(products)

    context["collection_name"] = collection_name

    context["collection_description"] = collection_row[3]

    return render(
        request,
        "store/collection_products.html",
        context
    )


# =====================================================
# BEST SELLERS
# =====================================================

def bestsellers(request):

    return collection_products(
        request,
        2
    )


# =====================================================
# PREMIUM PLANTS
# =====================================================

def premiumplants(request):

    return collection_products(
        request,
        3
    )


# =====================================================
# BEGINNER COLLECTION
# =====================================================

def beginnercollection(request):

    return collection_products(
        request,
        4
    )


# =====================================================
# FLOWERING COLLECTION
# =====================================================

def floweringcollection(request):

    return collection_products(
        request,
        5
    )


# =====================================================
# SEASONAL COLLECTION
# =====================================================

def seasonal(request):

    return collection_products(
        request,
        6
    )


# =====================================================
# SPRING
# =====================================================

def spring(request):

    return collection_products(
        request,
        7
    )


# =====================================================
# SUMMER
# =====================================================

def summer(request):

    return collection_products(
        request,
        8
    )


# =====================================================
# AUTUMN
# =====================================================

def autumn(request):

    return collection_products(
        request,
        9
    )


# =====================================================
# WINTER
# =====================================================

def winter(request):

    return collection_products(
        request,
        10
    )
# =====================================================
# LOGIN
# =====================================================

def login(request):

    global db, cursor

    print("==============================================")
    print("LOGIN FUNCTION CALLED")
    print("==============================================")

    msg = ""

    # =================================================
    # LOGIN KE LIYE FRESH DATABASE CONNECTION
    # =================================================

    login_db = None
    login_cursor = None

    try:

        login_db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="plant",
            port=3306,
            connection_timeout=10
        )

        login_cursor = login_db.cursor()

        print("LOGIN DATABASE CONNECTION OK")

    except Exception as e:

        print("LOGIN DATABASE CONNECTION ERROR:", e)

        msg = "Database connection error."

        context = navbar_context(request)

        context["Msg"] = msg

        return render(
            request,
            "store/login.html",
            context
        )

    # =================================================
    # POST
    # =================================================

    if request.method == "POST":

        print("==============================================")
        print("LOGIN POST CALLED")
        print("==============================================")

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        ).strip()

        print(
            "ENTERED EMAIL:",
            repr(email)
        )

       

        # =================================================
        # CHECK DATABASE
        # =================================================

        try:

            login_cursor.execute(
                "SELECT DATABASE()"
            )

            current_database = login_cursor.fetchone()

            print(
                "CURRENT DATABASE:",
                current_database
            )

        except Exception as e:

            print(
                "DATABASE CHECK ERROR:",
                e
            )

        # =================================================
        # FIND USER BY EMAIL
        # =================================================

        try:

            login_cursor.execute(
                """
                SELECT
                    id,
                    email,
                    password,
                    role
                FROM plant.login
                WHERE LOWER(TRIM(email)) =
                      LOWER(TRIM(%s))
                LIMIT 1
                """,
                (
                    email,
                )
            )

            data = login_cursor.fetchone()

           
        except Exception as e:

            print(
                "LOGIN QUERY ERROR:",
                e
            )

            data = None

        # =================================================
        # USER FOUND
        # =================================================

        if data:

            db_email = str(
                data[1] or ""
            ).strip()

            db_password = str(
                data[2] or ""
            ).strip()

            role = str(
                data[3] or ""
            ).strip().lower()

            print(
                "DB EMAIL:",
                repr(db_email)
            )

            

            print(
                "DB ROLE:",
                repr(role)
            )

            # =================================================
            # PASSWORD CHECK
            # =================================================

            if db_password != password:

                print("==============================================")
                print("PASSWORD DOES NOT MATCH")
                print("==============================================")

                msg = "Invalid Email or Password"

            else:

                print("==============================================")
                print("PASSWORD MATCHED")
                print("ROLE:", role)
                print("==============================================")

                # =================================================
                # ADMIN
                # =================================================

                if role == "admin":

                    request.session["admin"] = db_email

                    request.session.save()

                    print(
                        "ADMIN LOGIN SUCCESS:",
                        db_email
                    )

                    login_cursor.close()
                    login_db.close()

                    return redirect(
                        "/Admin/ADashboard/"
                    )

                # =================================================
                # USER
                # =================================================

                elif role == "user":

                    login_cursor.execute(
                        """
                        SELECT
                            status
                        FROM plant.register
                        WHERE LOWER(TRIM(email)) =
                              LOWER(TRIM(%s))
                        LIMIT 1
                        """,
                        (
                            db_email,
                        )
                    )

                    user_status_row = login_cursor.fetchone()

                    print(
                        "USER STATUS:",
                        user_status_row
                    )

                    if user_status_row:

                        user_status = str(
                            user_status_row[0] or "Active"
                        ).strip().lower()

                        print(
                            "USER STATUS VALUE:",
                            user_status
                        )

                        if user_status == "blocked":

                            if "user" in request.session:

                                del request.session["user"]

                            if "pending_cart_product" in request.session:

                                del request.session[
                                    "pending_cart_product"
                                ]

                            if "pending_cart_quantity" in request.session:

                                del request.session[
                                    "pending_cart_quantity"
                                ]

                            request.session.save()

                            msg = (
                                "Your account has been blocked by the manager."
                            )

                            login_cursor.close()
                            login_db.close()

                            context = navbar_context(request)

                            context["Msg"] = msg

                            return render(
                                request,
                                "store/login.html",
                                context
                            )

                    request.session["user"] = db_email

                    request.session.save()

                    print(
                        "USER LOGIN SUCCESS:",
                        db_email
                    )

                    # =================================================
                    # PENDING CART
                    # =================================================

                    pending_product_id = request.session.get(
                        "pending_cart_product"
                    )

                    pending_quantity = request.session.get(
                        "pending_cart_quantity",
                        1
                    )

                    try:

                        pending_quantity = int(
                            pending_quantity
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        pending_quantity = 1

                    if pending_quantity < 1:

                        pending_quantity = 1

                    print(
                        "PENDING CART PRODUCT:",
                        pending_product_id
                    )

                    print(
                        "PENDING CART QUANTITY:",
                        pending_quantity
                    )

                    if pending_product_id:

                        login_cursor.execute(
                            """
                            SELECT
                                id,
                                name,
                                price,
                                image,
                                stock
                            FROM plant.product
                            WHERE id = %s
                            AND LOWER(TRIM(status)) = 'active'
                            LIMIT 1
                            """,
                            (
                                pending_product_id,
                            )
                        )

                        product = login_cursor.fetchone()

                        print(
                            "PENDING PRODUCT DATA:",
                            product
                        )

                        if product:

                            product_id = product[0]

                            product_name = product[1]

                            price = product[2]

                            image = product[3]

                            stock = product[4]

                            if stock is None:

                                stock = 0

                            stock = int(stock)

                            if stock > 0:

                                if pending_quantity > stock:

                                    pending_quantity = stock

                                login_cursor.execute(
                                    """
                                    SELECT
                                        id,
                                        quantity
                                    FROM plant.cart
                                    WHERE user_email = %s
                                    AND product_id = %s
                                    LIMIT 1
                                    """,
                                    (
                                        db_email,
                                        product_id
                                    )
                                )

                                existing = login_cursor.fetchone()

                                print(
                                    "EXISTING CART ITEM:",
                                    existing
                                )

                                if existing:

                                    cart_id = existing[0]

                                    old_quantity = int(
                                        existing[1] or 0
                                    )

                                    new_quantity = (
                                        old_quantity
                                        + pending_quantity
                                    )

                                    if new_quantity > stock:

                                        new_quantity = stock

                                    new_total = (
                                        price
                                        * new_quantity
                                    )

                                    login_cursor.execute(
                                        """
                                        UPDATE plant.cart
                                        SET
                                            quantity = %s,
                                            total = %s
                                        WHERE id = %s
                                        AND user_email = %s
                                        """,
                                        (
                                            new_quantity,
                                            new_total,
                                            cart_id,
                                            db_email
                                        )
                                    )

                                else:

                                    item_total = (
                                        price
                                        * pending_quantity
                                    )

                                    login_cursor.execute(
                                        """
                                        INSERT INTO plant.cart
                                        (
                                            user_email,
                                            product_id,
                                            product_name,
                                            price,
                                            image,
                                            quantity,
                                            total
                                        )
                                        VALUES
                                        (
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s,
                                            %s
                                        )
                                        """,
                                        (
                                            db_email,
                                            product_id,
                                            product_name,
                                            price,
                                            image,
                                            pending_quantity,
                                            item_total
                                        )
                                    )

                                login_db.commit()

                        if "pending_cart_product" in request.session:

                            del request.session[
                                "pending_cart_product"
                            ]

                        if "pending_cart_quantity" in request.session:

                            del request.session[
                                "pending_cart_quantity"
                            ]

                        request.session.save()

                        login_cursor.close()
                        login_db.close()

                        return redirect(
                            "/User/mycart/"
                        )

                    login_cursor.close()
                    login_db.close()

                    return redirect(
                        "/User/UDashboard/"
                    )

                # =================================================
                # VENDOR
                # =================================================

                elif role == "vendor":

                    request.session["vendor"] = db_email

                    request.session.save()

                    print(
                        "=============================================="
                    )

                    print(
                        "VENDOR LOGIN SUCCESS:",
                        db_email
                    )

                    print(
                        "=============================================="
                    )

                    login_cursor.close()
                    login_db.close()

                    return redirect(
                        "/Vender/VDashboard/"
                    )

                # =================================================
                # MANAGER
                # =================================================

                elif role == "manager":

                    request.session["manager"] = db_email

                    request.session.save()

                    print(
                        "MANAGER LOGIN SUCCESS:",
                        db_email
                    )

                    login_cursor.close()
                    login_db.close()

                    return redirect(
                        "/Manager/MDashboard/"
                    )

                # =================================================
                # INVALID ROLE
                # =================================================

                else:

                    print(
                        "INVALID ROLE:",
                        repr(role)
                    )

                    msg = (
                        "Invalid role in database: "
                        + role
                    )

        else:

            print("==============================================")
            print("EMAIL NOT FOUND IN LOGIN TABLE")
            print("==============================================")

            msg = "Invalid Email or Password"

    # =================================================
    # CLOSE LOGIN CONNECTION
    # =================================================

    try:

        if login_cursor:

            login_cursor.close()

        if login_db:

            login_db.close()

    except Exception as e:

        print(
            "LOGIN CONNECTION CLOSE ERROR:",
            e
        )

    # =================================================
    # LOGIN PAGE
    # =================================================

    context = navbar_context(request)

    context["Msg"] = msg

    return render(
        request,
        "store/login.html",
        context
    )

# =====================================================
# REGISTER
# =====================================================

def register(request):

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        mobile = request.POST.get(
            "mobile",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        address = request.POST.get(
            "address",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        state = request.POST.get(
            "state",
            ""
        ).strip()

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        cursor.execute(
            """
            SELECT *
            FROM register
            WHERE email = %s
            """,
            (
                email,
            )
        )

        existing_user = cursor.fetchone()

        if existing_user:

            context = navbar_context(request)

            context["register_error"] = (
                "This email is already registered."
            )

            return render(
                request,
                "store/login.html",
                context
            )

        cursor.execute(
            """
            INSERT INTO register
            (
                name,
                mobile,
                email,
                password,
                address,
                city,
                state,
                pincode
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
                %s
            )
            """,
            (
                name,
                mobile,
                email,
                password,
                address,
                city,
                state,
                pincode
            )
        )

        cursor.execute(
            """
            INSERT INTO login
            (
                email,
                password,
                role
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                email,
                password,
                "user"
            )
        )

        db.commit()

        context = navbar_context(request)

        context["register_success"] = (
            "Account created successfully. Please login."
        )

        return render(
            request,
            "store/login.html",
            context
        )

    context = navbar_context(request)

    return render(
        request,
        "store/login.html",
        context
    )


# =====================================================
# LOGOUT
# =====================================================

def logout(request):

    request.session.flush()

    return redirect(
        "/login/"
    )


# =====================================================
# PRODUCT DETAIL
# =====================================================

def product_details(request, product_id):

    print("==============================================")
    print("PRODUCT DETAIL PAGE")
    print("PRODUCT ID:", product_id)
    print("==============================================")

    cmd = """
        SELECT
            id,
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
            status,
            created_at
        FROM product
        WHERE id = %s
        AND LOWER(TRIM(status)) = 'active'
    """

    cursor.execute(
        cmd,
        (product_id,)
    )

    row = cursor.fetchone()

    if row is None:

        print(
            "PRODUCT NOT FOUND:",
            product_id
        )

        return redirect(
            "/plant/"
        )

    product = make_product(row)

    # =================================================
    # REVIEW SUBMIT
    # =================================================

    if request.method == "POST":

        rating = request.POST.get(
            "rating",
            ""
        ).strip()

        review_text = request.POST.get(
            "review_text",
            ""
        ).strip()

        user_email = request.session.get(
            "user"
        )

        if not user_email:

            context = navbar_context(request)

            context["product"] = product

            context["review_error"] = (
                "Please login first to submit a review."
            )

            return render(
                request,
                "store/product_details.html",
                context
            )

        if not rating or not review_text:

            context = navbar_context(request)

            context["product"] = product

            context["review_error"] = (
                "Please select a rating and write your review."
            )

            return render(
                request,
                "store/product_details.html",
                context
            )

        try:

            rating = int(
                rating
            )

        except (
            ValueError,
            TypeError
        ):

            context = navbar_context(request)

            context["product"] = product

            context["review_error"] = (
                "Invalid rating."
            )

            return render(
                request,
                "store/product_details.html",
                context
            )

        if rating < 1 or rating > 5:

            context = navbar_context(request)

            context["product"] = product

            context["review_error"] = (
                "Rating must be between 1 and 5."
            )

            return render(
                request,
                "store/product_details.html",
                context
            )

        duplicate_cmd = """
            SELECT
                id
            FROM reviews
            WHERE product_id = %s
            AND user_email = %s
            LIMIT 1
        """

        cursor.execute(
            duplicate_cmd,
            (
                product_id,
                user_email
            )
        )

        existing_review = cursor.fetchone()

        if existing_review:

            context = navbar_context(request)

            context["product"] = product

            context["review_error"] = (
                "You have already reviewed this product."
            )

            review_select = """
                SELECT
                    id,
                    user_name,
                    rating,
                    review_text,
                    created_at
                FROM reviews
                WHERE product_id = %s
                ORDER BY created_at DESC
            """

            cursor.execute(
                review_select,
                (
                    product_id,
                )
            )

            review_rows = cursor.fetchall()

            reviews = []

            for review in review_rows:

                reviews.append(
                    {
                        "id": review[0],
                        "user_name": review[1],
                        "rating": review[2],
                        "review_text": review[3],
                        "created_at": review[4]
                    }
                )

            context["reviews"] = reviews

            avg_cmd = """
                SELECT
                    AVG(rating),
                    COUNT(*)
                FROM reviews
                WHERE product_id = %s
            """

            cursor.execute(
                avg_cmd,
                (
                    product_id,
                )
            )

            avg_row = cursor.fetchone()

            if avg_row and avg_row[0] is not None:

                context["average_rating"] = round(
                    float(avg_row[0]),
                    1
                )

                context["review_count"] = avg_row[1]

            else:

                context["average_rating"] = 0

                context["review_count"] = 0

            filled_count = int(
                context["average_rating"]
            )

            empty_count = 5 - filled_count

            context["filled_stars"] = range(
                filled_count
            )

            context["empty_stars"] = range(
                empty_count
            )

            return render(
                request,
                "store/product_details.html",
                context
            )

        user_cmd = """
            SELECT
                name
            FROM register
            WHERE email = %s
            LIMIT 1
        """

        cursor.execute(
            user_cmd,
            (
                user_email,
            )
        )

        user_row = cursor.fetchone()

        if user_row:

            user_name = user_row[0]

        else:

            user_name = user_email

        review_cmd = """
            INSERT INTO reviews
            (
                product_id,
                user_name,
                user_email,
                rating,
                review_text
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """

        cursor.execute(
            review_cmd,
            (
                product_id,
                user_name,
                user_email,
                rating,
                review_text
            )
        )

        db.commit()

        print("==============================================")
        print("REVIEW ADDED SUCCESSFULLY")
        print("PRODUCT ID:", product_id)
        print("USER:", user_email)
        print("RATING:", rating)
        print("==============================================")

        context = navbar_context(request)

        context["product"] = product

        context["review_success"] = (
            "Your review has been submitted successfully."
        )

    else:

        context = navbar_context(request)

        context["product"] = product

    # =====================================================
    # FETCH EXISTING REVIEWS
    # =====================================================

    review_select = """
        SELECT
            id,
            user_name,
            rating,
            review_text,
            created_at
        FROM reviews
        WHERE product_id = %s
        ORDER BY created_at DESC
    """

    cursor.execute(
        review_select,
        (
            product_id,
        )
    )

    review_rows = cursor.fetchall()

    reviews = []

    for review in review_rows:

        reviews.append(
            {
                "id": review[0],
                "user_name": review[1],
                "rating": review[2],
                "review_text": review[3],
                "created_at": review[4]
            }
        )

    context["reviews"] = reviews

    # =====================================================
    # AVERAGE RATING + REVIEW COUNT
    # =====================================================

    avg_cmd = """
        SELECT
            AVG(rating),
            COUNT(*)
        FROM reviews
        WHERE product_id = %s
    """

    cursor.execute(
        avg_cmd,
        (
            product_id,
        )
    )

    avg_row = cursor.fetchone()

    if avg_row and avg_row[0] is not None:

        context["average_rating"] = round(
            float(avg_row[0]),
            1
        )

        context["review_count"] = avg_row[1]

    else:

        context["average_rating"] = 0

        context["review_count"] = 0

    # =====================================================
    # RATING STARS
    # =====================================================

    filled_count = int(
        context["average_rating"]
    )

    empty_count = 5 - filled_count

    context["filled_stars"] = range(
        filled_count
    )

    context["empty_stars"] = range(
        empty_count
    )

    # =====================================================
    # RENDER PRODUCT DETAIL
    # =====================================================

    return render(
        request,
        "store/product_details.html",
        context
    )