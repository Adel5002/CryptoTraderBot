from pybit.unified_trading import WebSocket, HTTP
from time import sleep

from API_KEYS.api_keys import api_key, secret_key


class Main:

    def __init__(self):
        self.session = HTTP(
            testnet=True,
            api_key=api_key,
            api_secret=secret_key,
            max_retries=10,
            retry_delay=15,
        )
        self.fix_lastPrice = float(
            ''.join(
                [i['lastPrice'] for i in self.session.get_tickers(
                    category="spot",
                    symbol="BTCUSDT",
                )['result']['list']
                 ])
        )

    def get_curr_rate(self, message):
        current_price = round(float(message["data"]["lastPrice"]), 2)
        plus_three_percent = round(self.fix_lastPrice / 100 * 3, 2)
        if current_price >= self.fix_lastPrice + plus_three_percent:
            self.sell_coin()
            print(f'Текущая цена {current_price}')
            self.fix_lastPrice = current_price
            print()
            print('-----')
            print(f'Начальная цена {self.fix_lastPrice}')
        elif current_price <= self.fix_lastPrice - plus_three_percent:
            self.buy_coin()
            print(f'Текущая цена {current_price}')
            self.fix_lastPrice = current_price
            print()
            print('-----')
            print(f'Начальная цена {self.fix_lastPrice}')


    def buy_coin(self):
        print('Покупаем!')

    def sell_coin(self):
        print('Продаем!')

    def exchange_coin(self):
        pass


if __name__ == '__main__':
    main = Main()

    # WebSockets

    ws_spot = WebSocket(
        testnet=True,
        channel_type='spot'
    )

    wss = ws_spot.ticker_stream(
        symbol="BTCUSDT",
        callback=main.get_curr_rate
    )
    print(f'Начальная цена {main.fix_lastPrice}')

    while True:
        sleep(1)
