import streamlit as st
from utils.api import search_electronics, CATEGORY_HINTS, PLATFORMS
from components.ui import (
    inject_css,
    render_product_card,
    render_stats_bar,
    render_errors,
    render_empty,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ElectroFind — Multi-Platform Electronics Search",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ ElectroFind")
    st.markdown("Compare electronics across **Amazon**, **Google Shopping** and **Flipkart** — ranked by our Buy Score.")
    st.divider()

    st.markdown("**🎯 Buy Score formula**")
    st.markdown(
        """
        | Signal | Weight |
        |---|---|
        | ⭐ Rating | 40 pts |
        | 💬 Reviews | 30 pts |
        | 💰 Price (lower = better) | 30 pts |
        """
    )
    st.divider()

    st.markdown("**📡 Platforms**")
    for name, cfg in PLATFORMS.items():
        st.markdown(
            f'<span style="display:inline-flex;align-items:center;gap:.4rem;'
            f'background:{cfg["badge_color"]}18;color:{cfg["badge_color"]};'
            f'border:1px solid {cfg["badge_color"]}44;border-radius:20px;'
            f'padding:.15rem .55rem;font-size:.78rem;font-weight:600;">'
            f'{cfg["icon"]} {name}</span>',
            unsafe_allow_html=True,
        )
        st.write("")

    st.divider()
    st.caption("Data via [Oxylabs](https://oxylabs.io) Realtime Scraper API")

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="header-banner">
        <h1>⚡ ElectroFind</h1>
        <p>Search electronics across Amazon, Google Shopping & Flipkart — compare by price, rating and our Buy Score</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Search controls ────────────────────────────────────────────────────────────
col_cat, col_search, col_btn = st.columns([2, 4, 1.2])

with col_cat:
    category = st.selectbox(
        "Category",
        list(CATEGORY_HINTS.keys()),
        label_visibility="collapsed",
        placeholder="Select category…",
    )

with col_search:
    hint = CATEGORY_HINTS.get(category, "")
    default_query = f"best {hint}" if hint else "electronics"
    query = st.text_input(
        "Search",
        value="",
        placeholder=f"Search electronics, e.g. '{default_query}'…",
        label_visibility="collapsed",
    )

with col_btn:
    search_clicked = st.button("🔍 Search", use_container_width=True)

# ── Sort / filter bar ──────────────────────────────────────────────────────────
sort_col, filter_col = st.columns([2, 3])
with sort_col:
    sort_by = st.selectbox(
        "Sort by",
        ["Buy Score ↓", "Price: Low → High", "Price: High → Low", "Rating ↓", "Reviews ↓"],
        label_visibility="visible",
    )
with filter_col:
    platform_filter = st.multiselect(
        "Filter platforms",
        list(PLATFORMS.keys()),
        default=list(PLATFORMS.keys()),
        label_visibility="visible",
    )

# ── State init ─────────────────────────────────────────────────────────────────
if "products" not in st.session_state:
    st.session_state.products = []
if "errors" not in st.session_state:
    st.session_state.errors = {}
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# ── Run search ─────────────────────────────────────────────────────────────────
final_query = query.strip() or (f"best {hint}" if hint else "electronics")

if search_clicked:
    if not query.strip():
        st.info(f"No query entered — searching for **{final_query}**")

    with st.spinner(f"Fetching results for **{final_query}** from all platforms…"):
        try:
            products, errors = search_electronics(final_query)
            st.session_state.products = products
            st.session_state.errors = errors
            st.session_state.last_query = final_query
        except ValueError as e:
            st.error(f"🔑 Configuration error: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.stop()

# ── Display results ────────────────────────────────────────────────────────────
products: list[dict] = st.session_state.products
errors: dict = st.session_state.errors

if errors:
    render_errors(errors)

if products:
    # Apply platform filter
    filtered = [p for p in products if p["platform"] in platform_filter]

    # Apply sort
    if sort_by == "Price: Low → High":
        filtered = sorted(filtered, key=lambda x: x["price"] if x["price"] > 0 else float("inf"))
    elif sort_by == "Price: High → Low":
        filtered = sorted(filtered, key=lambda x: x["price"], reverse=True)
    elif sort_by == "Rating ↓":
        filtered = sorted(filtered, key=lambda x: x["rating"], reverse=True)
    elif sort_by == "Reviews ↓":
        filtered = sorted(filtered, key=lambda x: x["reviews"], reverse=True)
    else:  # Buy Score
        filtered = sorted(filtered, key=lambda x: x["score"], reverse=True)

    if st.session_state.last_query:
        st.markdown(
            f"<p style='color:#64748B;font-size:.9rem;margin-bottom:.75rem;'>"
            f"Showing <strong>{len(filtered)}</strong> results for "
            f"<strong>&ldquo;{st.session_state.last_query}&rdquo;</strong></p>",
            unsafe_allow_html=True,
        )

    render_stats_bar(filtered)

    if filtered:
        for i, product in enumerate(filtered, start=1):
            render_product_card(product, rank=i)
            if i < len(filtered):
                st.markdown("<hr>", unsafe_allow_html=True)
    else:
        render_empty()

elif not search_clicked:
    # Landing state
    st.markdown(
        """
        <div style="text-align:center;padding:4rem 2rem;color:#94A3B8;">
            <div style="font-size:3.5rem;margin-bottom:1rem;">🔌</div>
            <h3 style="color:#475569;font-size:1.3rem;margin-bottom:.5rem;">
                Ready to compare electronics
            </h3>
            <p style="font-size:.95rem;">
                Pick a category, enter a product name, and hit Search.<br>
                We'll rank results from Amazon, Google Shopping & Flipkart by Buy Score.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    render_empty()