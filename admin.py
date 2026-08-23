import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

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
# TIMEZONE
# =========================================================

def format_datetime_gmt7(created_at):

    if not created_at:

        return "-"

    try:

        # -------------------------------------------------
        # Ubah menjadi datetime
        # -------------------------------------------------

        dt = datetime.fromisoformat(
            str(created_at).replace(
                "Z",
                "+00:00"
            )
        )

        # -------------------------------------------------
        # Jika tidak memiliki timezone,
        # anggap data berasal dari UTC
        # -------------------------------------------------

        if dt.tzinfo is None:

            dt = dt.replace(
                tzinfo=ZoneInfo("UTC")
            )

        # -------------------------------------------------
        # Konversi UTC → Asia/Jakarta
        # GMT+7
        # -------------------------------------------------

        dt_gmt7 = dt.astimezone(
            ZoneInfo("Asia/Jakarta")
        )

        # -------------------------------------------------
        # Format tampilan
        # DD/MM/YYYY HH:MM
        # -------------------------------------------------

        return dt_gmt7.strftime(
            "%d/%m/%Y %H:%M"
        )

    except Exception:

        return str(created_at)


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
   MOBILE
   ===================================================== */

@media (max-width: 700px) {

    .block-container {

        padding-left: 14px;
        padding-right: 14px;

    }


    .admin-title {

        font-size: 28px;

    }


    .stat-grid {

        grid-template-columns:
            1fr;

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
# LOAD COMPLAINTS
# =========================================================

complaints = get_complaints()


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
    # FORMAT WAKTU GMT+7
    # =====================================================

    created_at_display = format_datetime_gmt7(
        created_at
    )


    # =====================================================
    # COMPLAINT CARD
    # =====================================================

    st.html(f"""
    <div class="complaint-card">

        <div class="complaint-id">
            LAPORAN #{complaint_id}
        </div>

        <div class="complaint-name">
            {customer_name}
        </div>

        <div class="complaint-info">
            📱 {customer_whatsapp}
            &nbsp;&nbsp;•&nbsp;&nbsp;
            🕒 {created_at_display}
        </div>

        <div class="complaint-text">
            {complaint_text}
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


    current_index = status_options.index(
        status
    )


    new_status = st.selectbox(

        f"Status laporan #{complaint_id}",

        status_options,

        index=current_index,

        key=f"status_{complaint_id}"

    )


    if new_status != status:

        update_complaint_status(

            complaint_id,

            new_status

        )

        st.success(
            f"Status laporan #{complaint_id} "
            f"berhasil diubah menjadi {new_status}."
        )

        st.rerun()


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