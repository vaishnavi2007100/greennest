from django.shortcuts import render, redirect
from django.contrib import messages

import mysql.connector


# =====================================================
# MYSQL DATABASE CONNECTION
# =====================================================

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="plant",
    port=3306
)

cursor = db.cursor()


# =====================================================
# USER DASHBOARD
# =====================================================

def UDashboard(request):

    # -------------------------------------------------
    # CHECK USER LOGIN
    # -------------------------------------------------

    if "user" not in request.session:
        return redirect("/login/")

    email = request.session["user"]

    # -------------------------------------------------
    # GET USER DATA
    # -------------------------------------------------

    cmd = """
        SELECT name, email, mobile
        FROM register
        WHERE email = %s
    """

    cursor.execute(cmd, (email,))

    user_data = cursor.fetchone()

    # -------------------------------------------------
    # GET USER ADDRESS
    # -------------------------------------------------

    address_cmd = """
        SELECT id, address, city, state, pincode
        FROM user_address
        WHERE email = %s
    """

    cursor.execute(address_cmd, (email,))

    address_data = cursor.fetchone()

    # -------------------------------------------------
    # RENDER
    # -------------------------------------------------

    return render(
        request,
        "store/User/UDashboard.html",
        {
            "user_data": user_data,
            "address_data": address_data
        }
    )



# =====================================================
# VIEW PROFILE
# =====================================================


def viewprofile(request):

    # =====================================================
    # USER LOGIN CHECK
    # =====================================================

    if "user" not in request.session:
        return redirect("/login/")


    # =====================================================
    # LOGGED-IN EMAIL
    # =====================================================

    logged_user = request.session.get("user")

    if isinstance(logged_user, dict):
        user_email = logged_user.get("email")
    else:
        user_email = logged_user


    if not user_email:
        return redirect("/login/")


    # =====================================================
    # DEFAULT
    # =====================================================

    edit_mode = False


    # =====================================================
    # POST REQUEST
    # =====================================================

    if request.method == "POST":

        action = request.POST.get("action")


        # =================================================
        # OPEN EDIT MODE
        # =================================================

        if action == "edit":

            edit_mode = True


        # =================================================
        # CANCEL EDIT
        # =================================================

        elif action == "cancel":

            return redirect(
                "/User/viewprofile/"
            )


        # =================================================
        # SAVE ALL PROFILE
        # =================================================

        elif action == "save":

            # =============================================
            # PROFILE DATA
            # =============================================

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


            # =============================================
            # ADDRESS DATA
            # =============================================

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


            # =============================================
            # VALIDATION
            # =============================================

            if name == "":

                messages.error(
                    request,
                    "Name is required."
                )

                edit_mode = True


            elif new_email == "":

                messages.error(
                    request,
                    "Email is required."
                )

                edit_mode = True


            elif mobile and (
                not mobile.isdigit()
                or len(mobile) != 10
                or mobile[0] not in "6789"
            ):

                messages.error(
                    request,
                    "Please enter a valid 10 digit mobile number."
                )

                edit_mode = True


            elif address == "":

                messages.error(
                    request,
                    "Address is required."
                )

                edit_mode = True


            elif city == "":

                messages.error(
                    request,
                    "City is required."
                )

                edit_mode = True


            elif state == "":

                messages.error(
                    request,
                    "State is required."
                )

                edit_mode = True


            elif (
                not pincode.isdigit()
                or len(pincode) != 6
            ):

                messages.error(
                    request,
                    "Please enter a valid 6 digit pincode."
                )

                edit_mode = True


            else:

                try:

                    # =====================================
                    # CHECK EMAIL CHANGE
                    # =====================================

                    email_changed = (
                        new_email.lower()
                        != user_email.lower()
                    )


                    # =====================================
                    # IF EMAIL CHANGED
                    # =====================================

                    if email_changed:

                        cursor.execute(
                            """
                            SELECT id
                            FROM login
                            WHERE LOWER(TRIM(email))
                                  = LOWER(TRIM(%s))
                            LIMIT 1
                            """,
                            (new_email,)
                        )

                        email_exists = cursor.fetchone()


                        if email_exists:

                            messages.error(
                                request,
                                "This email is already registered."
                            )

                            edit_mode = True

                        else:

                            # =============================
                            # UPDATE REGISTER
                            # =============================

                            cursor.execute(
                                """
                                UPDATE register
                                SET
                                    name = %s,
                                    email = %s,
                                    mobile = %s
                                WHERE LOWER(TRIM(email))
                                      = LOWER(TRIM(%s))
                                """,
                                (
                                    name,
                                    new_email,
                                    mobile,
                                    user_email
                                )
                            )


                            # =============================
                            # UPDATE LOGIN
                            # =============================

                            cursor.execute(
                                """
                                UPDATE login
                                SET email = %s
                                WHERE LOWER(TRIM(email))
                                      = LOWER(TRIM(%s))
                                """,
                                (
                                    new_email,
                                    user_email
                                )
                            )


                            # =============================
                            # UPDATE ADDRESS EMAIL
                            # =============================

                            cursor.execute(
                                """
                                UPDATE user_address
                                SET email = %s
                                WHERE LOWER(TRIM(email))
                                      = LOWER(TRIM(%s))
                                """,
                                (
                                    new_email,
                                    user_email
                                )
                            )


                            # =============================
                            # UPDATE REVIEWS EMAIL
                            # =============================

                            cursor.execute(
                                """
                                UPDATE reviews
                                SET user_email = %s
                                WHERE LOWER(TRIM(user_email))
                                      = LOWER(TRIM(%s))
                                """,
                                (
                                    new_email,
                                    user_email
                                )
                            )


                            # =============================
                            # UPDATE CART EMAIL
                            # =============================

                            cursor.execute(
                                """
                                UPDATE cart
                                SET user_email = %s
                                WHERE LOWER(TRIM(user_email))
                                      = LOWER(TRIM(%s))
                                """,
                                (
                                    new_email,
                                    user_email
                                )
                            )


                            # =============================
                            # UPDATE WISHLIST EMAIL
                            # =============================

                            cursor.execute(
                                """
                                UPDATE wishlist
                                SET user_email = %s
                                WHERE LOWER(TRIM(user_email))
                                      = LOWER(TRIM(%s))
                                """,
                                (
                                    new_email,
                                    user_email
                                )
                            )


                            # =============================
                            # UPDATE ORDERS EMAIL
                            # =============================

                            cursor.execute(
                                """
                                UPDATE orders
                                SET user_email = %s
                                WHERE LOWER(TRIM(user_email))
                                      = LOWER(TRIM(%s))
                                """,
                                (
                                    new_email,
                                    user_email
                                )
                            )


                            current_email = new_email


                    # =====================================
                    # SAME EMAIL
                    # =====================================

                    else:

                        cursor.execute(
                            """
                            UPDATE register
                            SET
                                name = %s,
                                mobile = %s
                            WHERE LOWER(TRIM(email))
                                  = LOWER(TRIM(%s))
                            """,
                            (
                                name,
                                mobile,
                                user_email
                            )
                        )


                        current_email = user_email


                    # =====================================
                    # GET EXISTING ADDRESS
                    # =====================================

                    cursor.execute(
                        """
                        SELECT id
                        FROM user_address
                        WHERE LOWER(TRIM(email))
                              = LOWER(TRIM(%s))
                        ORDER BY id DESC
                        LIMIT 1
                        """,
                        (current_email,)
                    )

                    existing_address = cursor.fetchone()


                    # =====================================
                    # UPDATE ADDRESS
                    # =====================================

                    if existing_address:

                        cursor.execute(
                            """
                            UPDATE user_address
                            SET
                                address = %s,
                                city = %s,
                                state = %s,
                                pincode = %s
                            WHERE id = %s
                            """,
                            (
                                address,
                                city,
                                state,
                                pincode,
                                existing_address[0]
                            )
                        )


                    # =====================================
                    # INSERT ADDRESS
                    # =====================================

                    else:

                        cursor.execute(
                            """
                            INSERT INTO user_address
                            (
                                email,
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
                                %s
                            )
                            """,
                            (
                                current_email,
                                address,
                                city,
                                state,
                                pincode
                            )
                        )


                    # =====================================
                    # COMMIT
                    # =====================================

                    db.commit()


                    # =====================================
                    # UPDATE SESSION
                    # =====================================

                    request.session["user"] = current_email

                    request.session.save()


                    # =====================================
                    # SUCCESS
                    # =====================================

                    messages.success(
                        request,
                        "Profile updated successfully."
                    )


                    return redirect(
                        "/User/viewprofile/"
                    )


                except Exception as e:

                    db.rollback()

                    print(
                        "UPDATE PROFILE ERROR:",
                        e
                    )

                    messages.error(
                        request,
                        "Profile update failed."
                    )

                    edit_mode = True


    # =====================================================
    # GET USER PROFILE
    # =====================================================

    user_data = None

    try:

        cursor.execute(
            """
            SELECT
                name,
                email,
                mobile
            FROM register
            WHERE LOWER(TRIM(email))
                  = LOWER(TRIM(%s))
            LIMIT 1
            """,
            (user_email,)
        )

        user_data = cursor.fetchone()

    except Exception as e:

        print(
            "VIEW PROFILE ERROR:",
            e
        )


    # =====================================================
    # GET ADDRESS
    # =====================================================

    address_data = None

    try:

        cursor.execute(
            """
            SELECT
                id,
                address,
                city,
                state,
                pincode
            FROM user_address
            WHERE LOWER(TRIM(email))
                  = LOWER(TRIM(%s))
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_email,)
        )

        address_data = cursor.fetchone()

    except Exception as e:

        print(
            "VIEW PROFILE ADDRESS ERROR:",
            e
        )


    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "store/User/viewprofile.html",
        {
            "user_data": user_data,
            "address_data": address_data,
            "edit_mode": edit_mode
        }
    )


# =====================================================
# MY ADDRESS
# =====================================================

def MyAddress(request):

    # -------------------------------------------------
    # CHECK USER LOGIN
    # -------------------------------------------------

    if "user" not in request.session:
        return redirect("/login/")

    email = request.session["user"]

    edit_mode = False

    # =================================================
    # POST
    # =================================================

    if request.method == "POST":

        action = request.POST.get("action")

        # -------------------------------------------------
        # EDIT
        # -------------------------------------------------

        if action == "edit":

            edit_mode = True

        # -------------------------------------------------
        # CANCEL
        # -------------------------------------------------

        elif action == "cancel":

            edit_mode = False

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        elif action == "save":

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

            # -------------------------------------------------
            # VALIDATION
            # -------------------------------------------------

            if (
                address == ""
                or city == ""
                or state == ""
                or pincode == ""
            ):

                messages.error(
                    request,
                    "All address fields are required."
                )

                edit_mode = True

            elif not pincode.isdigit() or len(pincode) != 6:

                messages.error(
                    request,
                    "Please enter a valid 6 digit pincode."
                )

                edit_mode = True

            else:

                # -------------------------------------------------
                # CHECK EXISTING ADDRESS
                # -------------------------------------------------

                check_address = """
                    SELECT id
                    FROM user_address
                    WHERE email = %s
                """

                cursor.execute(
                    check_address,
                    (email,)
                )

                existing_address = cursor.fetchone()

                # -------------------------------------------------
                # UPDATE ADDRESS
                # -------------------------------------------------

                if existing_address:

                    update_address = """
                        UPDATE user_address
                        SET address = %s,
                            city = %s,
                            state = %s,
                            pincode = %s
                        WHERE email = %s
                    """

                    cursor.execute(
                        update_address,
                        (
                            address,
                            city,
                            state,
                            pincode,
                            email
                        )
                    )

                    messages.success(
                        request,
                        "Address updated successfully."
                    )

                # -------------------------------------------------
                # INSERT ADDRESS
                # -------------------------------------------------

                else:

                    insert_address = """
                        INSERT INTO user_address
                        (
                            email,
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
                            %s
                        )
                    """

                    cursor.execute(
                        insert_address,
                        (
                            email,
                            address,
                            city,
                            state,
                            pincode
                        )
                    )

                    messages.success(
                        request,
                        "Address added successfully."
                    )

                # -------------------------------------------------
                # COMMIT
                # -------------------------------------------------

                db.commit()

                return redirect(
                    "/User/MyAddress/"
                )

    # =================================================
    # GET ADDRESS
    # =================================================

    address_query = """
        SELECT id, address, city, state, pincode
        FROM user_address
        WHERE email = %s
    """

    cursor.execute(
        address_query,
        (email,)
    )

    address_data = cursor.fetchone()

    # -------------------------------------------------
    # ADDRESS NOT AVAILABLE
    # -------------------------------------------------

    if address_data is None:

        edit_mode = True

    # =================================================
    # RENDER
    # =================================================

    return render(
        request,
        "store/User/MyAddress.html",
        {
            "address_data": address_data,
            "edit_mode": edit_mode
        }
    )


# =====================================================
# CHANGE PASSWORD
# =====================================================

def changepassword(request):

    # -------------------------------------------------
    # CHECK USER LOGIN
    # -------------------------------------------------

    if "user" not in request.session:
        return redirect("/login/")

    email = request.session["user"]

    msg = ""
    success = ""

    # =================================================
    # POST
    # =================================================

    if request.method == "POST":

        current_password = request.POST.get(
            "current_password",
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

        # =================================================
        # GET CURRENT PASSWORD
        # =================================================

        cmd = """
            SELECT password
            FROM login
            WHERE email = %s
        """

        cursor.execute(
            cmd,
            (email,)
        )

        data = cursor.fetchone()

        if not data:

            msg = "User account not found."

        else:

            database_password = data[0]

            # -------------------------------------------------
            # CURRENT PASSWORD
            # -------------------------------------------------

            if current_password != database_password:

                msg = "Current password is incorrect."

            # -------------------------------------------------
            # NEW PASSWORD
            # -------------------------------------------------

            elif new_password == "":

                msg = "New password is required."

            # -------------------------------------------------
            # CONFIRM PASSWORD
            # -------------------------------------------------

            elif new_password != confirm_password:

                msg = "New password and confirm password do not match."

            # -------------------------------------------------
            # SAME PASSWORD
            # -------------------------------------------------

            elif current_password == new_password:

                msg = "New password must be different from current password."

            # -------------------------------------------------
            # UPDATE PASSWORD
            # -------------------------------------------------

            else:

                # -------------------------------------------------
                # UPDATE LOGIN
                # -------------------------------------------------

                cmd = """
                    UPDATE login
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

                # -------------------------------------------------
                # UPDATE REGISTER
                # -------------------------------------------------

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

                success = "Password changed successfully."

    # =================================================
    # RENDER
    # =================================================

    return render(
        request,
        "store/User/changepassword.html",
        {
            "Msg": msg,
            "Success": success
        }
    )


# =====================================================
# USER LOGOUT
# =====================================================

def logout(request):

    request.session.flush()

    return redirect("/login/")


# =====================================================
# MY CART
# =====================================================

def mycart(request):

    # -------------------------------------------------
    # CHECK USER LOGIN
    # -------------------------------------------------

    if "user" not in request.session:
        return redirect("/login/")

    user_email = request.session["user"]

    # =================================================
    # POST
    # =================================================

    if request.method == "POST":

        action = request.POST.get("action")

        cart_id = request.POST.get("cart_id")

        # -------------------------------------------------
        # VALIDATE CART ID
        # -------------------------------------------------

        if not cart_id or not cart_id.isdigit():

            return redirect(
                "/User/mycart/"
            )

        # =================================================
        # REMOVE
        # =================================================

        if action == "remove":

            cmd = (
                "DELETE FROM cart "
                "WHERE id = " + cart_id +
                " AND user_email = %s"
            )

            cursor.execute(
                cmd,
                (user_email,)
            )

            db.commit()

            return redirect(
                "/User/mycart/"
            )

        # =================================================
        # INCREASE
        # =================================================

        elif action == "increase":

            cmd = (
                "UPDATE cart "
                "SET quantity = quantity + 1 "
                "WHERE id = " + cart_id +
                " AND user_email = %s"
            )

            cursor.execute(
                cmd,
                (user_email,)
            )

            # -------------------------------------------------
            # UPDATE TOTAL
            # -------------------------------------------------

            cmd = (
                "UPDATE cart "
                "SET total = price * quantity "
                "WHERE id = " + cart_id +
                " AND user_email = %s"
            )

            cursor.execute(
                cmd,
                (user_email,)
            )

            db.commit()

            return redirect(
                "/User/mycart/"
            )

        # =================================================
        # DECREASE
        # =================================================

        elif action == "decrease":

            cmd = (
                "UPDATE cart "
                "SET quantity = quantity - 1 "
                "WHERE id = " + cart_id +
                " AND user_email = %s "
                "AND quantity > 1"
            )

            cursor.execute(
                cmd,
                (user_email,)
            )

            # -------------------------------------------------
            # UPDATE TOTAL
            # -------------------------------------------------

            cmd = (
                "UPDATE cart "
                "SET total = price * quantity "
                "WHERE id = " + cart_id +
                " AND user_email = %s"
            )

            cursor.execute(
                cmd,
                (user_email,)
            )

            db.commit()

            return redirect(
                "/User/mycart/"
            )

    # =================================================
    # GET CART
    # =================================================

    cmd = """
        SELECT
            id,
            product_id,
            product_name,
            price,
            image,
            quantity,
            total,
            created_at
        FROM cart
        WHERE user_email = %s
        ORDER BY id DESC
    """

    cursor.execute(
        cmd,
        (user_email,)
    )

    rows = cursor.fetchall()

    # =================================================
    # CART ITEMS
    # =================================================

    cart_items = []

    total = 0

    for row in rows:

        cart_items.append(
            {
                "id": row[0],
                "product_id": row[1],
                "product_name": row[2],
                "price": row[3],
                "image": row[4],
                "quantity": row[5],
                "total": row[6],
                "created_at": row[7]
            }
        )

        total = total + float(row[6])

    # =================================================
    # RENDER
    # =================================================

    return render(
        request,
        "store/User/mycart.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )


# =====================================================
# ADD TO CART
# =====================================================

def AddToCart(request, product_id):

    if "user" not in request.session:
        quantity_value = request.POST.get("quantity", "1")

        try:
            quantity = int(quantity_value)
        except (ValueError, TypeError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        request.session["pending_cart_product"] = product_id
        request.session["pending_cart_quantity"] = quantity
        request.session["pending_cart_url"] = request.META.get(
            "HTTP_REFERER",
            f"/product/{product_id}/"
        )
        request.session.save()

        return redirect("/login/")

    user_email = request.session["user"]

    try:
        add_db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="plant",
            port=3306
        )
        add_cursor = add_db.cursor()

        try:
            quantity = int(request.POST.get("quantity", "1"))
        except (ValueError, TypeError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        add_cursor.execute(
            """
            SELECT
                id,
                name,
                price,
                image,
                stock,
                status
            FROM `plant`.`product`
            WHERE id = %s
            AND LOWER(TRIM(status)) = 'active'
            LIMIT 1
            """,
            (product_id,)
        )

        product = add_cursor.fetchone()

        if not product:
            messages.error(request, "Product not found.")
            return redirect("/plant/")

        product_id_db = product[0]
        product_name = product[1]
        price = product[2]
        image = product[3]
        stock = product[4]

        if stock is None or int(stock) <= 0:
            messages.error(request, "This product is out of stock.")
            return redirect(f"/product/{product_id_db}/")

        stock = int(stock)

        if quantity > stock:
            quantity = stock

        add_cursor.execute(
            """
            SELECT id, quantity
            FROM cart
            WHERE user_email = %s
            AND product_id = %s
            LIMIT 1
            """,
            (user_email, product_id_db)
        )

        existing_cart = add_cursor.fetchone()

        if existing_cart:
            cart_id = existing_cart[0]
            old_quantity = int(existing_cart[1] or 0)
            new_quantity = old_quantity + quantity

            if new_quantity > stock:
                new_quantity = stock

            add_cursor.execute(
                """
                UPDATE cart
                SET quantity = %s,
                    total = price * %s
                WHERE id = %s
                AND user_email = %s
                """,
                (
                    new_quantity,
                    new_quantity,
                    cart_id,
                    user_email
                )
            )

        else:
            total = price * quantity

            add_cursor.execute(
                """
                INSERT INTO cart
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
                    user_email,
                    product_id_db,
                    product_name,
                    price,
                    image,
                    quantity,
                    total
                )
            )

        add_db.commit()

        return redirect("/User/mycart/")

    except Exception as e:
        if "add_db" in locals() and add_db:
            add_db.rollback()

        print("ADD TO CART ERROR:", e)
        messages.error(request, "Unable to add product to cart.")
        return redirect(f"/product/{product_id}/")

    finally:
        if "add_cursor" in locals() and add_cursor:
            add_cursor.close()

        if "add_db" in locals() and add_db:
            add_db.close()





# =====================================================
# ADD TO WISHLIST
# =====================================================

def AddToWishlist(request, product_id):

    # -------------------------------------------------
    # CHECK USER LOGIN
    # -------------------------------------------------

    if "user" not in request.session:
        return redirect("/login/")

    user_email = request.session["user"]

    # =================================================
    # GET PRODUCT
    # IMPORTANT:
    # product table me "name" column hai
    # =================================================

    cmd = """
        SELECT
            id,
            name,
            price,
            image
        FROM product
        WHERE id = %s
    """

    cursor.execute(
        cmd,
        (product_id,)
    )

    product = cursor.fetchone()

    # -------------------------------------------------
    # PRODUCT NOT FOUND
    # -------------------------------------------------

    if product is None:

        return redirect(
            "/plant/"
        )

    # =================================================
    # PRODUCT DATA
    # =================================================

    product_id = product[0]

    product_name = product[1]

    price = product[2]

    image = product[3]

    # =================================================
    # CHECK EXISTING WISHLIST
    # =================================================

    cmd = """
        SELECT id
        FROM wishlist
        WHERE user_email = %s
        AND product_id = %s
    """

    cursor.execute(
        cmd,
        (
            user_email,
            product_id
        )
    )

    existing = cursor.fetchone()

    # =================================================
    # ALREADY IN WISHLIST
    # =================================================

    if existing:

        return redirect(
            "/User/wishlist/"
        )

    # =================================================
    # INSERT WISHLIST
    # =================================================

    cmd = """
        INSERT INTO wishlist
        (
            user_email,
            product_id,
            product_name,
            price,
            image
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
        cmd,
        (
            user_email,
            product_id,
            product_name,
            price,
            image
        )
    )

    # -------------------------------------------------
    # COMMIT
    # -------------------------------------------------

    db.commit()

    return redirect(
        "/User/wishlist/"
    )



# =====================================================
#                     MY WISHLIST
# =====================================================

def wishlist(request):

    # -------------------------------------------------
    # CHECK USER LOGIN
    # -------------------------------------------------

    if "user" not in request.session:
        return redirect("/login/")

    user_email = request.session["user"]


    # =================================================
    # POST REQUEST
    # =================================================

    if request.method == "POST":

        action = request.POST.get("action")

        wishlist_id = request.POST.get("wishlist_id")


        # =================================================
        # REMOVE WISHLIST ITEM
        # =================================================

        if action == "remove":

            # ---------------------------------------------
            # CHECK WISHLIST ID
            # ---------------------------------------------

            if wishlist_id and wishlist_id.isdigit():

                cmd = """
                    DELETE FROM wishlist
                    WHERE id = %s
                    AND user_email = %s
                """

                cursor.execute(
                    cmd,
                    (
                        int(wishlist_id),
                        user_email
                    )
                )

                # -----------------------------------------
                # SAVE DELETE
                # -----------------------------------------

                db.commit()


            # ---------------------------------------------
            # GO BACK TO WISHLIST
            # ---------------------------------------------

            return redirect(
                "/User/wishlist/"
            )


    # =================================================
    # GET WISHLIST DATA
    # =================================================

    cmd = """
        SELECT
            id,
            product_id,
            product_name,
            price,
            image,
            created_at
        FROM wishlist
        WHERE user_email = %s
        ORDER BY id DESC
    """

    cursor.execute(
        cmd,
        (user_email,)
    )

    rows = cursor.fetchall()


    # =================================================
    # CREATE WISHLIST ITEMS
    # =================================================

    wishlist_items = []


    for row in rows:

        wishlist_items.append(
            {
                "id": row[0],
                "product_id": row[1],
                "product_name": row[2],
                "price": row[3],
                "image": row[4],
                "created_at": row[5]
            }
        )


    # =================================================
    # RENDER WISHLIST
    # =================================================

    return render(
        request,
        "store/User/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )
# =====================================================
#                     MY ORDERS
# =====================================================

def myorders(request):

    # -------------------------------------------------
    # CHECK USER LOGIN
    # -------------------------------------------------

    if "user" not in request.session:
        return redirect("/login/")

    user_email = request.session["user"]


    # =================================================
    # GET CUSTOMER + ADDRESS DETAILS
    # =================================================

    user_cmd = """
        SELECT
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

        FROM register r

        LEFT JOIN user_address ua
            ON r.email = ua.email

        WHERE r.email = %s

        LIMIT 1
    """

    cursor.execute(user_cmd, (user_email,))

    user_row = cursor.fetchone()


    # =================================================
    # DEFAULT VALUES
    # =================================================

    user_name = ""
    user_mobile = ""
    user_address = ""
    user_city = ""
    user_state = ""
    user_pincode = ""


    # =================================================
    # CUSTOMER DATA
    # =================================================

    if user_row:

        user_name = user_row[0]
        user_email = user_row[1]
        user_mobile = user_row[2]

        user_address = user_row[3]
        user_city = user_row[4]
        user_state = user_row[5]
        user_pincode = user_row[6]


    # =================================================
    # GET ORDERS
    # =================================================

    cmd = """
        SELECT
            id,
            product_id,
            product_name,
            price,
            image,
            quantity,
            total,
            status,
            payment_method,
            created_at
        FROM orders
        WHERE user_email = %s
        ORDER BY id DESC
    """

    cursor.execute(cmd, (user_email,))

    rows = cursor.fetchall()


    # =================================================
    # ORDER ITEMS
    # =================================================

    order_items = []


    for row in rows:

        order_items.append(
            {
                "id": row[0],
                "product_id": row[1],
                "product_name": row[2],
                "price": row[3],
                "image": row[4],
                "quantity": row[5],
                "total": row[6],
                "status": row[7],

                # PAYMENT METHOD
                "payment_method": row[8],

                "created_at": row[9],

                # CUSTOMER
                "name": user_name,
                "email": user_email,
                "mobile": user_mobile,

                # ADDRESS
                "address": user_address,
                "city": user_city,
                "state": user_state,
                "pincode": user_pincode
            }
        )


    # =================================================
    # RENDER
    # =================================================

    return render(
        request,
        "store/User/myorders.html",
        {
            "order_items": order_items,

            "user_name": user_name,
            "user_email": user_email,
            "user_mobile": user_mobile,

            "user_address": user_address,
            "user_city": user_city,
            "user_state": user_state,
            "user_pincode": user_pincode
        }
    )
# =========================================================
#                    PLACE ORDER
# =========================================================

def placeorder(request):

    if "user" not in request.session:
        return redirect("/login/")

    user_email = request.session["user"]

    if request.method != "POST":
        return redirect("/User/mycart/")


    # =================================================
    # GET PAYMENT METHOD
    # =================================================

    payment_method = request.POST.get(
        "payment_method",
        "Cash on Delivery"
    )


    # =================================================
    # GET USER CART ITEMS
    # =================================================

    cmd = """
        SELECT
            product_id,
            product_name,
            price,
            image,
            quantity,
            total
        FROM cart
        WHERE user_email = %s
    """

    cursor.execute(cmd, (user_email,))

    cart_items = cursor.fetchall()


    # =================================================
    # CART EMPTY
    # =================================================

    if not cart_items:

        return redirect("/User/mycart/")


    # =================================================
    # INSERT EVERY CART ITEM INTO ORDERS
    # =================================================

    for row in cart_items:

        product_id = row[0]
        product_name = row[1]
        price = row[2]
        image = row[3]
        quantity = row[4]
        total = row[5]


        cmd = """
            INSERT INTO orders
            (
                user_email,
                product_id,
                product_name,
                price,
                image,
                quantity,
                total,
                status,
                payment_method
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
                %s
            )
        """


        cursor.execute(
            cmd,
            (
                user_email,
                product_id,
                product_name,
                price,
                image,
                quantity,
                total,
                "Pending",
                payment_method
            )
        )


    # =================================================
    # REMOVE CART ITEMS
    # =================================================

    cmd = """
        DELETE FROM cart
        WHERE user_email = %s
    """

    cursor.execute(cmd, (user_email,))


    # =================================================
    # SAVE
    # =================================================

    db.commit()


    # =================================================
    # GO TO MY ORDERS
    # =================================================

    return redirect("/User/myorders/")

# =====================================================
# CANCEL ORDER
# =====================================================

def cancelorder(request, order_id):

    if "user" not in request.session:
        return redirect("/login/")

    user_email = request.session["user"]

    if request.method != "POST":
        return redirect("/User/myorders/")

    cancel_reason = request.POST.get(
        "cancel_reason",
        ""
    ).strip()

    # =================================================
    # REASON REQUIRED
    # =================================================

    if cancel_reason == "":

        messages.error(
            request,
            "Please enter a cancellation reason."
        )

        return redirect("/User/myorders/")

    try:

        # =============================================
        # GET ORDER
        # =============================================

        cmd = """
            SELECT
                id,
                status,
                product_id,
                quantity
            FROM orders
            WHERE id = %s
              AND user_email = %s
            LIMIT 1
        """

        cursor.execute(
            cmd,
            (
                order_id,
                user_email
            )
        )

        order = cursor.fetchone()

        # =============================================
        # ORDER NOT FOUND
        # =============================================

        if not order:

            messages.error(
                request,
                "Order not found."
            )

            return redirect("/User/myorders/")


        order_id_db = order[0]
        order_status = order[1]
        product_id = order[2]
        quantity = order[3]


        # =============================================
        # CHECK STATUS
        # =============================================

        status = str(
            order_status or ""
        ).strip().lower()

        if status not in [
            "pending",
            "approved"
        ]:

            messages.error(
                request,
                "This order cannot be cancelled after shipping."
            )

            return redirect("/User/myorders/")


        # =============================================
        # CANCEL ORDER + SAVE REASON
        # =============================================

        update_order = """
            UPDATE orders
            SET
                status = 'Cancelled',
                cancel_reason = %s
            WHERE id = %s
              AND user_email = %s
              AND LOWER(TRIM(status))
                  IN ('pending', 'approved')
        """

        cursor.execute(
            update_order,
            (
                cancel_reason,
                order_id_db,
                user_email
            )
        )


        # =============================================
        # RESTORE STOCK
        # =============================================

        if cursor.rowcount == 1:

            restore_stock = """
                UPDATE product
                SET stock = stock + %s
                WHERE id = %s
            """

            cursor.execute(
                restore_stock,
                (
                    quantity,
                    product_id
                )
            )

            db.commit()

            messages.success(
                request,
                "Order cancelled successfully."
            )

        else:

            db.rollback()

            messages.error(
                request,
                "Order could not be cancelled."
            )


    except Exception as e:

        db.rollback()

        print(
            "CANCEL ORDER ERROR:",
            e
        )

        messages.error(
            request,
            "Unable to cancel order."
        )


    return redirect(
        "/User/myorders/"
    )
# =====================================================
# BUY NOW / CHECKOUT
# =====================================================

def BuyNow(request, product_id):

    # -------------------------------------------------
    # CHECK USER LOGIN
    # -------------------------------------------------

    if "user" not in request.session:
        return redirect("/login/")

    email = request.session["user"]

    buy_db = None
    buy_cursor = None

    try:

        # =================================================
        # DATABASE CONNECTION
        # =================================================

        buy_db = mysql.connector.connect(
            host="",
            user="root",
            password="",
            database="plant",
            port=3306,
            connection_timeout=10
        )

        buy_cursor = buy_db.cursor(dictionary=True)

        # =================================================
        # GET QUANTITY
        # =================================================

        quantity_value = (
            request.POST.get("quantity")
            or request.GET.get("quantity")
            or "1"
        )

        try:
            quantity = int(quantity_value)
        except (ValueError, TypeError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        # =================================================
        # GET PRODUCT
        # =================================================

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
            WHERE id = %s
              AND LOWER(TRIM(status)) = 'active'
            LIMIT 1
        """

        buy_cursor.execute(
            product_query,
            (product_id,)
        )

        product = buy_cursor.fetchone()

        # -------------------------------------------------
        # PRODUCT NOT FOUND
        # -------------------------------------------------

        if not product:

            messages.error(
                request,
                "Product not found."
            )

            return redirect("/plant/")

        # =================================================
        # STOCK
        # =================================================

        stock = product.get("stock") or 0

        try:
            stock = int(stock)
        except (ValueError, TypeError):
            stock = 0

        if stock <= 0:

            messages.error(
                request,
                "This product is currently out of stock."
            )

            return redirect(
                f"/product/{product_id}/"
            )

        # -------------------------------------------------
        # LIMIT QUANTITY
        # -------------------------------------------------

        if quantity > stock:

            quantity = stock

            messages.warning(
                request,
                f"Only {stock} item(s) are available."
            )

        # =================================================
        # PRICE
        # =================================================

        price = product.get("price") or 0

        try:
            price = float(price)
        except (ValueError, TypeError):
            price = 0

        total = price * quantity

        # =================================================
        # GET USER ADDRESS
        # =================================================

        address_query = """
            SELECT
                id,
                email,
                address,
                city,
                state,
                pincode
            FROM user_address
            WHERE email = %s
            LIMIT 1
        """

        buy_cursor.execute(
            address_query,
            (email,)
        )

        address = buy_cursor.fetchone()

        # =================================================
        # GET REQUEST METHOD
        # =================================================

        # =================================================
        # GET = SHOW CHECKOUT
        # =================================================

        if request.method == "GET":

            return render(
                request,
                "store/User/checkout.html",
                {
                    "product": product,
                    "quantity": quantity,
                    "total": total,
                    "address": address,
                    "user_email": email
                }
            )

        # =================================================
        # POST = PLACE ORDER
        # =================================================

        if request.method == "POST":

            # -------------------------------------------------
            # ADDRESS REQUIRED
            # -------------------------------------------------

            if not address:

                messages.error(
                    request,
                    "Please add your delivery address first."
                )

                return redirect(
                    "/User/MyAddress/"
                )

            # =================================================
            # PAYMENT METHOD
            # =================================================

            payment_method = request.POST.get(
                "payment_method",
                "Cash on Delivery"
            ).strip()

            allowed_payment_methods = [
                "Cash on Delivery",
                "UPI",
                "Card",
                "Net Banking"
            ]

            if payment_method not in allowed_payment_methods:

                messages.error(
                    request,
                    "Please select a valid payment method."
                )

                return redirect(
                    f"/User/BuyNow/{product_id}/?quantity={quantity}"
                )

            # =================================================
            # ONLINE PAYMENT DEMO VALIDATION
            # =================================================

            if payment_method == "UPI":

                upi_id = request.POST.get(
                    "upi_id",
                    ""
                ).strip()

                if not upi_id:

                    messages.error(
                        request,
                        "Please enter your UPI ID."
                    )

                    return redirect(
                        f"/User/BuyNow/{product_id}/?quantity={quantity}"
                    )

            elif payment_method == "Card":

                card_number = request.POST.get(
                    "card_number",
                    ""
                ).replace(" ", "").strip()

                card_name = request.POST.get(
                    "card_name",
                    ""
                ).strip()

                expiry = request.POST.get(
                    "expiry",
                    ""
                ).strip()

                cvv = request.POST.get(
                    "cvv",
                    ""
                ).strip()

                if (
                    not card_number
                    or not card_name
                    or not expiry
                    or not cvv
                ):

                    messages.error(
                        request,
                        "Please enter complete card details."
                    )

                    return redirect(
                        f"/User/BuyNow/{product_id}/?quantity={quantity}"
                    )

                if not card_number.isdigit() or len(card_number) != 16:

                    messages.error(
                        request,
                        "Please enter a valid 16 digit card number."
                    )

                    return redirect(
                        f"/User/BuyNow/{product_id}/?quantity={quantity}"
                    )

                if not cvv.isdigit() or len(cvv) != 3:

                    messages.error(
                        request,
                        "Please enter a valid 3 digit CVV."
                    )

                    return redirect(
                        f"/User/BuyNow/{product_id}/?quantity={quantity}"
                    )

            elif payment_method == "Net Banking":

                bank_name = request.POST.get(
                    "bank_name",
                    ""
                ).strip()

                if not bank_name:

                    messages.error(
                        request,
                        "Please select your bank."
                    )

                    return redirect(
                        f"/User/BuyNow/{product_id}/?quantity={quantity}"
                    )

            # =================================================
            # CHECK STOCK AGAIN
            # =================================================

            stock_check_query = """
                SELECT stock
                FROM product
                WHERE id = %s
                  AND LOWER(TRIM(status)) = 'active'
                FOR UPDATE
            """

            buy_cursor.execute(
                stock_check_query,
                (product_id,)
            )

            stock_row = buy_cursor.fetchone()

            if not stock_row:

                buy_db.rollback()

                messages.error(
                    request,
                    "Product is no longer available."
                )

                return redirect(
                    f"/product/{product_id}/"
                )

            current_stock = stock_row.get("stock") or 0

            try:
                current_stock = int(current_stock)
            except (ValueError, TypeError):
                current_stock = 0

            if current_stock < quantity:

                buy_db.rollback()

                messages.error(
                    request,
                    f"Only {current_stock} item(s) are available."
                )

                return redirect(
                    f"/product/{product_id}/"
                )

            # =================================================
            # UPDATE STOCK
            # =================================================

            update_stock_query = """
                UPDATE product
                SET stock = stock - %s
                WHERE id = %s
                  AND stock >= %s
            """

            buy_cursor.execute(
                update_stock_query,
                (
                    quantity,
                    product_id,
                    quantity
                )
            )

            if buy_cursor.rowcount != 1:

                buy_db.rollback()

                messages.error(
                    request,
                    "Unable to place order. Please try again."
                )

                return redirect(
                    f"/product/{product_id}/"
                )

            # =================================================
            # ORDER STATUS
            # =================================================

            if payment_method == "Cash on Delivery":

                order_status = "Pending"

            else:

                # Demo online payment
                order_status = "Pending"

            # =================================================
            # INSERT ORDER
            # =================================================

            order_query = """
                INSERT INTO orders
                (
                    user_email,
                    product_id,
                    product_name,
                    price,
                    image,
                    quantity,
                    total,
                    status,
                    payment_method,
                    created_at
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
                    NOW()
                )
            """

            buy_cursor.execute(
                order_query,
                (
                    email,
                    product_id,
                    product["name"],
                    price,
                    product.get("image"),
                    quantity,
                    total,
                    order_status,
                    payment_method
                )
            )

            # =================================================
            # COMMIT
            # =================================================

            buy_db.commit()

            messages.success(
                request,
                f"Order placed successfully using {payment_method}!"
            )

            return redirect(
                "/User/myorders/"
            )

    # =================================================
    # ERROR
    # =================================================

    except Exception as e:

        print(
            "BUY NOW / CHECKOUT ERROR:",
            repr(e)
        )

        if buy_db:

            try:
                buy_db.rollback()
            except Exception:
                pass

        messages.error(
            request,
            "Something went wrong while processing your order."
        )

        return redirect(
            f"/product/{product_id}/"
        )

    # =================================================
    # CLOSE DATABASE
    # =================================================

    finally:

        if buy_cursor:

            try:
                buy_cursor.close()
            except Exception:
                pass

        if buy_db:

            try:
                buy_db.close()
            except Exception:
                pass
# =========================================================
# USER CONTACT MESSAGES
# =========================================================

def MyMessages(request):

    # Check user login
    if "user" not in request.session:
        return redirect("/login/")

    user_email = request.session["user"]

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
        WHERE email = %s
        ORDER BY id DESC
    """

    cursor.execute(cmd, (user_email,))
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
        "store/User/MyMessages.html",
        {
            "contacts": contacts
        }
    )
# =====================================================
#                     MY RATINGS
# =====================================================

def MyRatings(request):

    # -------------------------------------------------
    # CHECK USER LOGIN
    # -------------------------------------------------

    if "user" not in request.session:
        return redirect("/login/")

    user_email = request.session["user"]

    # =================================================
    # GET USER REVIEWS
    # =================================================

    cmd = """
        SELECT
            id,
            product_id,
            rating,
            review_text,
            created_at
        FROM reviews
        WHERE user_email = %s
        ORDER BY id DESC
    """

    cursor.execute(
        cmd,
        (user_email,)
    )

    rows = cursor.fetchall()

    # =================================================
    # CREATE RATING LIST
    # =================================================

    ratings = []

    for row in rows:

        ratings.append(
            {
                "id": row[0],
                "product_id": row[1],
                "rating": row[2],
                "review_text": row[3],
                "created_at": row[4]
            }
        )

    # =================================================
    # RENDER
    # =================================================

    return render(
        request,
        "store/User/MyRatings.html",
        {
            "ratings": ratings
        }
    )