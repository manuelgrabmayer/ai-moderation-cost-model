import asyncio
import random  # For testing


class Job:
    def __init__(self, id, desc, func):
        self.func = func
        self.id = id
        self.desc = desc
        self.failed = False
        self.response = None
        self.error = None

    async def execute(self):
        print(f"Executing job: {self.id} {self.desc}")

        try:
            if asyncio.iscoroutinefunction(self.func):
                self.response = await self.func()
            else:
                self.response = self.func()
        except Exception as e:
            self.failed = True
            self.error = str(e)

        print(f"Job: {self.id} {self.desc} completed. Success: {not self.failed}")


async def test():
    print("--- Starting Job System Tests ---")

    async def mockCall():
        await asyncio.sleep(random.uniform(0.1, 3.0))
        return "Gemini response received"

    testJobs = [
        Job(1, "Sync Lambda Test", lambda: 2 + 2),
        Job(2, "Async Function Test", mockCall),
        Job(3, "Failure Test", lambda: 1 / 0),
    ]

    await asyncio.gather(*(job.execute() for job in testJobs))

    print("--- Job system test finished ---")
