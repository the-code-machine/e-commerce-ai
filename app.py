import streamlit as st
from utils.api import search_electronics, CATEGORY_HINTS, PLATFORMS
from components.ui import (
    inject_css, render_sidebar_content, render_product_card,
    render_stats_bar, render_errors, render_empty, render_landing,
)

st.set_page_config(
    page_title="ElectroFind — Electronics Price Comparison",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    render_sidebar_content(PLATFORMS)

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div>
        <span class="htag">Amazon</span>
        <span class="htag">Google Shopping</span>
        <span class="htag">Flipkart</span>
    </div>
    <h1>ElectroFind</h1>
    <p>Compare electronics prices, ratings and value — ranked by Buy Score</p>
</div>
""", unsafe_allow_html=True)

# ── Search controls ────────────────────────────────────────────────────────────
col_cat, col_q, col_btn = st.columns([2, 4, 1.2])

with col_cat:
    category = st.selectbox("Category", list(CATEGORY_HINTS.keys()), label_visibility="collapsed")

with col_q:
    hint = CATEGORY_HINTS.get(category, "")
    query = st.text_input(
        "Search",
        value="",
        placeholder=f'e.g. "best {hint}"' if hint else "Search any electronics product...",
        label_visibility="collapsed",
    )

with col_btn:
    with st.container():
        st.markdown('<div class="search-col">', unsafe_allow_html=True)
        do_search = st.button("Search", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Filters ────────────────────────────────────────────────────────────────────
col_sort, col_plat = st.columns([2, 3])
with col_sort:
    sort_by = st.selectbox(
        "Sort by",
        ["Buy Score", "Price: Low to High", "Price: High to Low", "Rating", "Reviews"],
    )
with col_plat:
    plat_filter = st.multiselect(
        "Platforms",
        list(PLATFORMS.keys()),
        default=list(PLATFORMS.keys()),
    )

# ── Session state ──────────────────────────────────────────────────────────────
for key, default in [("products", []), ("errors", {}), ("searched", False), ("last_query", "")]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Execute search ─────────────────────────────────────────────────────────────
if do_search:
    final_q = query.strip() or (f"best {hint}" if hint else "electronics")
    with st.spinner(f"Fetching results for **{final_q}**..."):
        try:
            products, errors = search_electronics(final_q)
            st.session_state.products  = products
            st.session_state.errors    = errors
            st.session_state.searched  = True
            st.session_state.last_query = final_q
        except ValueError as e:
            st.error(f"Configuration error: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.stop()

# ── Display ────────────────────────────────────────────────────────────────────
products = st.session_state.products
errors   = st.session_state.errors

if errors:
    render_errors(errors)

if not st.session_state.searched:
    render_landing()
elif not products:
    render_empty()
else:
    filtered = [p for p in products if p["platform"] in plat_filter]

    sort_key = {
        "Buy Score":           lambda x: -x["score"],
        "Price: Low to High":  lambda x:  x["price"] if x["price"] > 0 else 999999,
        "Price: High to Low":  lambda x: -x["price"],
        "Rating":              lambda x: -x["rating"],
        "Reviews":             lambda x: -x["reviews"],
    }.get(sort_by, lambda x: -x["score"])
    filtered.sort(key=sort_key)

    lq = st.session_state.last_query
    st.markdown(
        f'<p style="font-size:0.84rem;opacity:0.65;margin-bottom:0.6rem;">'
        f'<strong>{len(filtered)}</strong> results for '
        f'<strong style="color:#2563EB;">{lq}</strong></p>',
        unsafe_allow_html=True
    )

    render_stats_bar(filtered)

    if filtered:
        for i, product in enumerate(filtered, 1):
            render_product_card(product, i)
    else:
        render_empty()