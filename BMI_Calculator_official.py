from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import math

class Introduction:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("400x400+100+100")
        self.root.configure(bg='#EDBF7C')
        
        self.image_icon = PhotoImage(file = "top_icon.png")
        self.root.iconphoto(False, self.image_icon)

        self.name_label = Label(self.root, text="Surname:", font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08")
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

        self.name_entry = Entry(root, font="arial 15 bold")
        self.name_entry.grid(row=0, column=1, padx=20, pady=20)

        self.surname_label = Label(self.root, text="Last name:", font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08")
        self.surname_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

        self.surname_entry = Entry(root, font="arial 15 bold")
        self.surname_entry.grid(row=1, column=1, padx=20, pady=20)

        self.age_label = Label(self.root, text="Age:", font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08")
        self.age_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)

        self.age_sb = Spinbox(self.root, font="arial 15 bold", from_=1, to=120, command=self.update_age)
        self.age_sb.grid(row=2, column=1, padx=20, pady=20, sticky=tk.W)
        self.age_sb.delete(0, END)
        self.age_sb.insert(0, 1)
        
        self.gender= StringVar()
        self.male_rb = Radiobutton(self.root, text="Male", variable=self.gender, value ="male",  font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08", padx= 5)
        self.male_rb.grid(row=3, column=0, padx=20, pady=20, sticky=tk.E)
        
        self.female_rb = Radiobutton(self.root, text="Female", variable=self.gender, value ="female",  font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08", padx= 5)
        self.female_rb.grid(row=3, column=1, padx=20, pady=20, sticky=tk.W)

        self.save_enter_button = Button(self.root, text="Save and Enter", font="arial 10 bold", bg="#B58A78", fg="white",
                                        command=self.open_new_window)
        self.save_enter_button.grid(row=4, column=1, padx=20, pady=20, sticky=tk.E)

    def update_age(self):
        try:
            age = int(self.age_sb.get())
        except ValueError:
            age = 1
        return age

    def open_new_window(self):
        surname = self.name_entry.get()
        lastname = self.surname_entry.get()
        age = self.age_sb.get()
        
        with open("userdata.txt", "w") as file:
            file.write(f"Name: {surname} {lastname}\nAge: {age}\n")

        gender_value = self.gender.get()

        with open("userdata.txt", "a") as file:
            if gender_value == "male":
                file.write("Sex: Male\n")
            elif gender_value == "female":
                file.write("Sex: Female\n")

        self.root.destroy()
        root = Tk()
        app = BMICalculator(root, age, gender_value, height=0.,weight=0.)
        
        app.language_var.set("Englsih")    
        initial_image = app.images["English"]
        app.set_image(initial_image)
        
        app.switch_language()
        
    def go_back(self):
        self.root.destroy()
        
#-------------------------------BMICalculator-----------------------------

class BMICalculator:
    def __init__(self, root, age, gender, height=0., weight=0.):
        # root = Tk()
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("1200x600+20+0")
        self.root.configure(bg='#EDBF7C')

        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight

        #two boxes
        self.box = PhotoImage(file = "box.png")
        Label(self.root, image=self.box, bg="#EDBF7C").place(x=220, y=100)
        Label(self.root, image=self.box, bg="#EDBF7C").place(x=440, y=100)

        self.image_icon = PhotoImage(file="top_icon.png")
        self.root.iconphoto(False, self.image_icon)

        # ... Other initialization code ...
        
        #--------------------slider------------------------
        self.current_value = tk.DoubleVar()
        self.current_value2 = tk.DoubleVar()
        
        self.style = ttk.Style()
        self.style.configure("TScale",background="white")
        self.slider = ttk.Scale(root, from_=0, to=220, orient='horizontal', style="TScale",
                        command=self.slider_changed, variable=self.current_value)
        self.slider.place(x=280, y=250)

        self.style2 = ttk.Style()
        self.style2.configure("TScale",background="white")
        self.slider2 = ttk.Scale(root, from_=0, to=220, orient='horizontal', style="TScale",
                            command=self.slider_changed2, variable=self.current_value2)
        self.slider2.place(x=500, y=250)   

        #-----------------------------------------------------
        #--------------------------image----------------------
        self.images = {
            "English": self.load_and_resize_image("english.png"),
            "中文(简)": self.load_and_resize_image("chinese_jian.png"),
            "中文(繁)": self.load_and_resize_image("chinese_fan.png"),
            "ไทย": self.load_and_resize_image("thai.png"),
        }
        
        self.image_label = Label(self.root, bg="#EDBF7C")
        self.image_label.place(x=700, y=200)
        
        self.top_label = Label(self.root, text="BMI CALCULATOR", font="arial 40", bg="#B58A78", fg="white", padx=1000)
        self.top_label.pack()
        
        #--------------------------height,weight---------------
        self.height_label = Label(self.root, text="Height(cm):", font="arial 20 bold", bg="#fff", fg="#B47417")
        self.height_label.place(x=240, y=110)
        
        self.weight_label = Label(self.root, text="Weight(kg):", font="arial 20 bold", bg="#fff", fg="#B47417")
        self.weight_label.place(x=460, y=110)

        
        self.Height = StringVar()
        self.Weight = StringVar()
        self.height = Entry(self.root, textvariable=self.Height, width=5, font='arial 50', bg = "#fff", fg= "#000", bd=0, justify=CENTER)
        self.height.place(x=235, y=160)
        self.Height.set(self.get_current_value())

        self.weight = Entry(self.root, textvariable=self.Weight, width=5, font='arial 50', bg = "#fff", fg= "#000", bd=0, justify=CENTER)
        self.weight.place(x=455, y=160)
        self.Weight.set(self.get_current_value2())

        self.secondimage = Label(root, bg="#EDBF7C")
        self.secondimage.place(x=270, y=530)
        
        self.bmi = None

        self.scale = PhotoImage(file = "scale.png")
        Label(root, image=self.scale, bg="#EDBF7C").place(x=220, y=310)


        #------------------------------------------------------

        # ... Other widget creation ...

        self.language_var = StringVar(value="English")
        self.language_options = ["English", "中文(简)", "中文(繁)", "ไทย"]
        self.language_var.trace_add("write", self.switch_language)

        self.language_menu = OptionMenu(self.root, self.language_var, *self.language_options)
        self.language_menu.config(bg="#B58A78", fg="white")
        self.language_menu.place(x=1100, y=68)

        self.report_button = Button(self.root, text="View Report", width=15, height=2, font="arial 10 bold", bg="#B58A78", fg="white", command=self.BMI)
        self.report_button.place(x=560, y=340)
        
        self.label1 = Label(self.root, font="arial 60 bold", bg = "#EDBF7C", fg="#fff")
        self.label1.place(x=350,y=305)

        self.label2 = Label(self.root, font="arial 30 bold", bg = "#EDBF7C", fg="#3b3a3a")
        self.label2.place(x=480,y=430)

        self.label_3 = Label(self.root, font="arial 10", bg = "#EDBF7C", fg="red")
        self.label_3.place(x=500, y=400)
        
        self.reset_button = Button(self.root, text="Reset", width=15, height=2, font="arial 10 bold", bg="#B58A78", fg="white", command=self.reset)
        self.reset_button.place(x=560, y=290)
        
        self.more_button = Button(self.root, text="More", width=15, height=2, font="arial 10 bold", bg="#B58A78", fg="white", command=lambda: self.more())
        self.more_button.place(x=1000, y=500)
        
        self.cancel_button = Button(self.root, text="Cancel", width=15, height=2, font="arial 10 bold", bg="#B58A78", fg="white", command=self.cancel)
        self.cancel_button.place(x=1000, y=550)
        

    # def pop_up_message(self):
        
    def cancel(self):
        self.root.destroy()
    
    def BMI(self):
        try:
            h = float(self.Height.get())
            w = float(self.Weight.get())
            
            with open("userdata.txt", "a") as file:
                file.write(f"Height: {h:.2f}\nWeight: {w:.2f}\n")
                        
            
            if h == 0.0 or w==0.0:
                self.label_3.config(text="Missing value!\nPlease enter both height and weight.", fg="red")
            
            else:
                self.label_3.config(text="")
                m = h / 100.
                bmi = round(float(w / m ** 2), 1)
                self.bmi = bmi
                self.label1.config(text=bmi)
                
                with open("userdata.txt", "a") as file:
                    file.write(f"BMI Result: {round(bmi,1)}\n")
                    if bmi <= 18.5:
                        self.label2.config(text="Underweight")
                        file.write(f"BMI Level: Underweight\n")
                    if bmi > 18.5 and bmi < 25:
                        self.label2.config(text="Normal")
                        file.write(f"BMI Level: Normal\n")
                    if bmi > 25:
                        self.label2.config(text="Overweight")
                        file.write(f"BMI Level: Overweight\n")
                    
                messagebox.showinfo("For further information,", "by clicking \"More\" you know more information about your diet")

        except ValueError as e:
            self.label_3.config(text="Missing value!\nPlease enter both height and weight.", fg="red")
            self.bmi = None
            
        return bmi

    def reset(self):
        self.Height.set("")
        self.Weight.set("")
        self.current_value.set(0)
        self.current_value2.set(0)
        
        self.label1.config(text="")
        self.label2.config(text="")
        self.label_3.config(text="")
        self.bmi = None

    #---------------------creating slider-------------------
    #slider1
    def get_current_value(self):
        current_value = self.current_value.get()
        return '{: .2f}'.format(current_value)

    def slider_changed(self, event):
        self.Height.set(self.get_current_value())
        
        size = int(float(self.get_current_value()))
        img = (Image.open("man.png"))
        resized_image = img.resize((50, 10+size))
        photo2 = ImageTk.PhotoImage(resized_image)
        self.secondimage.config(image = photo2)
        self.secondimage.place(x=300, y=550-size)
        self.secondimage.image=photo2

    
    #slider2
    def get_current_value2(self):
        current_value2 = self.current_value2.get()
        
        return '{: .2f}'.format(current_value2)

    def slider_changed2(self, event):
        self.Weight.set(self.get_current_value2())
        
        
    def get_bmi_category(self, bmi):
        selected_language = self.language_var.get()

        if selected_language == "English":
            if bmi <= 18.5:
                self.label2.config(text="Underweight")
            if 18.5 < bmi < 25:
                self.label2.config(text="Normal")
            if bmi > 25:
                self.label2.config(text="Overweight")

        elif selected_language == "中文(简)":
            if bmi <= 18.5:
                self.label2.config(text="体重过轻")
            if 18.5 < bmi < 25:
                self.label2.config(text="正常范围")
            if bmi > 25:
                self.label2.config(text="异常范围")

        elif selected_language == "中文(繁)":
            if bmi <= 18.5:
                self.label2.config(text="體重過輕")
            if 18.5 < bmi < 25:
                self.label2.config(text="正常範圍")
            if bmi > 25:
                self.label2.config(text="異常範圍")

        elif selected_language == "ไทย":
            if bmi <= 18.5:
                self.label2.config(text="น้ำหนักน้อยเกินไป")
            if 18.5 < bmi < 25:
                self.label2.config(text="ช่วงปกติ")
            if bmi > 25:
                self.label2.config(text="ช่วงข้อยกเว้น")
                    
    
    def load_and_resize_image(self, image_path):
        image = Image.open(image_path)
        resized = image.resize((400, 200))
        return ImageTk.PhotoImage(resized)


    def set_image(self, image):
        self.image_label.config(image=image)
        self.image_label.image = image
    
    def more(self):
        self.root.destroy()
        
        root = Tk()
        app = NewWindow1(root, self.age, self.gender, self.Height.get(), self.Weight.get())
        
    
    #-------------------------------------------------------
    def switch_language(self, *args):
        selected_language = self.language_var.get()

        if selected_language == "English":
            self.report_button.config(text="View Report")
            self.root.title("BMI Calculator")
            self.top_label.config(text="BMI CALCULATOR")
            self.reset_button.config(text="Reset")
            category = self.get_bmi_category(self.bmi)
            self.label2.config(text=category)            

        elif selected_language == "中文(简)":
            self.report_button.config(text="查看报告")
            self.root.title("BMI 计算器")
            self.top_label.config(text="BMI 计算器")
            self.reset_button.config(text="清除")
            category = self.get_bmi_category(self.bmi)
            self.label2.config(text=category)  

        elif selected_language == "中文(繁)":
            self.report_button.config(text="查看報告")
            self.root.title("BMI 計算器")
            self.top_label.config(text="BMI 計算器")
            self.reset_button.config(text="清除")
            category = self.get_bmi_category(self.bmi)
            self.label2.config(text=category)  

        elif selected_language == "ไทย":
            self.report_button.config(text="ดูรายงาน")
            self.root.title("เครื่องคิดเลขค่าดัชนีมวลกาย")
            self.top_label.config(text="เครื่องคิดเลขค่าดัชนีมวลกาย")
            self.reset_button.config(text="รีเซ็ต")
            category = self.get_bmi_category(self.bmi)
            self.label2.config(text=category)  
                 
        if selected_language in self.images:
            self.image_label.config(image=self.images[selected_language])
            self.image_label.image = self.images[selected_language]
            
#--------------------------NewWindow1-------------------------

class NewWindow1:
    def __init__(self, root, age, gender, height, weight):
        self.root = root 
        self.root.title("BMI Calculator")
        self.root.geometry("1200x600+20+0")
        self.root.configure(bg='#EDBF7C')
        
        self.image_icon = PhotoImage(file = "top_icon.png")
        self.root.iconphoto(False, self.image_icon)
        
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        
        self.name_text = Label(
            self.root, 
            text=f"Please select one of the options and each option is explained as below.",
            font="arial 15 bold", bg="#EDBF7C", fg="#fff",
        )
        self.name_text.place(x=100,y=50)

        self.bmr_button = Button(self.root, text="BMR", font="arial 15 bold", width= 10, bg="#B58A78", fg="white", command=lambda:self.open_bmr(float(self.age),self.gender,float(self.height), float(self.weight)))
        self.bmr_button.place(x=150, y=100, )
        
        self.bmr_text = Label(
            self.root, 
            text="BMR(Basal Metabolic Rate): \n"
            "The amount of energy expended by the body at rest in order to maintain basic physiological functions\nsuch as breathing, circulation, and cell production. In other words,\nit represents the number of calories your body needs to function while at rest.",
            font="arial 10 bold", bg="#EDBF7C", fg="#fff", anchor='w', justify= LEFT
        )
        self.bmr_text.place(x=150, y=150)
        
        self.tdee_button = Button(self.root, text="TDEE", font="arial 15 bold", width= 10, bg="#B58A78", fg="white", command=self.open_tdee)
        self.tdee_button.place(x=150, y=230)

        self.tdee_text = Label(
            self.root, 
            text=f"TDEE(Total Daily Energy Expenditure):\nTakes into account your activity level and provides a more accurate\nestimate of the calories you need to consume to maintain, gain, or lose weight."
            "Common activity multipliers\ninclude sedentary, lightly active, moderately active, very active, etc. Multiply your BMR by the appropriate\nactivity level to get your TDEE.",
            font="arial 10 bold", bg="#EDBF7C", fg="#fff",anchor='w', justify= LEFT
        )
        self.tdee_text.place(x=150, y=280)
        
        self.BFP_button = Button(self.root, text="BFP", font="arial 15 bold", width= 10, bg="#B58A78", fg="white", command=self.open_bfp)
        self.BFP_button.place(x=150, y=370)
        
        self.BFP_text = Label(
            self.root,
            text=f"BFP(Body Fat Percentage):\nCalculate body fat percentage based on measurements such as waist, hip, neck circumference, and gender" ,
            font="arial 10 bold", bg="#EDBF7C", fg="#fff",anchor='w', justify= LEFT
        )
        self.BFP_text.place(x=150, y=420)
        
        self.cancel_button =  Button(self.root, text="Cancel", font="arial 15 bold", width= 10, bg="#B58A78", fg="white", command=lambda:self.root.destroy())
        self.cancel_button.place(x=1000, y=480)
        
        self.back_button =  Button(self.root, text="Back", font="arial 15 bold", width= 10, bg="#B58A78", fg="white", command=self.go_back)
        self.back_button.place(x=80, y=480)

    def go_back(self):
        self.root.destroy()
        root = Tk()
        app = BMICalculator(root, self.age, self.gender, self.height, self.weight)

    def open_bmr(self, age, gender, height, weight):
        self.root.destroy()
        root = Tk()
        app = BMR(root, age, gender, height, weight)
        app.display(height, weight)
    
    def open_tdee(self):
        self.root.destroy()
        root = Tk()
        app = More_Window(root, self.weight, self.height, self.age, self.gender)
        
    def open_bfp(self):
        self.root.destroy()
        root = Tk()
        app = BFPCalculator(root, self.age,self.gender,self.height, self.weight)
        
class BMR:
    def __init__(self, root, age, gender, height, weight):
    # def __init__(self, root):
        self.root = root 
        self.root.title("BMR Calculator")
        self.root.geometry("750x300+40+40")
        self.root.configure(bg='#EDBF7C')
        
        self.height = height
        self.weight = weight
        
        self.age = age
        self.gender = gender
        
        self.height_label = Label(self.root, text="Your Height :", font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08")
        self.height_label.place(x=150, y=50)
        
        self.height_result = Label(self.root, font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08")
        self.height_result.place(x=350, y=50)
        
        self.weight_label = Label(self.root, text="Your Weight :", font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08")
        self.weight_label.place(x=150, y=100)
        
        self.weight_result = Label(self.root, font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08")
        self.weight_result.place(x=350, y=100)
        
        self.bmr_label = Label(self.root, text="Your BMR Result :", font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08")
        self.bmr_label.place(x=150, y=150)      
          
        self.bmr_result = Label(self.root, font="arial 15 bold", bg="#EDBF7C", fg="#7F4E08")
        self.bmr_result.place(x=350, y=150)
        
        self.calculate_button = Button(root, text="Calculate",width=10,font="arial 10 bold", bg="#B58A78", fg="white", command=lambda:self.calculate_bmr(float(self.age), self.gender, self.height, self.weight))
        self.calculate_button.place(x=600, y=250)
         
        self.back_button = Button(root, text="Back", width=10,font="arial 10 bold", bg="#B58A78", fg="white", command=self.go_back)
        self.back_button.place(x=100, y=250)

    def display(self, height,weight):
        self.height_result.config(text=f"{height:.2f} centimeters")
        self.weight_result.config(text=f"{weight:.2f} kilograms")
        
    def calculate_bmr(self, age, gender, height, weight):
    
        if gender == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif gender == 'female':
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            raise ValueError("Invalid gender. Please enter 'male' or 'female'.")
        
        self.bmr_result.config(text=f"{bmr:.2f} calories/ a day")

    def go_back(self):
        self.root.destroy()
        root = Tk()
        app = NewWindow1(root, self.age, self.gender, self.height, self.weight)
        app

class More_Window():
    # def __init__(self, root):
    def __init__(self, root, weight, height, age, gender):
        self.weight = weight
        self.height = height
        self.age = age
        self.gender = gender
        
        self.root = root
        self.root.title("More Calculator")
        self.root.geometry("1150x600+20+0")
        self.root.configure(bg="#EDBF7C")
        
        self.image_icon = PhotoImage(file = "top_icon.png")
        self.root.iconphoto(False, self.image_icon)
        
        self.activity_frame = Frame(self.root, bg='white')
        self.activity_frame.place(x=280, y=150, width=600, height=200)
        
        self.activity_label = Label(self.root, text="Activity Levels:", font="arial 12 bold", bg='white', fg='#7F4E08')
        self.activity_label.place(x=280, y=150)
        
        self.activity_factor = DoubleVar()

        self.sedentary_rb = Radiobutton(self.root, text="Sedentary (little or no exercise)", variable=self.activity_factor, value=1.2, font="arial 12", bg='white', fg='#7F4E08', padx=5)
        self.sedentary_rb.place(x=280, y=180)

        self.lightly_active_rb = Radiobutton(self.root, text="Lightly active (light exercise/sports 1-3 days/week)", variable=self.activity_factor, value=1.375, font="arial 12", bg='white', fg='#7F4E08', padx=5)
        self.lightly_active_rb.place(x=280, y=210)

        self.moderately_active_rb = Radiobutton(self.root, text="Moderately active (moderate exercise/sports 3-5 days/week)", variable=self.activity_factor, value=1.55, font="arial 12", bg='white', fg='#7F4E08', padx=5)
        self.moderately_active_rb.place(x=280, y=240)

        self.very_active_rb = Radiobutton(self.root, text="Very active (hard exercise/sports 6-7 days a week)", variable=self.activity_factor, value=1.725, font="arial 12", bg='white', fg='#7F4E08', padx=5)
        self.very_active_rb.place(x=280, y=270)

        self.extremely_active_rb = Radiobutton(self.root, text="Extremely active (very hard exercise/sports & physical job or 2x training)", variable=self.activity_factor, value=1.9, font="arial 12", bg='white', fg='#7F4E08', padx=5)
        self.extremely_active_rb.place(x=280, y=300)
        
        self.calculate_button = Button(self.root, text="Calculate", width=15, height=2, font="arial 10 bold", bg="#B58A78", fg="white", command=self.calculate_bmr)
        self.calculate_button.place(x=480, y=430)
        
        self.back_button = Button(self.root, text="Back", width=15, height=2, font="arial 10 bold", bg="#B58A78", fg="white", command=self.go_back)
        self.back_button.place(x=480, y=480)
        
        self.goal_label = Label(self.root, text="Select Goal:", font="arial 12 bold", bg="#EDBF7C", fg='#7F4E08')
        self.goal_label.place(x=380, y=100)

        self.goals = ["Maintenance", "Weight Loss", "Weight Gain"]
        self.goal_var = StringVar()
        self.goal_combobox = ttk.Combobox(self.root, textvariable=self.goal_var, values=self.goals, state="readonly", font="arial 12")
        self.goal_combobox.place(x=480, y=100)
        self.goal_combobox.set("Maintenance")
        
        self.label_1 = Label(self.root, font="arial 10 bold", bg = "#EDBF7C", fg="#7F4E08")
        self.label_1.place(x=350,y=10)
        
        self.label_2 = Label(self.root, font="arial 10 bold", bg = "#EDBF7C", fg="#7F4E08")
        self.label_2.place(x=350,y=50)
        
        self.label_3 = Label(self.root, font="arial 10 bold", bg = "#EDBF7C", fg="#7F4E08")
        self.label_3.place(x=350,y=380)
        
    def go_back(self):
        self.root.destroy()
        
        root = Tk()
        app = NewWindow1(root, self.age, self.gender, self.height, self.weight)
                        
    def calculate_bmr(self):
        weight = float(self.weight)
        height = float(self.height)
        age = float(self.age)

        if self.gender == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif self.gender == 'female':
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            raise ValueError("Invalid gender. Please enter 'male' or 'female'.")

        self.label_1.config(text="")
        self.label_2.config(text="")
        self.label_3.config(text="")

        self.label_1.config(text="Your Result:")
        self.label_2.config(text=f"Your Basal Metabolic Rate (BMR) is {bmr:.2f} calories/day")

        tdee = bmr * self.activity_factor.get()

        goal = self.goal_var.get()
        if goal == "Maintenance":
            tmr = tdee
        elif goal == "Weight Loss":
            tmr = tdee - 500
        elif goal == "Weight Gain":
            tmr = tdee + 500

        self.label_3.config(text=f"For {self.goal_var.get()}, your daily calorie intake should be {tmr:.2f} calories.")        
        
        self.label_1.place(x=350, y=10)
        self.label_2.place(x=350, y=50)
        self.label_3.place(x=350, y=380)
        
        with open("userdata.txt", "a") as file:
            file.write(f"BMR result:\nYour Basal Metabolic Rate (BMR) is {bmr:.2f} calories/day")
            file.write(f"Goal: {goal}\nDaily Calories Intakes for {goal} is {tmr} calories.")

class BFPCalculator:
    def __init__(self, root, age,gender,height,weight):
        self.root = root        
        self.root.title("BFP Calculator")
        self.root.geometry("420x300+100+100")
        self.root.configure(bg='#EDBF7C')
        
        self.age = age
        self.height = height
        self.gender = gender
        self.weight = weight

        self.label1 = ttk.Label(root, text="Waist Circumference (in inches):", font="arial 10 bold", background="#EDBF7C", foreground="#6D4C41")
        self.label1.grid(row=0, column=0, sticky='e', padx=10, pady=5)

        self.waist_entry = ttk.Entry(root, font="arial 10 bold")
        self.waist_entry.grid(row=0, column=1, padx=10, pady=5)

        self.label2 = ttk.Label(root, text="Hip Circumference (in inches):", font="arial 10 bold", background="#EDBF7C", foreground="#6D4C41")
        self.label2.grid(row=1, column=0, sticky='e', padx=10, pady=5)

        self.hip_entry = ttk.Entry(root, font="arial 10 bold")
        self.hip_entry.grid(row=1, column=1, padx=10, pady=5)

        self.label3 = ttk.Label(root, text="Neck Circumference (in inches):", font="arial 10 bold", background="#EDBF7C", foreground="#6D4C41")
        self.label3.grid(row=2, column=0, sticky='e', padx=10, pady=5)

        self.neck_entry = ttk.Entry(root, font="arial 10 bold")
        self.neck_entry.grid(row=2, column=1, padx=10, pady=5)

        self.label4 = ttk.Label(root, text="Gender:", font="arial 10 bold", background="#EDBF7C", foreground="#6D4C41")
        self.label4.grid(row=3, column=0, sticky='e', padx=10, pady=5)

        gender_var = tk.StringVar()
        self.gender = gender_var.get()
        self.gender_combobox = ttk.Combobox(root, textvariable=gender_var, values=['Male', 'Female'], font="arial 10 bold")
        self.gender_combobox.grid(row=3, column=1, padx=10, pady=5)

        self.calculate_button = Button(root, text="Calculate Body Fat Percentage",command=lambda:self.calculate_body_fat(float(self.waist_entry.get()), float(self.hip_entry.get()), float(self.neck_entry.get()), gender_var.get(), self.height))
        self.calculate_button.config(font="arial 10 bold", bg="#B58A78", fg="white")
        self.calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(root, text="Result will be shown here.",font="arial 10 bold", background="#EDBF7C", foreground="#6D4C41")
        self.result_label.grid(row=5, column=0, columnspan=2, pady=10)

        #don't forget to write command 
        self.back_button = Button(root, text="Back",font="arial 10 bold", bg="#B58A78", fg="white",command=self.go_back)
        self.back_button.grid(row=6, column=0, columnspan=2, pady=10)

    def go_back(self):
            self.root.destroy()
            
            root = Tk()
            app = NewWindow1(root, self.age, self.gender, self.height, self.weight)

    def calculate_body_fat(self, waist, hip, neck, gender, height):
        try:
            waist = float(waist)
            hip = float(hip)
            neck = float(neck)
            height = float(self.height)/2.54
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter numeric values.")
            return

        if gender.lower() == 'male':
            formula = 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
        elif gender.lower() == 'female':
            formula = 163.205 * math.log10(waist + hip - neck) - 97.684 * math.log10(height) - 78.387
        else:
            self.result_label.config(text="Invalid gender. Please enter 'male' or 'female'.")
            return

        result = round(formula,2)
        self.result_label.config(text=f"Your estimated body fat percentage is: {result}%")
        
        with open("userdata.txt", "a") as file:
            file.write(f"Body Fat Percentage Result:\nGender: {gender}\nWaist: {waist}\nHip: {hip}\nNeck: {neck}\nResult: {result}%\n")

if __name__ == "__main__":
    root = Tk()
    app = Introduction(root)
    root.mainloop()