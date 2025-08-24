import streamlit as st
# from .zencore import ZENPLAYER_URL
# import requests


def get_zenrandom():
    def get_time(time_s):
        return str(int(time_s // 60)).zfill(2) + "m " + \
            str(int(time_s % 60)).zfill(2) + "s"

    st.markdown("**Random Album**")
    # data = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_state").json()
    # meta = requests.get(f"{ZENPLAYER_URL}/zenplayer/get_track_meta").json()

    # st.markdown(f"**{data['artist']}: {data['album']}** - " \
    #                 f"*{data['file_name'].split('/')[-1].split('.')[0]}*")
    # st.write(
    #     f"{meta['sample_rate']}hz, {meta['bitrate']}kbps, {get_time(meta['length'])}")
    # st.image(f"{ZENPLAYER_URL}/zenplayer/get_track_cover",
    #             use_container_width=True)
    # zp.write(streamlit_image_coordinates(
    #     f"{ZENPLAYER_URL}/zenplayer/get_track_cover"),
    #     use_column_width="always")
