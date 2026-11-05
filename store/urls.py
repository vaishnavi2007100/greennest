from django.urls import path

from . import views
from . import UserView
from . import AdminView
from . import Managerview
from . import Venderview


urlpatterns = [

    # =========================================================
    # PUBLIC PAGES
    # =========================================================

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    path(
        "plant/",
        views.plant,
        name="plant"
    ),

    path(
        "plantc/",
        views.plantc,
        name="plantc"
    ),

    path(
        "indoorp/",
        views.indoorp,
        name="indoorp"
    ),

    path(
        "outdoorp/",
        views.outdoorp,
        name="outdoorp"
    ),

    path(
        "flowerp/",
        views.flowerp,
        name="flowerp"
    ),
    path(
    "tablep/",
    views.tablep,
    name="tablep"
),
path("Vender/vorders/", Venderview.vorders, name="vorders"),

path(
    "Vender/ApproveOrder/<int:order_id>/",
    Venderview.ApproveOrder,
    name="ApproveOrder"
),

path(
    "Vender/ShipOrder/<int:order_id>/",
    Venderview.ShipOrder,
    name="ShipOrder"
),

path(
    "Vender/DeliverOrder/<int:order_id>/",
    Venderview.DeliverOrder,
    name="DeliverOrder"
),
path(
    "Vender/CancelOrder/<int:order_id>/",
    Venderview.CancelOrder,
    name="CancelOrder"
),




    path(
        "plantp/",
        views.plantp,
        name="plantp"
    ),

    path(
        "plantcare/",
        views.plantcare,
        name="plantcare"
    ),

    path(
        "homedecore/",
        views.homedecore,
        name="homedecore"
    ),

    path(
        "collection/",
        views.collection,
        name="collection"
    ),

    path(
        "planta/",
        views.planta,
        name="planta"
    ),

    path(
        "newarrivals/",
        views.newarrivals,
        name="newarrivals"
    ),

    path(
        "bestsellers/",
        views.bestsellers,
        name="bestsellers"
    ),

    path(
        "premium-plants/",
        views.premiumplants,
        name="premiumplants"
    ),

    path(
        "beginner-collection/",
        views.beginnercollection,
        name="beginnercollection"
    ),

    path(
        "flowering-collection/",
        views.floweringcollection,
        name="floweringcollection"
    ),

    path(
        "seasonal/",
        views.seasonal,
        name="seasonal"
    ),

    path(
        "spring/",
        views.spring,
        name="spring"
    ),

    path(
        "summer/",
        views.summer,
        name="summer"
    ),

    path(
        "autumn/",
        views.autumn,
        name="autumn"
    ),

    path(
        "winter/",
        views.winter,
        name="winter"
    ),


    # =========================================================
    # PUBLIC PRODUCT DETAIL
    # =========================================================

    path(
        "product/<int:product_id>/",
        views.product_details,
        name="product_details"
    ),


    # =========================================================
    # LOGIN / REGISTER
    # =========================================================

    path(
        "login/",
        views.login,
        name="login"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),


    # =========================================================
    # USER
    # =========================================================

    path(
        "User/UDashboard/",
        UserView.UDashboard,
        name="UDashboard"
    ),

    path(
        "User/viewprofile/",
        UserView.viewprofile,
        name="viewprofile"
    ),

    path(
        "User/changepassword/",
        UserView.changepassword,
        name="changepassword"
    ),

    path(
        "User/MyAddress/",
        UserView.MyAddress,
        name="MyAddress"
    ),

    path(
        "User/MyMessages/",
        UserView.MyMessages,
        name="MyMessages"
    ),

    path(
        "User/MyRatings/",
        UserView.MyRatings,
        name="MyRatings"
    ),

    path(
        "User/mycart/",
        UserView.mycart,
        name="mycart"
    ),

    path(
        "User/AddToCart/<int:product_id>/",
        UserView.AddToCart,
        name="AddToCart"
    ),
    path(
    "User/BuyNow/<int:product_id>/",
    UserView.BuyNow,
    name="BuyNow"
),

    path(
        "User/wishlist/",
        UserView.wishlist,
        name="wishlist"
    ),

    path(
        "User/AddToWishlist/<int:product_id>/",
        UserView.AddToWishlist,
        name="AddToWishlist"
    ),

    path(
        "User/myorders/",
        UserView.myorders,
        name="myorders"
    ),
    path(
    "User/cancelorder/<int:order_id>/",
    UserView.cancelorder,
    name="cancelorder"
),

    path(
        "User/placeorder/",
        UserView.placeorder,
        name="placeorder"
    ),


    # =========================================================
    # ADMIN
    # =========================================================
# =========================================================
# ADMIN
# =========================================================

# ---------------------------------------------------------
# ADMIN - DASHBOARD
# ---------------------------------------------------------

path(
    "Admin/ADashboard/",
    AdminView.ADashboard,
    name="ADashboard"
),


# ---------------------------------------------------------
# ADMIN - MANAGER
# ---------------------------------------------------------

path(
    "Admin/AddManager/",
    AdminView.AddManager,
    name="AddManager"
),

path(
    "Admin/Managerlist/",
    AdminView.Managerlist,
    name="Managerlist"
),

path(
    "Admin/EditManager/<int:id>/",
    AdminView.EditManager,
    name="EditManager"
),

path(
    "Admin/DeleteManager/<int:id>/",
    AdminView.DeleteManager,
    name="DeleteManager"
),
path(
    "Manager/Mreports/",
    Managerview.Mreports,
    name="Mreports"
),



# ---------------------------------------------------------
# ADMIN - VENDOR
# ---------------------------------------------------------

path(
    "Admin/Addvender/",
    AdminView.Addvender,
    name="Addvender"
),

path(
    "Admin/Vendorlist/",
    AdminView.Vendorlist,
    name="Vendorlist"
),

path(
    "Admin/EditVendor/<int:id>/",
    AdminView.EditVendor,
    name="EditVendor"
),

path(
    "Admin/DeleteVendor/<int:id>/",
    AdminView.DeleteVendor,
    name="DeleteVendor"
),
path(
    "Vender/DeleteProduct/<int:id>/",
    Venderview.DeleteProduct,
    name="VendorDeleteProduct"
),
path(
    "Vender/VendorReviews/",
    Venderview.VendorReviews,
    name="VendorReviews"
),


# ---------------------------------------------------------
# ADMIN - USER
# ---------------------------------------------------------

path(
    "Admin/UserList/",
    AdminView.UserList,
    name="UserList"
),

path(
    "Admin/AUserdetail/<int:id>/",
    AdminView.AUserdetail,
    name="AUserdetail"
),

path(
    "Admin/DeleteUser/<int:id>/",
    AdminView.DeleteUser,
    name="DeleteUser"
),


# ---------------------------------------------------------
# ADMIN - CATEGORY
# ---------------------------------------------------------

path(
    "Admin/AdminAddcategory/",
    AdminView.AdminAddcategory,
    name="AdminAddcategory"
),

path(
    "Admin/AdminCategorylist/",
    AdminView.AdminCategorylist,
    name="AdminCategorylist"
),

path(
    "Admin/AdminEditcategory/<int:id>/",
    AdminView.AdminEditcategory,
    name="AdminEditcategory"
),

path(
    "Admin/Deletecategory/<int:id>/",
    AdminView.Deletecategory,
    name="AdminDeletecategory"
),


# ---------------------------------------------------------
# ADMIN - SUBCATEGORY
# ---------------------------------------------------------

path(
    "Admin/AdminAddsubcategory/",
    AdminView.AdminAddsubcategory,
    name="AdminAddsubcategory"
),

path(
    "Admin/AdminSubcategorylist/",
    AdminView.AdminSubcategorylist,
    name="AdminSubcategorylist"
),

path(
    "Admin/Editsubcategory/<int:id>/",
    AdminView.Editsubcategory,
    name="AdminEditsubcategory"
),

path(
    "Admin/Deletesubcategory/<int:id>/",
    AdminView.deletesubcategory,
    name="AdminDeletesubcategory"
),


# ---------------------------------------------------------
# ADMIN - PRODUCT
# ---------------------------------------------------------

path(
    "Admin/AdminProductlist/",
    AdminView.AdminProductlist,
    name="AdminProductlist"
),

path(
    "Admin/AdminProductdetail/<int:id>/",
    AdminView.AdminProductdetail,
    name="AdminProductdetail"
),

path(
    "Admin/AdminEditProduct/<int:id>/",
    AdminView.AdminEditProduct,
    name="AdminEditProduct"
),

path(
    "Admin/AdminDeleteProduct/<int:id>/",
    AdminView.AdminDeleteProduct,
    name="AdminDeleteProduct"
),
path(
    "Admin/BlockUser/<int:id>/",
    AdminView.AdminBlockUser,
    name="AdminBlockUser"
),

path(
    "Admin/UnblockUser/<int:id>/",
    AdminView.AdminUnblockUser,
    name="AdminUnblockUser"
),

# ---------------------------------------------------------
# ADMIN - ORDER
# ---------------------------------------------------------

path(
    "Admin/AdminOrderlist/",
    AdminView.AdminOrderlist,
    name="AdminOrderlist"
),

path(
    "Admin/AdminOrderdetail/<int:id>/",
    AdminView.AdminOrderdetail,
    name="AdminOrderdetail"
),

path(
    "Admin/UpdateOrderStatus/<int:id>/",
    AdminView.AdminOrderstatus,
    name="AdminOrderstatus"
),


# ---------------------------------------------------------
# ADMIN - FEEDBACK
# ---------------------------------------------------------

path(
    "Admin/AdminFeedback/",
    AdminView.AdminFeedback,
    name="AdminFeedback"
),

path(
    "Admin/AdminFeedbackReply/<int:id>/",
    AdminView.AdminFeedbackReply,
    name="AdminFeedbackReply"
),


# ---------------------------------------------------------
# ADMIN - REVIEWS
# ---------------------------------------------------------

path(
    "Admin/AdminReviews/",
    AdminView.AdminReviews,
    name="AdminReviews"
),

path(
    "Admin/AdminDeleteReview/<int:id>/",
    AdminView.AdminDeleteReview,
    name="AdminDeleteReview"
),


# ---------------------------------------------------------
# ADMIN - REPORTS
# ---------------------------------------------------------

path(
    "Admin/Reports/",
    AdminView.Reports,
    name="Reports"
),

path(
    "Admin/AdminSalesReport/",
    AdminView.AdminSalesReport,
    name="AdminSalesReport"
),

path(
    "Admin/AdminUserReport/",
    AdminView.AdminUserReport,
    name="AdminUserReport"
),

path(
    "Admin/AdminProductReport/",
    AdminView.AdminProductReport,
    name="AdminProductReport"
),


# ---------------------------------------------------------
# ADMIN - PROFILE
# ---------------------------------------------------------

path(
    "Admin/AdminProfile/",
    AdminView.AdminProfile,
    name="AdminProfile"
),

path(
    "Admin/AdminChangePassword/",
    AdminView.AdminChangePassword,
    name="AdminChangePassword"
),
    


    # =========================================================
    # MANAGER
    # =========================================================

    path(
        "Manager/MDashboard/",
        Managerview.MDashboard,
        name="MDashboard"
    ),

    path(
        "Manager/mviewprofile/",
        Managerview.mviewprofile,
        name="mviewprofile"
    ),

    path(
        "Manager/cpassword/",
        Managerview.cpassword,
        name="mcpassword"
    ),
    path("Manager/Orderlist/", Managerview.Orderlist, name="MOrderlist"),
    path(
    "Manager/BlockUser/<int:id>/",
    Managerview.BlockUser,
    name="BlockUser"
),

   path(
    "Manager/UnblockUser/<int:id>/",
    Managerview.UnblockUser,
    name="UnblockUser"
),

    # ---------------------------------------------------------
    # MANAGER - CATEGORY
    # ---------------------------------------------------------

    path(
        "Manager/Addcategory/",
        Managerview.Addcategory,
        name="Addcategory"
    ),

    path(
        "Manager/Categorylist/",
        Managerview.Categorylist,
        name="Categorylist"
    ),

    path(
        "Manager/Editcategorylist/<int:id>/",
        Managerview.Editcategorylist,
        name="Editcategorylist"
    ),

    path(
        "Manager/Deletecategory/<int:id>/",
        Managerview.Deletecategory,
        name="Deletecategory"
    ),


    # ---------------------------------------------------------
    # MANAGER - SUBCATEGORY
    # ---------------------------------------------------------

    path(
        "Manager/Addsubcategory/",
        Managerview.Addsubcategory,
        name="Addsubcategory"
    ),

    path(
        "Manager/Subcategorylist/",
        Managerview.Subcategorylist,
        name="Subcategorylist"
    ),

    path(
        "Manager/Editsubcategory/<int:id>/",
        Managerview.Editsubcategory,
        name="Editsubcategory"
    ),

    path(
        "Manager/Deletesubcategory/<int:id>/",
        Managerview.Deletesubcategory,
        name="Deletesubcategory"
    ),


    # ---------------------------------------------------------
    # MANAGER - USER
    # ---------------------------------------------------------

    path(
        "Manager/Userlist/",
        Managerview.Userlist,
        name="Userlist"
    ),

    path(
        "Manager/Userdetail/<int:id>/",
        Managerview.Userdetail,
        name="Userdetail"
    ),


    # ---------------------------------------------------------
    # MANAGER - VENDOR
    # ---------------------------------------------------------

    path(
        "Manager/Venderlist/",
        Managerview.Venderlist,
        name="Venderlist"
    ),

    path(
        "Manager/Venderdetails/<int:id>/",
        Managerview.Venderdetails,
        name="Venderdetails"
    ),


    # ---------------------------------------------------------
    # MANAGER - PRODUCT
    # ---------------------------------------------------------

    path(
        "Manager/Productlist/",
        Managerview.Productlist,
        name="Productlist"
    ),

    path(
        "Manager/EditProduct/<int:id>/",
        Managerview.EditProduct,
        name="EditProduct"
    ),

    path(
        "Manager/DeleteProduct/<int:id>/",
        Managerview.DeleteProduct,
        name="DeleteProduct"
    ),

    path(
        "Manager/Productdetail/<int:id>/",
        Managerview.Productdetail,
        name="Productdetail"
    ),


    # ---------------------------------------------------------
    # MANAGER - CONTACT
    # ---------------------------------------------------------

    path(
        "Manager/ContactMessages/",
        Managerview.ContactMessages,
        name="ContactMessages"
    ),

   # =========================================================
# COLLECTION MANAGEMENT
# =========================================================

path(
    "Manager/Addcollection/",
    Managerview.Addcollection,
    name="Addcollection"
),

path(
    "Manager/Collectionlist/",
    Managerview.Collectionlist,
    name="Collectionlist"
),

path(
    "Manager/Editcollection/<int:id>/",
    Managerview.Editcollection,
    name="Editcollection"
),

path(
    "Manager/Deletecollection/<int:id>/",
    Managerview.Deletecollection,
    name="Deletecollection"
),
    

    path(
        "Manager/ContactReply/<int:id>/",
        Managerview.ContactReply,
        name="ContactReply"
    ),


    # =========================================================
    # VENDOR
    # =========================================================

    path(
        "Vender/VDashboard/",
        Venderview.VDashboard,
        name="VDashboard"
    ),

    path(
        "Vender/vviewprofile/",
        Venderview.vviewprofile,
        name="vviewprofile"
    ),

    path(
        "Vender/vcpassword/",
        Venderview.vcpassword,
        name="vcpassword"
    ),

    path(
        "Vender/vproducts/",
        Venderview.vproducts,
        name="vproducts"
    ),

    path(
        "Vender/AddProduct/",
        Venderview.AddProduct,
        name="AddProduct"
    ),

    path(
        "Vender/MyProducts/",
        Venderview.vproducts,
        name="MyProducts"
    ),

    path(
        "Vender/SalesReport/",
        Venderview.SalesReport,
        name="SalesReport"
    ),


    # =========================================================
    # LOGOUT
    # =========================================================

    path(
        "logout/",
        views.logout,
        name="logout"
    ),

    path(
        "Admin/Logout/",
        AdminView.AdminLogout,
        name="AdminLogout"
    ),

]