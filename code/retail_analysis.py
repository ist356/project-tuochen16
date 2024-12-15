import os
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from get_dataset_xlsx import download_kaggle_dataset 
from processing_util import calculate_discount_in_dollars, calculate_profit_margin, add_month_and_year_columns

download_kaggle_dataset("ishanshrivastava28/superstore-sales")
file_path = 'cache/Superstore.xlsx'

# Set up Streamlit app
st.title("Superstore Sales Analysis")

# Load and preprocess data
@st.cache_data
def load_data():
    # Dataset file

    # Read dataset
    data = pd.read_excel(file_path, sheet_name='Orders')

    # Drop unnecessary columns
    data = data.drop('Row ID', axis=1)

    # Keep only relevant columns
    data = data[[
        'Order Date', 'Ship Date', 'Region', 'Category', 'Sub-Category',
        'Sales', 'Quantity', 'Discount', 'Profit'
    ]]

    # Feature engineering
    data = add_month_and_year_columns(data, 'Order Date')
    data['total_discount_in_dollars'] = data.apply(
        lambda row: calculate_discount_in_dollars(row['Sales'], row['Discount']), axis=1
    )
    data['profit_margin'] = data.apply(
        lambda row: calculate_profit_margin(row['Sales'], row['Profit']), axis=1
    )

    return data

# Load data
data = load_data()

# First header
st.header("1. Data PreProcessing")

# Overview
st.subheader("1.1 Descriptive Statistics")
st.write(data.describe())
st.write("This table provides a quick overview of numeric data and helps identify anomalies or errors.")

# Null values heatmap
st.subheader("1.2 Null Values Heatmap")
plt.figure(figsize=(10, 8))
sns.heatmap(data.isnull(), cbar=False, cmap="viridis")
st.pyplot(plt)
st.write("The heatmap above confirms no missing values in the dataset.")

# Second header
st.header("2. Exploratory Data Analysis")

# Total Sales by Sub-Category
st.subheader("2.1 Product Categories")
st.write("Which product categories contributed the most to the company's sales? Which categories are underperforming, if any?")
df_sales = (
    data.groupby(['Category', 'Sub-Category'])['Sales']
    .sum()
    .reset_index()
    .sort_values('Sales', ascending=False)
)
fig1 = px.bar(
    df_sales,
    x='Sales',
    y='Sub-Category',
    color='Category',
    orientation='h',
    title="Total Sales per Sub-Category",
    labels={'Sales': 'Total Sales', 'Sub-Category': 'Sub-Category'},
    template='plotly'
)
st.plotly_chart(fig1)
st.write("The visualization above shows a general overview of the magnitude of sales for each product sub-category. For technology category, phones are the top sales-generating products. Chairs products for furnitures category, and storage products for office supplies category. Throughout the 4-year period from 2011 - 2014, phones, chairs, and storage products are the three most sales-generating products. Along with them are tables, binders, and machine products.")
st.write("Under the technology category, copier products are the least performing. For the furniture and office supplies category, furnishings and fasteners are the least performing.")
st.write("Cell Phones and Chairs have significantly higher sales than other subcategories and they belong to the Technology and Furniture product categories, which are usually expensive.")


# Yearly Sales by Sub-Category
st.subheader("2.2 Yearly Sales per Sub-Category")
st.write("Which year saw negative sales growth for binders, phones, storages, supplies, and tables?")
yearly_sales = data.groupby(['Sub-Category', 'year'])['Sales'].sum().reset_index()
fig2 = px.bar(
    yearly_sales,
    x='Sub-Category',
    y='Sales',
    color='year',
    barmode='group',
    title="Yearly Sales per Sub-Category",
    labels={'Sales': 'Total Sales', 'Sub-Category': 'Sub-Category', 'year': 'Year'},
    template='plotly'
)
st.plotly_chart(fig2)
st.write("Shown is how sales on different products had changed over the 4-year period. For some product categories, sales had been fastest growing in 2014. This was not the case for bookcases, machines, supplies, and tables, which all saw a slow growth in sales in the same year. In 2012, products under binders, phones, storages, supplies, and tables experienced negative growth in sales, especially machine products.")


# Annual Average Growth Rate
st.subheader("2.3 Annual Average Growth Rate")
st.write("Which year saw negative sales growth for each sub category?")
yearly_sales['yearly_growth_rate'] = yearly_sales.groupby('Sub-Category')['Sales'].pct_change() * 100
avg_growth_rate = yearly_sales.groupby('Sub-Category')['yearly_growth_rate'].mean().sort_values(ascending=False)
st.write(avg_growth_rate)
st.write("By average sales annual growth rate, envelope products had been the slowest while supplies products had been the fastest at 185% annual average growth rate (AAGR), followed by copier and appliances products at 86% and 43% AAGR, respectively.")

# Monthly Trends by Year
st.subheader("2.4 Monthly Sales Trends by Year")
st.write("How does sales performance vary across the regions? Are there promising geographical regions or areas requiring improved marketing?")
sorted_years = np.sort(data['year'].unique())
selected_year = st.selectbox("Select a year to view monthly sales trends across all regions:", sorted_years)
year_data = data[data['year'] == selected_year]

# Group by month and region to calculate total sales
monthly_sales = year_data.groupby(['month', 'Region'])['Sales'].sum().reset_index()

# Plot using px.line with different colors for each region
fig3 = px.line(
    monthly_sales,
    x='month',
    y='Sales',
    color='Region',
    markers=True,
    title=f"Monthly Sales Trends Across Regions in {selected_year}",
    labels={'month': 'Month', 'Sales': 'Total Sales', 'Region': 'Region'},
    template='plotly'
)
fig3.update_xaxes(tickmode='linear', tick0=1, dtick=1, title="Month")
st.plotly_chart(fig3)

st.write("As shown in the chart above, seasonal trends emerge, with sales increasing during the holidays (November and December), the start of school (September), and Easter (March). This pattern also holds true for regional annual sales data. The West region generally has higher total sales for the year, followed by the East, and the remaining two regions. The South region has lower sales than the other regions every year, with the exception of March 2011, when the South region had more than three times the sales of the second place region.")

# Insights and Recommendations
st.header("3. Conclusions")
st.write(
    """
    ##### 3.1 **Sales Distribution and Trends:**
    - **Top Performing Products:** Phones, chairs, and storage products consistently generated the highest sales over the 4-year period. These products belong to the technology, furniture, and office supplies categories, respectively. 
    - **Underperforming Products:** Copier products (technology), furnishings (furniture), and fasteners (office supplies) demonstrated the lowest sales performance. 
    - **Annual Growth Insights:** Supplies products showed the fastest growth with an impressive 185% annual average growth rate (AAGR), followed by copier (86%) and appliances (43%). In contrast, envelope products exhibited the slowest growth.
    - **Negative Sales Growth:** In 2012, binders, phones, storage, supplies, and tables experienced negative sales growth, particularly machines, which were significantly impacted. 

    ##### 3.2 **Regional and Seasonal Trends:**
    - **Regional Sales Trends:** The West region consistently outperformed other regions in sales, followed by the East, while the South lagged behind. However, in March 2011, the South region had a temporary sales surge, surpassing all other regions.
    - **Seasonal Peaks:** Sales spiked during holidays (November and December), the back-to-school season (September), and Easter (March), revealing strong seasonal trends.

    """
)

st.header("4. Recommendations")
st.write(
    """
    ##### 4.1 **Focus on Top-Performing Products:**
    - **Increase Inventory and Marketing Efforts:** Allocate more resources to promote and stock high-demand products like phones, chairs, and storage items, especially during peak seasons.
    - **Upsell Opportunities:** Create bundle offers with these popular items to increase overall revenue.

    ##### 4.2 **Address Underperforming Products:**
    - **Technology (Copiers):** Analyze customer needs to identify why copiers are underperforming. Introduce updated features or reduce prices to increase competitiveness.
    - **Furniture (Furnishings):** Investigate demand trends and explore repositioning or rebranding strategies for furnishings.
    - **Office Supplies (Fasteners):** Consider replacing or diversifying fasteners with products that have higher market demand.

    ##### 4.3 **Capitalize on Seasonal Trends:**
    - **Targeted Marketing Campaigns:** Launch aggressive promotional campaigns during key sales periods such as holidays, back-to-school, and Easter.
    - **Seasonal Stock Management:** Ensure adequate inventory levels for high-performing products during these peak times to meet demand and maximize sales.

    ##### 4.4 **Improve Regional Performance:**
    - **Expand Marketing in the South Region:** Investigate the causes of consistently low sales in the South and implement localized campaigns to boost sales.
    - **Leverage Strength in the West Region:** Focus on retaining market leadership in the West by enhancing customer loyalty programs and exclusive offers.
    """
)
