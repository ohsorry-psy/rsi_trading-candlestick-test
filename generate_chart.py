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
# 시각화: 가격 + 거래량 + RSI
# ==========================
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), sharex=True,
                                   gridspec_kw={'height_ratios': [3, 1, 1]})

# 가격 차트
ax1.plot(data.index, data['Close'], label='Close Price', color='royalblue')
ax1.plot(data.index, data['SMA_5'], label='SMA 5', linestyle='--')
ax1.plot(data.index, data['SMA_20'], label='SMA 20', linestyle='--')
ax1.plot(data.index, data['SMA_60'], label='SMA 60', linestyle='--')
ax1.scatter(data.iloc[bullish_points].index, data['Close'].iloc[bullish_points], color='green', label='Bullish Divergence')
ax1.scatter(data.iloc[bearish_points].index, data['Close'].iloc[bearish_points], color='red', label='Bearish Divergence')
ax1.legend()
ax1.set_ylabel('Price')
ax1.set_title(f"{symbol} Price, RSI Divergence, Volume")

# 거래량 차트
ax2.bar(data.index, data['Volume'], color='gray')
ax2.set_ylabel('Volume')

# RSI 차트
ax3.plot(data.index, data['RSI'], label='RSI', color='purple')
ax3.axhline(30, color='gray', linestyle='--')
ax3.axhline(70, color='gray', linestyle='--')
ax3.legend()
ax3.set_ylabel('RSI')

# 날짜 포맷
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.tight_layout()

# 저장 경로
os.makedirs("static/charts", exist_ok=True)
output_path = f"static/charts/{symbol}.png"
plt.savefig(output_path, dpi=300)
print(f"Chart saved to: {output_path}")
plt.close()

print(f"Absolute path: {os.path.abspath(output_path)}")
if os.path.exists(output_path):
    print("Image saved successfully:", output_path)
else:
    print("Image save failed. Please check the path.")

