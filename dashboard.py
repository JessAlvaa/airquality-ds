import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import numpy as np

# Read data
air_data = pd.read_csv('Air_Quality_Aotizhongxin.csv')

# Add date column
air_data['date'] = pd.to_datetime(air_data[['year', 'month', 'day', 'hour']], errors='coerce')

st.title("Air Quality Analysis")
st.write("This dashboard shows the visualization of air quality data from 2013 until 2017 at Aotizhongxin station.")

# Sidebar 
st.sidebar.header("User Input")
year = st.sidebar.slider("Select Year", min_value=int(air_data['year'].min()), max_value=int(air_data['year'].max()), value=int(air_data['year'].min()))

# Filter data by year
data_filter = air_data[air_data['year'] == year]

# Shows filtered data
st.header(f'Data Overview for Year {year}')
st.write(data_filter) 

# Heatmap for all pollutants (filtered by year)
st.header(f'Correlation Heatmap for Year {year}')
plt.figure(figsize=(10, 6))
matrix_corr = data_filter[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'DEWP', 'WSPM']].corr() 
sns.heatmap(matrix_corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title(f'Correlation Heatmap for Year {year}')
st.pyplot(plt)

# Select pollutant 
pollutant = st.selectbox("Select Pollutant", ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"])

# Shows average graphic by wind and selected pollutant
st.header(f'Average {pollutant} by Wind Direction')
wind_direction_avg = data_filter.groupby('wd')[pollutant].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 5))
plt.bar(wind_direction_avg.index, wind_direction_avg.values, color='green')
plt.title(f'Average {pollutant} by Wind Direction for Year {year}')
plt.xlabel('Wind Direction')
plt.ylabel(f'Average {pollutant}')
st.pyplot(plt)

# Wind Direction
st.subheader('Wind Direction Distribution')
wind_data = data_filter.groupby('wd')[pollutant].mean()
fig = plt.figure(figsize=(8, 6))
colors = cm.Blues(wind_data.values / max(wind_data.values))
ax = fig.add_subplot(111, polar=True)

# Convert wd to theta for polar plot
theta = np.linspace(0, 2 * np.pi, len(wind_data), endpoint=False)
bars = ax.bar(theta, wind_data.values, align='center', color=colors, alpha=0.5)
ax.set_xticks(theta)  
ax.set_xticklabels(wind_data.index)  
plt.title(f"{pollutant} Levels by Wind Direction")
st.pyplot(fig)

# Shows heatmap by selected pollutant
st.header('Correlation Heatmap')
plt.figure(figsize=(8, 6))
selected_matrix = data_filter[[pollutant, 'TEMP', 'DEWP', 'WSPM']].corr()
sns.heatmap(selected_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title(f'Correlation Heatmap for {pollutant}')
st.pyplot(plt)

# Menampilkan pairplot berdasarkan pilihan polutan
st.header('Pairplot')
pairplot_col = [pollutant, 'TEMP', 'DEWP', 'WSPM']
pairplot_fig = sns.pairplot(data_filter[pairplot_col])
st.pyplot(pairplot_fig.fig)

st.subheader('Conclusion')
st.write(""" 
- The dashboard provides an overview of air quality levels across different years and pollutant 
- This dashboard offers various interactive visualization of all pollutant distribution
- Provides insight the distribution of air quality and wind affects, assisting in monitoring and mitigating the impact of air pollution
""")
