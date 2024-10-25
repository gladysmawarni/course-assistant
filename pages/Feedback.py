import streamlit as st

st.set_page_config(page_title="Feedback", page_icon="💭")

with st.form("feedback_form"):
    st.write("Write a feeback about the Q&A bot")

    option = st.selectbox(
    "Select a subject",
    ("Bot Did Not Understand My Question", "Bot Provided an Incorrect or Irrelevant Answer", "Bot Response Was Too Slow or Unhelpful", "Bot Response Was Confusing or Incomplete"),
    )
    feedb = st.text_area("Tell use what you think!")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success('Thank you for your feedback!')