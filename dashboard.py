import streamlit as st
import json

st.title("User Feedback Dashboard")

feedback_list = []
with open('data/user_feedback.json', 'r') as f:
    for line in f:
        feedback_list.append(json.loads(line))

# Calculate metrics
total_feedback = len(feedback_list)
positive_feedback = sum(1 for feedback in feedback_list if feedback['feedback'] == 'Yes')
negative_feedback = total_feedback - positive_feedback

st.write(f"Total Feedback Entries: {total_feedback}")
st.write(f"Positive Feedback: {positive_feedback}")
st.write(f"Negative Feedback: {negative_feedback}")

# Display charts
st.subheader("Feedback Distribution")
st.bar_chart({"Feedback": {"Positive": positive_feedback, "Negative": negative_feedback}})

# Show recent feedback
st.subheader("Recent Feedback")
for feedback in reversed(feedback_list[-5:]):
    st.write(f"**Query:** {feedback['query']}")
    st.write(f"**Feedback:** {feedback['feedback']}")
    if feedback['comments']:
        st.write(f"**Comments:** {feedback['comments']}")
    st.write("---")
