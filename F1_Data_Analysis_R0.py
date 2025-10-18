# Import packages and set plots to be displayed inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

# Load data and assign column names
# Datasets from Kaggle F1 dataset
#results = pd.read_csv('results.csv')
results = pd.read_csv('results.csv', skiprows=1, names = ['result_id', 'race_id', 'driver_id', 'constructor_id', 'number', 'grid', 'position', 'position_text', 'position_order', 'points', 'laps', 'time', 'milliseconds', 'fastest_lap', 'rank', 'fastest_lap_time', 'fastest_lap_speed', 'status_id'],header = None)
races = pd.read_csv('races.csv', skiprows=1, usecols=[0,1,2,3,4,5,6,7], names = ['race_id', 'year', 'round', 'circuit_id', 'name', 'date', 'time', 'URL'], header = None)
drivers = pd.read_csv('drivers.csv', skiprows=1, names = ['driver_id', 'driver_ref', 'number', 'code', 'forename', 'surname', 'DOB', 'nationality', 'URL'], header = None)
constructors = pd.read_csv('constructors.csv', skiprows=1, names = ['constructor_id', 'constructor_ref', 'name', 'nationality', 'URL'], header = None)

# Set options to display all rows and columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000) # Width of dataframe adjustment

# Testing dataframe display result
#print(constructors.head())


# merge datasets
df = pd.merge(results, races[['race_id', 'year', 'name', 'round']], on = 'race_id', how='left') # on='race_id' is telling python to merge right data frame into left data frame beginning ON this column, how='left' is taking all rows from left table and only matching rows from right table
df = pd.merge(df, drivers[['driver_id', 'driver_ref', 'nationality']], on = 'driver_id', how = 'left')
df = pd.merge(df, constructors[['constructor_id', 'name', 'nationality']], on = 'constructor_id', how = 'left')

#print(df)

# Drop unnecessary columns
df.drop(['number', 'position', 'position_text', 'laps', 'fastest_lap', 'status_id', 'result_id', 'race_id', 'driver_id', 'constructor_id'], axis=1, inplace=True)

# Rename columns
df.rename(columns={'rank':'fastest_lap_rank','name_x':'gp_name', 'nationality_x':'driver_nationality','name_y':'constructor_name','nationality_y':'constructor_nationality','driver_ref':'driver'},inplace=True)

#print(df)
# Rearrange columns
df = df[['year', 'gp_name', 'round', 'driver', 'constructor_name', 'grid', 'position_order', 'points', 'time', 'milliseconds', 'fastest_lap_rank', 'fastest_lap_time', 'fastest_lap_speed', 'driver_nationality', 'constructor_nationality']]

#print(df.head())

# Drop 2019 season because the data set is incomplete
df = df[df['year']!=2019]
#print(df.head(21))

# Sort values
df = df.sort_values(by=['year', 'round', 'position_order'], ascending=[False, True, True])
#print(df.head(21))

# Replace \N values in time column
df.time.replace('\\N',np.nan,inplace=True)
df.milliseconds.replace('\\N',np.nan,inplace=True)
df.fastest_lap_rank.replace('\\N',np.nan,inplace=True)
df.fastest_lap_time.replace('\\N',np.nan,inplace=True)
df.fastest_lap_speed.replace('\\N',np.nan,inplace=True)
#print(df.head(21))

# Change datatypes
df.fastest_lap_rank = df.fastest_lap_rank.astype(float)
df.fastest_lap_speed = df.fastest_lap_speed.astype(float)
df.milliseconds = df.fastest_lap_speed.astype(float)
#print(df.head(21))

# Reset index to start indexing from 0 at the sorted row
df.reset_index(drop=True, inplace=True)
#print(df.head(21))

# Shape - returns total number of (rows, columns)
#print(df.shape)

# Info - returns all column names, total number of non-null objects, and memory usage
#df.info()

# head() - returns df table info for specified number of rows
#print(df.head(10))

# Setting Seaborn library Figure settings
sb.set_palette('Set3')
plt.rcParams['figure.figsize']=10,6

# Create dataframe with all GP winners
driver_winner=df.loc[df['position_order']==1].groupby('driver')['position_order'].count().sort_values(ascending=False).to_frame().reset_index()

# Barplot
#sb.barplot(data=driver_winner, y='driver', x='position_order', color='green', alpha=0.8)
#plt.title('Most GP Winners in F1')
#plt.ylabel('Driver Name')
#plt.xlabel('Number of GP Wins')
#plt.yticks([])
#plt.show()

# Create new dataframe of only top 10 GP winners
top10Drivers = driver_winner.head(10)
print(top10Drivers)

#print(df[['driver']])

# Top 10 Drivers plot
sb.barplot(data=top10Drivers, y='driver', x='position_order', color='blue', alpha=0.8, linewidth=0.8, edgecolor='black')
#plt.bar(data=top10Drivers, y='driver', x='position_order', height=0.8, width=0.8, color='blue', alpha=0.8, linewidth=0.8, edgecolor='black')
plt.title('Most GP Winners in F1 (Top 10)')
plt.ylabel('Driver Name')
plt.xlabel('Number of GP Wins')
plt.yticks([])
plt.show()

#print(df['driver'].dtype == 'object')
#print(isinstance(df['driver'].dtype, pd.StringDtype))

# GP Constructor winners
constructor_winner=df.loc[df['position_order']==1].groupby('constructor_name')['position_order'].count().sort_values(ascending=False).to_frame().reset_index()

#barplot
sb.barplot(data = constructor_winner, y = 'constructor_name', x = 'position_order', color='pink', alpha=0.8, linewidth=0.8, edgecolor='black')
plt.title('Most GP Winners in F1')
plt.ylabel('Constructor Name')
plt.xlabel('Number of GP Wins')
plt.yticks([])
plt.show()

# Top 10 GP Constructor Winners
top10Constructors=constructor_winner.head(10)
print(top10Constructors)

# Top 10 GP Constructor Winner bar plot
sb.barplot(data = top10Constructors, y = 'constructor_name', x = 'position_order', color='orange', alpha=0.8, linewidth=0.8, edgecolor='black')
plt.title('Most GP Winners in F1 (Top 10)')
plt.ylabel('Constructor Name')
plt.xlabel('Number of GP Wins')
plt.yticks([])
plt.show()

df_no_zero = df[df['grid'] != 0] #exclude grid 0 date (pit lane start) to avoid data skew

#create a plot
plt.figure(figsize = [12,7])
sb.regplot(data=df_no_zero, x='grid', y='position_order', x_jitter = 0.3, y_jitter = 0.3, scatter_kws={'alpha':1/5})
plt.title('Starting Position vs. Finish Position')
plt.ylabel('Finish Position')
plt.xlabel('Starting Position')
plt.show()

# Create new dataframe for season 2004 onwards
df_speed = df[df['year'] >= 2004]
df_group_speed = df_speed.groupby(['gp_name', 'year'])['fastest_lap_speed'].mean().to_frame().reset_index()

#create a facet grid
g = sb.FacetGrid(data = df_group_speed, col = 'gp_name', col_wrap=5)
g.map(plt.scatter, 'year', 'fastest_lap_speed', alpha = 0.8, linewidth = 0.8, edgecolor = 'black', s=100)
g.set_titles("{col_name}")
g.set_xlabels('Year')
g.set_ylabels('Average Fastest Speed (km/hr)')
plt.subplots_adjust(top=0.92)
g.fig.suptitle('Average speed amongst all teams during the fastest lap at individual GPs')
plt.show()

# Adding comments to log changes for git hub test



