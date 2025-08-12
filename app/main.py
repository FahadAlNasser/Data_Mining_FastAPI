import asyncio
from typing import List
from fastapi import FastAPI, HTTPException, Query
import httpx
import feedparser
from pydantic import BaseModel

app = FastAPI(title="This is data mining practice")

hackernews = "https://hacker-news.firebaseio.com/v0"
xml = "http://thehackernews.com/feeds/posts/default"
STEAM_game_appdetails = "https://store.steampowered.com/api/appdetails"

class HackerNewsItem(BaseModel):
    id: int
    title: str | None = None
    link: str | None = None
    by: str | None = None
    score: int | None = None

async def fetching_json(client: httpx.AsyncClient, link: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        resp = await client.get(link, timeout=10.0)
        resp.raise_for_status()
        return resp.json()
    
@app.get("/hackernews/top", response_model=List[HackerNewsItem])
async def hackernews_top(n: int = Query(10, ge=1, le=50)):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{hackernews}/topstories.json")
        resp.raise_for_status()
        ids = resp.json()[:n]
        sem = asyncio.Semaphore(5)
        tasks = [
            asyncio.create_task(fetching_json(client, f"{hackernews}/item/{i}.json", sem))
            for i in ids
        ]
        things = await asyncio.gather(*tasks, return_exceptions=True)
        results = []
        for thing in things:
            if isinstance(thing, Exception) or thing is None:
                continue
            results.append(HackerNewsItem(
                id=thing.get("id"),
                title=thing.get("title"),
                link=thing.get("url"),
                by=thing.get("by"),
                score=thing.get("score"),
            ))
        return results
    
@app.get("/thehackernews/latest")
async def thehackernews_latest(n: int = Query(5, ge=1, le=20)):
    feed = await asyncio.to_thread(feedparser.parse, xml)
    entries = feed.entries[:n]
    return [{"title": e.get("title"), "link": e.get("link"), "published": e.get("published")} for e in entries]

@app.get("/steam/{appid}")
async def steam(appid: int):
    params = {"appids": appid, "l": "en", "cc": "us"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(STEAM_game_appdetails, params=params, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
    app_key = str(appid)
    if app_key not in data or not data[app_key].get("success"):
        raise HTTPException(status_code=404, detail="There is no data to represent")
    info = data[app_key]["data"]
    return {"name": info.get("name"), "short_description": info.get("short_description"), "type": info.get("type")}