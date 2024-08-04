import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="My Project")

# Function to display the main page
def main_page():
    col1, col2 = st.columns([4, 1])  # Title column larger, button column smaller

    with col1:
        st.button("Home 🏠")  # Title in the left column

    with col2:
        if st.button(":blue[View Buses]"):
             st.session_state.page = "next_page"
        
    st.text("# Welcome to my project! 👋")

    st.title('Redbus Data Scraping')
    
   
    st.subheader('Domain:')
    st.markdown(' * Transportation')

   
   

    st.subheader('States 🌎 ')
    st.markdown('   *   Andhra Pradesh -  APSRTC ')
    st.markdown('   *   Kerala -KERALA RTC')
    st.markdown('   *   Telangana  - TSRTC')
    st.markdown('   *   Rajasthan  - RSRTC')
    st.markdown('   *   South Bengal - SBSTC')
    st.markdown('   *   Himachal - HRTC')
    st.markdown('   *   West Bengal - WBTC')
    st.markdown('   *   Uttar Pradesh - UPSRTC')
    st.markdown('   *   Punjab - PEPSU')
    st.markdown('   *   Chandigarh - CTU RTC')


    st.markdown("Developed by:")
    st.markdown(":blue[Siva Nanthini]")
    
   
# Function to display the next page
def next_page():
    # Create columns for title and button
    col3, col4 = st.columns([4, 1])  # Title column larger, button column smaller

    with col3:
        st.header("Buses and Routes:bus:")  # Title in the left column

    with col4:
        if st.button(":blue[Back]"):
            st.session_state.page = "main_page"  # Navigate back to main page

    
    # Function to get unique bus routes from MySQL
    def get_unique_bus_routes():
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="redbus"
        )

        # Create a cursor object
        mycursor = mydb.cursor()

        # SQL query to get unique bus routes
        query = "SELECT DISTINCT Busroutes FROM redbus_details"

        # Execute the query
        mycursor.execute(query)

        # Fetch all the rows
        bus_routes = [row[0] for row in mycursor.fetchall()]

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        return bus_routes
    
    # Get unique bus routes
    bus_routes = get_unique_bus_routes()
    
    # Create a single column for bus route
    col5 = st.columns([1])[0]  # Single column for bus route

    with col5:
        bus_route = st.selectbox("Select Bus Route", options=bus_routes) 

    # Create columns for rating filter and fare filter
    col6, col7 ,col8= st.columns([1, 1,1])  # Adjusting layout for filters

    with col6:
        rating_filter = st.selectbox("Select minimum rating", options=["All", "2 stars and above", "3 stars and above", "4 stars and above"])

    with col7:
        fare = st.selectbox("Select bus fare", options=["200-500", "500-900", "900-1700", "1700-2500"])

    with col8:
        bus_type = st.selectbox("Select bus type", options=["All", "A.C.Semi-Sleeper", "NON-AC", "Seater"])

    # Function to get data from MySQL
    def get_data_from_db(rating_filter, bus_route, fare, bus_type):
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="redbus"
        )

        # Create a cursor object
        mycursor = mydb.cursor()

        # SQL query with filters
        query = "SELECT * FROM redbus_details WHERE 1=1"
        params = []
        
        # Add fare filter
        if fare == "200-500":
            query += " AND Fare BETWEEN 200 AND 500"
        elif fare == "500-900":
            query += " AND Fare BETWEEN 500 AND 900"
        elif fare == "900-1700":
            query += " AND Fare BETWEEN 900 AND 1700"
        elif fare == "1700-2500":
            query += " AND Fare BETWEEN 1700 AND 2500"
        
        # Add bus route filter
        if bus_route:
            query += " AND Busroutes LIKE %s"
            params.append(f"%{bus_route}%")
               
        # Add rating filter
        if rating_filter == "2 stars and above":
            query += " AND Rating >= 2"
        elif rating_filter == "3 stars and above":
            query += " AND Rating >= 3"
        elif rating_filter == "4 stars and above":
            query += " AND Rating >= 4"

        # Add bus type filter
        if bus_type != "All":
            query += " AND Bus_type LIKE %s"
            params.append(f"%{bus_type}%")

        # Execute the query
        mycursor.execute(query, params)

        # Fetch all the rows
        data = mycursor.fetchall()

        # Get column names
        col_names = [desc[0] for desc in mycursor.description]

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        # Create a DataFrame from the data
        df = pd.DataFrame(data, columns=col_names)

        return df

    # Load data
    df = get_data_from_db(rating_filter, bus_route, fare, bus_type)

    # Display the DataFrame
    st.write(df)
    st.markdown(''' Happy Journey! :balloon:''')
# Main function to control page navigation
def main():
    # Initialize session state if not already done
    if "page" not in st.session_state:
        st.session_state.page = "main_page"

    # Display the appropriate page based on the session state
    if st.session_state.page == "main_page":
        main_page()
    elif st.session_state.page == "next_page":
        next_page()

if __name__ == "__main__":
    main()
