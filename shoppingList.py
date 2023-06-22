#---PIP PACKAGES---#
import streamlit as st
from streamlit_option_menu import option_menu
from isoweek import Week
import random

#---BUILT-IN PYTHON MODULES
from datetime import datetime, date
import calendar
import uuid

#---IMPORT THE DATABASE PYTHON FILE db.py---#
import db as db

#---STREAMLIT SETTINGS---#
pageTitle = "Weekly Shopping List App"
pageIcon = ":pouch:"
layout = "centered"

#---STREAMLIT PAGE CONFIG---#
st.set_page_config(page_title=pageTitle, page_icon=pageIcon, layout=layout)
st.title(f"{pageTitle} {pageIcon}")

#---STREAMLIT CONFIG HIDE---#
hide_st_style = """<style>
                #MainMenu {visibility : hidden;}
                footer {visibility : hidden;}
                header {visibility : hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

#---PERIOD VALUES---#
year = datetime.today().year
month = datetime.today().month
day = datetime.today().day
months = list(calendar.month_name[1:])
week_number = date(year, month, day).isocalendar()[1]
week = Week(year, week_number)
week_plus1 = Week(year, week_number + 1)


#---NAV BAR---#
nav_menu = option_menu(
    menu_title = None,
    options = ["Current Week", "History"],
    icons = ["list-task", "cup-straw" ],
    orientation = "horizontal"
)

if nav_menu == "Current Week":
    st.header(f"Monday {week.monday()} to Sunday {week.sunday()}")


    with st.form("entry_form", clear_on_submit=True):
                    
        shoppingList = st.text_input("Groceries","")
        
        submitted = st.form_submit_button("Save item", type = "primary")  

    if submitted:               
                key = uuid.uuid4()

                db.enter_shopping_list_items(key, week_number, shoppingList, False)


    with st.expander(label="List of Groceries", expanded=True):
        
        current_shopping_list = db.getAllItems()

        if current_shopping_list:
            for grocery in current_shopping_list:
                if grocery["weeknumber"] == week_number:
                    st.checkbox(label = grocery["shopping_list"], value = grocery["bought"], 
                                on_change=db.updateItem, args=(grocery, str(grocery["key"])))    
        else:
            st.caption(f"You have not created a shopping list yet for week from Thursday {week.thursday()} to Wednesday {week_plus1.wednesday()}")


#---HISTORY TAB---#

if nav_menu == "History":

    current_shopping_list = db.getAllItems()

    for wk in range(52):
        with st.expander(label=f"Semana {wk}", expanded=False):
            for grocery in current_shopping_list:
                if grocery["weeknumber"] == wk:
                    st.checkbox(label = grocery["shopping_list"], value = grocery["bought"], disabled=True)    