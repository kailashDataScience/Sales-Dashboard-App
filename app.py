import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Sales Dashboard',
                   page_icon=':bar_chart:',
                   layout='wide')

@st.cache_data
def get_data():
    df = pd.read_excel('supermarkt_sales.xlsx', 
                       skiprows=3,
                       sheet_name='Sales',
                       engine='openpyxl',
                       usecols='B:R',
                       nrows=1000)
    df['hour'] = pd.to_datetime(df['Time'], format="%H:%M:%S").dt.hour
    return df

df = get_data()

# ---- SIDEBAR ----

st.sidebar.header("Apply Filter here")
city = st.sidebar.multiselect(
    "Select the city",
    options=df['City'].unique(),
    default=df['City'].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# MAIN PAGE

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection['Total'].sum())
average_rate = round(df_selection['Rating'].mean(), 1)
star_rate = ":star:" * int(round(average_rate, 0))
avg_sale_by_transaction = round(df_selection['Total'].mean(), 2)

left, middle, right = st.columns(3)
with left:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rate} {star_rate}")
with right:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {avg_sale_by_transaction}")

st.markdown("---")

# Ensure only numeric columns are included in the sum
numeric_columns = df_selection.select_dtypes(include=['number']).columns

sales_by_product_line = df_selection.groupby('Product line')[numeric_columns].sum().sort_values(by='Total')

fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    title="<b>Sales By Product Line</b>",
    color_discrete_sequence=['#0083B8'] * len(sales_by_product_line),
    template='plotly_white',
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# st.plotly_chart(fig_product_sales)

# Sales by hour
sales_by_hour = df_selection.groupby('hour')[numeric_columns].sum()[['Total']]

fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y='Total',
    title='<b>Sales by Hour</b>',
    color_discrete_sequence=['#0083B8'] * len(sales_by_hour),
    template='plotly_white',
)

fig_hourly_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False)
)

# st.plotly_chart(fig_hourly_sales)


left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_product_sales, use_container_width=True)
right_col.plotly_chart(fig_hourly_sales, use_container_width=True)





hide_st_style = """ 
                    <style>
                        #MainMenu {visibility :hidden;}
                        footer {visibility :hidden;}
                        header {visibility :hidden;}
                    </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)