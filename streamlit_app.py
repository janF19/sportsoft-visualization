# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import streamlit as st

# Environment configuration
IS_PRODUCTION = os.getenv('RUNNING_IN_PRODUCTION', 'false').lower() == 'true'
HOST = '0.0.0.0' if IS_PRODUCTION else 'localhost'
PORT = int(os.getenv('PORT', 5000))
BASE_URL = os.getenv('RENDER_EXTERNAL_URL', f'http://{HOST}:{PORT}')

st.set_page_config(
    page_title="Sports Participation Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)



# Add this to handle CORS and running behind a proxy
if not os.getenv("RUNNING_IN_PRODUCTION"):
    # Local development
    BASE_URL = "http://localhost:8501"
else:
    # Production on Render.com
    BASE_URL = "https://your-app-name.onrender.com"

def load_preprocessed_data():
    """Load the preprocessed data from JSON files"""
    try:
        with open('preprocessed_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open('stats.json', 'r') as f:
            stats = json.load(f)
        return data, stats
    except Exception as e:
        st.error(f"Error loading preprocessed data: {str(e)}")
        return None, None

def create_dataframe_from_dict(data_dict):
    """Recreate DataFrame from the dictionary format"""
    if not data_dict:
        return pd.DataFrame()
    
    df = pd.DataFrame(
        data_dict['values'],
        index=data_dict['index'],
        columns=data_dict['columns']
    )
    # Set the index name explicitly
    df.index.name = data_dict['index_name']
    return df

def create_participation_chart(data, title):
    """Create an interactive line chart using Plotly"""
    if data is None or data.empty:
        return None
    
    # Reset index to make the date-year column available
    melted_data = data.reset_index().melt(
        id_vars=['date-year'],
        var_name='category',
        value_name='participants'
    )
    
    fig = px.line(
        melted_data,
        x='date-year',
        y='participants',
        color='category',
        markers=True,
        title=title
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Unique Athletes",
        legend_title="Event/Sport",
        hovermode='x unified'
    )
    
    return fig

def main():
    
    
   

    st.title("Sports Participation Analysis Dashboard")

    # Load preprocessed data
    data, stats = load_preprocessed_data()
    if not data or not stats:
        st.error("Could not load preprocessed data")
        return

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "All Sports", 
        "Running Events", 
        "MTB Events",
        "Road Cycling Events"
    ])

    with tab1:
        st.header("Participation Across All Sports")
        df_all = create_dataframe_from_dict(data['all_sports'])
        if not df_all.empty:
            fig1 = create_participation_chart(df_all, "Athlete Participation by Sport Over Time")
            st.plotly_chart(fig1, use_container_width=True)

            # Display statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Athletes", f"{stats['total_athletes']:,}")
            with col2:
                st.metric("Total Events", f"{stats['total_events']:,}")
            with col3:
                st.metric("Years Covered", f"2011–2024")

    with tab2:
        st.header("Running Events Analysis")
        df_running = create_dataframe_from_dict(data['running'])
        if not df_running.empty:
            fig2 = create_participation_chart(df_running, "Participation in Running Events Over Time")
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.header("Mountain Biking Events Analysis")
        df_mtb = create_dataframe_from_dict(data['mtb'])
        if not df_mtb.empty:
            fig3 = create_participation_chart(df_mtb, "Participation in MTB Events Over Time")
            st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        st.header("Road Cycling Events Analysis")
        df_road = create_dataframe_from_dict(data['road'])
        if not df_road.empty:
            fig4 = create_participation_chart(df_road, "Participation in Road Cycling Events Over Time")
            st.plotly_chart(fig4, use_container_width=True)

if __name__ == "__main__":
    main()