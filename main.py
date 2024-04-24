from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/stream")
async def stream():
    # Response headers
    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }
    # Log info
    print("Client connected")
    # A simple method generating date every second
    async def generate():
        i = 0
        while True:
            i += 1
            data = f"Hello, world! {i}"
            try:
                print("Sending:", data)
                # Note: yield is used to return data from the function
                # and the new line character is used to separate the messages
                yield f"data: {data}\n\n"
                # Wait for 1 second before sending the next message
                await asyncio.sleep(1)
            except Exception as e:
                print("Client connection closed:", e)
                break
    # Important: StreamingResponse should be used to ensure
    # that the connection is kept alive and the data is streamed
    return StreamingResponse(generate(), headers=headers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3005)