import streamlit as st

from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape

from database import (
    create_database,
    get_complaints,
    update_complaint_status,
    get_orders,
    update_order_status
)


# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Kays Kitchen - Admin",
    page_icon="🍗",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# ADMIN PASSWORD
# =========================================================

def get_admin_password():

    # -----------------------------------------------------
    # PRIORITAS 1: STREAMLIT SECRETS
    # -----------------------------------------------------

    try:

        password = st.secrets["ADMIN_PASSWORD"]

        if password:

            return password

    except Exception:

        pass


    # -----------------------------------------------------
    # PRIORITAS 2: ENVIRONMENT VARIABLE
    # -----------------------------------------------------

    import os

    password = os.getenv(
        "ADMIN_PASSWORD"
    )

    if password:

        return password


    return None


ADMIN_PASSWORD = get_admin_password()


# =========================================================
# LOGIN STATE
# =========================================================

if "admin_authenticated" not in st.session_state:

    st.session_state.admin_authenticated = False


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.admin_authenticated:

    st.html("""
    <style>

    .stApp {

        background:
            linear-gradient(
                180deg,
                #111827 0%,
                #172554 50%,
                #111827 100%
            );

    }


    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    .block-container {

        max-width: 500px;

        padding-top: 8rem;

    }


    .login-card {

        max-width: 420px;

        margin: 20px auto 30px auto;

        padding: 35px 25px;

        background:
            rgba(255, 255, 255, 0.08);

        border:
            1px solid
            rgba(255, 255, 255, 0.12);

        border-radius: 24px;

        text-align: center;

    }


    .login-logo {

        font-size: 55px;

        margin-bottom: 10px;

    }


    .login-title {

        font-size: 30px;

        font-weight: 800;

        color: white;

    }


    .login-subtitle {

        font-size: 14px;

        color: #94a3b8;

        margin-top: 6px;

    }


    @media (max-width: 700px) {

        .block-container {

            padding-left: 14px;
            padding-right: 14px;

            padding-top: 4rem;

        }

        .login-card {

            max-width: 100%;

            margin: 10px auto 25px auto;

            padding: 25px 18px;

            border-radius: 20px;

        }

        .login-logo {

            font-size: 42px;

        }

        .login-title {

            font-size: 26px;

        }

        .login-subtitle {

            font-size: 13px;

        }

    }

    </style>
    """)


    st.html("""
    <div class="login-card">

        <div class="login-logo">
            📋
        </div>

        <div class="login-title">
            Kays Indonesia
        </div>

        <div class="login-subtitle">
            Admin Dashboard
        </div>

    </div>
    """)


    password_input = st.text_input(

        "🔐 Password Admin",

        type="password",

        placeholder="Masukkan password admin",

        key="admin_password_input"

    )


    login_clicked = st.button(

        "🔓 Login Admin",

        use_container_width=True,

        type="primary"

    )


    if login_clicked:

        if not ADMIN_PASSWORD:

            st.error(
                "ADMIN_PASSWORD belum dikonfigurasi "
                "di Streamlit Secrets."
            )

        elif password_input == ADMIN_PASSWORD:

            st.session_state.admin_authenticated = True

            st.rerun()

        else:

            st.error(
                "❌ Password Admin salah."
            )


    st.stop()


# =========================================================
# CUSTOM CSS
# =========================================================

st.html("""
<style>

/* =====================================================
   MAIN APP
   ===================================================== */

.stApp {

    background:
        linear-gradient(
            180deg,
            #111827 0%,
            #172554 50%,
            #111827 100%
        );

}


/* =====================================================
   HIDE STREAMLIT DEFAULT ELEMENTS
   ===================================================== */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =====================================================
   MAIN CONTAINER
   ===================================================== */

.block-container {

    max-width: 1200px;

    padding-top: 2rem;
    padding-bottom: 3rem;

}


/* =====================================================
   HEADER
   ===================================================== */

.admin-header {

    margin-bottom: 25px;

}


.admin-title {

    color: white;

    font-size: 36px;

    font-weight: 800;

    line-height: 1.1;

}


.admin-subtitle {

    color: #94a3b8;

    font-size: 15px;

    margin-top: 7px;

}


/* =====================================================
   STAT GRID
   ===================================================== */

.stat-grid {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 15px;

    margin-bottom: 25px;

}


.stat-card {

    padding: 20px;

    background:
        rgba(255, 255, 255, 0.07);

    border:
        1px solid
        rgba(255, 255, 255, 0.10);

    border-radius: 18px;

}


.stat-label {

    color: #94a3b8;

    font-size: 13px;

    margin-bottom: 8px;

}


.stat-value {

    color: white;

    font-size: 28px;

    font-weight: 800;

}


/* =====================================================
   ORDER CARD
   ===================================================== */

.order-card {

    padding: 20px;

    margin-bottom: 12px;

    background:
        rgba(255, 255, 255, 0.06);

    border:
        1px solid
        rgba(255, 255, 255, 0.08);

    border-radius: 18px;

}


.order-id {

    color: #38bdf8;

    font-weight: 800;

    font-size: 14px;

    margin-bottom: 5px;

}


.order-name {

    color: white;

    font-size: 20px;

    font-weight: 800;

    margin-bottom: 5px;

}


.order-info {

    color: #cbd5e1;

    font-size: 13px;

    margin-bottom: 15px;

}


.order-items {

    color: white;

    font-size: 15px;

    line-height: 1.8;

}


.order-total {

    color: #facc15;

    font-size: 18px;

    font-weight: 800;

    margin-top: 12px;

}


.order-notes {

    color: #cbd5e1;

    font-size: 14px;

    margin-top: 12px;

    padding: 12px;

    background:
        rgba(0, 0, 0, 0.18);

    border-radius: 12px;

}


/* =====================================================
   COMPLAINT CARD
   ===================================================== */

.complaint-card {

    padding: 20px;

    margin-bottom: 15px;

    background:
        rgba(255, 255, 255, 0.06);

    border:
        1px solid
        rgba(255, 255, 255, 0.08);

    border-radius: 18px;

}


.complaint-id {

    color: #f97316;

    font-weight: 800;

    font-size: 14px;

}


.complaint-name {

    color: white;

    font-size: 18px;

    font-weight: 700;

}


.complaint-info {

    color: #cbd5e1;

    font-size: 13px;

}


.complaint-text {

    color: white;

    margin-top: 12px;

    line-height: 1.6;

}


/* =====================================================
   LOGOUT
   ===================================================== */

.logout-area {

    margin-top: 10px;

    margin-bottom: 20px;

}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {

    .block-container {

        padding-left: 14px;
        padding-right: 14px;

        padding-top: 1.5rem;

    }


    .admin-title {

        font-size: 28px;

    }


    .stat-grid {

        grid-template-columns:
            repeat(2, 1fr);

        gap: 10px;

    }


    .stat-card {

        padding: 15px;

    }


    .stat-value {

        font-size: 24px;

    }


    .order-card {

        padding: 16px;

    }


    .complaint-card {

        padding: 16px;

    }

}

</style>
""")


# =========================================================
# HELPER - FORMAT RUPIAH
# =========================================================

def format_rupiah(value):

    try:

        value = int(value or 0)

    except Exception:

        return "Rp0"


    return (
        "Rp"
        +
        f"{value:,}"
        .replace(",", ".")
    )


# =========================================================
# HELPER - FORMAT GMT+7
# =========================================================

def format_datetime_gmt7(created_at):

    if not created_at:

        return "-"


    try:

        created_at_string = str(
            created_at
        )


        # Supabase biasanya:
        # 2026-08-25T09:00:00+00:00

        dt = datetime.fromisoformat(

            created_at_string.replace(
                "Z",
                "+00:00"
            )

        )


        # Jika belum memiliki timezone

        if dt.tzinfo is None:

            dt = dt.replace(
                tzinfo=ZoneInfo("UTC")
            )


        dt_jakarta = dt.astimezone(

            ZoneInfo(
                "Asia/Jakarta"
            )

        )


        return dt_jakarta.strftime(
            "%d/%m/%Y %H:%M"
        )


    except Exception:

        return str(
            created_at
        )


# =========================================================
# HEADER
# =========================================================

st.html("""
<div class="admin-header">

    <div class="admin-title">
        🍗 Kays Kitchen
    </div>

    <div class="admin-subtitle">
        Admin Dashboard — Order & Complaint Center
    </div>

</div>
""")


# =========================================================
# LOGOUT
# =========================================================

logout_col1, logout_col2 = st.columns(
    [6, 1]
)


with logout_col2:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.admin_authenticated = False

        st.session_state.pop(
            "admin_password_input",
            None
        )

        st.rerun()


# =========================================================
# LOAD DATABASE
# =========================================================

try:

    complaints = get_complaints()

except Exception as e:

    st.error(
        "❌ Gagal mengambil data complaint dari database."
    )

    print(
        "ADMIN COMPLAINT DATABASE ERROR:",
        e
    )

    complaints = []


try:

    orders = get_orders()

except Exception as e:

    st.error(
        "❌ Gagal mengambil data order dari database."
    )

    print(
        "ADMIN ORDER DATABASE ERROR:",
        e
    )

    orders = []


# =========================================================
# COMPLAINT STATISTICS
# =========================================================

total_complaints = len(
    complaints
)


pending_complaints = sum(

    1

    for complaint in complaints

    if complaint[5] == "Pending"

)


process_complaints = sum(

    1

    for complaint in complaints

    if complaint[5] == "Diproses"

)


done_complaints = sum(

    1

    for complaint in complaints

    if complaint[5] == "Selesai"

)


# =========================================================
# ORDER STATISTICS
# =========================================================

total_orders = len(
    orders
)


pending_orders = sum(

    1

    for order in orders

    if order.get("status") == "Pending"

)


process_orders = sum(

    1

    for order in orders

    if order.get("status") == "Diproses"

)


done_orders = sum(

    1

    for order in orders

    if order.get("status") == "Selesai"

)


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

st.html(f"""
<div class="stat-grid">

    <div class="stat-card">

        <div class="stat-label">
            📦 TOTAL ORDER
        </div>

        <div class="stat-value">
            {total_orders}
        </div>

    </div>


    <div class="stat-card">

        <div class="stat-label">
            🟡 ORDER PENDING
        </div>

        <div class="stat-value">
            {pending_orders}
        </div>

    </div>


    <div class="stat-card">

        <div class="stat-label">
            🔵 ORDER DIPROSES
        </div>

        <div class="stat-value">
            {process_orders}
        </div>

    </div>


    <div class="stat-card">

        <div class="stat-label">
            🟢 ORDER SELESAI
        </div>

        <div class="stat-value">
            {done_orders}
        </div>

    </div>

</div>
""")


# =========================================================
# REFRESH
# =========================================================

refresh_col1, refresh_col2 = st.columns(
    [1, 5]
)


with refresh_col1:

    if st.button(
        "🔄 Refresh",
        use_container_width=True
    ):

        st.rerun()


# =========================================================
# MAIN TABS
# =========================================================

tab_orders, tab_complaints = st.tabs(

    [
        "📦 ORDER",
        "📋 COMPLAINT"
    ]

)


# =========================================================
# =========================================================
# ORDER CENTER
# =========================================================
# =========================================================

with tab_orders:

    st.subheader(
        "📦 Daftar Order"
    )


    # -----------------------------------------------------
    # ORDER FILTER
    # -----------------------------------------------------

    order_filter = st.selectbox(

        "Filter status order",

        [
            "Semua",
            "Pending",
            "Diproses",
            "Selesai",
            "Dibatalkan"
        ],

        key="order_filter"

    )


    # -----------------------------------------------------
    # FILTER ORDER
    # -----------------------------------------------------

    if order_filter == "Semua":

        filtered_orders = orders

    else:

        filtered_orders = [

            order

            for order in orders

            if order.get("status")
            == order_filter

        ]


    # -----------------------------------------------------
    # NO ORDER
    # -----------------------------------------------------

    if not filtered_orders:

        st.info(
            "📭 Belum ada order."
        )


    # -----------------------------------------------------
    # DISPLAY ORDERS
    # -----------------------------------------------------

    for order in filtered_orders:

        order_id = order.get(
            "id"
        )

        created_at = order.get(
            "created_at"
        )

        customer_name = order.get(
            "customer_name"
        )

        customer_whatsapp = order.get(
            "customer_whatsapp"
        )

        sambal_matah_qty = order.get(
            "sambal_matah_qty"
        ) or 0

        sambal_bawang_qty = order.get(
            "sambal_bawang_qty"
        ) or 0

        total_items = order.get(
            "total_items"
        ) or 0

        total_price = order.get(
            "total_price"
        ) or 0

        notes = order.get(
            "notes"
        ) or ""

        status = order.get(
            "status"
        ) or "Pending"


        # -------------------------------------------------
        # TIME
        # -------------------------------------------------

        formatted_time = format_datetime_gmt7(
            created_at
        )


        # -------------------------------------------------
        # ESCAPE DATA
        # -------------------------------------------------

        safe_id = escape(
            str(order_id)
        )

        safe_name = escape(
            str(customer_name or "-")
        )

        safe_whatsapp = escape(
            str(customer_whatsapp or "-")
        )

        safe_time = escape(
            str(formatted_time)
        )

        safe_notes = escape(
            str(notes)
        )


        # -------------------------------------------------
        # ORDER CARD
        # -------------------------------------------------

        st.html(f"""
        <div class="order-card">

            <div class="order-id">
                ORDER #{safe_id}
            </div>


            <div class="order-name">
                👤 {safe_name}
            </div>


            <div class="order-info">
                📱 {safe_whatsapp}
                &nbsp;&nbsp;•&nbsp;&nbsp;
                🕒 {safe_time}
            </div>


            <div class="order-items">

                🌶️ Sambal Matah:
                <b>{sambal_matah_qty}</b>

                <br>

                🧄 Sambal Bawang:
                <b>{sambal_bawang_qty}</b>

                <br>

                🍚 Total:
                <b>{total_items} ricebowl</b>

            </div>


            <div class="order-total">

                💰 Total Harga:
                {format_rupiah(total_price)}

            </div>


            <div class="order-notes">

                📝 <b>Catatan</b>

                <br><br>

                {safe_notes if safe_notes else "Tidak ada catatan."}

            </div>


        </div>
        """)


        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        order_status_options = [

            "Pending",

            "Diproses",

            "Selesai",

            "Dibatalkan"

        ]


        if status in order_status_options:

            current_order_index = (
                order_status_options.index(
                    status
                )
            )

        else:

            current_order_index = 0


        new_order_status = st.selectbox(

            f"Status Order #{order_id}",

            order_status_options,

            index=current_order_index,

            key=f"order_status_{order_id}"

        )


        # -------------------------------------------------
        # UPDATE STATUS
        # -------------------------------------------------

        if new_order_status != status:

            try:

                update_order_status(

                    order_id,

                    new_order_status

                )


                st.success(

                    f"Status Order #{order_id} "
                    f"berhasil diubah menjadi "
                    f"{new_order_status}."

                )


                st.rerun()


            except Exception as e:

                st.error(

                    f"Gagal mengubah status "
                    f"Order #{order_id}."

                )


                print(
                    "UPDATE ORDER STATUS ERROR:",
                    e
                )


        st.divider()


# =========================================================
# =========================================================
# COMPLAINT CENTER
# =========================================================
# =========================================================

with tab_complaints:

    st.subheader(
        "📋 Daftar Complaint"
    )


    # -----------------------------------------------------
    # COMPLAINT STATISTICS
    # -----------------------------------------------------

    st.html(f"""
    <div class="stat-grid">

        <div class="stat-card">

            <div class="stat-label">
                TOTAL COMPLAINT
            </div>

            <div class="stat-value">
                {total_complaints}
            </div>

        </div>


        <div class="stat-card">

            <div class="stat-label">
                PENDING
            </div>

            <div class="stat-value">
                {pending_complaints}
            </div>

        </div>


        <div class="stat-card">

            <div class="stat-label">
                DIPROSES
            </div>

            <div class="stat-value">
                {process_complaints}
            </div>

        </div>


        <div class="stat-card">

            <div class="stat-label">
                SELESAI
            </div>

            <div class="stat-value">
                {done_complaints}
            </div>

        </div>

    </div>
    """)


    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    complaint_filter = st.selectbox(

        "Filter status complaint",

        [
            "Semua",
            "Pending",
            "Diproses",
            "Selesai"
        ],

        key="complaint_filter"

    )


    # -----------------------------------------------------
    # FILTER DATA
    # -----------------------------------------------------

    if complaint_filter == "Semua":

        filtered_complaints = complaints

    else:

        filtered_complaints = [

            complaint

            for complaint in complaints

            if complaint[5]
            == complaint_filter

        ]


    # -----------------------------------------------------
    # NO DATA
    # -----------------------------------------------------

    if not filtered_complaints:

        st.info(
            "📭 Belum ada complaint."
        )


    # -----------------------------------------------------
    # DISPLAY COMPLAINTS
    # -----------------------------------------------------

    for complaint in filtered_complaints:

        (
            complaint_id,
            created_at,
            customer_name,
            customer_whatsapp,
            complaint_text,
            status

        ) = complaint


        # -------------------------------------------------
        # TIME GMT+7
        # -------------------------------------------------

        formatted_time = format_datetime_gmt7(
            created_at
        )


        # -------------------------------------------------
        # ESCAPE
        # -------------------------------------------------

        safe_id = escape(
            str(complaint_id)
        )

        safe_name = escape(
            str(customer_name or "-")
        )

        safe_whatsapp = escape(
            str(customer_whatsapp or "-")
        )

        safe_complaint = escape(
            str(complaint_text or "-")
        )

        safe_time = escape(
            str(formatted_time)
        )


        # -------------------------------------------------
        # COMPLAINT CARD
        # -------------------------------------------------

        st.html(f"""
        <div class="complaint-card">

            <div class="complaint-id">
                LAPORAN #{safe_id}
            </div>


            <div class="complaint-name">
                {safe_name}
            </div>


            <div class="complaint-info">

                📱 {safe_whatsapp}

                &nbsp;&nbsp;•&nbsp;&nbsp;

                🕒 {safe_time}

            </div>


            <div class="complaint-text">

                {safe_complaint}

            </div>

        </div>
        """)


        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        complaint_status_options = [

            "Pending",

            "Diproses",

            "Selesai"

        ]


        if status in complaint_status_options:

            current_complaint_index = (
                complaint_status_options.index(
                    status
                )
            )

        else:

            current_complaint_index = 0


        new_complaint_status = st.selectbox(

            f"Status laporan #{complaint_id}",

            complaint_status_options,

            index=current_complaint_index,

            key=f"complaint_status_{complaint_id}"

        )


        # -------------------------------------------------
        # UPDATE STATUS
        # -------------------------------------------------

        if new_complaint_status != status:

            try:

                update_complaint_status(

                    complaint_id,

                    new_complaint_status

                )


                st.success(

                    f"Status laporan #{complaint_id} "
                    f"berhasil diubah menjadi "
                    f"{new_complaint_status}."

                )


                st.rerun()


            except Exception as e:

                st.error(

                    f"Gagal mengubah status "
                    f"laporan #{complaint_id}."

                )


                print(
                    "UPDATE COMPLAINT STATUS ERROR:",
                    e
                )


        st.divider()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#94a3b8;
        padding:30px;
        font-size:13px;
    ">
        Kays Kitchen Admin System<br>
        © 2026 Kays Kitchen
    </div>
    """,
    unsafe_allow_html=True
)