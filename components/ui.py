import html as _h
import streamlit as st


# ── CSS: only decorative / layout styles — no hardcoded text/bg colors ────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    /* ── Sidebar ── use Streamlit vars so it adapts to theme */
    section[data-testid="stSidebar"] {
        border-right: 1px solid var(--border-color, rgba(128,128,128,0.2)) !important;
    }
    .sb-header {
        background: linear-gradient(135deg, #1E3A8A, #2563EB);
        padding: 1.25rem 1rem 1.1rem;
        margin: -1rem -1rem 1.25rem -1rem;
        border-radius: 0 0 12px 12px;
    }
    .sb-header h2 {
        color: #FFFFFF !important;
        font-size: 1.2rem; font-weight: 800; margin: 0; letter-spacing: -0.3px;
    }
    .sb-header p {
        color: rgba(255,255,255,0.72) !important;
        font-size: 0.75rem; margin: 0.2rem 0 0;
    }
    .sb-section {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #9CA3AF !important;
        margin: 1.1rem 0 0.5rem;
        border-bottom: 1px solid rgba(128,128,128,0.15);
        padding-bottom: 0.35rem;
    }
    .plat-row {
        display: flex; align-items: center; gap: 0.4rem;
        padding: 0.3rem 0;
    }
    .plat-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .plat-name { font-size: 0.8rem; font-weight: 600; }
    .score-tbl { width:100%; border-collapse:collapse; font-size:0.8rem; }
    .score-tbl td { padding: 0.25rem 0; border-bottom: 1px solid rgba(128,128,128,0.1); }
    .score-tbl td:last-child { text-align:right; font-weight:700; color:#2563EB; }
    .guide-row { display:flex; justify-content:space-between; padding:0.2rem 0; font-size:0.78rem; }
    .guide-row span:last-child { font-weight:700; }

    /* ── Page header banner ── */
    .page-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 55%, #3B82F6 100%);
        padding: 2.5rem 2.75rem 2.75rem;
        margin: -1rem -2rem 1.75rem -2rem;
        position: relative; overflow: hidden;
    }
    .page-header::before {
        content:''; position:absolute; top:-50px; right:-50px;
        width:200px; height:200px; background:rgba(255,255,255,0.06); border-radius:50%;
    }
    .page-header::after {
        content:''; position:absolute; bottom:-80px; left:42%;
        width:280px; height:280px; background:rgba(255,255,255,0.04); border-radius:50%;
    }
    .page-header .htag {
        display:inline-block; background:rgba(255,255,255,0.14);
        border:1px solid rgba(255,255,255,0.22);
        color:#fff; font-size:0.7rem; font-weight:700;
        padding:0.18rem 0.55rem; border-radius:20px;
        margin-right:0.35rem; margin-bottom:0.65rem;
        letter-spacing:0.04em; position:relative; z-index:1;
    }
    .page-header h1 {
        color:#fff; font-size:2rem; font-weight:800;
        margin:0 0 0.4rem; letter-spacing:-0.4px;
        position:relative; z-index:1;
    }
    .page-header p {
        color:rgba(255,255,255,0.78); font-size:0.9rem;
        margin:0; position:relative; z-index:1;
    }

    /* ── Search row ── */
    .stTextInput > div > div > input {
        border-radius: 9px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.93rem !important;
    }
    .stSelectbox > div > div { border-radius: 9px !important; }

    /* ── Primary search button ── */
    .search-col .stButton > button {
        background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 9px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        transition: opacity 0.15s !important;
    }
    .search-col .stButton > button:hover { opacity: 0.88 !important; }

    /* ── Stats strip ── */
    .stats-strip {
        display: flex; gap: 0;
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 10px; overflow: hidden;
        margin-bottom: 1.25rem;
    }
    .stat-cell {
        flex: 1; padding: 0.75rem 1rem;
        border-right: 1px solid rgba(128,128,128,0.15);
    }
    .stat-cell:last-child { border-right: none; }
    .stat-n  { font-size:1.3rem; font-weight:800; color:#1D4ED8; font-family:'Fira Code',monospace; }
    .stat-d  { font-size:0.65rem; font-weight:700; text-transform:uppercase;
               letter-spacing:0.06em; color:#9CA3AF; margin-top:1px; }

    /* ── Card rank + platform badge ── */
    .card-top {
        display: flex; align-items: center; gap: 0.4rem; margin-bottom: 5px;
    }
    .rank-badge {
        font-size: 0.62rem; font-weight: 800; padding: 2px 6px;
        border-radius: 4px; color: #fff; letter-spacing: 0.02em;
    }
    .plat-badge {
        font-size: 0.67rem; font-weight: 700; padding: 2px 7px;
        border-radius: 4px; text-transform: uppercase; letter-spacing: 0.05em;
    }

    /* ── Score pill ── */
    .sc-pill {
        display: inline-block; border-radius: 8px;
        padding: 5px 10px; text-align: center; margin-bottom: 6px;
    }
    .sc-val { font-size: 1rem; font-weight: 800; font-family: 'Fira Code', monospace; }
    .sc-lbl { font-size: 0.56rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; }

    /* ── Price text ── */
    .price-text {
        font-size: 1.2rem; font-weight: 800;
        font-family: 'Fira Code', monospace;
        margin: 3px 0 2px;
    }

    /* ── No-image placeholder ── */
    .no-img {
        height: 115px; display: flex; align-items: center; justify-content: center;
        border-radius: 8px; font-size: 0.75rem; font-weight: 600;
        background: rgba(128,128,128,0.08); color: rgba(128,128,128,0.5);
        border: 1px dashed rgba(128,128,128,0.2);
    }

    /* ── Error banner ── */
    .err-strip {
        border-left: 3px solid #EF4444;
        background: rgba(239,68,68,0.07);
        border-radius: 0 8px 8px 0;
        padding: 0.55rem 0.9rem;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }
    .err-strip strong { color: #DC2626; }

    /* ── Landing ── */
    .landing { text-align: center; padding: 3.5rem 1rem 2rem; }
    .landing h3 { font-size: 1.1rem; font-weight: 700; margin: 0.5rem 0 0.3rem; }
    .landing p  { font-size: 0.85rem; opacity: 0.65; }
    .chip {
        display: inline-block;
        border: 1px solid rgba(37,99,235,0.3);
        background: rgba(37,99,235,0.06);
        color: #2563EB;
        border-radius: 20px; padding: 0.25rem 0.7rem;
        font-size: 0.75rem; font-weight: 600; margin: 0.2rem;
    }
    </style>
    """, unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar_content(platforms):
    st.markdown("""
    <div class="sb-header">
        <h2>ElectroFind</h2>
        <p>Multi-platform electronics search</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Platforms</div>', unsafe_allow_html=True)
    for cfg in platforms.values():
        bc = _h.escape(cfg['badge_color'])
        lbl = _h.escape(cfg['label'])
        st.markdown(
            f'<div class="plat-row">'
            f'<div class="plat-dot" style="background:{bc};"></div>'
            f'<span class="plat-name">{lbl}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="sb-section">Buy Score Breakdown</div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="score-tbl">
        <tr><td>Star Rating</td><td>40 pts</td></tr>
        <tr><td>Review Volume</td><td>30 pts</td></tr>
        <tr><td>Price Value</td><td>30 pts</td></tr>
        <tr><td><strong>Total</strong></td><td><strong>100 pts</strong></td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Score Guide</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guide-row"><span>72 – 100</span><span style="color:#059669;">Excellent Buy</span></div>
    <div class="guide-row"><span>45 – 71</span><span style="color:#2563EB;">Good Value</span></div>
    <div class="guide-row"><span>0 – 44</span><span style="color:#D97706;">Consider Options</span></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Data Source</div>', unsafe_allow_html=True)
    st.caption("Powered by Oxylabs Realtime Scraper API. Prices fetched live.")


# ── Stats bar ─────────────────────────────────────────────────────────────────
def render_stats_bar(products):
    if not products:
        return
    prices  = [p["price"] for p in products if p["price"] > 0]
    n_plats = len({p["platform"] for p in products})
    best    = products[0]["score"] if products else 0
    pr_rng  = f"${min(prices):,.0f} – ${max(prices):,.0f}" if prices else "N/A"

    st.markdown(f"""
    <div class="stats-strip">
        <div class="stat-cell"><div class="stat-n">{len(products)}</div><div class="stat-d">Results</div></div>
        <div class="stat-cell"><div class="stat-n">{n_plats}</div><div class="stat-d">Platforms</div></div>
        <div class="stat-cell"><div class="stat-n" style="font-size:0.95rem;">{pr_rng}</div><div class="stat-d">Price Range</div></div>
        <div class="stat-cell"><div class="stat-n">{best}</div><div class="stat-d">Top Score</div></div>
    </div>
    """, unsafe_allow_html=True)


# ── Product card (hybrid native + minimal HTML) ───────────────────────────────
def render_product_card(product, rank):
    bc   = product['badge_color']
    lbl  = _h.escape(product['label'])
    rank_bg = {1: "#B45309", 2: "#6B7280", 3: "#78350F"}.get(rank, "#1D4ED8")

    # Score styling
    sc = product['score']
    if sc >= 72:
        sc_bg, sc_fg = "rgba(5,150,105,0.12)", "#059669"
    elif sc >= 45:
        sc_bg, sc_fg = "rgba(37,99,235,0.10)", "#1D4ED8"
    else:
        sc_bg, sc_fg = "rgba(217,119,6,0.10)",  "#D97706"

    with st.container(border=True):
        c_img, c_body = st.columns([1, 3], gap="medium")

        # ── Image column ──
        with c_img:
            if product["image"]:
                st.image(product["image"], use_container_width=True)
            else:
                st.markdown('<div class="no-img">No Image</div>', unsafe_allow_html=True)

        # ── Body column ──
        with c_body:
            # Rank + platform badge (only badge_color is dynamic, already hex-safe)
            st.markdown(
                f'<div class="card-top">'
                f'<span class="rank-badge" style="background:{rank_bg};">#{rank}</span>'
                f'<span class="plat-badge" style="background:{bc}20;color:{bc};border:1px solid {bc}40;">{lbl}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            # Title — use safe HTML with escape
            title_safe = _h.escape(product["title"][:115])
            st.markdown(
                f'<p style="font-weight:600;font-size:0.88rem;line-height:1.45;margin:0 0 8px;">{title_safe}</p>',
                unsafe_allow_html=True
            )

            c_left, c_right = st.columns([3, 2])

            with c_left:
                if product["price"] > 0:
                    st.markdown(
                        f'<div class="price-text">${product["price"]:,.2f}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.caption("Price unavailable")

                parts = []
                if product["rating"] > 0:
                    parts.append(f"★ {product['rating']:.1f}")
                if product["reviews"] > 0:
                    parts.append(f"{product['reviews']:,} reviews")
                if parts:
                    st.caption(" · ".join(parts))

            with c_right:
                st.markdown(
                    f'<div class="sc-pill" style="background:{sc_bg};">'
                    f'<div class="sc-val" style="color:{sc_fg};">{sc}</div>'
                    f'<div class="sc-lbl" style="color:{sc_fg};">Score</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                if product["url"]:
                    st.link_button("View Deal", product["url"], use_container_width=True)


# ── Errors ────────────────────────────────────────────────────────────────────
def render_errors(errors):
    for platform, msg in errors.items():
        p_safe = _h.escape(platform)
        m_safe = _h.escape(str(msg)[:180])
        st.markdown(
            f'<div class="err-strip"><strong>{p_safe} unavailable</strong> — {m_safe}</div>',
            unsafe_allow_html=True
        )


# ── Empty state ───────────────────────────────────────────────────────────────
def render_empty():
    st.markdown("""
    <div style="text-align:center;padding:4rem 1rem;">
        <p style="font-size:2.5rem;margin-bottom:0.5rem;">&#128269;</p>
        <h3 style="font-size:1.05rem;font-weight:700;margin-bottom:0.3rem;">No results found</h3>
        <p style="font-size:0.85rem;opacity:0.6;">Try a different search term or check your API credentials.</p>
    </div>
    """, unsafe_allow_html=True)


# ── Landing state ─────────────────────────────────────────────────────────────
def render_landing():
    st.markdown("""
    <div class="landing">
        <p style="font-size:2.5rem;margin:0;">&#9889;</p>
        <h3>Search electronics across 3 platforms instantly</h3>
        <p>Results ranked by Buy Score — combining rating, review count and price value.</p>
        <div style="margin-top:0.75rem;">
            <span class="chip">iPhone 16 Pro</span>
            <span class="chip">Sony WH-1000XM5</span>
            <span class="chip">MacBook Air M3</span>
            <span class="chip">Samsung OLED TV</span>
            <span class="chip">iPad Pro</span>
            <span class="chip">Canon EOS R50</span>
        </div>
    </div>
    """, unsafe_allow_html=True)