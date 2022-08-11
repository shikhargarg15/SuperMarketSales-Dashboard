#Made By : SHIKHAR GARG
#Roll No : 101917064
#Batch : 3CS3
#Topic : SuperMarket Sales Dashboard
#To run, use the command : streamlit run 101917064_Shikhar_Dashboard.py OR py -m streamlit run 101917064_Shikhar_Dashboard.py
#I have set background color, text color, font, primary color which are present in config.toml file.

#importing all the required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import datetime

#Setting Page Configuration
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

#Made function to load dataset so that it can be present in cache and it need not be loaded again and again 
#when dashboard is refreshed.
@st.cache
def load_data():
    df = pd.read_csv('supermarket_sales.csv')    #reading the required dataset
    df["hour"] = pd.to_datetime(df["Time"]).dt.hour    #making column of hour in dataframe
    return df

df = load_data() #calling load_data function to load dataset


col1 , col2 = st.columns(2)    # made columns just to display text and image side-by-side.
with col1:     # accessing the left column
    #Below 2 lines are to display SuperMarket Sales and Developer in center with the help of HTML and CSS.
    st.markdown("<h1 style='text-align: center; color: red;'>SuperMarket Sales</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: lime;'>Developer : Shikhar Garg</h4>", unsafe_allow_html=True)

with col2:      #accessing the right column
    #displaying image
    st.image("https://www.retailgazette.co.uk/wp-content/uploads/Supermarket-sales-in-November-worst-for-4-months.jpeg", 
             width=300)

# SIDEBAR
st.sidebar.header("Please Filter Here :")
#Here user can select his choices of city and customer type.
city = st.sidebar.multiselect("Select the City : ",options=df['City'].unique(),default=df['City'].unique())
customerType = st.sidebar.multiselect("Select the Customer Type : ",options=df['Customer_type'].unique(),
                                                default=df['Customer_type'].unique())


#Fetching dataset according to user selected choices
df_selection = df.query("City == @city & Customer_type == @customerType")
# st.dataframe(df_selection)

# MAINPAGE
st.write('')
total_sales = int(df_selection["Total"].sum()) #calculating total sales 
average_rating = round(df_selection["Rating"].mean(), 1) #calculating average rating of user selected choices data.

left_column , right_column = st.columns(2)  
with left_column:
    st.subheader(f"Total Sales : US ${total_sales}")   #displaying total sales calculated above
with right_column:
    st.subheader(f"Average Rating : {average_rating}:star:")   #displaying average rating
st.write("---")

#Pie Chart Plot b/w gross income & payment method.
payment_plot = px.pie(
    df_selection,
    values="gross income",
    names="Payment",
    title="<b>Gross Income vs Payment Type</b>",  #giving title to the pie chart
    color_discrete_sequence=px.colors.sequential.RdBu
)

#Grouping dataset on the basis of gender and product line
df1 = df_selection.groupby(['Gender', 'Product line']).sum().reset_index()

#Bar Graph of gross income , product and gender wise
sales_product_line = px.bar(
    df1, #passing the dataframe
    x="Product line",
    y="gross income",
    title="<b>Gross Income per Product</b>",
    color='Gender',
    color_discrete_map={         #assigning the colors
        'Female': 'royalblue',
        'Male': 'orange'
    },
    template="plotly_white",
    barmode="group"  #To place bars beside each other
)
#setting the display layout of the bar chart plot
sales_product_line.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
) 

df_hours = df_selection.groupby(["Gender", "hour"]).sum().reset_index()
#Line Graph
line_plot = px.line(
    df_hours,
    x="hour",
    y="gross income",
    title="<b>Gross Income Hour Wise</b>",
    color="Gender",
    color_discrete_map={
        'Female': 'darkblue',
        'Male': "#ff3131"
    },
    template="plotly_white",
    labels={
            "gross income": "Gross Income in US $",
            "hour":"Hour"
        }
)
line_plot.update_layout(plot_bgcolor = '#D2C3C3')   #setting background color
line_plot.update_traces(mode='markers+lines')

# Box Plot
box_fig = px.box(df_selection, 
                 x = "Gender", 
                 y="gross income",
                 title="<b>Gross Income per Gender , Customer Type </b>", 
                 color="Customer_type", 
                 points="outliers",  # displaying outlier data points
                 color_discrete_map={
                        'Member': 'orange',
                        'Normal': "#ff3131"
                        }
                )
box_fig.update_layout(plot_bgcolor = '#CDC9C9')

#Pie Chart
pie_gender = px.pie(
       df_selection,
       values = "gross income",
       names = "Gender",
       title="<b>Gross Income vs Gender</b>",
       template="plotly_white",
       hole=0.6,
       color_discrete_sequence=['lime','firebrick']
    )

#Scatter Plot showing different cities Ratings product wise.
scatter_plot = px.scatter(df_selection, x="Product line", color="Rating", 
                           facet_col="City",title="<b>Rating of Products City-wise</b>")
scatter_plot.update_layout(plot_bgcolor = '#CDC9C9')

#Displaying above made plots 
left , right = st.columns(2)
with left:
    st.plotly_chart(payment_plot, use_container_width=True)
    st.plotly_chart(line_plot, use_container_width=True)
    st.plotly_chart(scatter_plot, use_container_width=True)
with right:
    st.plotly_chart(sales_product_line, use_container_width=True)
    st.plotly_chart(box_fig, use_container_width=True)
    st.plotly_chart(pie_gender,use_container_width=True)

col1, col2, col3 = st.columns([3,7,2])
#made 3 columns and leaving col1,col3 empty just to display histogram plot in the middle.
with col1:
    st.write("")

with col2:
    bar_plot = px.bar(
    df1, x="Product line", y='Quantity',color="Gender",
    color_discrete_map={
        'Female': 'firebrick',
        'Male': 'green'
    },
    title="<b>Quantity sold per Product</b>"
    )
    bar_plot.update_layout(plot_bgcolor = '#D2C3C3')
    st.plotly_chart(bar_plot)

with col3:
    st.write("")

# To hide streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)