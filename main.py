import asyncio
from ble.field import field_data_retrieval
from graph import graph
import globals

async def main():
    globals.init()
    task1 = asyncio.create_task(field_data_retrieval())
    task2 = asyncio.create_task(graph())
    tasks = [task1, task2]

    try:    
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("\nProgram interrupted by user.")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
