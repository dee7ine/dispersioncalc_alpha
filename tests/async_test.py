import asyncio

async def main():
    print('1')
    await asyncio.sleep(1)
    print('2')

if __name__ == "__main__":
    asyncio.run(main())