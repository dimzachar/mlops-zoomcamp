#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('python -V')


# In[2]:


import pandas as pd


# In[3]:


import pickle


# In[4]:


import seaborn as sns
import matplotlib.pyplot as plt


print(sns.__version__)


# In[5]:


import os


# In[6]:


from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge

from sklearn.metrics import mean_squared_error


# In[7]:


df = pd.read_parquet('../data/green_tripdata_2021-01.parquet')
df


# In[8]:


df.dtypes


# In[9]:


# df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
# df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

# df = df[(df.duration >= 1) & (df.duration <= 60)]

# categorical = ['PULocationID', 'DOLocationID']
# numerical = ['trip_distance']

# df[categorical] = df[categorical].astype(str)
#replace with

df['duration'] = (df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']).dt.total_seconds() / 60
df = df[(df['duration'] >= 1) & (df['duration'] <= 60)].copy()

categorical = ['PULocationID', 'DOLocationID']
numerical = ['trip_distance']

df.loc[:, categorical] = df[categorical].astype(str)


# In[10]:


df


# In[11]:


train_dicts = df[categorical + numerical].to_dict(orient='records')

dv = DictVectorizer()
X_train = dv.fit_transform(train_dicts)

target = 'duration'
y_train = df[target].values

lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred = lr.predict(X_train)

mean_squared_error(y_train, y_pred, squared=False)


# In[12]:


sns.histplot(y_pred, label='prediction', kde=True,
    stat="density", kde_kws=dict(cut=0),
    alpha=.6, edgecolor=(1, 1, 1, .4),
)

sns.histplot(y_train, label='actual', kde=True,
    stat="density", kde_kws=dict(cut=0),
    alpha=.6, edgecolor=(1, 1, 1, .4),
)

plt.legend()


# # Main

# In[13]:


def read_dataframe(filename):
    if filename.endswith('.csv'):
        df = pd.read_csv(filename)

        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    elif filename.endswith('.parquet'):
        df = pd.read_parquet(filename)

#     df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
#     df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

#     df = df[(df.duration >= 1) & (df.duration <= 60)]

#     categorical = ['PULocationID', 'DOLocationID']
#     df[categorical] = df[categorical].astype(str)
    
    df['duration'] = (df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']).dt.total_seconds() / 60
    df = df[(df['duration'] >= 1) & (df['duration'] <= 60)].copy()

    categorical = ['PULocationID', 'DOLocationID']
#     numerical = ['trip_distance']

    df.loc[:, categorical] = df[categorical].astype(str)
    
    return df


# In[14]:


df_train = read_dataframe('../data/green_tripdata_2021-01.parquet')
df_val = read_dataframe('../data/green_tripdata_2021-02.parquet')


# In[15]:


len(df_train), len(df_val)


# In[16]:


df_train['PU_DO'] = df_train['PULocationID'] + '_' + df_train['DOLocationID']
df_val['PU_DO'] = df_val['PULocationID'] + '_' + df_val['DOLocationID']


# In[17]:


df_train


# In[18]:


categorical = ['PU_DO'] #'PULocationID', 'DOLocationID']
numerical = ['trip_distance']

dv = DictVectorizer()

train_dicts = df_train[categorical + numerical].to_dict(orient='records')
X_train = dv.fit_transform(train_dicts)

val_dicts = df_val[categorical + numerical].to_dict(orient='records')
X_val = dv.transform(val_dicts)


# In[19]:


target = 'duration'
y_train = df_train[target].values
y_val = df_val[target].values


# In[20]:


lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred = lr.predict(X_val)

mean_squared_error(y_val, y_pred, squared=False)


# In[21]:


# Create directory if it doesn't exist
if not os.path.exists('models'):
    os.makedirs('models')

with open('models/lin_reg.bin', 'wb') as f_out:
    pickle.dump((dv, lr), f_out)


# In[22]:


lr = Lasso(0.01)
lr.fit(X_train, y_train)

y_pred = lr.predict(X_val)

mean_squared_error(y_val, y_pred, squared=False)


# In[ ]:




