from app.fosmis import updateDB
import logging
import asyncio


async def main():
    count = 0
    logging.info("Initial Run Stated!!!")
    while True:
        logging.info(f"round {count} initialized!!!")
        try:
            await asyncio.sleep(60 * 10)
            updateDB()
        except Exception as e:
            logging.info(f"Error Occured - {e}")
        count += 1
    #updateDB()

if __name__ == "__main__":
    asyncio.run(main())
