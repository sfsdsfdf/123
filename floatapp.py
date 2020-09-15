import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from functools import partial
import pandas as pd
import time
from datetime import datetime
import winsound

class Grid(FloatLayout):
    company_id=ObjectProperty(None)
    target=ObjectProperty(None)
    details=ObjectProperty(None)
    id_list=list()
    target_list=list()
    def add_company(self):
        self.id_list.append(self.company_id.text)
        self.target_list.append(self.target.text)
        website="http://www.nepalstock.com/marketdepthofcompany/"
        df=pd.read_html(website+str(self.company_id.text))
        company_name=df[0].iloc[0,0]
        if(len(self.details.text)>0 and self.details.text.split()[-1]=="Terminated"):
            self.details.text=""
        self.details.text+="\n"+str(company_name)+"   "+str(self.target.text)
        self.company_id.text=""
        self.target.text=""
    def update(self):
        Clock.schedule_interval(self.submit_list, 60)
    def submit_list(self,dt):
        company=[None]*len(self.id_list)
        all_values=[None]*len(self.id_list)
        website="http://www.nepalstock.com/marketdepthofcompany/"
        #while True:
        for i in range(len(self.id_list)):
            identifier=self.id_list[i]
            target=self.target_list[i]
            try:
                df=pd.read_html(website+str(identifier))
                company[i]=df[0].iloc[0,0]
                all_values[i]=df[1].iloc[0,0]
                values=list(map(str,all_values[i].split()))
                all_values[i]=float(values[0])
                time.sleep(5)
                if(all_values[i]>float(target)):
                    frequency = 2500  # Set Frequency To 2500 Hertz
                    duration = 2000  # Set Duration To 1000 ms == 1 second
                    winsound.Beep(frequency, duration)
            except:
                self.details.text="Retrying in 1 minute"
                time.sleep(5)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.details.text=""
        self.details.text=current_time
        for i in range(len(self.id_list)):
            self.details.text+="\n"+str(company[i])+"   "+str(all_values[i])
    def stop(self):
        Clock.unschedule(self.submit_list)
        self.details.text+="\n Task Terminated"
class Meroapp(App):
    def build(self):
        return Grid()
    
if (__name__ == "__main__"):
    Meroapp().run()
