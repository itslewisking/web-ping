import asyncio
import aiohttp
import aiofiles
import time
import calculatorTools
import sys
import requests

# learning notes
# async just means it's able to be 'paused' -- with session means it awaits the response
# awaiting from main will pause the coroutine (blocking) until it completes
# if something pauses it means the event loop can do something else
# await gather means whilst the fetches are running, other coroutine can run


async def pulse():
    while True:
        for phase in [".    ", "..   ", "...  ", ".... ", "....."]:
            print(f"\r{phase}", end="")
            await asyncio.sleep(0.5)


async def fetch(url: str, session: aiohttp.ClientSession) -> int:
    start = time.monotonic()
    async with session.get(url) as response:
        assert response.status == 200
        end = f"{round(time.monotonic() - start, 4):.3f}"
        return end


async def log_to_file(line: str) -> None:
    try:
        async with aiofiles.open("last_run.txt", mode="a") as f:
            await f.write(f"{line},\n")
    except PermissionError:
        print("not logging")


async def call_loop(
    results: list[list[int]],
    workers: int,
    runs: int,
    interval_in_seconds: int,
    url: str,
    logging: int,
) -> None:
    async with aiohttp.ClientSession() as client:
        for i in range(runs):
            try:
                print("\r     ", end="")
                print(f"\rlap {i+1}: {((i+1)/runs)*100:.2f}%")
                start_time = time.monotonic()

                jobs = [fetch(url, client) for _ in range(workers)]

                responses = await asyncio.gather(*jobs)
                end_time = time.monotonic() - start_time
                results.append(responses)
                print("calls complete, sleeping")
                if i + 1 == runs:
                    return

                if logging:
                    asyncio.create_task(log_to_file(str(responses)))

                pulsing_task = asyncio.create_task(pulse())
                await asyncio.sleep(max(0, interval_in_seconds - end_time))
                pulsing_task.cancel()

                try:
                    await pulsing_task  # await tells it to wait until it's done, we cancelled it so immediately finishes
                except asyncio.CancelledError:
                    pass
            except:
                pass
    return


def main(
    runs: int, workers: int, interval_in_seconds: int, url: str, logging: int
) -> None:
    results = []

    asyncio.run(call_loop(results, workers, runs, interval_in_seconds, url, logging))
    calculated_results = calculatorTools.build_results(results)
    print("\r\n")
    for row in results:
        print(row)
    print("\n")

    for fact in calculated_results.items():
        print(f"{fact[0]}: {fact[1]}")


if __name__ == "__main__":
    arguments = sys.argv
    if (
        len(arguments) == 6
        and arguments[1].isnumeric()
        and arguments[2].isnumeric()
        and arguments[3].isnumeric()
        and arguments[5].isnumeric()
    ):
        print("trying url")
        ping = requests.get(arguments[4])
        if ping.status_code == 200:
            print("initial ping successful, starting workers")
            if int(arguments[5]):
                try:
                    with open("last_run.txt", "w"):
                        pass
                    print("logging file created")
                except PermissionError:
                    print("unable to create logging file, logging will not happen")
            main(
                int(arguments[1]),
                int(arguments[2]),
                int(arguments[3]),
                arguments[4],
                int(arguments[5]),
            )
        else:
            print(f"initial ping returnd {ping.status_code}")
    else:
        print("usage: ./letsplay.py  runs  workers  interval(s)  url  logging(0/1)")
