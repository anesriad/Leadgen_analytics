"""LeadSense — Interactive Lead Analytics Dashboard."""

from pathlib import Path

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="LeadSense", page_icon="📊", layout="wide")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LEADS_PATH = DATA_DIR / "leads_clean.parquet"
MODEL_PATH = DATA_DIR / "lead_model.joblib"
COST_PER_LEAD = 55


@st.cache_data
def load_leads():
    return pd.read_parquet(LEADS_PATH)


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


leads = load_leads()
bundle = load_model()

st.sidebar.title("LeadSense")
page = st.sidebar.radio("Navigate", ["Overview", "Dimensional Analysis", "Lead Scorer"])

# ──────────────────────────────────────
# PAGE 1: Overview
# ──────────────────────────────────────
if page == "Overview":
    st.title("📊 Lead Performance Overview")

    total_leads = len(leads)
    total_sold = int(leads["converted"].sum())
    conv_rate = total_sold / total_leads
    total_premium = leads["premium"].sum()
    total_cost = total_leads * COST_PER_LEAD
    rpl = total_premium / total_leads
    net_per_lead = rpl - COST_PER_LEAD

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Leads", f"{total_leads:,}")
    c2.metric("Conversions", f"{total_sold:,}", f"{conv_rate:.1%}")
    c3.metric("RPL", f"£{rpl:.2f}", f"{'↑' if net_per_lead > 0 else '↓'} £{net_per_lead:.2f} net")
    c4.metric(
        "Total Revenue",
        f"£{total_premium:,.0f}",
        f"ROI: {(total_premium - total_cost) / total_cost * 100:.1f}%",
    )

    st.divider()

    st.subheader("Lead Funnel")
    funnel_data = (
        leads["lead_status"]
        .value_counts()
        .reindex(["Contacted", "No Contact", "Quoted", "Sold", "Invalid"])
        .reset_index()
    )
    funnel_data.columns = ["Status", "Count"]
    fig_funnel = px.bar(
        funnel_data,
        x="Count",
        y="Status",
        orientation="h",
        color="Status",
        color_discrete_map={
            "Contacted": "#4e9af1",
            "No Contact": "#888888",
            "Quoted": "#f0a500",
            "Sold": "#00c896",
            "Invalid": "#ff4d6d",
        },
        text="Count",
    )
    fig_funnel.update_layout(
        template="plotly_dark",
        showlegend=False,
        paper_bgcolor="#0f0f0f",
        plot_bgcolor="#0f0f0f",
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    st.subheader("⚠️ Zero-Sale Keywords (≥15 leads)")
    kw_perf = (
        leads.groupby("keyword")
        .agg(leads=("lead_id", "count"), sales=("converted", "sum"))
        .reset_index()
    )
    zero_sale = kw_perf[(kw_perf["leads"] >= 15) & (kw_perf["sales"] == 0)].copy()
    zero_sale["wasted_spend"] = zero_sale["leads"] * COST_PER_LEAD
    zero_sale = zero_sale.sort_values("leads", ascending=False)

    if len(zero_sale) > 0:
        st.warning(
            f"**{len(zero_sale)} keywords** with ≥15 leads and zero conversions — "
            f"**£{zero_sale['wasted_spend'].sum():,}** wasted."
        )
        st.dataframe(
            zero_sale[["keyword", "leads", "wasted_spend"]].rename(
                columns={"keyword": "Keyword", "leads": "Leads", "wasted_spend": "Wasted (£)"}
            ),
            hide_index=True,
        )
    else:
        st.success("No zero-sale keywords found.")

# ──────────────────────────────────────
# PAGE 2: Dimensional Analysis
# ──────────────────────────────────────
elif page == "Dimensional Analysis":
    st.title("🔍 RPL by Dimension")

    dimension = st.selectbox(
        "Select dimension",
        ["verification_status", "device_type", "keyword_group", "current_insurance", "cover_for", "smoker"],
    )

    stats = (
        leads.groupby(dimension)
        .agg(leads=("lead_id", "count"), sales=("converted", "sum"), revenue=("premium", "sum"))
        .reset_index()
    )
    stats["conv_%"] = (stats["sales"] / stats["leads"] * 100).round(1)
    stats["rpl"] = (stats["revenue"] / stats["leads"]).round(2)
    stats["net_per_lead"] = (stats["rpl"] - COST_PER_LEAD).round(2)
    stats = stats.sort_values("rpl", ascending=True)

    stats["color"] = stats["rpl"].apply(
        lambda x: "Profitable" if x >= COST_PER_LEAD else "Loss-making"
    )
    fig = px.bar(
        stats,
        x="rpl",
        y=dimension,
        orientation="h",
        color="color",
        color_discrete_map={"Profitable": "#00c896", "Loss-making": "#ff4d6d"},
        text=stats["rpl"].apply(lambda x: f"£{x:.0f}"),
    )
    fig.add_vline(
        x=COST_PER_LEAD,
        line_dash="dash",
        line_color="#f0a500",
        annotation_text=f"Breakeven £{COST_PER_LEAD}",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f0f0f",
        plot_bgcolor="#0f0f0f",
        xaxis_title="RPL (£)",
        yaxis_title="",
        legend_title="",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        stats[[dimension, "leads", "sales", "conv_%", "rpl", "net_per_lead"]]
        .rename(
            columns={
                "leads": "Leads",
                "sales": "Sales",
                "conv_%": "Conv %",
                "rpl": "RPL (£)",
                "net_per_lead": "Net/Lead (£)",
            }
        )
        .sort_values("RPL (£)", ascending=False),
        hide_index=True,
    )

# ──────────────────────────────────────
# PAGE 3: Lead Scorer
# ──────────────────────────────────────
elif page == "Lead Scorer":
    st.title("🎯 Score a Lead")
    st.caption("Predict the conversion probability of a single lead using the model trained in NB05.")

    if bundle is None:
        st.error(
            "Model not found. Run [notebooks/05_modeling.ipynb](../notebooks/05_modeling.ipynb) "
            "to train and save it to `data/lead_model.joblib`."
        )
        st.stop()

    with st.form("lead_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.number_input("Age", 18, 120, 35)
            gender = st.selectbox("Gender", ["Male", "Female"])
            smoker = st.selectbox("Smoker", ["no", "yes"])
        with col2:
            current_insurance = st.selectbox(
                "Current Insurance", sorted(leads["current_insurance"].dropna().unique())
            )
            device_type = st.selectbox("Device", ["Smartphone", "Desktop", "Tablet"])
            match_type = st.selectbox("Match Type", ["Exact", "Phrase", "Broad"])
        with col3:
            cover_for = st.selectbox("Cover For", sorted(leads["cover_for"].dropna().unique()))
            verification_status = st.selectbox("Verification", ["verified", "not_verified"])
            keyword_group = st.selectbox("Keyword Group", sorted(leads["keyword_group"].unique()))
            pc_area = st.text_input("Postcode Area", "M")

        submitted = st.form_submit_button("Score Lead")

    if submitted:
        raw = {
            "age": age,
            "gender": gender,
            "smoker": smoker,
            "current_insurance": current_insurance,
            "device_type": device_type,
            "match_type": match_type,
            "cover_for": cover_for,
            "verification_status": verification_status,
            "keyword_group": keyword_group,
            "pc_area": pc_area,
        }

        encoded = []
        for feat in bundle["features"]:
            val = raw[feat]
            if feat in bundle["encoders"]:
                le = bundle["encoders"][feat]
                val = le.transform([val])[0] if val in le.classes_ else 0
            encoded.append(val)

        X = pd.DataFrame([encoded], columns=bundle["features"])
        prob = float(bundle["model"].predict_proba(X)[0, 1])
        tier = "high" if prob >= 0.08 else "medium" if prob >= 0.04 else "low"
        tier_icons = {"high": "🟢", "medium": "🟡", "low": "🔴"}

        st.divider()
        r1, r2 = st.columns(2)
        r1.metric("Conversion Probability", f"{prob:.1%}")
        r2.metric("Risk Tier", f"{tier_icons[tier]} {tier.upper()}")
