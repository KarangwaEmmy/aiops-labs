# %% [markdown]
# # Step 1: Install and Import Libraries

# %%
# Get time series data
#import yfinance as yf

# Prophet model for time series forecast
from prophet import Prophet

# Data processing
import numpy as np
import pandas as pd

# Visualization
import seaborn as sns
import matplotlib.pyplot as plt

# Model performance evaluation
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

# %% [markdown]
# # Step 2: Pull Data

# %%
import json

# %%
f = open("frontend_shipping_source_300m_30s_pruned.json")
prom = json.load(f)
df_train = pd.DataFrame( prom['data']['result'][0]['values'] )
df_train.columns = ['ds', 'y']
df_train

# %%
f = open("20min.json")
prom = json.load(f)
df_test = pd.DataFrame( prom['data']['result'][0]['values'] )
df_test.columns = ['ds', 'y']
df_test.head()
    

# %%
#align test timestamps with training by time shifting back to the first train time...assume test data starts from 0 cycle time like training data

train_start_ds = df_train['ds'].iloc[0]
print(train_start_ds)

test_start_ds = df_test['ds'].iloc[0]
print(test_start_ds)

test_delta = test_start_ds - train_start_ds
print(test_delta)

# %%
df_test['ds'] = df_test['ds'] - test_delta

# %%
from datetime import datetime

# %%
df_train['ds'] = df_train['ds'].apply(lambda sec: datetime.fromtimestamp(sec))
df_train

# %%
df_test['ds'] = df_test['ds'].apply(lambda sec: datetime.fromtimestamp(sec))
df_test

# %%
# Information on the dataframe
df_train['y']=df_train['y'].astype(float)
df_train.info()

# %%
# Information on the dataframe
df_test['y']=df_test['y'].astype(float)
df_test.info()

# %% [markdown]
# Next, let's visualize the closing prices of the two tickers using `seaborn`, and add the legend to the plot using `matplotlib`. We can see that the price for Google increased a lot starting in late 2020, and almost doubled in late 2021.

# %%
# Visualize data using seaborn
sns.set(rc={'figure.figsize':(12,8)})
sns.lineplot(x=df_train['ds'], y=df_train['y'])
plt.legend(['Training metric'])

# %% [markdown]
# # Step 3: Build Time Series Model Using Prophet in Python

# %%
# Add seasonality
model = Prophet(interval_width=0.99, yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False, growth='flat')
model.add_seasonality(name='hourly', period=1/24, fourier_order=5)

# Fit the model on the training dataset
model.fit(df_train)

# %% [markdown]
# # Step 4: Make Predictions Using Prophet in Python

# %% [markdown]
# After building the model, in step 4, we use the model to make predictions on the dataset. The forecast plot shows that the predictions are in general aligned with the actual values.

# %%
# Make prediction
forecast = model.predict(df_test)

# Visualize the forecast
model.plot(forecast); # Add semi-colon to remove the duplicated chart

# %% [markdown]
# We can also check the components plot for the trend, weekly seasonality, and yearly seasonality.

# %%
# Visualize the forecast components
model.plot_components(forecast);

# %% [markdown]
# # Step 5: Check Time Series Model Performace

# %%
forecast

# %%
# Merge actual and predicted values
performance = pd.merge(df_test, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')

# %%
performance

# %%
# Check MAE value
performance_MAE = mean_absolute_error(performance['y'], performance['yhat'])
print(f'The MAE for the model is {performance_MAE}')

# Check MAPE value
performance_MAPE = mean_absolute_percentage_error(performance['y'], performance['yhat'])
print(f'The MAPE for the model is {performance_MAPE}')

# %% [markdown]
# # Step 6: Identify Anomalies

# %% [markdown]
# In step 6, we will identify the time series anomalies by checking if the actual value is outside of the uncertainty interval. If the actual value is smaller than the lower bound or larger than the upper bound of the uncertainty interval, the anomaly indicator is set to 1, otherwise, it's set to 0.
# 
# Using `value_counts()`, we can see that there are 6 outliers out of 505 data points.

# %%
# Create an anomaly indicator
performance['anomaly'] = performance.apply(lambda rows: 1 if ((float(rows.y)<rows.yhat_lower)|(float(rows.y)>rows.yhat_upper)) else 0, axis = 1)


# %%
performance.info()

# %%
# Check the number of anomalies
performance['anomaly'].value_counts()

# %% [markdown]
# After printing out the anomalies, we can see that all the outliers are lower than the lower bound of the uncertainty interval.

# %%
# Take a look at the anomalies
anomalies = performance[performance['anomaly']==1].sort_values(by='ds')
anomalies

# %% [markdown]
# In the visualization, all the dots are actual values and the black line represents the predicted values. The orange dots are the outliers.

# %%
# Visualize the anomalies
sns.scatterplot(x='ds', y='y', data=performance, hue='anomaly')
sns.lineplot(x='ds', y='yhat', data=performance, color='black')

# %%



