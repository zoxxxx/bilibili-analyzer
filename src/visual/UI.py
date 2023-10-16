import streamlit as st
from streamlit.web import cli as stcli
from src.utils import *
from src.crawler import *
from PIL import Image
import requests
from streamlit_echarts import st_echarts
import sys
import datetime
    
def main():
    st.set_page_config(layout="wide", page_title="b站up主数据查询")
    with st.sidebar.form("my_form"):
        st.write("## 选择用户")
        name_input = st.text_input("输入用户名", "老番茄")

        if st.form_submit_button(label='查询'):
            name = name_input
            progress_text = '正在加载数据...'
            my_bar = st.progress(0, text=progress_text)

            st.session_state.userData = UserData(name=name)
            st.session_state.userDataStorage = st.session_state.userData.getData()
            st.session_state.userDataStorage["videos"].sort(key=lambda x: x["created"])

            st.session_state.videoDataStorage = []
            count = 0
            for i in st.session_state.userDataStorage["videos"]:
                videoData = VideoData(i["bvid"])
                res = videoData.getData()
                st.session_state.videoDataStorage.append(res)
                count += 1
                my_bar.progress(count / len(st.session_state.userDataStorage["videos"]), text=progress_text)
            my_bar.empty()


    with st.sidebar:
        if st.button("刷新数据", disabled=st.session_state.userData is None):
            progress_text = '正在刷新数据...'
            my_bar = st.progress(0, text = progress_text)
            st.session_state.userData.update()
            st.session_state.userDataStorage = st.session_state.userData.getData()

            st.session_state.videoDataStorage = []
            count = 0
            for i in st.session_state.userDataStorage["videos"]:
                videoData = VideoData(i["bvid"])
                videoData.update()
                res = videoData.getData()
                st.session_state.videoDataStorage.append(res)
                count += 1
                my_bar.progress(count / len(st.session_state.userDataStorage["videos"]), text=progress_text)
            my_bar.empty()

        if st.session_state.userData is not None:
            st.write("数据获取时间：{}".format(st.session_state.userData.time.strftime("%Y-%m-%d %H:%M:%S")))

    st.markdown("""
    <style>
        .st-emotion-cache-1v0mbdj.e115fcil1 img{
            border-radius: 50%;
        }
    </style>
    """, unsafe_allow_html=True)

    url = st.session_state.userDataStorage["face"]

    face = Image.open(requests.get(url, stream=True).raw)

    colmn1, colmn2 = st.columns([1,7])
    colmn1.image(face, width=100)
    colmn2.markdown("#### <span style='color:#fb7299;'>{}</span>".format(st.session_state.userDataStorage["name"]), unsafe_allow_html=True)
    colmn2.write(st.session_state.userDataStorage["sign"])
    date = [datetime.datetime.fromtimestamp(i["pubdate"]).strftime("%Y-%m-%d") for i in st.session_state.videoDataStorage]
    # set echarts size in options

    options = {
        "tooltip": {
            "trigger": "axis",
        },
        "xAxis": {
            "type": "category",
            "data": date,
        },
        "yAxis": [
            {
                "type": "value",
                "name": "播放量",
            },
            {
                "type": "value",
                "name": "点赞/投币/收藏",
            },
        ],
        "series": [
            {"name": "视频名称", "data": [i["title"] for i in st.session_state.videoDataStorage], "type": "line"},  
            {"name": "播放量", "data": [i["stat"]["view"] for i in st.session_state.videoDataStorage], "type": "line", "yAxisIndex": 0},
            {"name": "点赞", "data": [i["stat"]["like"] for i in st.session_state.videoDataStorage], "type": "line", "yAxisIndex": 1},
            {"name": "投币", "data": [i["stat"]["coin"] for i in st.session_state.videoDataStorage], "type": "line", "yAxisIndex": 1},
            {"name": "收藏", "data": [i["stat"]["favorite"] for i in st.session_state.videoDataStorage], "type": "line", "yAxisIndex": 1},
            {"name": "视频封面", "data": [i['pic'] for i in st.session_state.videoDataStorage], "type": "line","tooltip": {"show": False}}, 
        ],
        "legend": {
            "data": ["播放量", "点赞", "投币", "收藏"],
            "orient": "horizontal",
        },
        "dataZoom": [
            {
                "type": "slider",
                "start": 0,
                "end": 100,
            },
        ]
    }
    
    st_echarts(options=options, height=500, width="100%")

if __name__ == '__main__':
    if st.runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

