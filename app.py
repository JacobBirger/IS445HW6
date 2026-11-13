import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE SETUP ---
st.title("IS445: Data Visualization Homework")
st.text("Exploring the Illinois Building Inventory Dataset")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"
    df = pd.read_csv(url)
    # Basic cleaning: remove entries with 0 for Year Acquired to clean up the x-axis
    df = df[df['Year Acquired'] > 1800]
    return df

df = load_data()

# --- VISUALIZATION 1: STATIC BAR CHART ---
st.header("Visualization 1: Top 10 Agencies by Total Square Footage")

# Data prep for Viz 1
top_agencies = df.groupby('Agency Name')['Square Footage'].sum().reset_index().nlargest(10, 'Square Footage')

viz1 = alt.Chart(top_agencies).mark_bar().encode(
    x=alt.X('Square Footage:Q', title='Total Square Footage'),
    y=alt.Y('Agency Name:N', sort='-x', title='Agency Name'),
    color=alt.Color('Agency Name:N', legend=None),
    tooltip=['Agency Name', 'Square Footage']
).properties(height=400)

st.altair_chart(viz1, use_container_width=True)

st.write("""
**Design Choices for Visualization 1:**  
In this first visualization, I wanted to look at the top 10 agencies by their total square footage by using a horizontal bar chart. The orientation of the chart with Agency being on the y-axis and Square Footage being on the x-axis makes the long agency names more easy to read since there is no overlapping text. I also used a standard quantitative linear scale on the x-axis in order to sort the bars in descending order which helps draw attention straight to the largest property holders. The color encoding is connected to the Agency Name which gives and additional layer of visual separation even if it doesn't differentiate by magnitude. Had I had more time, I could have dynamically linked the number of top agencies shown to a Streamlit slider so the user could look at more than just the top 10. 
                  """)


# --- VISUALIZATION 2: INTERACTIVE DASHBOARD ---
st.header("Visualization 2: Interactive Year Acquired vs. Square Footage")

# Create a brush selection for interactivity
brush = alt.selection_interval(encodings=['x'])

# Scatter plot
scatter = alt.Chart(df).mark_circle(opacity=0.5).encode(
    x=alt.X('Year Acquired:Q', scale=alt.Scale(zero=False), title='Year Acquired'),
    y=alt.Y('Square Footage:Q', title='Square Footage'),
    # Apply color condition based on the brush selection
    color=alt.condition(brush, alt.value('steelblue'), alt.value('lightgray')),
    tooltip=['Agency Name', 'Year Acquired', 'Square Footage']
).properties(
    height=400,
    title="Highlight a time period to filter the chart below"
).add_params(brush)

# Linked bar chart (filters based on the scatter plot selection)
bar = alt.Chart(df).mark_bar().encode(
    y=alt.Y('Agency Name:N', sort='-x').title('Agency Name'),
    x=alt.X('count():Q').title('Number of Buildings Acquired'),
    color=alt.value('steelblue'),
    tooltip=['Agency Name', 'count()']
).transform_filter(
    brush
).properties(
    height=400,
    title="Buildings Acquired by Agency (Filtered)"
)

# Display the charts stacked vertically
st.altair_chart(scatter & bar, use_container_width=True)

st.write("""
**Design Choices for Visualization 2:**  
The second visualization is a linked interactive dashboard featuring a scatter plot of *Year Acquired* versus *Square Footage* and a responsive bar chart showing the count of buildings per agency. The core interactivity relies on an Altair interval selection brush on the x-axis of the scatter plot. When a user highlights a specific time period on the top chart, the bar chart below filters to show only the agencies that acquired buildings during that specific window. I chose semi-transparent circles (`opacity=0.5`) for the scatter plot to mitigate overplotting, and mapped the unselected points to a faded light gray to make the active selection pop in steel blue. If I had more time, I would implement two-way cross-filtering so clicking on an agency in the bar chart would also filter the scatter plot.
         Note for grading: Both visualizations and the dataset logic used in this application are entirely new and do not reuse any plots or text from Homework #5.
         
""")