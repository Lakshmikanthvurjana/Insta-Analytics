import streamlit as st
import pandas as pd
import json

st.title("Instagram Chat Analytics Dashboard")

uploaded_files = st.file_uploader(
    "Upload your Instagram message JSON files (from inbox folders)", 
    type="json", 
    accept_multiple_files=True
)

if uploaded_files:
    messages = []
    for uploaded_file in uploaded_files:
        data = json.load(uploaded_file)
        messages.extend(data.get("messages", []))
    if messages:
        df = pd.DataFrame(messages)
        st.write(f"Total messages: {len(df)}")
        st.write(df.head())

        # Convert timestamp to datetime
        df['date'] = pd.to_datetime(df['timestamp_ms'], unit='ms')
        df['day'] = df['date'].dt.date
        df['hour'] = df['date'].dt.hour

        # Messages per day
        st.subheader("Messages per Day")
        st.line_chart(df.groupby('day').size())

        # Messages per hour
        st.subheader("Messages by Hour of Day")
        st.bar_chart(df.groupby('hour').size())

        # Top senders
        st.subheader("Top Senders")
        st.bar_chart(df['sender_name'].value_counts().head(10))
    else:
        st.warning("No messages found in uploaded files.")
else:
    st.info("Please upload your Instagram message JSON files.")
