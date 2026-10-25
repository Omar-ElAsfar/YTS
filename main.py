import logging
from infoCollection import basicInfo
from YTAPI import *


logging.basicConfig(level=logging.INFO, filename=f"{__name__}.log", filemode="w",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def main():
    channels = basicInfo()
    logging.info(f"The Handles of the YouTube Channels Have Been Collected.\nHandles: {channels}")
    channelIDs = channelIdCollecter(handles=channels)
    logging.info(f"All the IDs of the Specified Channels Have Been Aquired.\nIDs: {channelIDs}")
    collectedDataVersion1 = playlistsExtraction(channelIDs)
    logging.info(f"All Playlists in {channels} Have Been Collected Successfully")
    collectedDataVersion2, allVideos = playlistsItemsExtraction(collectedDataVersion1, channelIDs)
    logging.info("Every Video ID in the Collected Playlists Have Been Successfully Colleceted")
    collectedDataVersion3 = videoDataExtraction(collectedDataVersion2, channelIDs, allVideos)
    logging.info("All the Data of the Videos in Each of the Selected Channels Have Been Successfully Collected")


if __name__ == "__main__":
    main()
