import logging, json, os, dotenv
from googleapiclient.discovery import build


dotenv.load_dotenv("keys.env")
apiKey = os.getenv("YOUTUBE_API_KEY")


def channelIdCollecter(handles: list):
    channelIDs = []

    for handle in handles:
        try:
            with build("youtube", "v3", developerKey=apiKey) as service:
                data = service.channels().list(
                    part = "id",
                    forHandle = str(handle)
                ).execute()
                try:
                    for item in data["items"]:
                        channelIDs.append(item["id"])
                except Exception as collectionException:
                    logging.exception(f"There was an exception while gathering the IDs for the channels.\n{collectionException}")

        except Exception as requestException:
            logging.exception(f"An exception has occured while forming a respons.\n{requestException}")

    return channelIDs


def playlistsExtraction(channelIDs: list):
    

    collectedData = []
    for channelID in channelIDs:
        token = ""
        channelData = []
        channelDict = {"Total Number of Playlists": None, "Channel ID:": channelID, "Playlists": None}

        try:
            with build("youtube", "v3", developerKey=apiKey) as service:
                while True:
                    data = service.playlists().list(
                        part = ["id", "snippet"],
                        channelId = channelID,
                        maxResults = 50,
                        pageToken = token
                    ).execute()
                    for item in data["items"]:
                        playlistTitle = item["snippet"]["title"]
                        playlistID = item["id"]
                        channelDataFormat = {"Title": playlistTitle, "ID": playlistID, "Items": None}
                        channelData.append(channelDataFormat)

                    if "nextPageToken" in data:
                        token = data["nextPageToken"]
                    
                    else:
                        token = ""
                        channelDict["Playlists"] = channelData
                        channelDict["Total Number of Playlists"] = data["pageInfo"]["totalResults"]
                        collectedData.append(channelDict)
                        break

        except Exception as requestException:
            logging.exception(f"An error happend while creating a request to the channel holding this ID: {channelID}.\n{requestException}")

    return collectedData


def playlistsItemsExtraction(collectedData: list):
    
    allVideosIDs = []
    token = ""
    for channelIndex, _ in enumerate(collectedData):
        for playlistIndex, playlist in enumerate(collectedData[channelIndex]["Playlists"]):
            playlistID = playlist["ID"]
            videoIDs = []

            try:
                with build("youtube", "v3", developerKey=apiKey) as service:
                    while True:
                        data = service.playlistItems().list(
                            part = ["contentDetails", "snippet"],
                            playlistId = playlistID,
                            pageToken = token,
                            maxResults = 50
                        ).execute()

                        for item in data["items"]:
                            videoID = item["contentDetails"]["videoId"]
                            collectedDataFormat = {"ID": videoID}
                            videoIDs.append(collectedDataFormat)
                            allVideosIDs.append(videoID)
                        
                        if "nextPageToken" in data:
                            token = data["nextPageToken"]
                        
                        else:
                            token = ""
                            collectedData[channelIndex]["Playlists"][playlistIndex]["Items"] = videoIDs
                            break

            except Exception as videoExtractionError:
                logging.exception(f"An error occured while fetching the Video IDs from the {playlist}, in channel {collectedData[channelIndex]['Channel ID:']}\n{videoExtractionError}")

    return collectedData, allVideosIDs


def videoDataExtraction(collectedData: list, videosIDs: list):
    videosIDs = list(dict.fromkeys(videosIDs))
    
    requestLimit = 50
    requestsChunks = [videosIDs[i:i+requestLimit] for i in range(0, len(videosIDs), requestLimit)]
    lookupDict = {}

    try:

        with build("youtube", "v3", developerKey=apiKey) as service:
            for chunck in requestsChunks:
                data = service.videos().list(
                    part = ["snippet", "statistics"],
                    id = chunck
                ).execute()
                for item in data["items"]:
                    lookupDict[item["id"]] = item

    except Exception as videoDataExtractionError:
        logging.exception(f"There was an error while collecting the data of the videos.\n{videoDataExtractionError}")

    for channelIndex, _ in enumerate(collectedData):
        for playlist in collectedData[channelIndex]["Playlists"]:
            for video in playlist["Items"]:
                video["Views"] = None
                video["Likes"] = None
                video["Title"] = None
                video["Publication Date"] = None

                if video["ID"] in lookupDict:
                    item = lookupDict[video["ID"]]
                    video["Views"] = item.get("statistics", {}).get("viewCount")
                    video["Likes"] = item.get("statistics", {}).get("likeCount")
                    video["Title"] = item.get("snippet", {}).get("title")
                    video["Publication Date"] = item.get("snippet", {}).get("publishedAt")


    with open(file="D:\YTS\collectedData.json", mode= "w") as file:
        file.write(json.dumps(collectedData, indent=2))

    return collectedData
