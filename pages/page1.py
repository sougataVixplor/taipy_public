
import os
import pandas as pd

from pages.data_generator import DataGen


class Page1:
    data=pd.read_excel(os.path.join('data','data.xlsx'))
    def section_1(self):
        sec1="""
        <center>
        <|navbar|lov={[("page1", "Home"), ("page2", "Live Matches"), ("Page3", "Upcoming Matches"), ("Page4", "Past Results"), ("Page5", "Players Stats")]}|>
        </center>
        """
        return sec1
    def section_2(self,data):
        sec2="""
        <center>
        <|navbar|>
        </center>
        <|{data}|chart|type=bar|x=Match|y=Run|>
        """
        return sec2
    def section_3(self):
        obj=DataGen()
        df=obj.cricket_api_data_live_matches()
        sec3="""
        <center>
        <|navbar|>
        </center>
        <|{df}|table|height=400px|y=70%|>
        """
        return sec3