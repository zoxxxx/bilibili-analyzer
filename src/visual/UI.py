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
    st.set_page_config(layout="wide")
    data = []
    # st.session_state.mid = None
    # st.session_state["userData"] = None
    with st.sidebar.form("my_form"):
        st.write("## 选择用户")
        mid_input = st.text_input("输入用户mid", "546195")

        if st.form_submit_button(label='查询'):
            st.session_state.mid = mid_input
            with st.spinner('正在加载数据...'):
                st.session_state.userData = UserData(st.session_state.mid)
                data  = st.session_state.userData.getData()

    with st.sidebar:
        if st.session_state.userData is not None:
            st.write("数据获取时间：{}".format(st.session_state.userData.time.strftime("%Y-%m-%d %H:%M:%S")))
        if st.button("刷新数据", disabled=st.session_state.userData is None):
            with st.spinner('正在刷新数据...'):
                print(st.session_state.mid)
                st.session_state.userData.update()
                data = st.session_state.userData.getData()

    st.markdown("""
    <style>
        .st-emotion-cache-1v0mbdj.e115fcil1 img{
            border-radius: 50%;
        }
    </style>
    """, unsafe_allow_html=True)

    url = data["face"]

    face = Image.open(requests.get(url, stream=True).raw)

    colmn1, colmn2 = st.columns([1,7])
    colmn1.image(face, width=100)
    colmn2.markdown("#### <span style='color:#fb7299;'>{}</span>".format(data["name"]), unsafe_allow_html=True)
    colmn2.write(data["sign"])
    data["videos"].sort(key=lambda x: x["created"])
    timestamp = []
    views = []
    names = []
    covers = []
    for i in data["videos"]:
        timestamp.append(i["created"])
        views.append(i["play"])
        names.append(i["title"])  # 添加视频名称
        covers.append(i["pic"])  # 添加视频封面
        # covers.append(i["pic"].replace("http://", "https://"))  # 添加视频封面
    date = [datetime.datetime.fromtimestamp(i).strftime("%Y-%m-%d") for i in timestamp]
    # set echarts size in options

    options = {
        # "width": "1000px",
        # "height": "1000px",
        "tooltip": {
            "trigger": "axis",
            "formatter": """
                <div style='display: flex; align-items: center;'>
                    <img src={c2} width='80' height='60' style='margin-right: 10px;' referrerpolicy='no-referrer'/>
                    <div>
                        <b>{b}</b><br />
                        <b>{a0}</b>: {c0}<br />
                        <b>{a1}</b>: {c1}<br />
                    </div>
                </div>
            """
        },
        "xAxis": {
            "type": "category",
            "data": date,
        },
        "yAxis": {"type": "value"},
        "series": [
            {"name": "播放量", "data": views, "type": "line"},
            {"name": "视频名称", "data": names, "type": "line"},  
            {"name": "视频封面", "data": covers, "type": "line"}, 
        ],
        "dataZoom": [
            {
                "type": "slider",
                "start": 0,
                "end": 100,
            }
        ]
    }
    st_echarts(options=options, height=500,width=1000)


if __name__ == '__main__':
    if st.runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

