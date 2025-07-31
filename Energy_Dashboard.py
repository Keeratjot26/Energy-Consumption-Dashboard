# energy_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Setup
st.set_page_config(page_title="Energy Dashboard", layout="wide")
sns.set(style='whitegrid', palette='pastel')
np.random.seed(42)

#Palette = Your paint colors. Like are you painting with warm reds or cool blues? Vibrant neon or soft pastels?
#Style = Your canvas and frame. Is the canvas white, black, with grid lines, or with little ticks on the edges?



# Generate dataset
num_rows = 1000
states = ['Delhi', 'Mumbai', 'Kolkata', 'Jammu & Kashmir', 'Gujarat']
regions = ['Urban', 'Rural']
appliances = ['AC', 'Fridge', 'Fan', 'TV', 'Lights']
time_of_day = ['Morning', 'Afternoon', 'Evening', 'Night']

data = {
    'Household_ID': np.arange(1, num_rows + 1),
    'State': np.random.choice(states, num_rows),
    'Region': np.random.choice(regions, num_rows),
    'Appliances': np.random.choice(appliances, num_rows),
    'Units_Consumed': np.round(np.random.normal(4, 2, num_rows), 2),
    'Usage Time': np.random.choice(time_of_day, num_rows),
    'Monthly Income': np.random.randint(10000, 100000, num_rows)
}

df = pd.DataFrame(data)

# Tariff calculation
def calculate_tariff(units):
    if units <= 2:
        return 'Low'
    elif 2 < units <= 5:
        return 'Medium'
    else:
        return 'High'

df['Tariff_Slab'] = df['Units_Consumed'].apply(calculate_tariff)

# Sidebar Filters
st.sidebar.header("Filter the Data 🎛️")

state = st.sidebar.selectbox("State", [""] + df['State'].unique().tolist(), index=0)
region = st.sidebar.selectbox("Region", ['All'] + df['Region'].unique().tolist())
time_list = st.sidebar.multiselect("Time of Day", options=df['Usage Time'].unique().tolist(), default=df['Usage Time'].unique().tolist())

# Filter dataset
filtered = df.copy()
if state != "":
    filtered = filtered[filtered['State'] == state]
if region != 'All':
    filtered = filtered[filtered['Region'] == region]
filtered = filtered[filtered['Usage Time'].isin(time_list)]

st.title("🏠 Household Energy Consumption Dashboard")

st.markdown(f"### Showing {len(filtered)} filtered records")

# Display head of data
st.dataframe(filtered.head())

# Plotting
fig, axes = plt.subplots(3, 1, figsize=(8, 10))

# Countplot
ax = sns.countplot(data=filtered, y="Appliances", palette='mako', ax=axes[0])
axes[0].set_title(f'Appliance Usage in {state if state else "All States"}')
axes[0].tick_params(axis='x', rotation=45)
for bar in ax.patches: #ax.patches consists of a list of all the bars present in the plot so we loop through each of them one by one
    width = bar.get_width() # we get the width of the bar i.e the total count of appliances used that we want to show on top of the bar
    ax.text( #we are adding the label/count on the plot 
        width+1, # to place the count on the right of the bar 
        bar.get_y()+ bar.get_height()/2,
        #bar.get_y() → finds the bottom edge of the bar ,bar.get_height() → the vertical thickness of the bar.
        #So, bar.get_y() + bar.get_height()/2 puts the text at the vertical center of the bar → keeps the label nice and aligned with            the bar.
        str(width) ,# we convert it to string the count/width that we want to annotate 
        ha = 'left',
        va = 'center',
        fontsize = 9
    )
        
# Pie Chart
tariff_counts = filtered['Tariff_Slab'].value_counts()
max_index = tariff_counts.idxmax() # it returns high, medium or low -> since i want to highlight the max slab and highlight it returns the label of the row with the max value
explode = [0.1 if slab == max_index else 0 for slab in tariff_counts.index] # Create explode list: 0.1 for max, 0 for others
axes[1].clear()

axes[1].pie(
    tariff_counts.values,autopct='%1.1f%%', labels=tariff_counts.index,colors=sns.color_palette("pastel"),explode = explode,shadow = True)

axes[1].set_title('Tariff Distribution with highlighted Max distribution')
axes[1].set_ylabel('')

# Scatterplot
sns.scatterplot(data=filtered, x='Monthly Income', y='Units_Consumed',
                hue='Region', alpha=0.6, ax=axes[2])
axes[2].set_title('Income vs Consumption')
plt.tight_layout()
# Render plots
st.pyplot(fig)
plt.grid(True)
