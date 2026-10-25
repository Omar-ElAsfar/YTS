import sqlite3, json

with sqlite3.connect("D:\YTS\YouTubeDB.db") as connection:
    cursor = connection.cursor()

def dataPopulating(collectedData, handles):
    with open(file="D:\YTS\schema.sql", mode="r") as sqlScript:
        try:
            cursor.executescript(sqlScript.read())
        except sqlite3.OperationalError:
            pass
        
        channelsData = []
        playlistsData = []
        videosData = []
        playlistItemsData = []
        for handle, channel in zip(handles, collectedData):
            channelsData.append((handle, channel["Channel ID:"]))

            for playlist in channel["Playlists"]:
                playlistsData.append((playlist["ID"], playlist["Title"], channel["Channel ID:"]))

                for video in playlist["Items"]:
                    videosData.append((video["ID"], video["Views"], video["Likes"], video["Title"], video["Publication Date"]))
                    playlistItemsData.append((playlist["ID"], video["ID"]))
        
        cursor.executemany("INSERT OR REPLACE INTO Channels(Handle, ChannelID) VALUES(?, ?)", channelsData)
        cursor.executemany("INSERT OR REPLACE INTO Playlists(PlaylistID, PlaylistTitle, ChannelID) VALUES(?, ?, ?)", playlistsData)
        cursor.executemany("INSERT OR REPLACE INTO Videos(VideoID, Views, Likes, Title, ReleaseDate) VALUES(?, ?, ?, ?, ?)", videosData)
        cursor.executemany("INSERT OR REPLACE INTO PlaylistItems(PlaylistID, VideoID) VALUES(?, ?)", playlistItemsData)
        connection.commit()

def getChannelNumber():
    cursor.execute("SELECT Handle FROM Channels")
    data = cursor.fetchall()
    print(f"Number of channels: {len(data)}\nChannel Names:")
    for handle in data:
        print(f"{str(handle).strip('()').strip(',')}")


def getPlaylistNumberInChannel():
    cursor.execute("SELECT ChannelID, COUNT(PlaylistID) FROM Playlists GROUP BY ChannelID")
    numberOfPlaylistsInChannel = cursor.fetchall()
    return numberOfPlaylistsInChannel


def getVideoNumberInChannel(numberOfPlaylistsInChannel):
    cursor.execute("SELECT ChannelID, VideoID INNER JOIN Playlists ON PlaylistItems.PlaylistID = Playlist.PlaylistID")
    test = cursor.fetchall()
    print(test)
    for channel in numberOfPlaylistsInChannel:
        print(channel)
    


getVideoNumberInChannel(getPlaylistNumberInChannel())