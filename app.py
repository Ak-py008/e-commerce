# app.py — AI Smart Cart Abandonment Predictor (Advanced Rule-Based Version)
import streamlit as st

# --- Page Setup ---
st.set_page_config(page_title="AI Smart Cart Abandonment Predictor", layout="centered")

# --- Header ---
st.title("🛒 AI Smart Cart Abandonment Predictor")
st.subheader("Predict abandonment probability, identify key reasons, and view intelligent recommendations")
st.write("---")

# --- Input Fields ---
st.write("### Enter User & Cart Behavior Details")

col1, col2 = st.columns(2)
with col1:
    session_time = st.number_input("Session Duration (seconds)", min_value=10, max_value=2000, value=300)
    items_in_cart = st.number_input("Items in Cart", min_value=1, max_value=20, value=3)
    cart_value = st.number_input("Cart Value ($)", min_value=10, max_value=10000, value=200)
    discount_offered = st.number_input("Discount Offered (%)", min_value=0, max_value=100, value=10)
    device_type = st.selectbox("Device Type", ["Mobile", "Desktop", "Tablet"])

with col2:
    payment_attempts = st.number_input("Payment Attempts", min_value=0, max_value=5, value=1)
    email_open_rate = st.number_input("Email Open Rate (%)", min_value=0, max_value=100, value=40)
    previous_abandon_rate = st.number_input("Previous Abandon Rate (%)", min_value=0, max_value=100, value=30)
    engagement_score = st.number_input("Engagement Score (0–100)", min_value=0, max_value=100, value=60)
    price_change = st.selectbox("Price Change Since Last Visit", ["Increased", "Decreased", "No Change"])

# --- Rule-Based Abandonment Probability ---
def predict_abandonment(session_time, cart_value, discount_offered, email_open_rate,
                        device_type, previous_abandon_rate, engagement_score, price_change):
    score = 0
    if session_time < 120: score += 25
    elif session_time < 300: score += 15
    else: score += 5
    if cart_value > 1000: score += 15
    elif cart_value < 100: score -= 10
    if discount_offered >= 30: score -= 20
    elif discount_offered < 5: score += 10
    if email_open_rate < 20: score += 15
    else: score -= 10
    if device_type == "Mobile": score += 10
    elif device_type == "Desktop": score -= 5
    if previous_abandon_rate > 50: score += 20
    if engagement_score < 40: score += 20
    else: score -= 10
    if price_change == "Increased": score += 15
    elif price_change == "Decreased": score -= 10
    return max(0, min(100, score))

# --- Prediction Button ---
if st.button("Predict Now"):
    abandonment_probability = predict_abandonment(
        session_time, cart_value, discount_offered, email_open_rate,
        device_type, previous_abandon_rate, engagement_score, price_change
    )

    # --- Combined Condition-Based Recommendation Logic ---
    if abandonment_probability > 75:
        if discount_offered < 5 and cart_value > 2000:
            recommendation = (
                "• Offer a higher discount (10–15%) or free shipping to incentivize completion.\n"
                "• Use exit-intent popups highlighting savings on their high-value cart.\n"
                "• Provide a limited-time countdown to encourage urgency.\n"
                "• Add live chat to address premium product concerns instantly."
            )
            explanation = (
                f"The predicted abandonment is **very high** ({abandonment_probability:.1f}%). "
                "High cart value with a low discount suggests cost hesitation. "
                "Boosting perceived deal value and giving real-time support can recover this sale."
            )

        elif session_time < 60 and items_in_cart >= 3:
            recommendation = (
                "• Simplify checkout by combining review and payment steps.\n"
                "• Add a progress bar to show how close they are to finishing.\n"
                "• Offer 'Save Cart' or 'Checkout Later' options for convenience.\n"
                "• Send an instant reminder email with their cart summary."
            )
            explanation = (
                f"The abandonment is **very high** ({abandonment_probability:.1f}%), but behavior suggests rush or impatience. "
                "These users abandon due to a complex process. Simplify and make checkout faster."
            )

        else:
            recommendation = (
                "• Trigger personalized offers through SMS or email.\n"
                "• Highlight security badges and payment reliability.\n"
                "• Introduce a 'Buy Now, Pay Later' option for flexibility.\n"
                "• Capture feedback to identify checkout pain points."
            )
            explanation = (
                f"The abandonment rate is **critical** ({abandonment_probability:.1f}%). "
                "The combination of your inputs shows strong hesitation across multiple factors. "
                "Multi-channel recovery and trust reassurance are essential."
            )

    elif 50 < abandonment_probability <= 75:
        if payment_attempts == 1:
            recommendation = (
                "• Remind users that multiple secure payment methods are available.\n"
                "• Highlight fast payment options like UPI or wallets.\n"
                "• Offer small incentive like cashback on successful payment.\n"
                "• Send a 'Payment Failed?' assistance email."
            )
            explanation = (
                f"The abandonment probability is **moderately high** ({abandonment_probability:.1f}%). "
                "Few payment attempts and moderate time suggest friction during checkout. "
                "Offering reassurance and quick retries can convert these users."
            )

        elif discount_offered >= 10:
            recommendation = (
                "• Emphasize the time-limited nature of the ongoing discount.\n"
                "• Use notification bars like 'Only 2 hours left for this offer!'.\n"
                "• Simplify cart steps to ensure discount clarity.\n"
                "• Avoid overloading with too many upsell prompts."
            )
            explanation = (
                f"The abandonment probability is **moderate-high** ({abandonment_probability:.1f}%). "
                "Users have incentive but may be overwhelmed or distracted. "
                "Streamlining and reinforcing urgency helps complete the sale."
            )

        else:
            recommendation = (
                "• Add testimonials or product ratings to build trust.\n"
                "• Offer small loyalty rewards to complete checkout.\n"
                "• Re-engage via personalized remarketing emails."
            )
            explanation = (
                f"The model predicts a **medium-high** risk ({abandonment_probability:.1f}%). "
                "Behavior suggests hesitation due to perceived risk or indecision. "
                "Trust-building and gentle incentives are ideal here."
            )

    elif 30 < abandonment_probability <= 50:
        if session_time > 200 and items_in_cart < 2:
            recommendation = (
                "• Suggest related or complementary products.\n"
                "• Highlight benefits like free delivery above ₹500.\n"
                "• Offer a cart completion bonus like extra loyalty points."
            )
            explanation = (
                f"The predicted abandonment is **moderate** ({abandonment_probability:.1f}%). "
                "Users seem to browse longer with fewer items — indicating exploratory behavior. "
                "Encouraging cart expansion and value offers may drive completion."
            )
        else:
            recommendation = (
                "• Send a friendly follow-up email after a few hours.\n"
                "• Simplify address or payment steps.\n"
                "• Offer chat support for any checkout questions."
            )
            explanation = (
                f"The abandonment probability is **moderate** ({abandonment_probability:.1f}%). "
                "Users likely distracted or unsure about small details. "
                "Timely, non-intrusive nudges can re-engage them."
            )

    else:
        if items_in_cart >= 3 and discount_offered >= 10:
            recommendation = (
                "• Celebrate loyalty with a thank-you banner.\n"
                "• Offer early access to upcoming deals.\n"
                "• Encourage sharing purchase on social media for extra rewards."
            )
            explanation = (
                f"Abandonment risk is **low** ({abandonment_probability:.1f}%). "
                "High engagement and discounts show strong purchase intent. "
                "Focus on rewarding and retaining these users for repeat sales."
            )
        else:
            recommendation = (
                "• Maintain consistent experience and fast checkout.\n"
                "• Reinforce trust with 'Your order is secure' messages.\n"
                "• Encourage feedback for UX improvement."
            )
            explanation = (
                f"The predicted abandonment probability is **low** ({abandonment_probability:.1f}%). "
                "Everything looks stable. Maintain the good flow and encourage satisfaction-driven retention."
            )

    # --- Display Results ---
    st.write("### Prediction Summary")
    st.write(f"**Abandonment Probability:** {abandonment_probability:.1f}%")
    st.write(f"**Recommendation:**")
    st.info(recommendation)
    st.write("**Explanation:**")
    st.write(explanation)

else:
    st.info("Fill in all details above and click 'Predict Now' to view your insights.")

st.write("---")
st.caption("© 2025 AI Smart Cart Analytics | Rule-Based Decision Model | Streamlit Demo")
