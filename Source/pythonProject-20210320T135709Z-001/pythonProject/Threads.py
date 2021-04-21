import main
import app
import asyncio

async def web_data():
    main.run()

async def dash_code():
    app.run()

async def main():
    await asyncio.gather(web_data(), dash_code())

asyncio.run(main())