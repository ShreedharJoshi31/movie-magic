from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json
import os
from groq import Groq

client = Groq(api_key="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")

async def stream_groq_response(prompt: str):
    # Stream response from Groq
    stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "you're a helpfull assistant"},
            {"role": "user", "content": prompt},
        ],
        model="llama3-8b-8192",
        stream=True,
    )

    # Stream each chunk of the response to the WebSocket
    for chunk in stream:
        delta_content = chunk.choices[0].delta.content
        # if delta_content:
            # await websocket.send_json({"response": delta_content})
        yield json.dumps({"data": delta_content}) + "\n\n"


router = APIRouter()

@router.get("/latency_20ms")
async def latency_20ms():
    await asyncio.sleep(0.02)  # Non-blocking sleep
    return {"message": "Response after 20ms"}

@router.get("/latency_200ms")
async def latency_200ms():
    await asyncio.sleep(0.2)  # Non-blocking sleep
    return {"message": "Response after 200ms"}

@router.get("/latency_2s")
async def latency_2s():
    await asyncio.sleep(2)  # Non-blocking sleep
    return {"message": "Response after 2 seconds"}

@router.get("/latency_20s")
async def latency_20s():
    await asyncio.sleep(20)  # Non-blocking sleep
    return {"message": "Response after 20 seconds"}

@router.get("/latency_60s")
async def latency_60s():
    await asyncio.sleep(60)  # Non-blocking sleep
    return {"message": "Response after 60 seconds"}

@router.get("/latency_180s")
async def latency_180s():
    await asyncio.sleep(180)  # Non-blocking sleep
    return {"message": "Response after 180 seconds"}

async def generate():
    for i in range(10):
        yield f"data: {i}\n\n"
        await asyncio.sleep(1)

@router.get("/stream")
async def stream():
    return StreamingResponse(stream_groq_response("hello, tell me about yourself, elaborate on how AI works."), media_type="application/json")
