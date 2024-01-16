import pandas as pd
import xlsxwriter
import traceback
import requests
from bs4 import BeautifulSoup


def player_stat(player):
  name=player.split(' ')[0]
  title=player.split(' ')[1]
  domain='https://search.espncricinfo.com'
  domain2='https://www.espncricinfo.com'
  playerURL='https://search.espncricinfo.com/ci/content/site/search.html?search=$name%20$title;type=player'
  playerURL=playerURL.replace('$name',name).replace('$title',title)
  
  print(playerURL)
  data=requests.get(playerURL)
  soup=BeautifulSoup(data.content,'html5lib')

  pfraim=soup.find('div',class_='results in-players')
  link=pfraim.find_all('a')
  path=link[0].get('href')
  path=domain+path
  page2=requests.get(path)
  soup2=BeautifulSoup(page2.content,'html5lib')
  stat=soup2.find_all('div',class_='ds-w-full ds-bg-fill-content-prime ds-overflow-hidden ds-rounded-xl ds-border ds-border-line')

  for s in stat:
    t=s.find('h2')
    if t==None:
      continue
    print(t.text)
    if 'recent' not in str(t.text).lower():
      continue
    link3=s.find('a',title='View more')
    path3=link3.get('href')
    path3=domain2+path3
    data3=requests.get(path3)
    soup3=BeautifulSoup(data3.content,'html5lib')
    stat2=soup3.find_all('div',class_='ds-w-full ds-bg-fill-content-prime ds-overflow-hidden ds-rounded-xl ds-border ds-border-line ds-pb-4')
    player_dict={}
    for s in stat2:

      t=s.find('span',class_='ds-text-title-xs ds-font-bold ds-text-typo')

      if t==None:
        continue
      print(t.text)
      if 'recent' not in str(t.text).lower():
        continue

      records=s.find_all('tr')
      count=0
      for record in records:
        count+=1
        if count==1:
          continue
        matc=record.find_all('td')[0].text
        bat=record.find_all('td')[1].text
        bowl=record.find_all('td')[2].text
        bat=bat.replace(' ','')
        bowl=bowl.replace(' ','')
        if '/' in bat:
          bowl=bat
          bat='0'

        bat_value=''.join(i for i in bat if (i.isdigit()))

        if bat_value==None or len(bat_value)==0:
          bat_value=0

        if 'c' in bowl and '/' in bowl and 's' in bowl:
          bowl='0'
        elif '/' in bowl:
          bowl=bowl.split('/')[0]

        bowl_value=''.join(i for i in bowl if (i.isdigit()))
        if bowl_value==None or len(bowl_value)==0:
          bowl_value=0
        elif int(bowl_value)>10000:
          bowl_value=0
        player_dict[count]={'Match':matc,'Bat':bat,'Bowl':bowl}
      return player_dict
      

def generate_excel():
  playerList=['Rohit Sharma', 'Shubman Gill', 'Virat Kohli', 'KL Rahul', 'Ishan Kishan', 'Hardik Pandya', 'Ravindra Jadeja', 'Kuldeep Yadav', 'Jasprit Bumrah', 'Mohammed Siraj']
  df=pd.DataFrame(columns=['Player Name','Match 1','Match 2','Match 3','Match 4','Match 5','Match 6','Match 7','Match 8','Match 8','Match 9','Match 10'])
  
  writer = pd.ExcelWriter('cric_stats.xlsx' , engine="xlsxwriter")
  
  startrowval=0  
  for idx,player in enumerate(playerList):

    try:
      workbook = writer.book
      stats_dict=player_stat(player)
      matchs=[]
      bats=[]
      bowls=[]
      player_df=pd.DataFrame(columns=['Match','Bat','Bowl'])
      for k,v in stats_dict.items():
        matchs.append(v['Match'])
        bats.append(v['Bat'])
        bowls.append(v['Bowl'])
      player_df['Match']=matchs
      player_df['Bat']=bats
      player_df['Bowl']=bowls
      player_df.to_excel(writer, sheet_name=player.split(' ')[1], index=False)
      worksheet = writer.sheets[player.split(' ')[1]]
      worksheet.set_zoom(100)
      header_format = workbook.add_format(
            {
                "valign": "vcenter",
                "align": "center",
                "bg_color": "#D7E4BC",
                "text_wrap": True,
                "bold": True,
                "font_color": "black",
                "border": 1,
            }
        )

      for col_num, value in enumerate(player_df.columns.values):
          worksheet.write(startrowval, col_num, value, header_format)
      border_fmt = workbook.add_format({"align": "center","text_wrap": True,"border": 1,})
      if len(player_df.columns) == 0:
            continue
      worksheet.conditional_format(
            xlsxwriter.utility.xl_range(0, 0, len(player_df), len(player_df.columns) - 1),
            {"type": "no_errors", "format": border_fmt},
        )
      
    except Exception as e:
      traceback.print_exc()
      continue
  writer.save()


