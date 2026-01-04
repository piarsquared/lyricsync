import aiohttp

class LyricsService:
    BASE_URL = "https://lrclib.net/api/search"

    @staticmethod
    async def fetch_lyrics(song: str, artist: str):
        params = {'track_name': song, 'artist_name': artist}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(LyricsService.BASE_URL, params=params) as resp:
                if resp.status != 200:
                    return None
                
                data = await resp.json()
                return data[0] if data else None
