import streamlit as st
from streamlit_option_menu import option_menu
import home, overview, agents, location, date, Hotel

st.set_page_config(
    page_title='Supplier Booking Report',layout="wide")

class MultiApp:
    def __init__ (self):
        self.apps = []
    def add_app (self,title,function):
        self.apps.append({
            "title": title,
            "function": function
        })
    def run():
        with st.sidebar:
            image_url = "Saltours logo.jpg"
            st.image(image_url,width=100, use_column_width=False)
            st.header('Supplier Booking Report')
            app = option_menu(
                menu_title="Options:",
                options=['Home','Overview','Agents','Location','Date','Hotel'],
                default_index=1,
                styles = {
                    "containers": {"padding": "5px!important", "background-color": "grey"},
                    "icons": {"color": "black", "font-size": "23px"},
                    "nav-link": {"color": "black", "font-size": "20px", "text-align": "left"},
                    "nav-link-selected": {"background-color": "#02ab21"}
                }

            )
            
        if app == "Home":
            home.app()
        if app == "Overview":
            overview.app()
        if app == "Agents":
            agents.app()
        if app == "Location":
            location.app()
        if app == "Date":
            date.app()
        if app =="Hotel":
            Hotel.app()
        
                
    run()