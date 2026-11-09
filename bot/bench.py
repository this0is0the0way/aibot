import asyncio
import time

from statistics import mean

from bot.search_service.general_search import general_search

from bot.providers.wikipedia import search_wiki
from bot.providers.github import search_github
from bot.providers.stack_over_flow import search_stack_ov_fl


QUERY = "python asyncio"
ATTEMPTS = 3
TIMEOUT = 5

PROVIDERS = {
    "Wikipedia": search_wiki,
    "GitHub": search_github,
    "StackOverFlow": search_stack_ov_fl,
}


async def benchmark_sequential(query: str) -> float | None:
    start = time.perf_counter()

    for name, provider in PROVIDERS.items():
        try:
            await asyncio.wait_for(provider(query), timeout=TIMEOUT)
        except Exception as error:
            print(f"Последовательный поиск: {name} — {error}")
            return None

    return time.perf_counter() - start


async def benchmark_concurrent(query: str) -> float | None:
    semaphore = asyncio.Semaphore(6)
    start = time.perf_counter()

    try:
        _, broken_providers = await general_search(query, semaphore)
    except Exception as error:
        print(f"Конкурентный поиск: {error}")
        return None

    elapsed = time.perf_counter() - start

    if broken_providers:
        print(
            "Конкурентный поиск: ошибка источников — "
            + ", ".join(broken_providers)
        )
        return None

    return elapsed


async def main():
    measurements = []

    for attempt in range(1, ATTEMPTS + 1):
        print(f"\nЗамер {attempt}/{ATTEMPTS}")

        sequential = await benchmark_sequential(QUERY)

        if sequential is None:
            print("Замер исключён: ошибка последовательного поиска.")
            continue

        concurrent = await benchmark_concurrent(QUERY)

        if concurrent is None:
            print("Замер исключён: ошибка конкурентного поиска.")
            continue

        measurements.append((sequential, concurrent))

        print(f"Последовательно: {sequential:.3f} с")
        print(f"Конкурентно:     {concurrent:.3f} с")

    if not measurements:
        print("\nНет успешных пар замеров.")
        return

    sequential_avg = mean(pair[0] for pair in measurements)
    concurrent_avg = mean(pair[1] for pair in measurements)
    speedup = sequential_avg / concurrent_avg

    print("\nИТОГИ")
    print(f"Успешных пар: {len(measurements)}/{ATTEMPTS}")
    print(f"Последовательно: {sequential_avg:.3f} с")
    print(f"Конкурентно:     {concurrent_avg:.3f} с")
    print(f"Ускорение:       {speedup:.2f} раза")


if __name__ == "__main__":
    asyncio.run(main())
