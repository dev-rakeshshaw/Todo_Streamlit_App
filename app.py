import pymongo  
import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Todo Streamlit App",
    page_icon="./images/todo.ico",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)



#Function to create Database
def create_database(db_name):
    if db_name in client.list_database_names():
        print(f"{db_name} already present")
        todo_db_obj = client[db_name]
    else:
        todo_db_obj = client[db_name]
        print(f"{db_name} Created")
    return todo_db_obj

#Function to create collection
def create_collection(todo_db_obj,collection_name):
    if collection_name in todo_db_obj.list_collection_names():
        print(f"{collection_name} already present")
        todo_collection_obj=todo_db_obj[collection_name]
    else:
        todo_collection_obj=todo_db_obj[collection_name]
        print(f"{collection_name} Created")
    return todo_collection_obj

#Function To insert one document
def insert_document(todo_collection_obj,todo_data):
    todo_id = todo_collection_obj.insert_one(todo_data).inserted_id
    return todo_id
    

#Function To read documents based on query
def read_documents(todo_collection_obj,query=""):
    mytodos = todo_collection_obj.find(query)
    return mytodos

#Function for todos input from user using streamlit.
def todos_input():
    
    with st.form(key='myform',clear_on_submit=True):
        name=st.text_input("Enter Your Name")
        day=st.text_input("Enter the Day")
        task=st.text_input("Enter Your task")
        st.form_submit_button("Submit")

    return [name,day,task]

    
if __name__ == '__main__':

    username=st.secrets.mongodb_atlas.username
    password=st.secrets.mongodb_atlas.password

    client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.yndrb7y.mongodb.net/?retryWrites=true&w=majority")
    db = client.test

    #Creating the database.
    db_name="todo_db"
    todo_db_obj=create_database(db_name)
    # todo_db_obj

    #Creating the collection.
    collection_name="todo_collection"
    todo_collection_obj = create_collection(todo_db_obj,collection_name)
    # todo_collection_obj

    #Title of the App
    st.title("Todo Streamlit App")
   
    #Collecting todo from user
    data = todos_input()
   
    todo_data={
        "Early_Morning":data[0],
        "Morning":data[1],
        "Noon":data[2]}


    #Inserting the document in the collection.
    if "" not in todo_data.values():
        todo_id=insert_document(todo_collection_obj,todo_data)
        print(f"Todo with id {todo_id} has been created")
    else:
        st.error('Please fill all the fields.', icon="🚨")


    #Fetching the documents based on queries.
    query={}
    # query={"Night":"Study"}
    mytodos = read_documents(todo_collection_obj,query)
    mytodos=list(mytodos)
    df = pd.DataFrame(mytodos)
    st.table(df)

    # st.snow()
