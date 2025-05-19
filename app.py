import streamlit as st
import pandas as pd
import json
import os

st.title("Instagram Analytics Dashboard")

# Path to your Instagram messages data
DATA_DIR = "your_instagram_activity/messages/inbox"  # Update this if your path is different

def load_messages(data_dir):
    messages = []
    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.startswith("message") and file.endswith(".json"):
                    with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        messages.extend(data.get("messages", []))
    return pd.DataFrame(messages)

df = load_messages(DATA_DIR)

if not df.empty:
    st.write(f"Total messages: {len(df)}")
    st.write(df.head())

    # Number of messages per sender
    sender_counts = df['sender_name'].value_counts()
    st.subheader("Messages per Sender")
    st.bar_chart(sender_counts)

    # Messages over time
    df['date'] = pd.to_datetime(df['timestamp_ms'], unit='ms')
    messages_per_day = df.groupby(df['date'].dt.date).size()
    st.subheader("Messages Over Time")
    st.line_chart(messages_per_day)
else:
    st.warning("No messages found. Please check your data path.")