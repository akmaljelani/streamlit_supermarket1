import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Jualan",
                   page_icon= ":money_with_wings:",
                   layout='wide')

## caching for loading. Preprocessing in pandas should happen here
@st.cache
def get_data():

    df = pd.read_csv('supermarket_sales - Sheet1.csv')
    df.columns = df.columns.str.replace(' ','_')
    #print(df.head(10))
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
    return df
    #st.dataframe(df)
df = get_data()

# ----- SIDEBAR -----
st.sidebar.header("Sila Tapis disini, :mag: ")
city = st.sidebar.multiselect(
    "Pilih bandar disini:",
    options=df["City"].unique(),
#    default=df["City"].unique()
)


customer_type = st.sidebar.multiselect(
    "Para Pelanggan:",
    options=df["Customer_type"].unique(),
#    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Pilih Jantina:",
    options=df["Gender"].unique(),
#    default=df["Gender"].unique()
)

#use @ to refer to a variable
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# ---- MAINPAGE ----
st.title(":money_with_wings::money_with_wings: Dashboard Jualan :money_with_wings::money_with_wings:")
st.markdown("##")

# -- TOP KPI'S --

total_sales = int(round(df_selection["Total"].sum(), 2)) #sum of the total columns, float convert to int
average_rating = round(df_selection["Rating"].mean(),1) #mean of rating column, round it to one decimal
#star_rating = ":star2:" * int(round(average_rating, 0)) # rating score by emoji. Multiply star emoji with average rating
average_sale_by_transaction = round(df_selection["Total"].mean(), 2) #mean to total column with two decimal places

#-- Creating columns --
# using f string to concatenate USD symbol with values
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Jumlah Jualan:")
    st.subheader(f"US $ {total_sales:,}")  # passing total sales with , thousands separator 1,000,0000

with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} :star:")

with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

# -- SALES BY PRODUCT LINE BAR CHART ---

sales_by_product_line = (
    df_selection.groupby(by=["Product_line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Total",
    y = sales_by_product_line.index,
    orientation="h", #horizontal
    title = "<b>Jualan Mengikut Kategori Produk</b>",  #using html bold
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),   #colour change according to length of df
    template = "plotly_white",
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",  # setting to transparent
    xaxis=(dict(showgrid=False))
)

## ---- SALES BY HOUR BAR CHART ----
#convert Time to date hour format first. Check df.info

sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    title = "<b> Jualan per Jam</b>",
    color_discrete_sequence = ["#0083B8"] * len(sales_by_hour),
    template = "plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis = dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


st.dataframe(df_selection)