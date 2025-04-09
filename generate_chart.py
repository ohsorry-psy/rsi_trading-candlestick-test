import os
import yfinance as yf
import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def find_bullish_divergence(df):
    divergences = []
    for i in range(30, len(df)):
        price_now = df['Close'].iloc[i].item()
        price_prev = df['Close'].iloc[i - 5:i].min().item()
        rsi_now = df['RSI'].iloc[i].item()
        rsi_prev = df['RSI'].iloc[i - 5:i].min().item()
        if price_now < price_prev and rsi_now > rsi_prev:
            divergences.append(i)
    return divergences


def find_bearish_divergence(df):
    divergences = []
    for i in range(30, len(df)):
        price_now = df['Close'].iloc[i].item()
        price_prev = df['Close'].iloc[i - 5:i].max().item()
        rsi_now = df['RSI'].iloc[i].item()
        rsi_prev = df['RSI'].iloc[i - 5:i].max().item()
        if price_now > price_prev and rsi_now < rsi_prev:
            divergences.append(i)
    return divergences


def generate_chart(symbol: str, start_date: str, end_date: str) -> str:
    try:
        print(f"[generate_chart] 시작: {symbol}, {start_date} ~ {end_date}")

        data = yf.download(symbol, start=start_date, end=end_date)
        if data.empty:
            raise ValueError("No data downloaded. Check the symbol or date range.")

        close = data['Close'].squeeze()
        data['RSI'] = ta.momentum.RSIIndicator(close=close, window=14).rsi().squeeze()
        data['SMA_5'] = close.rolling(window=5).mean()
        data['SMA_20'] = close.rolling(window=20).mean()
        data['SMA_60'] = close.rolling(window=60).mean()
        data.dropna(inplace=True)

        bullish_points = find_bullish_divergence(data)
        bearish_points = find_bearish_divergence(data)

        # 🔧 리스트 변환: np.array + flatten
        bullish_x = data.index[bullish_points].to_list()
        bullish_y = np.array(data['Close'].iloc[bullish_points]).flatten().tolist()
        bearish_x = data.index[bearish_points].to_list()
        bearish_y = np.array(data['Close'].iloc[bearish_points]).flatten().tolist()

        # 디버깅 로그 (선택)
        print("🐍 bullish_x:", bullish_x[:3])
        print("🐍 bullish_y:", bullish_y[:3])
        print("🐍 bearish_x:", bearish_x[:3])
        print("🐍 bearish_y:", bearish_y[:3])

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), sharex=True,
                                            gridspec_kw={'height_ratios': [3, 1, 1]})

        ax1.plot(data.index, data['Close'], label='Close Price', color='royalblue')
        ax1.plot(data.index, data['SMA_5'], label='SMA 5', linestyle='--')
        ax1.plot(data.index, data['SMA_20'], label='SMA 20', linestyle='--')
        ax1.plot(data.index, data['SMA_60'], label='SMA 60', linestyle='--')
        ax1.scatter(bullish_x, bullish_y, color='green', label='Bullish Divergence')
        ax1.scatter(bearish_x, bearish_y, color='red', label='Bearish Divergence')
        ax1.legend()
        ax1.set_ylabel('Price')
        ax1.set_title(f"{symbol} Price, RSI Divergence, Volume")

        ax2.bar(data.index, data['Volume'].astype(float).fillna(0), color='gray')
        ax2.set_ylabel('Volume')

        ax3.plot(data.index, data['RSI'], label='RSI', color='purple')
        ax3.axhline(30, color='gray', linestyle='--')
        ax3.axhline(70, color='gray', linestyle='--')
        ax3.legend()
        ax3.set_ylabel('RSI')

        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        plt.tight_layout()

        os.makedirs("static/charts", exist_ok=True)
        output_path = f"static/charts/{symbol}.png"
        plt.savefig(output_path, dpi=300)
        plt.close()

        if os.path.exists(output_path):
            print(f"[성공] 차트 저장 완료: {output_path}")
            return output_path
        else:
            raise FileNotFoundError("Image save failed.")

    except Exception as e:
        import traceback
        print("[Error in generate_chart]:", e)
        traceback.print_exc()
        raise


if __name__ == "__main__":
    try:
        path = generate_chart("AAPL", "2024-04-01", "2025-04-07")
        print("저장된 경로:", path)
    except Exception as e:
        print("실행 오류:", e)
