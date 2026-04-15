import streamlit as st

# ── Global CSS ─────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        /* ── Google Font ─────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        /* ── Page reset ──────────────────────────── */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        /* ── Header banner ───────────────────────── */
        .header-banner {
            background: linear-gradient(135deg, #1E40AF 0%, #2563EB 50%, #3B82F6 100%);
            border-radius: 20px;
            padding: 2.5rem 3rem;
            margin-bottom: 2rem;
            color: white;
        }
        .header-banner h1 {
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0 0 0.4rem 0;
            letter-spacing: -0.5px;
        }
        .header-banner p {
            font-size: 1rem;
            opacity: 0.85;
            margin: 0;
        }

        /* ── Search area ─────────────────────────── */
        .stTextInput > div > div > input {
            border-radius: 12px !important;
            border: 2px solid #E2E8F0 !important;
            padding: 0.75rem 1rem !important;
            font-size: 1rem !important;
            font-family: 'DM Sans', sans-serif !important;
            transition: border-color 0.2s;
        }
        .stTextInput > div > div > input:focus {
            border-color: #2563EB !important;
            box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
        }

        /* ── Selectbox ───────────────────────────── */
        .stSelectbox > div > div {
            border-radius: 12px !important;
            border: 2px solid #E2E8F0 !important;
        }

        /* ── Primary button ──────────────────────── */
        .stButton > button {
            background: linear-gradient(135deg, #1E40AF, #2563EB) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.65rem 2rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            font-family: 'DM Sans', sans-serif !important;
            transition: transform 0.15s, box-shadow 0.15s !important;
            width: 100%;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(37,99,235,0.35) !important;
        }

        /* ── Sort pills ──────────────────────────── */
        .sort-row {
            display: flex;
            gap: 0.5rem;
            align-items: center;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }
        .sort-label {
            font-size: 0.8rem;
            font-weight: 600;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-right: 0.25rem;
        }

        /* ── Product card ────────────────────────── */
        .product-card {
            background: #FFFFFF;
            border: 1.5px solid #E2E8F0;
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
            position: relative;
            overflow: hidden;
        }
        .product-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(15,23,42,0.10);
            border-color: #BFDBFE;
        }
        .product-card .rank-badge {
            position: absolute;
            top: -1px;
            left: -1px;
            background: #1E40AF;
            color: white;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 0.25rem 0.6rem;
            border-radius: 16px 0 12px 0;
            letter-spacing: 0.05em;
        }
        .product-card .platform-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            margin-bottom: 0.75rem;
        }
        .product-card .product-title {
            font-size: 0.93rem;
            font-weight: 600;
            color: #0F172A;
            line-height: 1.4;
            margin-bottom: 0.75rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .product-card .meta-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-top: 0.75rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .product-card .price-tag {
            font-size: 1.35rem;
            font-weight: 700;
            color: #0F172A;
            font-family: 'DM Mono', monospace;
        }
        .product-card .price-tag.no-price {
            font-size: 0.85rem;
            color: #94A3B8;
            font-family: 'DM Sans', sans-serif;
        }
        .product-card .rating-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            background: #FFF7ED;
            border: 1px solid #FED7AA;
            border-radius: 20px;
            padding: 0.2rem 0.55rem;
            font-size: 0.78rem;
            font-weight: 600;
            color: #C2410C;
        }
        .product-card .reviews-count {
            font-size: 0.72rem;
            color: #64748B;
        }

        /* ── Score circle ────────────────────────── */
        .score-wrap {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .score-circle {
            width: 52px;
            height: 52px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            font-weight: 700;
            font-family: 'DM Mono', monospace;
            flex-shrink: 0;
        }
        .score-label {
            font-size: 0.62rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 3px;
        }

        /* ── Buy button ──────────────────────────── */
        .buy-btn {
            display: inline-block;
            background: #2563EB;
            color: white !important;
            text-decoration: none !important;
            padding: 0.45rem 1rem;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            font-family: 'DM Sans', sans-serif;
            transition: background 0.15s;
            white-space: nowrap;
        }
        .buy-btn:hover {
            background: #1D4ED8;
        }

        /* ── Stats bar ───────────────────────────── */
        .stats-bar {
            display: flex;
            gap: 1.5rem;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-bottom: 1.75rem;
            flex-wrap: wrap;
        }
        .stat-item {
            display: flex;
            flex-direction: column;
        }
        .stat-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: #2563EB;
            font-family: 'DM Mono', monospace;
        }
        .stat-desc {
            font-size: 0.72rem;
            color: #64748B;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        /* ── Platform filter pills ───────────────── */
        .platform-filter {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.3rem 0.75rem;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            border: 2px solid #E2E8F0;
            background: white;
            color: #475569;
            transition: all 0.15s;
        }

        /* ── Error card ──────────────────────────── */
        .error-card {
            background: #FEF2F2;
            border: 1px solid #FECACA;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            font-size: 0.82rem;
            color: #991B1B;
        }

        /* ── No results ──────────────────────────── */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            color: #94A3B8;
        }
        .empty-state .emoji { font-size: 3rem; margin-bottom: 1rem; }
        .empty-state h3 { color: #475569; font-size: 1.2rem; margin-bottom: 0.5rem; }

        /* ── Divider ─────────────────────────────── */
        hr { border-color: #E2E8F0 !important; }

        /* ── Sidebar ─────────────────────────────── */
        section[data-testid="stSidebar"] {
            background: #F8FAFC;
            border-right: 1px solid #E2E8F0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Score colour helper ────────────────────────────────────────────────────────
def _score_style(score: float) -> tuple[str, str]:
    """Returns (bg_color, text_color) based on score band."""
    if score >= 75:
        return "#DCFCE7", "#166534"
    elif score >= 50:
        return "#DBEAFE", "#1E40AF"
    elif score >= 30:
        return "#FEF9C3", "#854D0E"
    else:
        return "#F1F5F9", "#475569"


# ── Single product card ────────────────────────────────────────────────────────
def render_product_card(product: dict, rank: int):
    bg, fg = _score_style(product["score"])
    price_html = (
        f'<span class="price-tag">${product["price"]:,.2f}</span>'
        if product["price"] > 0
        else '<span class="price-tag no-price">Price N/A</span>'
    )
    rating_html = (
        f'<span class="rating-pill">⭐ {product["rating"]}</span>'
        if product["rating"] > 0
        else ""
    )
    reviews_html = (
        f'<span class="reviews-count">({product["reviews"]:,} reviews)</span>'
        if product["reviews"] > 0
        else ""
    )
    buy_html = (
        f'<a href="{product["url"]}" target="_blank" class="buy-btn">View Deal →</a>'
        if product["url"]
        else ""
    )

    col_img, col_info = st.columns([1, 3])

    with col_img:
        if product["image"]:
            st.image(product["image"], use_container_width=True)
        else:
            st.markdown(
                '<div style="height:120px;background:#F1F5F9;border-radius:10px;'
                'display:flex;align-items:center;justify-content:center;font-size:2rem;">📷</div>',
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown(
            f"""
            <div class="product-card">
                <div class="rank-badge">#{rank}</div>
                <div style="margin-top:0.4rem;">
                    <span class="platform-badge"
                          style="background:{product['badge_color']}22;
                                 color:{product['badge_color']};
                                 border:1px solid {product['badge_color']}44;">
                        {product['icon']} {product['platform']}
                    </span>
                </div>
                <div class="product-title">{product['title']}</div>
                <div class="meta-row">
                    <div>
                        {price_html}
                        <div style="margin-top:0.3rem;display:flex;gap:0.4rem;align-items:center;">
                            {rating_html}
                            {reviews_html}
                        </div>
                    </div>
                    <div style="display:flex;gap:0.75rem;align-items:center;">
                        <div class="score-wrap">
                            <div class="score-circle" style="background:{bg};color:{fg};">
                                {product['score']}
                            </div>
                            <div class="score-label" style="color:{fg};">Score</div>
                        </div>
                        {buy_html}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Stats summary bar ──────────────────────────────────────────────────────────
def render_stats_bar(products: list[dict]):
    if not products:
        return
    prices = [p["price"] for p in products if p["price"] > 0]
    platforms = len({p["platform"] for p in products})
    best_score = products[0]["score"] if products else 0

    st.markdown(
        f"""
        <div class="stats-bar">
            <div class="stat-item">
                <span class="stat-value">{len(products)}</span>
                <span class="stat-desc">Results Found</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{platforms}</span>
                <span class="stat-desc">Platforms</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">${min(prices):,.0f} – ${max(prices):,.0f}</span>
                <span class="stat-desc">Price Range</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{best_score}</span>
                <span class="stat-desc">Top Score</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    ) if prices else None


# ── Platform error notices ─────────────────────────────────────────────────────
def render_errors(errors: dict):
    for platform, msg in errors.items():
        st.markdown(
            f'<div class="error-card">⚠️ <strong>{platform}</strong>: {msg}</div>',
            unsafe_allow_html=True,
        )


# ── Empty state ────────────────────────────────────────────────────────────────
def render_empty():
    st.markdown(
        """
        <div class="empty-state">
            <div class="emoji">🔍</div>
            <h3>No results found</h3>
            <p>Try a different search term or check your API credentials.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )