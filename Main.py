from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
import csv
from pathlib import Path


Builder.load_file('Design.kv')

class WelcomeScreen(Screen):
    def employee(self):
        self.manager.current = "employee_screen"

    def employer(self):
            self.manager.current = "employer_screen"

class EmployeeScreen(Screen):

    def submit(self,name,workload):

            if Path('workload.csv').is_file(): #check if file exists, if it doesn't create the file and add headers
                pass
            else:
                with open('workload.csv', 'w', newline='') as file_write:
                    writer = csv.writer(file_write)
                    headers = "Entry", "Name", "Date", "Workload"
                    writer.writerow(headers)
                    file_write.close

            with open('workload.csv', newline='') as file_read: #get row number to use for the first column
                data = []
                reader = csv.reader(file_read)
                for row in reader:
                    data.append(row)
                file_read.close
                #print(data[-1][0])


            with open('workload.csv', 'a+', newline='') as file_append: #add row into csv data
                writer = csv.writer(file_append)
                if name=="" or workload =="":#check if can be done in kv file
                    print("no input")
                else:
                    if data[-1][0] == "Entry": #check if is not the header row and use 1 for the first row if True
                        row_1 = 1,name,datetime.now().strftime("%d-%m-%Y"),workload
                        writer.writerow(row_1)
                    else:
                        row = int(data[-1][0])+1,name,datetime.now().strftime("%d-%m-%Y"),workload
                        writer.writerow(row)

                file_append.close

                self.manager.current = "submit_success_screen"

    def previous(self):
        #self.manager.transition.direction = 'right'
        self.manager.current = "welcome_screen"

    def exit(self):
        self.exit()

class EmployerScreen(Screen):
    def single(self):
        self.manager.current = "choose_screen"

    def all(self):
        self.manager.current = "all_screen"

    def previous(self):
        #self.manager.transition.direction = 'right'
        self.manager.current = "welcome_screen"

    def exit(self):
        self.exit()
class Submit_SuccessScreen(Screen):
    def next(self):
        self.manager.current = "employee_summary_screen"
    def exit(self):
        self.exit()

class Employee_SummaryScreen(Screen):
    pass

class ChooseScreen(Screen):
    pass

class AllScreen(Screen):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()
