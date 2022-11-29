from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from datetime import datetime
import csv
from pathlib import Path
import pandas
import matplotlib.axes


Builder.load_file('Design.kv')

class WelcomeScreen(Screen):
    def employee(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "employee_screen"


    def employer(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "employer_screen"

class EmployeeScreen(Screen):

    def submit(self,name,workload):

            if Path('workload.csv').is_file(): #check if file exists, if it doesn't create the file and add headers
                with open('workload.csv', newline='') as file_read:
                    data = []
                    reader = csv.reader(file_read)
                    index = 0
                    for row in reader:
                        index = index+1
                        if row[1] == name and row[2] == datetime.now().strftime("%d-%m-%Y"): #check if input already given by the user on that day
                            print("Input already given today!") #test
                            show_popup()
                            file_read.close
                            return
                        else:
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

            with open('workload.csv', 'a+', newline='') as file_append: #add row into csv data
                writer = csv.writer(file_append)
                if name=="" or workload =="": #check if can be done in kv file
                    print("no input")
                else:
                    if data[-1][0] == "Entry": #check if is not the header row and use 1 for the first row if True
                        row_1 = 0,name,datetime.now().strftime("%d-%m-%Y"),workload
                        writer.writerow(row_1)
                    else:
                        row = int(data[-1][0])+1,name,datetime.now().strftime("%d-%m-%Y"),workload
                        writer.writerow(row)
                file_append.close

                self.manager.transition.direction = 'left'
                self.manager.current = "submit_success_screen"



    def previous(self):
        #self.manager.transition.direction = 'right'
        self.manager.transition.direction = 'right'
        self.manager.current = "welcome_screen"


    def exit(self):
        self.exit()

    def overwrite(self, name, workload): #overwrite current record
        #select_screen = self.manager.get_screen("employee_screen")
        #name = self.ids.name.text
        #workload = self.ids.workload.int
        with open('workload.csv', newline='') as file_read:
            data = []
            reader = csv.reader(file_read)
            index = 0
            for row in reader:
                index = index+1
                if row[1] == name and row[2] == datetime.now().strftime("%d-%m-%Y"):

                    data = pandas.read_csv("workload.csv")
                    df = pandas.DataFrame(data)
                    df.loc[self.index, ['workload']] == workload

                    file_read.close
                    popupWindow.dismiss




class EmployerScreen(Screen):
    def single(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "choose_screen"


    def all(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "all_screen"


    def previous(self):
        #self.manager.transition.direction = 'right'
        self.manager.transition.direction = 'right'
        self.manager.current = "welcome_screen"


    def exit(self):
        self.exit()

class Submit_SuccessScreen(Screen):
    def next(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "employee_summary_screen"

    def exit(self):
        self.exit()

class Employee_SummaryScreen(Screen):

    def on_enter(self):
        select_screen = self.manager.get_screen("employee_screen")
        name = select_screen.ids.name.text
        df = pandas.read_csv("workload.csv")
        df['Name'] = df['Name'].astype('|S80')
        df['Date'] = df['Date'].astype('datetime64')
        df['Workload'] = df['Workload'].astype('int64')
        df['Name'] = df['Name'].str.decode('utf-8')
        data_name = df[df['Name'] == ("Oskar Przybylski")] #replace Oskar Przybylski with name when not testing

        print (data_name)

        plot = data_name.plot('Date','Workload', linestyle='--', marker='o', ylim = (0, 6), legend = False)            # Graph creation and customization
        plt.plot()
        plt.xlabel('Date')
        plt.ylabel('Stress Level')
        plt.grid(True, color='lightgray')
        plt.margins()
        y = [1, 2, 3, 4, 5]
        plt.yticks(y)
        plt.xticks(data_name['Date'], rotation=45)
        box = self.ids.box

        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def save(self):
        pass                                                 # needs fixing
        select_screen = self.manager.get_screen("employee_screen")
        name = select_screen.ids.name.text
        plt.savefig(name + ".jpg", format='jpg' )

    def exit(self):
        self.exit()


class ChooseScreen(Screen): #employer inputs employee name on this screen
    def choose(self, employee_choice):
        with open('workload.csv', newline='') as file_read: #check if record exist for selected employee. If true, go to the next screen
            data = []
            reader = csv.reader(file_read)
            index = 0
            for row in reader:
                index = index+1
                if row[1] == employee_choice:

                    self.manager.transition.direction = 'left'
                    self.manager.current = "employee_graph_screen"
                else:                                                 #let user know if employee name entered does not exist in the records
                    print("Employee does not exist.") #test
                    self.ids.prompt.text = "Records for this employee do not exist, please check and try again."

    def previous(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "employer_screen"

class EmployeeGraphScreen(Screen):
    def on_enter(self):
        select_screen = self.manager.get_screen("choose_screen")
        employee_choice = select_screen.ids.employee_choice.text
        df = pandas.read_csv("workload.csv")
        df['Name'] = df['Name'].astype('|S80')
        df['Date'] = df['Date'].astype('datetime64')
        df['Workload'] = df['Workload'].astype('int64')
        df['Name'] = df['Name'].str.decode('utf-8')
        data_name = df[df['Name'] == (employee_choice)]

        plot = data_name.plot('Date','Workload', linestyle='--', marker='o', ylim = (0, 6), legend = False)            # Graph creation and customization
        plt.plot()
        plt.xlabel('Date')
        plt.ylabel('Stress Level')
        plt.grid(True, color='lightgray')
        plt.margins()
        y = [1, 2, 3, 4, 5]
        plt.yticks(y)
        plt.xticks(data_name['Date'], rotation=45)
        box = self.ids.box

        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def save(self):
        pass                                                 # needs fixing
        select_screen = self.manager.get_screen("choose_screen")
        employee_choice = select_screen.ids.employee_choice.text
        print(employee_choice)
        plt.savefig( employee_choice + ".jpg", format='jpg' )

    def another(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "choose_screen"


    def exit(self):
        self.exit()

    def on_leave(self, *args):
        plt.clf()
        box = self.ids.box
        box.clear_widgets()


class AllScreen(Screen):
    def on_enter(self):
        # select_screen = self.manager.get_screen("employee_screen")
        # name = select_screen.ids.name.text
        df = pandas.read_csv("workload.csv")
        df['Name'] = df['Name'].astype('|S80')
        df['Date'] = df['Date'].astype('datetime64')
        df['Workload'] = df['Workload'].astype('int64')
        df['Name'] = df['Name'].str.decode('utf-8')

        names = df.Name.unique()

        df_all = pandas.DataFrame(df['Date'])

        for name in names:
            data_each = df[df['Name'] == name]

            df_all[name] = data_each['Workload']

        plot = df_all.plot('Date', linestyle='--', marker='o', ylim = (0, 6), label = name).legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
        plt.axes()
        plt.plot()
        plt.xlabel('Date')
        plt.ylabel('Stress Level')
        plt.grid(True, color='lightgray')
        plt.margins()
        y = [1, 2, 3, 4, 5]
        plt.yticks(y)
        plt.xticks(df_all['Date'], rotation=45)
        box = self.ids.box

        fig = FigureCanvasKivyAgg(plt.gcf())
        fig.size_hint_x = 1
        fig.size_hint_y =1
        fig.pos_hint={"x":0, "y":0}
        box.add_widget(fig)

    def previous(self):
        #self.manager.transition.direction = 'right'
        self.manager.transition.direction = 'right'
        self.manager.current = "employee_screen"

class EmployeePopUp(FloatLayout):
    pass



class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
        mypopup = MyPopup()

        return mypopup.show_popup()


def show_popup():
    mytext= "It looks like you have already submitted something today, would you like to overwrite?"

    content = BoxLayout(orientation="vertical")

    content.add_widget(Label(text=mytext, font_size=20))

    yesbutton = Button(text="Yes", size_hint=(1,.20), font_size=20)
    content.add_widget(yesbutton)
    nobutton = Button(text="No", size_hint=(1,.20), font_size=20)
    content.add_widget(nobutton)

    popupWindow = Popup(content = content,title = "Popup", auto_dismiss = False)
    yesbutton.bind(on_press=EmployeeScreen.overwrite)
    nobutton.bind(on_press=popupWindow.dismiss)
    popupWindow.open()


if __name__=="__main__":
    MainApp().run()
