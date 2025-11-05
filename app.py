import streamlit as st
import numpy as np
import pandas as pd
import cloudpickle
import random

# =========================
# Load models
# =========================
def load_model(path):
    with open(path, "rb") as f:
        return cloudpickle.load(f)

cart_model = load_model("simple_cart_abandon_model.pkl")
conversion_model = load_model("model_conversion_gb.pkl")
reason_model = load_model("model_reason_xgb.pkl")
intervention_model = load_model("model_intervention_xgb.pkl")
label_encoder_reason = load_model("label_encoder_reason.pkl")

# =========================
# Streamlit UI Setup
# =========================
st.set_page_config(page_title="🛒 Smart Cart Abandonment Predictor", layout="centered")
st.title("🧠 AI-Powered Cart Abandonment & Conversion Predictor")
st.markdown("Predict user intent, abandonment reason, and best intervention strategy 🚀")
st.divider()

# =========================
# Input Section
# =========================
col1, col2 = st.columns(2)
with col1:
    session_duration = st.number_input("⏱️ Session Duration (minutes)", min_value=0.0, step=0.1)
    pages_viewed = st.number_input("📄 Pages Viewed", min_value=1, step=1)
with col2:
    cart_value = st.number_input("💰 Cart Value ($)", min_value=0.0, step=0.1)
    discount_percent = st.number_input("🏷️ Discount (%)", min_value=0.0, step=0.1)

# =========================
# Helper to create complete feature dataframe
# =========================
def create_full_feature_df(base_features):
    """Fill missing model-required columns with random or default values"""
    all_cols = [
        'session_duration', 'pages_viewed', 'cart_value', 'discount_percent',
        'user_age_group', 'last_action', 'device_type', 'email_open_rate', 'time_of_day',
        'user_location', 'engagement_score', 'avg_time_per_page', 'product_category',
        'is_returning_user', 'added_to_cart', 'total_time_spent',
        'num_items_in_cart', 'clicked_promo', 'intervention_type', 'purchased'
    ]

    df = pd.DataFrame([base_features], columns=['session_duration', 'pages_viewed', 'cart_value', 'discount_percent'])
    for col in all_cols:
        if col not in df.columns:
            if col in ['user_age_group']:
                df[col] = random.choice(['18-25', '26-35', '36-45', '46+'])
            elif col in ['device_type']:
                df[col] = random.choice(['Mobile', 'Desktop', 'Tablet'])
            elif col in ['last_action']:
                df[col] = random.choice(['Viewed Product', 'Added to Cart', 'Clicked Promo', 'Exited'])
            elif col in ['user_location']:
                df[col] = random.choice(['Urban', 'Suburban', 'Rural'])
            elif col in ['time_of_day']:
                df[col] = random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])
            elif col in ['product_category']:
                df[col] = random.choice(['Electronics', 'Fashion', 'Home', 'Beauty', 'Sports'])
            elif col in ['intervention_type']:
                df[col] = random.choice(['Email', 'SMS', 'Push Notification', 'Discount'])
            elif col in ['purchased']:
                df[col] = random.choice([0, 1])
            elif col in ['is_returning_user', 'added_to_cart', 'clicked_promo']:
                df[col] = random.choice([0, 1])
            elif col in ['total_time_spent', 'avg_time_per_page', 'engagement_score', 'email_open_rate', 'num_items_in_cart']:
                df[col] = round(random.uniform(1, 10), 2)
            else:
                df[col] = 0
    return df

# =========================
# Prediction Logic
# =========================
if st.button("🔍 Predict User Behaviour"):
    base_features = [session_duration, pages_viewed, cart_value, discount_percent]
    input_df = create_full_feature_df(base_features)

    try:
        # Predict
        abandon_pred = cart_model.predict(input_df)[0]
        reason_pred = reason_model.predict(input_df)[0]
        conversion_pred = conversion_model.predict(input_df)[0]
        intervention_pred = intervention_model.predict(input_df)[0]

        reason_label = label_encoder_reason.inverse_transform([reason_pred])[0]

        # Suggest actions
        if abandon_pred == 1:
            if reason_label.lower() == "slow delivery":
                suggestion = "🚚 Offer express or next-day delivery."
            elif reason_label.lower() == "high price":
                suggestion = "💰 Provide limited-time discounts or combo offers."
            elif reason_label.lower() == "trust issue":
                suggestion = "🔒 Show trust badges and real customer reviews."
            elif reason_label.lower() == "complex checkout":
                suggestion = "🧾 Simplify your checkout process."
            elif reason_label.lower() == "no need":
                suggestion = "📢 Retarget with personalized product recommendations."
            else:
                suggestion = "✨ Send personalized follow-up via email or WhatsApp."
        else:
            suggestion = "✅ User likely to complete purchase without any intervention."

        # Display results
        st.success("✅ Predictions Generated")
        colA, colB = st.columns(2)
        with colA:
            st.metric("🛒 Cart Abandonment", "Yes" if abandon_pred == 1 else "No")
            st.metric("🧠 Abandonment Reason", reason_label)
        with colB:
            st.metric("💹 Conversion Likelihood", "High" if conversion_pred == 1 else "Low")
            st.metric("🧭 Intervention Effective", "Yes" if intervention_pred == 1 else "No")
        st.info(f"💡 **Suggested Action:** {suggestion}")

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")

st.divider()
st.caption("Built by Akshat Saxena | AI x FinTech Hackathon 💻")
