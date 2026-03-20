import asyncio
from uuid import UUID
from app.core.celery_app import celery_app
from app.infrastructure.db.session import async_session_factory
from app.repository.tasks import TaskRepository  # Нам нужен метод update
from app.repository.leads import LeadRepository

import asyncio
import random
from playwright.async_api import async_playwright


# Обертка для запуска асинхронных функций в Celery
def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


@celery_app.task(name="process_parsing")
def process_parsing(task_id: UUID, search_queries: dict):
    return run_async(execute_workflow(task_id=task_id, search_queries=search_queries))


async def execute_workflow(task_id: UUID, search_queries: dict):
    async with async_session_factory() as session:
        task_repo = TaskRepository(session)
        lead_repo = LeadRepository(session)

        # 1. Ставим статус RUNNING
        await task_repo.update_task_status(task_id, "RUNNING")

        try:
            # 2. Здесь будет вызов твоего будущего парсера (OLX, LinkedIn и т.д.)
            # Пока имитируем задержку и результат
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
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
                ]
                context = await browser.new_context(
                    user_agent=random.choice(user_agents),
                    viewport={"width": random.randint(1280, 1920), "height": random.randint(800, 1080)},
                )
                await context.add_init_script("""
                            Object.defineProperty(navigator, 'webdriver', {
                                get: () => undefined
                            });
                        """)
                page = await context.new_page()
                search_url = "https://bot.sannysoft.com/"
                await page.goto(search_url, wait_until="domcontentloaded")
                await page.screenshot(path=f"app/img/screenshot_{task_id}.png")

            #await asyncio.sleep(10)

            # 3. Сохраняем лидов
            # ... код сохранения ...

            # 4. Завершаем
            await task_repo.update_task_status(task_id, "COMPLETED")

        except Exception as e:
            await task_repo.update_task_status(task_id, "FAILED")
            raise e