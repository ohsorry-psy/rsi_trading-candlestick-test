import sys
import os
import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ==========================
# 설정 (Flask나 CLI에서 인자 받기)
# ==========================
symbol = sys.argv[1]
start_date = sys.argv[2]
end_date = sys.argv[3]

# ==========================
# 데이터 다운로드 및 지표 계산
# ==========================
data = yf.download(symbol, start=start_date, end=end_date)
close = data['Close'].squeeze()

# RSI 계산
data['RSI'] = ta.momentum.RSIIndicator(close=close, window=14).rsi().squeeze()

# 이동 평균선
data['SMA_5'] = close.rolling(window=5).mean()
data['SMA_20'] = close.rolling(window=20).mean()
data['SMA_60'] = close.rolling(window=60).mean()
data.dropna(inplace=True)

# ==========================
# RSI 다이버전스 포착
# ==========================
def find_bullish_divergence(df):
    divergences = []
    for i in range(30, len(df)):
        price_now = df['Close'].iloc[i].item()
        price_prev = df['Close'].iloc[i-5:i].min().item()
        rsi_now = df['RSI'].iloc[i].item()
        rsi_prev = df['RSI'].iloc[i-5:i].min().item()
        if price_now < price_prev and rsi_now > rsi_prev:
            divergences.append(i)
    return divergences

def find_bearish_divergence(df):
    divergences = []
    for i in range(30, len(df)):
        price_now = df['Close'].iloc[i].item()
        price_prev = df['Close'].iloc[i-5:i].max().item()
        rsi_now = df['RSI'].iloc[i].item()
        rsi_prev = df['RSI'].iloc[i-5:i].max().item()
        if price_now < price_prev and rsi_now > rsi_prev:
            divergences.append(i)
    return divergences

bullish_points = find_bullish_divergence(data)
bearish_points = find_bearish_divergence(data)

# ==========================
# 시각화
# ==========================
plt.figure(figsize=(14, 8))

# 가격 차트
plt.subplot(2, 1, 1)
plt.plot(data['Close'], label='Close Price', color='royalblue')
plt.plot(data['SMA_5'], label='SMA 5', linestyle='--')
plt.plot(data['SMA_20'], label='SMA 20', linestyle='--')
plt.plot(data['SMA_60'], label='SMA 60', linestyle='--')
plt.scatter(data.iloc[bullish_points].index, data['Close'].iloc[bullish_points], color='green', label='Bullish Divergence')
plt.scatter(data.iloc[bearish_points].index, data['Close'].iloc[bearish_points], color='red', label='Bearish Divergence')
plt.xticks(rotation=45)
plt.legend()
plt.title(f'{symbol} Price with RSI Divergence Signals')

# RSI 차트
plt.subplot(2, 1, 2)
plt.plot(data['RSI'], label='RSI', color='purple')
plt.axhline(30, color='gray', linestyle='--')
plt.axhline(70, color='gray', linestyle='--')
plt.legend()

plt.tight_layout()

# 저장 경로
os.makedirs("static/charts", exist_ok=True)
output_path = f"static/charts/{symbol}.png"
plt.savefig(output_path, dpi=300)
print(f" Chart saved to: {output_path}")
plt.close()

print(f"Absolute path: {os.path.abspath(output_path)}")
if os.path.exists(output_path):
    print("Image saved successfully:", output_path)
else:
    print("Image save failed. Please check the path.")
