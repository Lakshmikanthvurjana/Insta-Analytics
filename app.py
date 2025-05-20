import streamlit as st
import pandas as pd
import json
import os

st.title("Instagram Chat Analytics Dashboard")

# Ask user for the path to their inbox folder
data_dir = st.text_input(
    "Enter the path to your Instagram 'inbox' folder (e.g., C:/Users/YourName/Downloads/instagram-data/messages/inbox):"
)
st.write(f"DEBUG: Path entered: '{data_dir}'")  # <-- No indentation here

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

if data_dir:
    if os.path.exists(data_dir):
        df = load_messages(data_dir)
        if not df.empty:
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
            st.warning("No messages found in the folder.")
    else:
        st.error(f"Folder '{data_dir}' not found. Please check the path and try again.")
else:
    st.info("Please enter the path to your Instagram 'inbox' folder above.")
