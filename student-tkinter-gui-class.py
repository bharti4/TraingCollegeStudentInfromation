"""
Programming Language : Python
Approach : procedural programming approach
GUi design : tkinter
database : mariaDb
Functionality :
1. Create database name MyTrainingCollege
2. create table student with userID, name, course,marks, password
3. create login functionality for admins and students
4. admin can  insert update delete and view student information
5. student can only view the information

Thank you for visiting the code you do further modification more practice :
1. add email ID , address field to student table
2. Student can also edit email id , address , password


"""

from tkinter import *
from tkinter import messagebox

import bcrypt as bcrypt
from DatabaseFunctionality import *

def login():
    username = username_entry.get()
    password = userpassword_entry.get()
    is_admin = var_admin.get()

    if is_admin:
        rows = fetchwithConditioaColumn("adminUser", ["userName"], [username])
        # print(rows)
        if len(rows) > 0:
            hashedPassword = rows[0][2].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashedPassword):
                 messagebox.showinfo("Login Successful", "Welcome!")
                 # calling to display admin view functionality
                 hideFrame(loginFrame)
                 showFrame(adminFrame)
                 populate_studentlist()
                 showLogoutButton()

        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")
    else:
        rows = fetchwithConditioaColumn("student", ["ID"], [username])

        if rows:
            if len(rows) > 0:
                hashedPassword = rows[0][4].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashedPassword):
                    messagebox.showinfo("Login Successful", "Welcome!")
                    # Allow Access to Display student view functionality
                    hideFrame(loginFrame)
                    Label(studnentFrame, text="ID:",anchor="w",width=10,bg="#f7f5dd").grid(row=0, column=0)
                    Label(studnentFrame, text=rows[0][0],anchor="w",width=50,bg="#f7f5dd").grid(row=0, column=1)

                    Label(studnentFrame, text="Name:",anchor="w",width=10,bg="#f7f5dd").grid(row=1, column=0)
                    Label(studnentFrame, text=rows[0][1],anchor="w",width=50,bg="#f7f5dd").grid(row=1, column=1)

                    Label(studnentFrame, text="Course:",anchor="w",width=10,bg="#f7f5dd").grid(row=2, column=0)
                    Label(studnentFrame, text=rows[0][2],anchor="w",width=50,bg="#f7f5dd").grid(row=2, column=1)

                    Label(studnentFrame, text="Marks:",anchor="w",width=10,bg="#f7f5dd").grid(row=3, column=0)
                    Label(studnentFrame, text=rows[0][3],anchor="w",width=50,bg="#f7f5dd").grid(row=3, column=1)

                    showFrame(studnentFrame)
                    showLogoutButton()

        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")
#To display the logout button
def showLogoutButton():
    btn_logout.grid(row=1, column=6, columnspan=1, pady=0)


def logout():
    global selected_item
    hideFrame(studnentFrame)
    hideFrame(adminFrame)
    showFrame(loginFrame)
    username_entry.delete(0, END)
    userpassword_entry.delete(0, END)
    selected_item = None;
    btn_logout.grid_forget()
    username_entry.focus_set()

def selectStudent(event):
    try:
        global selected_item
        index = studentlist.curselection()[0]
        selected_item = studentlist.get(index)
        clearText()

        studentID_entry.insert(END, selected_item[0])
        studnentName_entry.insert(END, selected_item[1])
        course_entry.insert(END, selected_item[2])
        marks_entry.insert(END, selected_item[3])

    except IndexError:
        pass
    pass


# populate  list of student items
def populate_studentlist():
    studentlist.delete(0, END)
    #studentlists = fetch("student")
    studentlists= load_data("student",["ID", "studentName", "course"  , "marks"])
    for studentRow in studentlists:
        studentlist.insert(END, studentRow)

def addStudent():
    if studentID_entry.get() == '' or studnentName_entry.get() == '' or password_entry.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    try:
        password = password_entry.get()
        # Hash the password securely using bcrypt
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        insertData("student", ["ID", "studentName", "course", "marks", "studentPassword"],
                   [studentID_entry.get(), studnentName_entry.get(), course_entry.get(), marks_entry.get(),
                    hashedPassword])

        studentlist.insert(END, (
        studentID_entry.get(), studnentName_entry.get(), course_entry.get(), marks_entry.get()))
        clearText()
    except Exception as error:
        messagebox.showerror("Error",f"Error: {error}")

#allows to update selected students data
def updateStudent():
    if studentID_entry.get() == '' or studnentName_entry.get() == '' :
        messagebox.showerror('Required Fields', 'Please include all Required fields-ID and Name ')
        return
    try:
        if(password_entry.get() == ''):
            update("student", ["studentName", "course", "marks", ],
                   [studnentName_entry.get(), course_entry.get(), marks_entry.get()], "ID",
                   studentID_entry.get())
            populate_studentlist()
            messagebox.showinfo("Information", "Update operation confirmed.")
            clearText()
        else:
            result = messagebox.askyesno("Confirmation","Are you sure you want to update passowrd")
            if result:
                password = password_entry.get()
                hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                update("student", ["studentName", "course", "marks","studentPassword" ],
                       [studnentName_entry.get(), course_entry.get(), marks_entry.get(),hashedPassword], "ID",
                       studentID_entry.get())
                populate_studentlist()
                clearText()
                messagebox.showinfo("Information", "Update operation confirmed.")
            else:
                messagebox.showinfo("Information", "Update operation canceled.")

    except Exception as error:
        messagebox.showerror("Error",f"Error: {error}")


def removeStudnent():
    try:
        result = messagebox.askyesno("Confirmation", f"Are you sure you want to delete student with ID {selected_item[0]}")
        if result:
            remove("student", "ID", selected_item[0])
            clearText()
            populate_studentlist()
            messagebox.showinfo("Information","Delete operation confirmed.")
        else:
            messagebox.showinfo("Information","Delete operation canceled.")
    except Exception as error:
        messagebox.showerror("Error",f"Error: {error}")
#Hide the frame
def hideFrame(frameToHide):
    frameToHide.grid_forget()

# clear student entry fields
def clearText():
    studentID_entry.delete(0, END)
    studnentName_entry.delete(0, END)
    password_entry.delete(0, END)
    course_entry.delete(0, END)
    marks_entry.delete(0, END)

#Show the frame
def showFrame(frameToShow):
    frameToShow.grid(row=1, column=0,columnspan=3,padx=20, pady=20)

# create Database and table require for this application
def initializeDatabase():
    global DbName
    DbName = "MyTrainingCollege"
    createDatabase(DbName)

    createTable("student",
                "ID VARCHAR(30) PRIMARY KEY, studentName VARCHAR(100), course VARCHAR(30) , marks INT , studentPassword VARCHAR(80)")
    createTable("adminUser",
                "userId INT AUTO_INCREMENT PRIMARY KEY, userName VARCHAR(50) NOT NULL,  password VARCHAR(100) NOT NULL")
    '''
    # Inserting Sample data to user table for testing application for admin login
    password = "admin"
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    insertData("adminUser",['userName', 'password'],["admin" ,hashedPassword])
    '''

# Main application code
# Create the main  application window and call to initial database
initializeDatabase()
win = Tk()
win.title('Training College')
win.geometry('550x550')
win.config(padx=50,pady=10,bg="#D7FFDF")
win.columnconfigure(0, weight=1)
win.columnconfigure(1, weight=3)


# top level heading and logout button holding frame
mainTopheadingFrame = Frame(bg="#D7FFDF",pady=10,padx=0)
# Add logout button

Label1 = Label(mainTopheadingFrame, text="Welcome to the Application", font=("Arial", 16), fg="darkgreen", bg="#D7FFDF")
Label1.grid(row=0, column=0, columnspan=5, pady=20,padx=60)
btn_logout = Button(mainTopheadingFrame, text="Logout", command=logout , bg="lightgreen",padx=4)
mainTopheadingFrame.grid(row=0,column=0,columnspan=6,padx=0, pady=0)


### Loing Frame
loginFrame = Frame(win)
loginFrame.config(bg="#f7f5dd",padx=10,pady=20)
# loginFrame.grid(row=0, column=0, padx=10, pady=10)
# Add username and password entry fields
label_username = Label(loginFrame, text="Username:",bg="#f7f5dd")
label_username.grid(row=1, column=0, padx=10, pady=5)
username_entry = Entry(loginFrame, width=30)
username_entry.grid(row=1, column=1, padx=10, pady=5)

label_password = Label(loginFrame, text="Password:",bg="#f7f5dd")
label_password.grid(row=2, column=0, padx=10, pady=5)
userpassword_entry = Entry(loginFrame, show="*", width=30)
userpassword_entry.grid(row=2, column=1, padx=10, pady=5)

var_admin = BooleanVar()
check_admin = Checkbutton(loginFrame, text="Admin Login", variable=var_admin,bg="#f7f5dd")
check_admin.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Add login button
btn_login = Button(loginFrame, text="Login", command=login)
btn_login.grid(row=4, column=0, columnspan=2, pady=20)

adminFrame = Frame(win)
adminFrame.config(bg="#f7f5dd",pady=10,padx=5)
# adminFrame.grid(row=0, column=0, padx=10, pady=10)
# Studnent ID
studentID = StringVar()
studentID_label = Label(adminFrame, text='Student ID :', font=('bold', 10), pady=2 ,anchor="w", width=10,bg="#f7f5dd")
studentID_label.grid(row=0, column=0, sticky=W, pady=0)
studentID_entry = Entry(adminFrame, textvariable=studentID,width=30)
studentID_entry.grid(row=0, column=1, columnspan=2)
# Student Name
studnentName = StringVar()
studnentName_label = Label(adminFrame, text='Student Name:', font=('bold', 10),bg="#f7f5dd")
studnentName_label.grid(row=1, column=0, sticky=W, pady=0)
studnentName_entry = Entry(adminFrame, textvariable=studnentName,width=30)
studnentName_entry.grid(row=1, column=1, columnspan=2)
# course
course = StringVar()
course_label = Label(adminFrame, text='Course :', font=('bold', 10),bg="#f7f5dd")
course_label.grid(row=2, column=0, sticky=W)
course_entry = Entry(adminFrame, textvariable=course,width=30)
course_entry.grid(row=2, column=1, columnspan=2)
# marks
marks = StringVar()
marks_label = Label(adminFrame, text='Total Marks :', font=('bold', 10),bg="#f7f5dd")
marks_label.grid(row=3, column=0, sticky=W)
marks_entry = Entry(adminFrame, textvariable=marks,width=30)
marks_entry.grid(row=3, column=1, columnspan=2)
# Password
password = StringVar()
password_label = Label(adminFrame, text='Password :', font=('bold', 10),bg="#f7f5dd")
password_label.grid(row=4, column=0, sticky=W)
password_entry = Entry(adminFrame, textvariable=password,show="*", width=30)
password_entry.grid(row=4, column=1, columnspan=2)

# Buttons for add remove update and clear
add_btn = Button(adminFrame, text='Add ', width=12, command=addStudent)
add_btn.grid(row=5, column=0, padx=5, pady=20)

remove_btn = Button(adminFrame, text='Remove ', width=12, command=removeStudnent)
remove_btn.grid(row=5, column=1, padx=5, pady=20)

update_btn = Button(adminFrame, text='Update ', width=12, command=updateStudent)
update_btn.grid(row=5, column=2, padx=5, pady=20)

clear_btn = Button(adminFrame, text='Clear ', width=12, command=clearText)
clear_btn.grid(row=5, column=3, padx=5, pady=20)

# student List (Listbox)

studentlist = Listbox(adminFrame,  width=100, border=0)
studentlist.grid(row=6, column=0,   pady=20, padx=20)

# Create a Scrollbar widget
scrollbar = Scrollbar(adminFrame, command=studentlist.yview)
scrollbar.grid(row=6, column=3, sticky=NS)
#allow list box to expand
adminFrame.grid_rowconfigure(6, weight=1)
adminFrame.grid_columnconfigure(0, weight=1)

studentlist.grid(row=6, column=0, columnspan=3, rowspan=6, pady=20, padx=20,sticky=NSEW)

# Bind select
studentlist.bind('<<ListboxSelect>>', selectStudent)

#Frame to display student information
studnentFrame = Frame(win)
studnentFrame.config(bg="#f7f5dd",pady=5,padx=5)

showFrame(loginFrame)

win.mainloop()


