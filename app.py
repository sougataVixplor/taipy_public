import os
from taipy import Gui
import pandas as pd
from pages.data_generator import DataGen
from pages.page1 import Page1

data=pd.read_excel(os.path.join('data','data.xlsx'))
obj=DataGen()
df=obj.cricket_api_data_live_matches()
p1_obj=Page1()
value='Search'
login_id=None
passcode=None

def button_pressed(state):
    print(state.value)
def auth_login(state):
    print(state.login_id)
    print(state.passcode)

# section_1="""
# <center>
# <|navbar|lov={[("page1", "Home"), ("page2", "Live Matches"), ("Page3", "Upcoming Matches"), ("Page4", "Past Results"), ("Page5", "Players Stats")]}|>
# </center>
# """

login="""

<|text-center|
Enter User ID and Passcode

<|{login_id}|input|>
<|{passcode}|input|>
<|Button Label|button|on_action=auth_login|>

|>

"""    

section_2="""
<center>
<|navbar|>
</center>
<|layout|columns=1 1 1|

<|{data}|chart|type=bar|x=Match|y=Run|>

<|{data}|chart|type=lines|x=Match|y=Run|>

<|{data}|chart|type=pie|x=Match|y=Run|>
|>

<|{df}|table|height=400px|y=70%|>
"""
section_3="""
<center>
<|navbar|>
</center>

<|{df}|table|height=400px|y=70%|>
"""

section_4="""
<center>
<|navbar|>
</center>
##Enter Player Name to see stat
<|text-center|

<|{value}|input|>
<|Button Label|button|on_action=button_pressed|>

|>
"""

if __name__=="__main__":
    pages={
        'HOME':section_2,
        'MATCHES':section_3,
        'SEARCH':section_4

    }
    app= Gui(pages=pages)
    app.run(dark_mode=False)
