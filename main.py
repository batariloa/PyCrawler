from gui import startGUI
import asyncio


async def main():

    await startGUI()


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
