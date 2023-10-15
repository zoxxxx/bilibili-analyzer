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
    with st.sidebar.form("my_form"):
        st.write("## 选择用户")
        mid_input = st.text_input("输入用户mid", "546195")
        if st.form_submit_button(label='Submit'):
            mid = mid_input
        with st.spinner('正在加载数据...'):
            userData = UserData(mid)
            data  = userData.getData()
        url = data["face"]
        image = Image.open(requests.get(url, stream=True).raw)
        st.write("## " + data["name"])
        st.image(image, width=200)
    date = []
    views = []
    for i in data["videos"]:
        date.append(i["created"])
        views.append(i["play"])
    options = {
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": date,
        },
        "yAxis": {"type": "value"},
        "series": [
            {"data": views, "type": "line"}
        ],
        "dataZoom": [
            {
                "type": "slider",
                "start": 0,
                "end": 100,
            }
        ]
    }
    st_echarts(options=options)


if __name__ == '__main__':
    if st.runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())

