import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import anthropic

# Load local dataset for demo
def load_demo_data():
    file_path = "./data/clio_data.csv"  # Adjusted for GitHub-hosted file structure
    df = pd.read_csv(file_path)
    return df

# Function to generate AI-powered dashboard insights using Claude AI
def generate_ai_insights(df, category):
    prompt = f"Analyze the following {category} performance data and provide insights:\n{df.to_string()}"
    client = anthropic.Anthropic(api_key="your_claude_api_key")
    response = client.completions.create(
        model="claude-3.5-sonnet",
        prompt=prompt,
        max_tokens=500
    )
    return response["completion"].strip()

# Streamlit UI
st.set_page_config(page_title="LegalTech Dashboard", layout="wide")
st.title("LegalTech AI Dashboard")

# Load demo data
st.subheader("Preview Your Data")
df = load_demo_data()
st.dataframe(df)

if st.button("Confirm Data and Proceed"):
    # Sidebar customization options
    st.sidebar.subheader("Customize Your Dashboard")
    category = st.sidebar.selectbox("Choose Analysis Type:", ["Attorney Performance", "Firm Performance", "Billing Overview", "Client Insights", "Financial Analysis"])
    metric = st.sidebar.selectbox("Select Metric:", df.columns)
    chart_type = st.sidebar.selectbox("Choose Chart Type:", ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Heatmap", "Treemap"])
    
    # Dynamic Filtering
    st.sidebar.subheader("Filters")
    date_range = st.sidebar.date_input("Select Date Range", [df["date"].min(), df["date"].max()])
    attorney_filter = st.sidebar.multiselect("Filter by Attorney", df["Attorney"].unique())
    client_filter = st.sidebar.multiselect("Filter by Client", df["Client"].unique())
    
    filtered_df = df.copy()
    if attorney_filter:
        filtered_df = filtered_df[filtered_df["Attorney"].isin(attorney_filter)]
    if client_filter:
        filtered_df = filtered_df[filtered_df["Client"].isin(client_filter)]
    if date_range:
        filtered_df = filtered_df[(filtered_df["date"] >= date_range[0]) & (filtered_df["date"] <= date_range[1])]
    
    # Visualization Preview before Adding to Dashboard
    if st.sidebar.button("Preview Visualization"):
        st.subheader("Visualization Preview")
        if chart_type == "Line Chart":
            fig_preview = px.line(filtered_df, x="date", y=metric, title=f"{category} Trends Preview")
        elif chart_type == "Bar Chart":
            fig_preview = px.bar(filtered_df, x="date", y=metric, title=f"{category} Distribution Preview")
        elif chart_type == "Pie Chart":
            fig_preview = px.pie(filtered_df, names="Client", values=metric, title=f"{category} Breakdown Preview")
        elif chart_type == "Heatmap":
            fig_preview = px.density_heatmap(filtered_df, x="Attorney", y="Client", z=metric, title=f"{category} Heatmap")
        elif chart_type == "Treemap":
            fig_preview = px.treemap(filtered_df, path=["Client", "Attorney"], values=metric, title=f"{category} Treemap")
        else:
            fig_preview = px.scatter(filtered_df, x="date", y=metric, title=f"{category} Comparison Preview")
        
        st.plotly_chart(fig_preview)
        if st.button("Add to Dashboard"):
            st.session_state["confirmed_visualization"] = fig_preview
    
    # AI Insights
    if st.sidebar.button("Generate AI Insights"):
        insights = generate_ai_insights(filtered_df, category)
        st.sidebar.markdown("### AI-Generated Insights")
        st.sidebar.write(insights)
    
    # Custom Dashboard Section
    st.subheader("Your Interactive Dashboard")
    if "confirmed_visualization" in st.session_state:
        st.plotly_chart(st.session_state["confirmed_visualization"])
    
    # Drag-and-Drop Widget Placeholder
    st.subheader("Drag & Drop to Customize")
    st.write("(This section will allow interactive widget placement in future updates)")

