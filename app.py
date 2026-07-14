import streamlit as st

st.set_page_config(
    page_title="Aakash BPR",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Aakash BPR")

# ---------------- LOGIN ----------------

if not st.user.is_logged_in:

    st.info("Please login using your AESL Google account.")

    if st.button("Login with Google"):
        st.login()

    st.stop()

# ---------------- LOGGED IN ----------------

col1, col2 = st.columns([8,1])

with col1:
    st.success(f"Welcome {st.user.name}")

with col2:
    if st.button("Logout"):
        st.logout()

st.write("Email :", st.user.email)
st.write("Name  :", st.user.name)
