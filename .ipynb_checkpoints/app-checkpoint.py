import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. Page Configuration ---
st.set_page_config(page_title="Superstore Profit Analytics", page_icon="📊", layout="wide")

# --- 2. Data Loading & Caching ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/Final_Analysis.csv")
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file not found. Please ensure 'Final_Analysis.csv' is generated and placed in the 'data/' folder.")
        st.stop()

df = load_data()

# --- 3. Sidebar: Filters & Navigation ---
st.sidebar.title("Superstore Analytics")
st.sidebar.markdown("TCS iON Industry Project ")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigation:", 
                        ["Executive Overview", "Product & Financial Analysis", "Power BI Dashboards"])

st.sidebar.markdown("---")
st.sidebar.markdown("### Global Filters")
year_filter = st.sidebar.multiselect("Select Year(s):", options=sorted(df['Order Year'].unique()), default=sorted(df['Order Year'].unique()))
region_filter = st.sidebar.multiselect("Select Region(s):", options=df['Region'].unique(), default=df['Region'].unique())

filtered_df = df[(df['Order Year'].isin(year_filter)) & (df['Region'].isin(region_filter))]

# --- 4. Page 1: Executive Overview ---
if page == "Executive Overview":
    st.title("📈 Executive Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.0f}")
    col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
    col3.metric("Avg Profit Margin", f"{filtered_df['Profit Margin (%)'].mean():.2f}%")
    col4.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")

    st.markdown("---")
    
    st.subheader("Revenue & Profit Trends Over Time")
    monthly_trend = filtered_df.groupby(filtered_df['Order Date'].dt.to_period("M")).agg({'Sales':'sum', 'Profit':'sum'}).reset_index()
    monthly_trend['Order Date'] = monthly_trend['Order Date'].dt.to_timestamp()
    
    fig_trend = px.line(monthly_trend, x='Order Date', y=['Sales', 'Profit'], 
                        color_discrete_map={"Sales": "#1f77b4", "Profit": "#2ca02c"})
    st.plotly_chart(fig_trend, use_container_width=True)

# --- 5. Page 2: Product & Financial Analysis ---
elif page == "Product & Financial Analysis":
    st.title("💡 Product & Financial Insights")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Profit Generators (Sub-Category)")
        profit_gen = filtered_df.groupby('Sub-Category')['Profit'].sum().reset_index().nlargest(10, 'Profit')
        fig_gen = px.bar(profit_gen, x='Profit', y='Sub-Category', orientation='h', color='Profit', color_continuous_scale='Greens')
        fig_gen.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_gen, use_container_width=True)

    with col2:
        st.subheader("Financial Bleed: Loss-Making States")
        state_profit = filtered_df.groupby('State')['Profit'].sum().reset_index()
        loss_states = state_profit[state_profit['Profit'] < 0].nsmallest(10, 'Profit')
        
        if not loss_states.empty:
            fig_loss = px.bar(loss_states, x='Profit', y='State', orientation='h', color='Profit', color_continuous_scale='Reds_r')
            fig_loss.update_layout(yaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig_loss, use_container_width=True)
        else:
            st.success("No loss-making states in this filtered view!")

    st.markdown("---")
    st.subheader("The Discount Dilemma: Does discounting drive profit?")
    fig_scatter = px.scatter(filtered_df, x='Discount', y='Profit Margin (%)', color='Category', 
                             hover_data=['Sub-Category', 'Sales'], opacity=0.7)
    fig_scatter.add_hline(y=0, line_dash="dash", line_color="black")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- 6. Page 3: Power BI Dashboards ---
elif page == "Power BI Dashboards":
    st.title("🖥️ Original Power BI Dashboards")
    st.markdown("Original business intelligence dashboards created for this project.")
    
    image_folder = "images"
    if os.path.exists(image_folder):
        images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if images:
            for img in images:
                st.image(os.path.join(image_folder, img), caption=img.split('.')[0].title(), use_container_width=True)
                st.markdown("---")
        else:
            st.info("No images found. Please place your .jpg files in the 'images' folder.")
    else:
        st.warning("The 'images' folder is missing.")