from gui import startGUI
import asyncio
from concurrent.futures import ProcessPoolExecutor


def main(loop):
    executor = ProcessPoolExecutor(5)

    loop.run_in_executor(executor,  startGUI(executor))


loop = asyncio.new_event_loop()
loop.run_until_complete(main(loop))
