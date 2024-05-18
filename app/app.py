import streamlit as st
import pandas as pd
import numpy as np

st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

# Transform the data

pop = pd.read_csv('pop.csv')
gni = pd.read_csv('ny_gnp_pcap_pp_cd.csv')
life = pd.read_csv('lex.csv')

# Fill in missing rows

gni = gni.ffill()
gni = gni.ffill(axis=1)
pop = pop.ffill()
pop = pop.ffill(axis=1)
life = life.ffill()
life = life.ffill(axis=1)

# Converting df from wide to long format

gni = pd.melt(gni, id_vars=['country'], var_name='year', value_name='gni')
pop = pd.melt(pop, id_vars=['country'], var_name='year', value_name='population')
life = pd.melt(life, id_vars=['country'], var_name='year', value_name='life_expectancy')

# Converting year column to numeric
gni['year'] = pd.to_numeric(gni['year'], errors='coerce')
pop['year'] = pd.to_numeric(pop['year'], errors='coerce')
life['year'] = pd.to_numeric(life['year'], errors='coerce')

# Merging together

df = pd.merge(gni, pop, on=['country', 'year'])

df = pd.merge(df, life, on=['country', 'year'])


# Function to clean and convert GNI and population data

def clean_numbers(value):
    if isinstance(value, str):
        if 'k' in value:
            return int(float(value.replace('k', '')) * 1e3)
        elif 'M' in value:
            return int(float(value.replace('M', '')) * 1e6)
        elif 'B' in value:
            return int(float(value.replace('B', '')) * 1e9)
        else:
            return int(value)
    return value
    
# Clean and preprocess the data

df['gni'] = df['gni'].apply(clean_numbers)
df['population'] = df['population'].apply(clean_numbers)

# Apply the logarithmic transformation

df['gni'] = np.log(df['gni'])

# Filtering widgets

selected_countries = st.multiselect('Select Countries', df['country'].unique(), default='Pakistan')
selected_year = st.slider('Year :calendar:', min_value=1800, max_value=2022, value=2022, step=1)

filtered_df = df[(df['country'].isin(selected_countries)) & (df['year'] == selected_year)]

# Creating scatter plot
if not filtered_df.empty:
    st.scatter_chart(filtered_df, x='gni', y='life_expectancy', color='country', size=('population'), width=10)
else:
    st.write("No data available for the selected year and countries.")

st.cache_data()