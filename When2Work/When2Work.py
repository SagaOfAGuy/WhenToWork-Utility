from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from Browser import Chrome
from selenium.webdriver.chrome.options import Options
import calendar
from ICSWriter import * 
import time 
import argparse
from dotenv import load_dotenv

class When2Work():
    def __init__(self):
        # .env file 
        load_dotenv('creds.env')
        
        self.options = Options()
        self.options.add_argument("headless")
        self.chromedriver = Chrome(options=self.options)
        self.chromedriver.set_window_size(1920,1080)
        self.wait = WebDriverWait(self.chromedriver, 10)
        self.login()
        print("Browser Started!")
    def login(self): 
        username = os.environ['WHEN2WORK_USER']
        pss = os.environ['WHEN2WORK_PASS']
        self.chromedriver.execute_script("window.location='https://whentowork.com/logins.htm';")
        user = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        pswd = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        self.chromedriver.slow_type(user, 0.078, username)
        self.chromedriver.slow_type(pswd, 0.083, pss)
        submit = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
        submit.click()
        print("Login Successful!")
    def schedule_screenshot(self,jobtitle):
        self.chromedriver.execute_script(
            "ReplWin('empschedule','&MyView=Month')")
        page_source = self.chromedriver.page_source
        counter = 0
        while(jobtitle in page_source):
            counter += 1 
            calendar = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "modwide")))
            self.chromedriver.execute_script("window.scrollTo(0,0)")
            print("Loading screenshot...")
            self.chromedriver.save_elem_screenshot(calendar, f"Schedule{counter}.png")
            print("Wating...")
            self.chromedriver.execute_script("ReplaceWindow('empschedule','&Month=Next');return false;")
            page_source = self.chromedriver.page_source
        self.chromedriver.quit()

    def team_schedule_screenshot(self):
        self.chromedriver.execute_script("ReplWin('empfullschedule','&View=Week')")
        page_source = self.chromedriver.page_source
        counter = 0
        while(not 'has not been published' in page_source):
            counter += 1
            calendar = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "modwide")))
            self.chromedriver.save_elem_screenshot(calendar, f"TeamSchedule{counter}.png")
            self.chromedriver.execute_script("ReplaceWindow('empfullschedule','&Week=Next');return false;")
            page_source = self.chromedriver.page_source
        

    def dump_shifts(self):
        def convert_time(time):
            if (time[0:2] == str(12)):
                return str(time[0:2])
            elif ('pm' in time):
                time_var = int(time[0]) + 12
                return str(time_var)
            else:
                return str(time[0])
        def fraction_time(time):
            if (':' in time):
                return str(time[time.index(':'):time.index('m')-1])
            else:
                return ':00'
        
        def add_zero(number):
            if (len(number) == 1):
                return '0' + number
            else:
                return number
                
        def main():
            month_dates = []
            month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            self.chromedriver.execute_script("ReplWin('empschedule','&MyView=Future')")
            shift_body = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/table[1]/tbody/tr[2]/td/table/tbody")))
            shift_cells = shift_body.find_elements_by_tag_name("tr")
            month_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
            icsfile = open('Schedule.ics', 'w')
            ics_beginning = start_ics()
            icsfile.write(ics_beginning+"\n")
            for shift_cell in shift_cells:
                shift_cell_text = shift_cell.text.replace('\n', ' ').split()
                shift_start = shift_cell_text[4] 
                shift_end = shift_cell_text[6]
                start_hour = convert_time(shift_start)
                year = shift_cell_text[3]
                end_hour = convert_time(shift_end)
                start_fraction = fraction_time(shift_start)
                end_fraction = fraction_time(shift_end)
                start_hour_number = f'{add_zero(start_hour)}{start_fraction[1:]}'
                end_hour_number = f'{add_zero(end_hour)}{end_fraction[1:]}'
                shift_day = shift_cell_text[2][0: shift_cell_text[2].index(',')]
                month = str(month_to_num[shift_cell.text[4:7]])
                ics_content = write_ics_middle("VCU",year, add_zero(month),add_zero(shift_day),start_hour_number, end_hour_number)
                icsfile.write(ics_content)
            ics_ending = end_ics()
            icsfile.write(ics_ending)
            icsfile.close() 
            print("Shifts written to file")
            self.chromedriver.quit()
            print("Browser exited")
        main()
if __name__ == "__main__":
    # Change this variable per your employment position
    jobtitle = ""
    
    my_parser = argparse.ArgumentParser(description='Automate When2Work Schedule Retrieval')
    my_parser.add_argument("mode", type=str, default=1.0, help="Adjust schedule mode")
    args = my_parser.parse_args()
    if (args.mode == "self"):
        When2Work().schedule_screenshot(jobtitle)
        When2Work().dump_shifts()
    elif (args.mode == "team"):
        When2Work().team_schedule_screenshot(jobtitle)
    else:
        print("Invalid option. Use 'team' for team schedule and 'self' for your schedule. Ex: 'python3 When2Work.py team' ")





