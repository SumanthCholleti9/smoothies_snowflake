# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title("Customize Your Smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want in your **Custom Smoothie!**
    """
)

option1=st.selectbox(
    'How would you like to be contacted?',
    ('E-mail','Home-phone','Mobile-phone')
)

st.write('Preferred Method:',option1)

from snowflake.snowpark.functions import col

session=get_active_session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe,use_container_width=True)
ingredient_list=st.multiselect('Choose upto 5 ingredients:',my_dataframe)

if ingredient_list:
    ingredients_string= ''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)
    my_insert_stmnt=""" insert into smoothies.public.orders(ingredients) values
       ('""" + ingredients_string + """')"""
    #st.write(my_insert_stmnt)
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmnt).collect()
        st.success('Your smoothie is ordered!')
