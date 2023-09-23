import yt_dlp as ydlp
import asyncio

def download_video(url, options=None):
    with ydlp.YoutubeDL(options) as ydl:
        ydl.download([url])

async def download_video_async(url, options=None):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, download_video, url, options)

async def main():
    # Set the options for yt-dlp. These are optional and can be customized.
    options = {
        # 'format': 'bestaudio/best',
        'outtmpl': f'%(title)s.%(ext)s',
        # Add other options as needed.
    }

    # List of URLs to download
    urls = [
        'https://www.youtube.com/watch?v=mGrJml5nq0o',
        # Add more URLs as needed.
    ]

    # Use asyncio to run the download tasks concurrently
    await asyncio.gather(*(download_video_async(url, options) for url in urls))

if __name__ == '__main__':
    asyncio.run(main())