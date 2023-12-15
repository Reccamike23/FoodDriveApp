import streamlit as st
import joblib
import folium
from geopy.geocoders import Nominatim
import pandas as pd
from gradientai import Gradient
import plotly.express as px
import sqlite3
from sqlite3 import Error
from datetime import datetime
import geocoder

#import socket
#import requests
#import barcode
#from barcode import Code128
#from barcode.writer import ImageWriter
#from io import BytesIO


# Create tabs for Volunteer and Donation
st.sidebar.title("FOOD DRIVE APP")
tabs = st.sidebar.radio("Select a Page", ["Journey Overview",  "Generate Barcode",  "Volunteer Registration",  "Volunteer Login", "Food Donation Form", "Collected Food Donation",   "Map Generator",   "Interactive Food Drive Assistant"])

if tabs == "Journey Overview":

  # Load the dataset with a specified encoding
  #data = pd.read_csv('Cleaned Proposed Data Collection.csv', encoding='latin1')
  data = pd.read_csv('clean_data.csv', encoding='latin1')


  # Page 1: Dashboard
  def dashboard():
      st.image('Logo.png', use_column_width=True)

      st.subheader("💡 Abstract:")

      inspiration = '''
      Our entire journey has been a rollercoaster ride, marked by numerous challenges that we encountered along the way. Despite the hurdles, we remained determined to overcome each one, driven by the goal of creating something truly beneficial for our community. Throughout this process, we gained invaluable insights and learned significant lessons.

One of the key takeaways from our journey is the realization of the immense potential inherent in leveraging various platforms. We discovered how harnessing the capabilities of different tools and technologies can amplify our impact and broaden our reach. Whether it was collaborating with diverse communities or utilizing innovative solutions, our experience taught us the importance of strategic platform utilization.

Additionally, we delved into the world of coding and witnessed the transformative power of small lines of code. It's fascinating how seemingly minor snippets of code can wield a tremendous influence, automating tasks, streamlining processes, and contributing to the development of impactful solutions.

As we reflect on our journey, we recognize that overcoming challenges and mastering new skills are integral parts of the process. Each obstacle was an opportunity to learn and grow, and our ability to navigate through them has been a testament to our resilience and commitment to our community.

Moving forward, we are excited about the potential impact of our efforts and are motivated to continue exploring, innovating, and applying our newfound knowledge. Our journey has not only equipped us with technical skills but has also instilled in us a deep sense of determination and adaptability.
      '''

      st.write(inspiration)

      st.subheader("👨🏻‍💻 What our Project Does?")

      what_it_does = '''
        Objective: The Food Drive Innovation Project aims to streamline and modernize the process of organizing and conducting food drives for communities in need. \n

Our Goal in this Project:\n

Our project aims to enhance and optimize food drives by implementing an efficient and streamlined data collection system. We integrate QR/barcode technology to monitor the number of collected bags seamlessly. This data is then utilized in a web application for predictive analysis, estimating the potential number of bags that can be collected from any stake. Additionally, our application offers a map generation feature, automating the creation of route-specific maps. This comprehensive solution ensures a more effective and data-driven approach to food drive management.\n

To further enhance our model's accuracy, continuous data feeding with the information gathered over time will be invaluable. This ongoing update will empower the model to provide increasingly precise predictions. Additionally, we plan to refine our route maps by incorporating actual neighborhood names, adding a layer of specificity to our mapping feature. As part of our commitment to user satisfaction, we aim to regularly update the application, introducing new features and optimizing existing ones based on user feedback. This approach ensures that our application remains user-friendly and aligned with evolving needs.

      '''

      st.write(what_it_does)

      st.subheader("Who are the Project Creator?")

      projectcreator = '''
         The Creator of this Project \n
         Group OGS \n
         Mike Kevin De Vera \n
         Abhishek Singh \n
         Gurjot Singh \n
         We are the Machine Learning Analyst Student of MLI 3830 

      '''

      st.write(projectcreator)


  # Page 2: Exploratory Data Analysis (EDA)
  def exploratory_data_analysis():
      st.title("Exploratory Data Analysis")
      # Rename columns for clarity
      data_cleaned = data.rename(columns={
          'Drop Off Location': 'Location',
          'Stake': 'Stake',
          '# of Adult Volunteers in this route': '# of Adult Volunteers',
          '# of Youth Volunteers in this route': '# of Youth Volunteers',
          '# of Donation Bags Collected/Route': 'Donation Bags Collected',
          'Time to Complete (in minutes) pick up of bags /route': 'Time to Complete (min)',
          'Number of routes completed': 'Routes Completed',
          '# of Doors in Route': 'Doors in Route'
        })

      # Visualize the distribution of numerical features using Plotly
      fig = px.histogram(data_cleaned, x='# of Adult Volunteers', nbins=20, labels={'# of Adult Volunteers': 'Adult Volunteers'})
      st.plotly_chart(fig)

      fig = px.histogram(data_cleaned, x='# of Youth Volunteers', nbins=20, labels={'# of Youth Volunteers': 'Youth Volunteers'})
      st.plotly_chart(fig)

      fig = px.histogram(data_cleaned, x='Donation Bags Collected', nbins=20, labels={'Donation Bags Collected': 'Donation Bags Collected'})
      st.plotly_chart(fig)

      fig = px.histogram(data_cleaned, x='Time to Complete (min)', nbins=20, labels={'Time to Complete (min)': 'Time to Complete'})
      st.plotly_chart(fig)

   # Page 3: Machine Learning Modeling
  def machine_learning_modeling():
      st.title("Machine Learning Modeling")
      st.write("Enter the details to predict donation bags:")

      # Mapping of options to their equivalent data
      options_data = {
      "Londonderry Chapel": 29.59322034,
      "Gateway Stake Centre": 30.29457364,
      "Bearspaw Chapel": 25.03571429,
      "Bonnie Doon Stake Centre": 22.5,
      "Coronation Park Chapel": 32.02380952,
      "North Stake Centre": 30.20930233,
      "Riverbend Stake Centre": 42.69444444,
      "Parkland (Spruce Grove/Stony Plain)": 45.14285714,
      "Morinville" : 52.5,
      "Onoway" : 10.0
      }

      # Create a dropdown list
      selected_option = st.selectbox(
      "Drop Off Locations:",
      list(options_data.keys())
      )


      # Display the equivalent data for the selected option
      if selected_option in options_data:
        selected_data = options_data[selected_option]
        st.write(f"Data for '{selected_option}': {selected_data}")
      else:
        st.write("No data available for the selected option.")

      # Mapping of options to their equivalent data
      options_data_stake = {
      "Bonnie Doon Stake": 27.515625,
      "Gateway Stake": 28.72251309,
      "Edmonton North Stake": 31.57723577,
      "Riverbend Stake": 42.69444444,
      "YSA Stake": 50.0
      }

      # Create a dropdown list
      selected_option_stake = st.selectbox(
      "Stake:",
      list(options_data_stake.keys())
      )


      # Display the equivalent data for the selected option
      if selected_option_stake in options_data_stake:
        selected_data_stake = options_data_stake[selected_option_stake]
        st.write(f"Data for '{selected_option_stake}': {selected_data_stake}")
      else:
        st.write("No data available for the selected option.")

      routes_completed = st.slider("Routes Completed", 1, 10, 5)
      time_spent = st.slider("Time Spent (minutes)", 10, 300, 60)
      adult_volunteers = st.slider("Number of Adult Volunteers", 1, 50, 10)
      doors_in_route = st.slider("Number of Doors in Route", 10, 500, 100)
      youth_volunteers = st.slider("Number of Youth Volunteers", 1, 50, 10)


    # Predict button
      if st.button("Predict"):

         # Load the trained model
         rf = joblib.load("random_forest_regressor_model.pkl")

          # Prepare input data for prediction
         input_data = [[selected_data, selected_data_stake,  routes_completed, time_spent, adult_volunteers, doors_in_route, youth_volunteers]]

          # Make prediction
         prediction = rf.predict(input_data)

          # Display the prediction
         st.success(f"Predicted Donation Bags: {prediction[0]}")
          # You can add additional information or actions based on the prediction if needed
    # Page 4: Neighbourhood Mapping
    # Read geospatial data
  geodata = pd.read_csv("Location_data_updated.csv")

  def neighbourhood_mapping():
      st.title("Neighbourhood Mapping")

      # Get user input for neighborhood
      user_neighbourhood = st.text_input("Enter the neighborhood:")

    # Check if user provided input
      if user_neighbourhood:
          # Filter the dataset based on the user input
          filtered_data = geodata[geodata['Neighbourhood'] == user_neighbourhood]

          # Check if the filtered data is empty, if so, return a message indicating no data found
          if filtered_data.empty:
              st.write("No data found for the specified neighborhood.")
          else:
              # Create the map using the filtered data
              fig = px.scatter_mapbox(filtered_data,
                                      lat='Latitude',
                                      lon='Longitude',
                                      hover_name='Neighbourhood',
                                      zoom=12)

              # Update map layout to use OpenStreetMap style
              fig.update_layout(mapbox_style='open-street-map')

              # Show the map
              st.plotly_chart(fig)
      else:
           st.write("Please enter a neighborhood to generate the map.")


# Page 5: Data Collection
  def data_collection():
      st.title("Google Drive Data Collection")
      st.write("Please fill out the Google form to contribute to our Food Drive!")
      google_form_url = "https://forms.gle/Sif2hH3zV5fG2Q7P8"#YOUR_GOOGLE_FORM_URL_HERE
      st.markdown(f"[Fill out the form]({google_form_url})")

  # Main App Logic
  def main():
      st.sidebar.title("ML Journey")
      app_page = st.sidebar.radio("Select a Page", ["Dashboard", "EDA", "ML Modeling", "Neighbourhood Mapping", "Data Collection"])

      if app_page == "Dashboard":
          dashboard()
      elif app_page == "EDA":
          exploratory_data_analysis()
      elif app_page == "ML Modeling":
          machine_learning_modeling()
      elif app_page == "Neighbourhood Mapping":
          neighbourhood_mapping()
      elif app_page == "Data Collection":
          data_collection()

  if __name__ == "__main__":
     main()

elif tabs == "Generate Barcode":

    st.title("Barcode Generator")
    st.write("Enter text to generate a barcode:")

    # User input for barcode text
 #   barcode_text = st.text_input("Enter Text", "")

  #  if st.button("Generate Barcode"):
 #     if barcode_text:
  #       # Generate the barcode using python-barcode library
   #      code128 = barcode.get_barcode_class('code128')
    #     barcode_generated = code128(barcode_text, writer=ImageWriter())
     #    filename = barcode_generated.save('barcode')

        # Display the generated barcode image
      #   st.image(filename)

elif tabs == "Volunteer Registration":

  # Function to create or connect to the SQLite database
  def create_connection():
      conn = None
      try:
          conn = sqlite3.connect('food_drive.db')
          return conn
      except Error as e:
          print(e)
      return conn

  conn = create_connection()
  if conn:
     c = conn.cursor()
     c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT, email TEXT)''')
     conn.commit()

  # Streamlit user registration form
  st.title('"Volunteer Registration"')
  st.write('Create your account:')

  new_username = st.text_input('Enter a username')
  new_password = st.text_input('Enter a password', type='password')
  new_name = st.text_input('Enter your name')
  new_email = st.text_input('Enter your email')

  register_button = st.button('Register')

  if register_button:
      # Check if the username already exists in the database
      query = f"SELECT * FROM users WHERE username='{new_username}'"
      result = c.execute(query).fetchone()

      if result:
          st.error('Username already exists. Please choose a different username.')
      else:
          # Add new user to the database
          insert_query = f"INSERT INTO users (username, password, name, email) VALUES ('{new_username}', '{new_password}', '{new_name}', '{new_email}')"
          c.execute(insert_query)
          conn.commit()
          st.success('Registration successful! Please proceed to login.')
          new_username = ''
          new_password = ''
          new_name = ''
          new_email = ''

  conn.close()

elif tabs == "Volunteer Login":

    # Function to create a new database for food drive
    def create_food_drive_db():
        conn = sqlite3.connect('food_drive.db')  # Connect or create a new database file
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                name TEXT,
                email TEXT
            )
        ''')
        conn.commit()
        conn.close()

    # Function to authenticate user
    def authenticate_user(username, password):
        conn = sqlite3.connect('food_drive.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        return user

    # Streamlit login page
    def login():
        st.title('Food Drive Login')
        create_food_drive_db()  # Create the users table if it doesn't exist

        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            user = authenticate_user(username, password)
            if user:
                st.success('Logged in successfully!')
                st.success(f"Logged in as {username}")
                # Store username and password in session state
                st.session_state.username = username
                st.session_state.password = password
                # Redirect to another page after successful login
                st.experimental_rerun()
                return True

            else:
                st.error('Invalid credentials')
                return False


    def main():
          st.session_state.setdefault('logged_in', False)

          if not st.session_state.logged_in:
            login()
          else:
             tabs == "Food Donation Form"

    if __name__ == '__main__':
          main()


elif tabs == "Food Donation Form":
  if 'username' in st.session_state and 'password' in st.session_state:
      uname = st.session_state.username
      st.write(f'Logged in as: {st.session_state.username}')
    
           
      st.title("Food Drive Donation Form")
      st.write(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
      date_time_data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

      def create_connection():
         conn = None
         try:
             conn = sqlite3.connect('food_drive.db')
             return conn
         except Error as e:
             print(e)
         return conn

      conn = create_connection()
      if conn:
        c = conn.cursor()
        c.execute('''
                  CREATE TABLE IF NOT EXISTS donations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    drop_off_location TEXT,
                    house_address TEXT,
                    number_of_bags INTEGER,
                    donation_date TEXT,
                    volunteer_name TEXT,
                    volunteer_barcode TEXT,
                    volunteer_location TEXT
                  )
                ''')
        conn.commit()
    
        locations = [
                  "Londonderry Chapel",
                  "Gateway Stake Centre",
                  "Bearspaw Chapel",
                  "Bonnie Doon Stake Centre",
                  "Coronation Park Chapel",
                  "North Stake Centre",
                  "Riverbend Stake Centre",
                  "Parkland (Spruce Grove/Stony Plain)",
                  "Morinville",
                  "Onoway"
                  ]

        drop_off_location = st.selectbox("Select Drop-off Location", locations)

        st.write("You selected:", drop_off_location)

        house_address = st.text_input('Route Address')
        number_of_bags = st.number_input('Number of Bags', min_value=1, value=1)
        volunteer_barcode = st.text_input('Bag Barcode')
        volunteer_location = st.text_input('Volunteer Location')

        submit_button = st.button('Submit Donation')

        if submit_button:
            # Add new user to the database
          insert_query = f"INSERT INTO donations (drop_off_location, house_address, number_of_bags, donation_date, volunteer_name, volunteer_barcode, volunteer_location) VALUES ('{drop_off_location}', '{house_address}', '{number_of_bags}', '{date_time_data}', '{uname}' , '{volunteer_barcode}', '{volunteer_location}')"
          c.execute(insert_query)
          conn.commit()
          st.success('Donation Data Added successful!')
          house_address = ''
          number_of_bags = ''
          volunteer_barcode = ''
          volunteer_location = ''

  else:
    st.write('Not logged in!') 

elif tabs == "Collected Food Donation":
      
    # Function to fetch all data and column names from the SQLite table
    def fetch_data_and_columns():
      conn = sqlite3.connect('food_drive.db')  # Replace with your database name
      cursor = conn.cursor()
      cursor.execute('SELECT * FROM donations')  # Replace with your table name
      data = cursor.fetchall()
      columns = [desc[0] for desc in cursor.description]  # Fetch column names here
      conn.close()
      return data, columns

   # Streamlit app to display the table
    def main():
      st.title('Food Drive Dataset')
      st.write('Displaying data from SQLite table')

      # Fetching data and columns from the SQLite table
      table_data, columns = fetch_data_and_columns()

      # If there's data fetched, display it in a Streamlit table
      if table_data:
          df = pd.DataFrame(table_data, columns=columns)
          st.write(df)
      else:
          st.write('No data found in the table.')

    if __name__ == '__main__':
        main()

elif tabs == "Map Generator":
 
  def main():
    st.title('Generated Google Maps')
    st.write('Edmonton data property assesment dataset:')

    # Embedding Google Map using HTML iframe
    st.markdown("""
    <iframe src="https://www.google.com/maps/d/u/0/embed?mid=1Ggf6MerBO7sA1X2qgJ9rnPwoAwRxfic&ehbc=2E312F" width="640" height="480"></iframe>
    """, unsafe_allow_html=True)

  if __name__ == "__main__":
      main()

elif tabs == "Interactive Food Drive Assistant":
  def main():
    # Streamlit title and description
    st.title("Interactive Food Drive Assistant")
    st.write("Ask a question about the Food Drive!")

    with Gradient() as gradient:
        base_model = gradient.get_base_model(base_model_slug="nous-hermes2")
        new_model_adapter = base_model.create_model_adapter(name="interactive_food_drive_model")

        user_input = st.text_input("Ask your question:")
        if user_input and user_input.lower() not in ['quit', 'exit']:
            sample_query = f"### Instruction: {user_input} \n\n### Response:"
            st.markdown(f"Asking: {sample_query}")

            # before fine-tuning
            completion = new_model_adapter.complete(query=sample_query, max_generated_token_count=100).generated_output
            st.markdown(f"Generated: {completion}")

        # Delete the model adapter after generating the response
        new_model_adapter.delete()

  if __name__ == "__main__":
    main()
