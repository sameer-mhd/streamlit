import streamlit as st
import pandas as pd
import os
from agno.agent import Agent
from agno.models.google import Gemini 
from dotenv import load_dotenv
from bigquery import upload_csv_to_bigquery
from bigquery_response import response_data

load_dotenv()
api_key=os.environ.get("G_KEY")
 
st.set_page_config(page_title="Analyze your Data with AI", page_icon="♾️")
 
st.title("♾️ Data Analysis with Gemini AI")
 
uploaded_file = st.file_uploader("Choose a file")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
 
if uploaded_file is not None:
 
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
 
    column_names = dataframe.columns.values
    names = pd.DataFrame(column_names,columns=['columns'])
    list_of_columns = names.values.tolist()
 
    prompt = str(st.chat_input("Ask something on the uploaded data"))
 
    #-----------start-----------------------
 
    agent = Agent(
    model=Gemini(id="gemini-1.5-flash", 
                api_key=api_key                
                ),
 
    description="Your a skilled SQL data engineer and data summarizer ",
 
    instructions=[

        "Provide the description & Suggestions based on the prompts related to SQL and Data Modelling",
    ],
    
    markdown=True,
    )
    #------------end----------------------
     
    print(prompt)
 
    if prompt == "None":
        initial_response = list_of_columns
        response = agent.run('Describe the following '+str(initial_response))
        st.write(f"**Gemini AI:** {response.content}")
        print('---------Initial Response----------')
        print(list_of_columns)        
        upload_csv_to_bigquery(dataframe)

        st.write("**Uploaded Data has been Analyzed you can ask further Queries**")

    else:
        response_be = agent.run('The columns are:'+str(list_of_columns)+'and table name is proj2026.streamlit.data create only Bigquery SQL statement for'+str(prompt)+'Only SQL code required')
        bq_res = response_data(response_be.content)


        try:
            response_ui = agent.run('Analyze the data and respond not more than one line'+bq_res)
            st.write("**Highlights on Data:**")
            st.write(response_ui.content)
        except Exception as e:
            st.write(e)



        print('--------Response from Chat--------')
