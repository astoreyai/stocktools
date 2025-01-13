import os
import pandas as pd
import numpy as np
import talib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
import matplotlib.pyplot as plt

# Load and Prepare Data
folder_path = r'C:\Users\aaron\OneDrive\Desktop\stocktools_main\data\stock_data\\15min_data'  # Change this to your folder path
file_list = [f for f in os.listdir(folder_path) if f.endswith('.csv')]  # Automatically find all CSV files
dfs = []


for file in file_list:
    df = pd.read_csv(os.path.join(folder_path, file))
    df['Symbol'] = file.split('_')[0]  # Add a column for the stock symbol
    df['Datetime'] = pd.to_datetime(df['Datetime'])  # Convert datetime column to datetime type
    dfs.append(df)

data = pd.concat(dfs, ignore_index=True)

# Feature Engineering
def add_features(data):
    data['SMA_20'] = data.groupby('Symbol')['Close'].transform(lambda x: x.rolling(window=20).mean())
    data['SMA_50'] = data.groupby('Symbol')['Close'].transform(lambda x: x.rolling(window=50).mean())
    data['SMA_200'] = data.groupby('Symbol')['Close'].transform(lambda x: x.rolling(window=200).mean())
    data['EMA_20'] = data.groupby('Symbol')['Close'].transform(lambda x: talib.EMA(x, timeperiod=20))
    data['EMA_50'] = data.groupby('Symbol')['Close'].transform(lambda x: talib.EMA(x, timeperiod=50))
    data['EMA_200'] = data.groupby('Symbol')['Close'].transform(lambda x: talib.EMA(x, timeperiod=200))
    data['RSI'] = data.groupby('Symbol')['Close'].transform(lambda x: talib.RSI(x, timeperiod=14))
    macd, macd_signal, _ = zip(*data.groupby('Symbol')['Close'].apply(lambda x: talib.MACD(x)))
    data['MACD'] = np.concatenate(macd)
    data['MACD_signal'] = np.concatenate(macd_signal)
    upper_band, _, lower_band = zip(*data.groupby('Symbol')['Close'].apply(lambda x: talib.BBANDS(x, timeperiod=20, nbdevup=2, nbdevdn=2)))
    data['BB_upper'] = np.concatenate(upper_band)
    data['BB_lower'] = np.concatenate(lower_band)
    data['ATR'] = data.groupby('Symbol').apply(lambda x: talib.ATR(x['High'], x['Low'], x['Close'], timeperiod=14)).reset_index(level=0, drop=True)
    slowk, slowd = zip(*data.groupby('Symbol').apply(lambda x: talib.STOCH(x['High'], x['Low'], x['Close'])))
    data['Stochastic_slowk'] = np.concatenate(slowk)
    data['Stochastic_slowd'] = np.concatenate(slowd)
    aroon_up, aroon_down = zip(*data.groupby('Symbol').apply(lambda x: talib.AROON(x['High'], x['Low'], timeperiod=14)))
    data['Aroon_up'] = np.concatenate(aroon_up)
    data['Aroon_down'] = np.concatenate(aroon_down)
    data['Price_ROC'] = data.groupby('Symbol')['Close'].transform(lambda x: talib.ROC(x, timeperiod=10))
    data['OBV'] = data.groupby('Symbol').apply(lambda x: talib.OBV(x['Close'], x['Volume'])).reset_index(level=0, drop=True)
    data['CMF'] = data.groupby('Symbol').apply(lambda x: talib.ADOSC(x['High'], x['Low'], x['Close'], x['Volume'])).reset_index(level=0, drop=True)
    data['Accumulation_Distribution'] = data.groupby('Symbol').apply(lambda x: talib.AD(x['High'], x['Low'], x['Close'], x['Volume'])).reset_index(level=0, drop=True)
    data['Williams_%R'] = data.groupby('Symbol').apply(lambda x: talib.WILLR(x['High'], x['Low'], x['Close'], timeperiod=14)).reset_index(level=0, drop=True)
    data['ADX'] = data.groupby('Symbol').apply(lambda x: talib.ADX(x['High'], x['Low'], x['Close'], timeperiod=14)).reset_index(level=0, drop=True)
    data['MFI'] = data.groupby('Symbol').apply(lambda x: talib.MFI(x['High'], x['Low'], x['Close'], x['Volume'], timeperiod=14)).reset_index(level=0, drop=True)
    data['CCI'] = data.groupby('Symbol').apply(lambda x: talib.CCI(x['High'], x['Low'], x['Close'], timeperiod=14)).reset_index(level=0, drop=True)
    data['DPO'] = data.groupby('Symbol')['Close'].transform(lambda x: talib.DEMA(x, timeperiod=20) - x)
    data['TRIMA'] = data.groupby('Symbol')['Close'].transform(lambda x: talib.TRIMA(x, timeperiod=14))
    return data

data = add_features(data)

# Data Cleaning
data.dropna(inplace=True)

# Normalization/Standardization
scaler = StandardScaler()
data_scaled = data.copy()
numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns

# Exclude non-numeric columns from scaling
exclude_cols = ['Symbol', 'Datetime']
numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
data_scaled[numeric_cols] = scaler.fit_transform(data[numeric_cols])

# Splitting Data
X = data_scaled.drop(['Close'], axis=1)
X = X.drop(exclude_cols, axis=1)  # Ensure non-numeric columns are dropped
y = data_scaled['Close']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Selection
selector = SelectKBest(score_func=f_regression, k=10)
X_train_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)

# Further Preprocessing
# Apply any additional preprocessing steps if needed

# Model Training and Evaluation
model = RandomForestRegressor()
model.fit(X_train_selected, y_train)
score = model.score(X_test_selected, y_test)

print("Model Score:", score)

# Interdependence Visualization
# Visualize feature interdependence using correlation matrix
correlation_matrix = data[numeric_cols].corr()

# Filter correlation matrix to only show correlations between 0.5 and 0.99
filtered_corr = correlation_matrix[(correlation_matrix > 0.5) & (correlation_matrix < 0.99)].dropna(how='all').dropna(axis=1, how='all')

plt.figure(figsize=(14, 12))
sns.heatmap(filtered_corr, annot=True, cmap='coolwarm', center=0)
plt.title('Feature Interdependence - Correlation Matrix (0.5 < |corr| < 0.99)')
plt.show()

