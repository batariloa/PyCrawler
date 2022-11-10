from gui.gui import startGUI
import asyncio
from concurrent.futures import ProcessPoolExecutor
from hanging_threads import start_monitoring


def main():

    startGUI()


main()
