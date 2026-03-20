import asyncio
import random
from playwright.async_api import async_playwright


async def parse_google_search(query):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,  # Установите в False для отладки
            # Можно добавить аргументы для скрытия признаков headless
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',  # Помогает скрыть Playwright
                '--disable-dev-shm-usage',  # Часто полезно в контейнерах
                '--disable-gpu'  # Отключает использование GPU
            ]
        )

        # 2. Создание нового контекста с настройками
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
        ]

        # 3. Использование прокси (если доступно)
        # proxy_config = {"server": "http://user:password@proxy.example.com:8080"}
        # context = await browser.new_context(
        #     user_agent=random.choice(user_agents),
        #     viewport={"width": random.randint(1280, 1920), "height": random.randint(800, 1080)},
        #     proxy=proxy_config # раскомментируйте, если используете прокси
        # )

        context = await browser.new_context(
            user_agent=random.choice(user_agents),
            viewport={"width": random.randint(1280, 1920), "height": random.randint(800, 1080)},
        )

        # Отключение признаков автоматизации (иногда бывает полезно, но Playwright уже это делает по умолчанию)
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        page = await context.new_page()

        try:
            search_url = f"https://www.google.com/search?q={query}"
            await page.goto(search_url, wait_until="domcontentloaded")
            await asyncio.sleep(random.uniform(2, 5))  # Случайная задержка после загрузки

            # 4. Имитация прокрутки (опционально)
            await page.mouse.wheel(0, random.randint(500, 1500))
            await asyncio.sleep(random.uniform(1, 3))

            # Здесь будет ваш код для парсинга результатов
            # Используйте надежные селекторы, например, по классам или data-атрибутам
            # Примечание: Google часто меняет классы, поэтому этот код может устареть.
            results = await page.locator("div.g").all()  # Пример селектора для блоков результатов

            parsed_data = []
            for result_elem in results:
                try:
                    title = await result_elem.locator("h3").text_content()
                    link = await result_elem.locator("a").first.get_attribute("href")
                    snippet = await result_elem.locator("div.VwiC3b").text_content()  # Пример для описания
                    parsed_data.append({"title": title, "link": link, "snippet": snippet})
                except Exception as e:
                    print(f"Error parsing result element: {e}")
                    continue

            # 5. Сохранение состояния (cookies и local storage) для следующего запроса (опционально)
            await context.storage_state(path="playwright_state.json")

            return parsed_data

        except Exception as e:
            print(f"An error occurred: {e}")
            # Здесь можно добавить логику для обработки CAPTCHA или повторных попыток
            return None
        finally:
            await browser.close()


if __name__ == "__main__":
    search_term = "python playwright"
    results = asyncio.run(parse_google_search(search_term))
    if results:
        for i, item in enumerate(results):
            print(f"Result {i + 1}:")
            print(f"  Title: {item.get('title')}")
            print(f"  Link: {item.get('link')}")
            print(f"  Snippet: {item.get('snippet')}")
            print("-" * 20)
    else:
        print("Failed to get search results.")