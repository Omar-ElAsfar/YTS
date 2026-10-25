A project that utilizes the YouTube API to collect data on channels, videos, and playlists.
To run it, get the Handle of a channel (it is the @youtuber under a channel's name) and pass it through the basicInfo function. After ensuring the Handle is correct, the project goes through a multi-step process to fetch the channel's ID, all the playlists in it, and the videos in them.
This data is then used to populate a database made with SQLite.
