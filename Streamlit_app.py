# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title("Customize Your Smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want in your **Custom Smoothie!**
    """
)

name=st.text_input('Name on smoothie: ')
st.write('The smoothie order will be',name)

option1=st.selectbox(
    'How would you like to be contacted?',
    ('E-mail','Home-phone','Mobile-phone')
)

st.write('Preferred Method:',option1)

Contact=st.text_input("Provide the detail of contact box chosen")
st.write('Contact details:',Contact)

cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredient_list=st.multiselect('Choose upto 5 ingredients:',my_dataframe,max_selections=5)

if ingredient_list:
    ingredients_string= ''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutritional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        name_on_order=name
        contact_details=Contact
    #st.write(ingredients_string)
    my_insert_stmnt=""" insert into smoothies.public.orders(ingredients,name_on_order,contact_details) values
       ('""" + ingredients_string + """','""" + name_on_order + """','""" + contact_details + """')"""
    #st.write(my_insert_stmnt)
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmnt).collect()
        st.success('Your smoothie is ordered!')
        


