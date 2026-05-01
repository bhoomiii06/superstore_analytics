import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Superstore Profit Analytics", page_icon="📊", layout="wide")

# ==========================================
# 2. DATA LOADING & CACHING
# ==========================================
@st.cache_data
def load_data():
    try:
        # Load the cleaned dataset generated from our notebook
        df = pd.read_csv("data/Final_Analysis.csv")
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        
        # Ensure Profit Margin exists in case it wasn't saved properly
        if 'Profit Margin (%)' not in df.columns:
            df['Profit Margin (%)'] = (df['Profit'] / df['Sales']) * 100
            
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file not found. Please ensure 'Final_Analysis.csv' is generated and placed in the 'data/' folder.")
        st.stop()

df = load_data()

# ==========================================
# 3. SIDEBAR: FILTERS & NAVIGATION
# ==========================================
st.sidebar.title("📊 Superstore Analytics")
st.sidebar.markdown("---")
st.sidebar.markdown("---")

# Navigation Menu matching Power BI Tabs
page = st.sidebar.radio("Navigation Menu:", [
    "1. Superstore Overview", 
    "2. Sales by Geographics", 
    "3. Customer Segment Insights", 
    "4. Product Performance", 
    "5. Financial Analysis",
    "6. Original Dashboards (Images)"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### Global Filters")
year_filter = st.sidebar.multiselect("Select Year(s):", options=sorted(df['Order Year'].unique()), default=sorted(df['Order Year'].unique()))
region_filter = st.sidebar.multiselect("Select Region(s):", options=df['Region'].unique(), default=df['Region'].unique())

# Apply Global Filters
filtered_df = df[(df['Order Year'].isin(year_filter)) & (df['Region'].isin(region_filter))]

# Helper function for KPIs to prevent division by zero
def calc_margin(profit, sales):
    return (profit / sales) * 100 if sales > 0 else 0

# ==========================================
# PAGE 1: SUPERSTORE OVERVIEW
# ==========================================
if page == "1. Superstore Overview":
    st.title("🛒 Superstore Overview")
    
    # Top KPIs
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Sales", f"${total_sales/1e6:,.2f}M")
    col2.metric("Total Profit", f"${total_profit/1e3:,.2f}K")
    col3.metric("Profit Margin", f"{calc_margin(total_profit, total_sales):.2f}%")
    col4.metric("Total Quantities", f"{filtered_df['Quantity'].sum():,}")
    col5.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")
    st.markdown("---")

    colA, colB = st.columns((1, 2))
    with colA:
        st.subheader("Sales by Region")
        region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        fig_region = px.pie(region_sales, values='Sales', names='Region', hole=0.4, color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_region, use_container_width=True)

    with colB:
        st.subheader("Sales vs Profit by Month")
        monthly_trend = filtered_df.groupby(filtered_df['Order Date'].dt.to_period("M")).agg({'Sales':'sum', 'Profit':'sum'}).reset_index()
        monthly_trend['Order Date'] = monthly_trend['Order Date'].dt.to_timestamp()
        fig_trend = px.area(monthly_trend, x='Order Date', y=['Sales', 'Profit'], color_discrete_map={"Sales": "#add8e6", "Profit": "#00008b"})
        st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("Sales Heatmap by State")
    
    # Dictionary to convert full state names to abbreviations for Plotly
    state_abbr = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
        'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
        'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
        'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
        'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
        'District of Columbia': 'DC'
    }
    
    # Group the sales by state
    state_sales = filtered_df.groupby('State')['Sales'].sum().reset_index()
    
    # Map the full names to the abbreviations
    state_sales['State Code'] = state_sales['State'].map(state_abbr)
    
    # Draw the map using the new 'State Code'
    fig_map = px.choropleth(state_sales, 
                            locations='State Code', 
                            locationmode="USA-states", 
                            color='Sales', 
                            scope="usa", 
                            color_continuous_scale="Blues",
                            hover_name='State') # Keeps the full name when you hover over it
                            
    st.plotly_chart(fig_map, use_container_width=True)
# ==========================================
# PAGE 2: SALES BY GEOGRAPHICS
# ==========================================
elif page == "2. Sales by Geographics":
    st.title("🌎 Sales by Geographics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
    col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
    col3.metric("Total Quantities", f"{filtered_df['Quantity'].sum():,}")
    col4.metric("Total Products", f"{filtered_df['Product Name'].nunique():,}")
    st.markdown("---")

    colA, colB = st.columns((2, 1))
    with colA:
        st.subheader("Geographical Decomposition (Region > State > City)")
        sunburst_df = filtered_df[filtered_df['Sales'] > 0].groupby(['Region', 'State', 'City'])['Sales'].sum().reset_index()
        fig_sunburst = px.sunburst(sunburst_df, path=['Region', 'State', 'City'], values='Sales', color='Sales', color_continuous_scale='Blues')
        fig_sunburst.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=400)
        st.plotly_chart(fig_sunburst, use_container_width=True)

    with colB:
        st.subheader("Top 10 Cities by Quantity")
        city_qty = filtered_df.groupby('City')['Quantity'].sum().reset_index().nlargest(10, 'Quantity')
        fig_city_qty = px.bar(city_qty, x='Quantity', y='City', orientation='h', color='Quantity', color_continuous_scale='Purples')
        fig_city_qty.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig_city_qty, use_container_width=True)

    st.markdown("---")
    colC, colD = st.columns(2)
    with colC:
        st.subheader("Top 3 Cities by Sales Over Time")
        top_3_cities = filtered_df.groupby('City')['Sales'].sum().nlargest(3).index
        top_cities_df = filtered_df[filtered_df['City'].isin(top_3_cities)]
        city_trend = top_cities_df.groupby([top_cities_df['Order Date'].dt.to_period("M"), 'City'])['Sales'].sum().reset_index()
        city_trend['Order Date'] = city_trend['Order Date'].dt.to_timestamp()
        fig_city_trend = px.line(city_trend, x='Order Date', y='Sales', color='City', line_shape='spline')
        st.plotly_chart(fig_city_trend, use_container_width=True)
        
    with colD:
        st.subheader("Quantity by Sub-Category & Region")
        subcat_region = filtered_df.groupby(['Sub-Category', 'Region'])['Quantity'].sum().reset_index()
        fig_subcat_reg = px.bar(subcat_region, x='Quantity', y='Sub-Category', color='Region', orientation='h')
        fig_subcat_reg.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_subcat_reg, use_container_width=True)

# ==========================================
# PAGE 3: CUSTOMER SEGMENT INSIGHTS
# ==========================================
elif page == "3. Customer Segment Insights":
    st.title("👥 Customer Segment Insights")
    st.markdown("Analyze behavior and profitability across Consumer, Corporate, and Home Office segments.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales by Customer Segment")
        seg_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
        fig_seg_sales = px.pie(seg_sales, values='Sales', names='Segment', hole=0.3, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_seg_sales, use_container_width=True)

    with col2:
        st.subheader("Profit by Segment & Category")
        seg_cat_profit = filtered_df.groupby(['Segment', 'Category'])['Profit'].sum().reset_index()
        fig_seg_cat = px.bar(seg_cat_profit, x='Segment', y='Profit', color='Category', barmode='group')
        st.plotly_chart(fig_seg_cat, use_container_width=True)

    st.markdown("---")
    st.subheader("Shipping Mode Preferences by Segment")
    ship_seg = filtered_df.groupby(['Segment', 'Ship Mode'])['Order ID'].nunique().reset_index()
    ship_seg.rename(columns={'Order ID': 'Total Orders'}, inplace=True)
    fig_ship = px.bar(ship_seg, x='Segment', y='Total Orders', color='Ship Mode', barmode='stack', color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_ship, use_container_width=True)

# ==========================================
# PAGE 4: PRODUCT PERFORMANCE
# ==========================================
elif page == "4. Product Performance":
    st.title("📦 Product Performance")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Products by Sales")
        top_prod_sales = filtered_df.groupby('Product Name')['Sales'].sum().reset_index().nlargest(10, 'Sales')
        fig_prod_sales = px.bar(top_prod_sales, x='Sales', y='Product Name', orientation='h', color='Sales', color_continuous_scale='Blues')
        fig_prod_sales.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig_prod_sales, use_container_width=True)

    with col2:
        st.subheader("Top 10 Products by Profit")
        top_prod_profit = filtered_df.groupby('Product Name')['Profit'].sum().reset_index().nlargest(10, 'Profit')
        fig_prod_profit = px.bar(top_prod_profit, x='Profit', y='Product Name', orientation='h', color='Profit', color_continuous_scale='Greens')
        fig_prod_profit.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        st.plotly_chart(fig_prod_profit, use_container_width=True)

    st.markdown("---")
    st.subheader("Category vs Sub-Category Performance (Sales & Profit)")
    cat_sub_perf = filtered_df.groupby(['Category', 'Sub-Category']).agg({'Sales':'sum', 'Profit':'sum'}).reset_index()
    fig_scatter_prod = px.scatter(cat_sub_perf, x='Sales', y='Profit', color='Category', size='Sales', 
                                  hover_name='Sub-Category', size_max=40)
    fig_scatter_prod.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig_scatter_prod, use_container_width=True)

# ==========================================
# PAGE 5: FINANCIAL ANALYSIS
# ==========================================
elif page == "5. Financial Analysis":
    st.title("💰 Financial Analysis & Bleed Identification")
    st.markdown("Identify areas of financial bleed and the impact of discounts on overall profitability.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("The Discount Dilemma: Profit Margin vs Discount")
        fig_discount = px.scatter(filtered_df, x='Discount', y='Profit Margin (%)', color='Category', 
                                  hover_data=['Sub-Category', 'Sales'], opacity=0.6)
        fig_discount.add_hline(y=0, line_dash="dash", line_color="black")
        st.plotly_chart(fig_discount, use_container_width=True)
        
    with col2:
        st.subheader("Top Problem Areas (Loss-Making States)")
        state_perf = filtered_df.groupby('State').agg({'Sales':'sum', 'Profit':'sum'}).reset_index()
        loss_areas = state_perf[state_perf['Profit'] < 0].sort_values('Profit')
        
        if not loss_areas.empty:
            fig_loss = px.bar(loss_areas.head(10), x='Profit', y='State', orientation='h', 
                              color_discrete_sequence=['#d62728'])
            fig_loss.update_layout(yaxis={'categoryorder':'total descending'})
            st.plotly_chart(fig_loss, use_container_width=True)
        else:
            st.success("No loss-making states found with the current filters! 🎉")

    st.markdown("---")
    st.subheader("Bottom 10 Loss-Making Products")
    bottom_products = filtered_df.groupby('Product Name')['Profit'].sum().reset_index().nsmallest(10, 'Profit')
    fig_bottom_prod = px.bar(bottom_products, x='Profit', y='Product Name', orientation='h', color_discrete_sequence=['#d62728'])
    fig_bottom_prod.update_layout(yaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig_bottom_prod, use_container_width=True)

# ==========================================
# PAGE 6: POWER BI DASHBOARDS
# ==========================================
elif page == "6. Original Dashboards (Images)":
    st.title("🖥️ Original Power BI Dashboards")
    st.markdown("Below are the original Power BI dashboard visualizations created during the initial phase of this project.")
    
    image_folder = "images"
    if os.path.exists(image_folder):
        images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if images:
            for img in images:
                st.image(os.path.join(image_folder, img), caption=img.split('.')[0].title().replace('_', ' '), use_container_width=True)
                st.markdown("---")
        else:
            st.info("No images found. Please place your .jpg files in the 'images' folder.")
    else:
        st.warning("The 'images' folder is missing. Create it and add your Power BI screenshots to view them here.")
