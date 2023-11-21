#!/usr/bin/env python3
# countasync.py

import asyncio

class Task:

    """
    The Task Object.

    Attributes:
        priority:    The priority level assigned to the task.
        frequency:   Number of times the task must be executed in 1 second (Hz).
        name:        Name of the task object for future reference
        color:       Debug color for serial terminal
    """

    priority = 10
    frequency = 1
    name = 'temp'
    color = 'gray'

    def __init__(self, satellite, a):
        """
        Initialize the Task using the PyCubed cubesat object.
        
        :type satellite: Satellite
        :param satellite: The cubesat to be registered

        """
        self.a = a
        self.cubesat = satellite

    def debug(self,msg,level=1):
        """
        Print a debug message formatted with the task name and color

        :param msg: Debug message to print
        :param level: > 1 will print as a sub-level

        """
        if level==1:
            print(f'[{co(msg=self.name,color=self.color):>30}] {msg}')
        else:
            print(f'\t   └── {msg}')

    async def main_task(self, *args, **kwargs):
        print(self.a)

        """
        Contains the code for the user defined task. 

        :param `*args`: Variable number of arguments used for task execution.
        :param `**kwargs`: Variable number of keyword arguments used for task execution. 

        """
        pass

class Satellite:
    data = {}

# init the sat
satellite = Satellite()


possible_tasks = [Task(satellite, 1), Task(satellite, 2)]

async def start_task(task):
    print("b")
    while True:
        await task.main_task()
        await asyncio.sleep(1 / task.frequency);

async def main():
    await asyncio.gather(*[start_task(task) for task in possible_tasks])

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