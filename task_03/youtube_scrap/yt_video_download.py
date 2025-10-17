# from googleapiclient.discovery import build
# import pandas as pd
# import yt_dlp
# import os

# # --- API Setup ---
# API_KEY = "AIzaSyDFgvmW1Opy4LVccsCTtsN7-bLoN3RBL5A"
# youtube = build('youtube', 'v3', developerKey=API_KEY)

# # --- Parameters ---
# queries = ["Power BI", "Machine Learning", "Deep Learning"]
# max_results = 5
# download_limit = 1   # number of videos to download per topic
# download_path = "downloads"

# # --- Create download folder ---
# os.makedirs(download_path, exist_ok=True)

# all_data = []

# # --- YouTube Search + Download ---
# for query in queries:
#     print(f"\n🔍 Searching for: {query}")
#     request = youtube.search().list(
#         q=query,
#         part="snippet",
#         type="video",
#         maxResults=max_results
#     )
#     response = request.execute()

#     query_downloaded = 0

#     for item in response.get("items", []):
#         if query_downloaded >= download_limit:
#             break

#         video_id = item["id"].get("videoId")
#         if not video_id:
#             continue

#         title = item["snippet"]["title"]
#         channel = item["snippet"]["channelTitle"]
#         publish_date = item["snippet"]["publishedAt"]
#         url = f"https://www.youtube.com/watch?v={video_id}"

#         all_data.append({
#             "query": query,
#             "title": title,
#             "channel": channel,
#             "publish_date": publish_date,
#             "url": url
#         })

#         try:
#             # --- Download video ---
#             ydl_opts = {
#                 'outtmpl': f'{download_path}/%(title).50s.%(ext)s',
#                 'format': 'best[ext=mp4]',
#                 'quiet': True,
#             }
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([url])

#             print(f"✅ Downloaded: {title[:60]}")
#             query_downloaded += 1

#         except Exception as e:
#             print(f"❌ Skipped {url} → {e}")

# # --- Save results to CSV ---
# df = pd.DataFrame(all_data)
# df.to_csv("youtube_search_results.csv", index=False)
# print("\n✅ Data saved to youtube_search_results.csv")




from googleapiclient.discovery import build
import pandas as pd
import yt_dlp
import os

# --- API Setup ---
API_KEY = "AIzaSyDFgvmW1Opy4LVccsCTtsN7-bLoN3RBL5A"
youtube = build('youtube', 'v3', developerKey=API_KEY)

# --- Parameters ---
queries = ["Power BI", "Machine Learning", "Deep Learning"]
max_results = 5
download_limit = 1   # number of videos to download per topic
download_path = "downloads"
max_duration_seconds = 1800  # 30 minutes = 1800 seconds

# --- Create download folder ---
os.makedirs(download_path, exist_ok=True)

all_data = []

# --- YouTube Search ---
for query in queries:
    print(f"\n🔍 Searching for: {query}")
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    query_downloaded = 0

    for item in response.get("items", []):
        if query_downloaded >= download_limit:
            break

        video_id = item["id"].get("videoId")
        if not video_id:
            continue

        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        publish_date = item["snippet"]["publishedAt"]
        url = f"https://www.youtube.com/watch?v={video_id}"

        all_data.append({
            "query": query,
            "title": title,
            "channel": channel,
            "publish_date": publish_date,
            "url": url
        })

        try:
            # --- Get video info ---
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                duration = info.get("duration", 0)

            if duration > max_duration_seconds:
                print(f"⏩ Skipped (too long): {title[:60]} ({duration//60} min)")
                continue

            # --- Download video ---
            ydl_opts = {
                'outtmpl': f'{download_path}/%(title).50s.%(ext)s',
                'format': 'best[ext=mp4]',
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"✅ Downloaded: {title[:60]}")
            query_downloaded += 1

        except Exception as e:
            print(f"❌ Skipped {url} → {e}")

# --- Save to CSV ---
df = pd.DataFrame(all_data)
df.to_csv("youtube_search_results.csv", index=False)
print("\n✅ Data saved to youtube_search_results.csv")
