CREATE TABLE Channels (
    ChannelID VARCHAR(24) PRIMARY KEY,
    Handle VARCHAR(30)
);

CREATE TABLE Playlists (
    PlaylistID VARCHAR(34) PRIMARY KEY,
    PlaylistTitle VARCHAR(150),
    ChannelID VARCHAR(24),

    FOREIGN KEY(ChannelID)
    REFERENCES Channels(ChannelID)
);

CREATE TABLE Videos(
    VideoID VARCHAR(11) PRIMARY KEY,
    Views INT,
    Likes INT,
    Title VARCHAR(100),
    ReleaseDate DATE
);

CREATE TABLE PlaylistItems(
    PlaylistID VARCHAR(34),
    VideoID VARCHAR(11),

    PRIMARY KEY(PlaylistID, VideoID),

    FOREIGN KEY(PlaylistID)
    REFERENCES Playlists(PlaylistID),

    FOREIGN KEY(VideoID)
    REFERENCES VideoData(VideoID)
);
