from app.fosmis import updateDB
import asyncio


async def main():
    while True:
        try:
            await asyncio.sleep(60*10)
            updateDB()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(main())

