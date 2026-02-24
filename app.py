import os
import requests
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Sensor Analyzer", layout="wide")

# ---------- HEADER ----------
st.title("AI SENSOR ANALYZER")

st.markdown("""
Upload industrial sensor logs and let AI:

✔ Detect abnormal readings  
✔ Explain possible causes  
✔ Suggest corrective actions  
✔ Generate downloadable reports  

This tool simulates automated monitoring used in smart factories, IoT systems, aerospace testing, and environmental control systems.
""")

st.divider()

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("Upload CSV sensor log", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # ---------- DASHBOARD METRICS ----------
    st.subheader("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isna().sum().sum()))

    st.dataframe(df.head())

    # ---------- NUMERIC DATA ----------
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        st.subheader("📈 Sensor Trends")
        st.line_chart(df[numeric_cols])

        # ---------- ANOMALY DETECTION ----------
        st.subheader("⚠ Automated Diagnostics")

        model = IsolationForest(contamination=0.05, random_state=42)
        df["anomaly"] = model.fit_predict(df[numeric_cols])
        anomalies = df[df["anomaly"] == -1]

        if anomalies.empty:
            st.success("✅ No major anomalies detected")

        else:
            st.error("⚠ Abnormal readings detected")
            st.dataframe(anomalies)

            # ---------- AI EXPLANATION ----------
            api_key = os.getenv("OPENROUTER_API_KEY")
            answer = None

            if api_key:
                st.subheader(" AI Diagnostic Explanation")

                anomaly_summary = anomalies.describe().to_string()

                prompt = f"""
                The following sensor readings were detected as abnormal:

                {anomaly_summary}

                Explain in simple terms:
                1. What might have caused these abnormal readings
                2. Possible risks to the system
                3. Suggested corrective actions
                Keep the explanation practical and engineering-focused.
                """

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "openai/gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )

                if response.status_code == 200:
                    answer = response.json()["choices"][0]["message"]["content"]
                    st.info(answer)
                else:
                    st.warning("AI explanation request failed")

            else:
                st.info("Add OPENROUTER_API_KEY in .env to enable AI explanations")

            # ---------- DOWNLOAD FULL REPORT ----------
            st.subheader("📥 Download Detailed Diagnostics Report")

            total_rows = df.shape[0]
            total_anomalies = anomalies.shape[0]

            summary_text = f"""
 AI Sensor Analyzer Report
--------------------
Total Records: {total_rows}
Detected Anomalies: {total_anomalies}
Anomaly Percentage: {(total_anomalies/total_rows)*100:.2f}%
"""

            if answer:
                summary_text += f"\n\nAI DIAGNOSTIC NOTES:\n{answer}\n"

            full_report = summary_text + "\n\nDATASET WITH ANOMALY LABELS:\n"
            full_report += df.to_csv(index=False)

            report_bytes = full_report.encode("utf-8")

            st.download_button(
                label="Download Full AI Diagnostics Report",
                data=report_bytes,
                file_name="AI_Sensor_Analyzer_Full_Report.csv",
                mime="text/csv"
            )

    else:
        st.warning("No numeric sensor columns found in dataset")

else:
    st.info("Upload a CSV file to begin automated analysis")