import streamlit as st
import requests

st.set_page_config(page_title="Career Advisor AI", page_icon="🎓", layout="centered") # Configure Streamlit page settings

st.title("🚀 AI-Powered Career Guidance") # Display title and description
st.markdown("### Enter your skills & interests to get personalized career suggestions!")

skills = st.text_input("Enter your skills (comma-separated)") # Input fields for user skills and interests
interests = st.text_input("Enter your interests (comma-separated)")

# Button to trigger career suggestion process
if st.button("Get Career Suggestions"):
    if skills and interests:
        with st.spinner("Analyzing career options... 🧠"):
            response = requests.post("http://127.0.0.1:8000/get_career_suggestions", json={"skills": skills, "interests": interests})
            if response.status_code == 200:
                st.success("Career recommendations generated!")
                st.markdown("### Suggested Careers:")
                st.text_area("", response.json()["career_suggestions"], height=300)
            else:
                st.error("Error fetching career suggestions!")
    else:
        st.warning("Please enter both skills and interests!")