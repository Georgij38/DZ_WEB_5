import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys


async def fetch_currency_rate(session, currency, date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
    async with session.get(url) as response:
        data = await response.json()
        currency_info = next((item for item in data['exchangeRate'] if item['currency'] == currency), None)
        return currency_info


async def get_currency_rates(currencies, days=10):
    async with aiohttp.ClientSession() as session:
        rates = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y")
            currency_info = {}
            for currency in currencies:
                info = await fetch_currency_rate(session, currency.upper(), date)
                if info:
                    currency_info[currency] = {
                        'sale': info['saleRate'],
                        'purchase': info['purchaseRate']
                    }
            if currency_info:
                rates.append({date: currency_info})
        return rates


async def main():
    currencies = sys.argv[1:]  # Отримання валютних кодів з аргументів командного рядка
    days = 2
    if not currencies:
        currencies = ['USD', 'EUR']

    currency_rates = await get_currency_rates(currencies, days)

    for x in currency_rates:
        print(x)

if __name__ == "__main__":
    asyncio.run(main())
