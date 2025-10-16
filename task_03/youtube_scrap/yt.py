from googleapiclient.discovery import build
import pandas as pd

# Replace with your API key
API_KEY = "AIzaSyDFgvmW1Opy4LVccsCTtsN7-bLoN3RBL5A"
youtube = build('youtube', 'v3', developerKey=API_KEY)

queries = ["Power BI", "Machine Learning", "Deep Learning"]
max_results = 50
all_data = []

for query in queries:
    print(f"\n🔍 Searching for: {query}")
    next_page_token = None
    page = 1

    while True:
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results,
            pageToken=next_page_token
        )
        response = request.execute()

        data = []
        for item in response.get("items", []):
            # ✅ Some items might not have 'videoId'
            video_id = item["id"].get("videoId")
            if not video_id:
                continue

            title = item["snippet"]["title"]
            channel = item["snippet"]["channelTitle"]
            publish_date = item["snippet"]["publishedAt"]
            url = f"https://www.youtube.com/watch?v={video_id}"

            data.append({
                "query": query,
                "title": title,
                "channel": channel,
                "publish_date": publish_date,
                "url": url
            })

        # Get stats (views/comments)
        video_ids = [d["url"].split("v=")[1] for d in data]
        if video_ids:
            stats_request = youtube.videos().list(
                part="statistics",
                id=",".join(video_ids)
            )
            stats_response = stats_request.execute()

            for i, stat in enumerate(stats_response.get("items", [])):
                data[i]["views"] = stat["statistics"].get("viewCount", 0)
                data[i]["comments"] = stat["statistics"].get("commentCount", 0)

        all_data.extend(data)
        print(f"  ✅ Page {page} fetched: {len(data)} videos")

        # Stop after a few pages (to avoid quota overuse)
        next_page_token = response.get("nextPageToken")
        if not next_page_token or page >= 3:  # fetch up to 3 pages per query
            break
        page += 1

# Save to CSV
df = pd.DataFrame(all_data)
df.to_csv("youtube_search_results.csv", index=False)
print("\n✅ All data saved to youtube_search_results.csv")
