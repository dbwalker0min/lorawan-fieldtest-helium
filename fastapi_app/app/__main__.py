import sys
import asyncio

from pathlib import Path
import os

print("Current working directory:", os.getcwd())
print("Path of __main__.py:", __file__)
print("sys.path:")
for p in sys.path:
    print(" ", p)

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=17560)
