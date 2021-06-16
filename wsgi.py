from app.fosmis import updateDB
import asyncio


async def main():
    while True:
        try:
            updateDB()
            await asyncio.sleep(60*2)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(main())

