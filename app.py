import streamlit as st
from pathlib import Path

from analyzer import analyze_log, classify_issues
from health_checker import check_url
from system_monitor import get_system_metrics
from database import init_db, save_incident, get_incidents

st.set_page_config(
    page_title="SupportPulse",
    page_icon="🛠️",
    layout="wide"
)

init_db()

st.title("🛠️ SupportPulse")
st.caption("Application Health & Troubleshooting Toolkit")

st.sidebar.header("Controls")
log_files = {
    path.stem.replace("_", " ").title(): str(path)
    for path in Path("sample_logs").glob("*.log")
}
selected_log = st.sidebar.selectbox("Select a sample log", list(log_files.keys()))
uploaded_file = st.file_uploader(
    "Or upload your own log file",
    type=["log"]
)

st.sidebar.divider()
url = st.sidebar.text_input("API URL to check", "https://httpbin.org/status/200")

# --- System health ---
st.header("1. System Health")
metrics = get_system_metrics()

c1, c2, c3 = st.columns(3)
c1.metric("CPU Usage", f"{metrics['cpu']}%")
c2.metric("Memory Usage", f"{metrics['memory']}%")
c3.metric("Disk Usage", f"{metrics['disk']}%")

# --- Log analysis ---
st.header("2. Log Analysis")

if uploaded_file is not None:
    log_text = uploaded_file.read().decode("utf-8")
else:
    log_path = Path(log_files[selected_log])
    log_text = log_path.read_text(encoding="utf-8")
stats = analyze_log(log_text)
classification = classify_issues(stats, log_text)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Errors", stats["errors"])
c2.metric("Warnings", stats["warnings"])
c3.metric("HTTP 500", stats["http_500"])
c4.metric("Timeouts", stats["timeouts"])

st.subheader("Incident Assessment")
a1, a2 = st.columns(2)
a1.info(f"**Likely Issue:** {classification['issue']}")
a2.warning(f"**Priority:** {classification['priority']}")

st.write("**Recommended Checks**")
for item in classification["recommendations"]:
    st.write(f"- {item}")

with st.expander("View selected log"):
    st.code(log_text, language="text")

# --- API health ---
st.header("3. REST API Health Check")

if st.button("Check API"):
    result = check_url(url)
    if result["ok"]:
        st.success(f"API is healthy — HTTP {result['status']} — {result['response_time_ms']} ms")
    else:
        st.error(
            f"API check failed — Status: {result['status']} — "
            f"Response: {result['response_time_ms']} ms — {result['message']}"
        )

# --- Incident tracking ---
st.header("4. Incident Tracking")

with st.form("incident_form"):
    title = st.text_input("Incident title", f"{classification['issue']} detected")
    application = st.text_input("Application", "OrderService")
    priority = st.selectbox(
                "Priority",
                ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
                index=["LOW", "MEDIUM", "HIGH", "CRITICAL"].index(
                classification["priority"]
                )
            )
    status = st.selectbox("Status", ["OPEN", "IN PROGRESS", "RESOLVED"])
    root_cause = st.text_area("Root cause", classification["issue"])
    resolution = st.text_area("Resolution notes", "Investigation completed.")
    submitted = st.form_submit_button("Save Incident")

if submitted:
    save_incident(
        title, application, priority, status,
        root_cause, resolution
    )
    st.success("Incident saved successfully.")

incidents = get_incidents()

if incidents:
    incident_table = [
        {
            "Incident ID": f"INC-{incident['id']:04d}",
            "Title": incident["title"],
            "Application": incident["application"],
            "Priority": incident["priority"],
            "Status": incident["status"],
            "Root Cause": incident["root_cause"],
            "Resolution": incident["resolution"],
            "Created At": incident["created_at"],
        }
        for incident in incidents
    ]

    st.dataframe(incident_table, use_container_width=True)
