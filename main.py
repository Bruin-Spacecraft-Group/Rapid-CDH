#!/usr/bin/env python3
# countasync.py
# inspired by Pycubed's task system
# also see https://github.com/SmallSatGasTeam/CubeWorks/blob/master/flightLogic/mainFlightLogic.py#L12

# ========== code style guide: =============
# try to follow PEP8: https://peps.python.org/pep-0008/
#
# classes, enums are PascalCase
# vars., funcs., dicts., etc. are snake_case
# constants and enum values are in UPPER_SNAKE_CASE
# bools and funcs. which return bools are prefixed with 'is_', for example: is_receiving_beacon()

import asyncio

from task import Task
from tasks.comms import *

class Satellite:
    data = {}

    def get_data(self, key):
        if key in self.data:
            return data.key
        else:
            return False

    async def start_task(self, task):
        while True:
            await task.main_task()
            await asyncio.sleep(1 / task.frequency);

# init the sat
satellite = Satellite()

possible_tasks = [Task(satellite, 1), CommsMainTask(satellite, 2)]

async def main():
    await asyncio.gather(*[satellite.start_task(task) for task in possible_tasks])

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")





"""

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    """