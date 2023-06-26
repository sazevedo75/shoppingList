from deta import Deta
from pprint import pprint
import streamlit as st

DETA_KEY = st.secrets.DETA_KEY
deta = Deta(DETA_KEY)

sl = deta.Base("shoppingList")

#---SHOPPING LIST FUNCTIONS---#
def enter_shopping_list_items(key, week, shopping_list, bought):
    """This function will add all items in the shopping_list dictionary and the week title to the database with the week number as a key. Will return None if successful. """
    return sl.put({"key":str(key), "week":str(week), "shopping_list":shopping_list, "bought":bought})


def get_shopping_list(week):
    """Returns the entire shopping list item for a certain week based on the period. This period is the week title used in the function above."""
    return sl.get({"week":str(week)})

def getAllItems():
    return sl.fetch().items

def updateItem(grocery, key):

    if grocery["bought"] == True:
        grocery["bought"] = False
    else:
        grocery["bought"] = True
    
    shopping_list_update_line = {f"bought": grocery["bought"]}

    sl.update(shopping_list_update_line, key)
           

def remove_item_shopping_list(week, item_cat, item_to_remove):
    """Function  to remove a single item from the list. It takes a weeknumber as the principal key to get the list for the correct week. The item_cat selects the category and the item_to_remove is the actual item to get rid off. The same update function as above is then used to apply the changes."""
    shopping_list_to_change = get_shopping_list(week)["shopping_list"][item_cat]['items']
    shopping_list_to_change.remove(item_to_remove)
    print(shopping_list_to_change)
   
    shopping_list_update_line = {
        f"shopping_list.{item_cat}.items": shopping_list_to_change
        }
    sl.update(shopping_list_update_line, week)