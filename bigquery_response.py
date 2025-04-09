from google.cloud import bigquery
import re
import pandas as pd
import streamlit as st

client = bigquery.Client()

def response_data(ai_data):
# Perform a query.
    QUERY = str(ai_data)
    s = QUERY.replace('sql','')
    m = s.replace('```','')
    t = m.replace('```','')
    print(QUERY)
    query_job = client.query(t)  # API request

    try:
        data = query_job.result()  # Waits for query to finish
    except Exception as e:
        data = []
    
    # Convert the query results to a list of dictionaries
    rows = list(data)  # List of Row objects

    try:
        if rows:
            df = pd.DataFrame([dict(row) for row in rows])  # Convert each Row object into a dictionary
            st.write("**Gemini AI: Data from BigQuery**")
            st.write(df)  # Display the DataFrame as a table in Streamlit

        else:
            st.write("No data available.")
            df = 'No data available'
    except Exception as e:
        st.write(e)

    return f"{df}"
