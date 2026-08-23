import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from html import escape

from database import (
    create_database,
    get_complaints,
    update_complaint_status
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

    </style>
    """)


    st.html("""
    <div class="login-card">

        <div class="login-logo">
            🍗
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
   STAT CARD
   ===================================================== */

.stat-grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

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
   LOGOUT BUTTON
   ===================================================== */

.logout-area {

    margin-top: 10px;

    margin-bottom: 20px;

}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {

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
            1fr;

    }


    .complaint-card {

        padding: 16px;

    }

}



</style>
""")


# =========================================================
# HEADER
# =========================================================

st.html("""
<div class="admin-header">

    <div class="admin-title">
        🍗 Kays Kitchen
    </div>

    <div class="admin-subtitle">
        Complaint Center — Admin Dashboard
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
# LOAD COMPLAINTS
# =========================================================

try:

    complaints = get_complaints()

except Exception as e:

    st.error(
        "❌ Gagal mengambil data complaint dari database."
    )

    print(
        "ADMIN DATABASE ERROR:",
        e
    )

    st.stop()


# =========================================================
# CALCULATE STATISTICS
# =========================================================

total_complaints = len(
    complaints
)


pending_count = sum(

    1

    for complaint in complaints

    if complaint[5] == "Pending"

)


process_count = sum(

    1

    for complaint in complaints

    if complaint[5] == "Diproses"

)


done_count = sum(

    1

    for complaint in complaints

    if complaint[5] == "Selesai"

)


# =========================================================
# STATISTICS
# =========================================================

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
            {pending_count}
        </div>

    </div>


    <div class="stat-card">

        <div class="stat-label">
            SELESAI
        </div>

        <div class="stat-value">
            {done_count}
        </div>

    </div>

</div>
""")


# =========================================================
# REFRESH
# =========================================================

col1, col2 = st.columns(
    [1, 5]
)


with col1:

    if st.button(
        "🔄 Refresh",
        use_container_width=True
    ):

        st.rerun()


# =========================================================
# FILTER
# =========================================================

with col2:

    filter_status = st.selectbox(

        "Filter status",

        [
            "Semua",
            "Pending",
            "Diproses",
            "Selesai"
        ]

    )


# =========================================================
# FILTER DATA
# =========================================================

if filter_status == "Semua":

    filtered_complaints = complaints

else:

    filtered_complaints = [

        complaint

        for complaint in complaints

        if complaint[5] == filter_status

    ]


# =========================================================
# TITLE
# =========================================================

st.subheader(
    "📋 Daftar Complaint"
)


# =========================================================
# NO DATA
# =========================================================

if not filtered_complaints:

    st.info(
        "Belum ada complaint."
    )


# =========================================================
# DISPLAY COMPLAINTS
# =========================================================

for complaint in filtered_complaints:

    (
        complaint_id,
        created_at,
        customer_name,
        customer_whatsapp,
        complaint_text,
        status

    ) = complaint


    # =====================================================
    # CONVERT TIME TO GMT+7
    # =====================================================

    try:

        if created_at:

            created_at_string = str(
                created_at
            )

            # Supabase biasanya mengirim:
            # 2026-08-23T15:26:21+00:00

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
                ZoneInfo("Asia/Jakarta")
            )


            formatted_time = dt_jakarta.strftime(
                "%d/%m/%Y %H:%M"
            )

        else:

            formatted_time = "-"


    except Exception:

        formatted_time = str(
            created_at
        )


    # =====================================================
    # ESCAPE DATA
    # =====================================================

    safe_id = escape(
        str(complaint_id)
    )

    safe_name = escape(
        str(customer_name)
    )

    safe_whatsapp = escape(
        str(customer_whatsapp)
    )

    safe_complaint = escape(
        str(complaint_text)
    )

    safe_time = escape(
        str(formatted_time)
    )


    # =====================================================
    # COMPLAINT CARD
    # =====================================================

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


    # =====================================================
    # STATUS UPDATE
    # =====================================================

    status_options = [

        "Pending",

        "Diproses",

        "Selesai"

    ]


    if status in status_options:

        current_index = status_options.index(
            status
        )

    else:

        current_index = 0


    new_status = st.selectbox(

        f"Status laporan #{complaint_id}",

        status_options,

        index=current_index,

        key=f"status_{complaint_id}"

    )


    if new_status != status:

        try:

            update_complaint_status(

                complaint_id,

                new_status

            )

            st.success(

                f"Status laporan #{complaint_id} "
                f"berhasil diubah menjadi "
                f"{new_status}."

            )

            st.rerun()


        except Exception as e:

            st.error(

                f"Gagal mengubah status "
                f"laporan #{complaint_id}."

            )

            print(
                "UPDATE STATUS ERROR:",
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