import tkinter as tk
import random
import smtplib
import json
from tkinter import ttk
from tkinter import messagebox

def perm_butt_toggle():
    global perm_bar
    if perm_bar.get()==1:
        perm_butt.config(state='normal')
    else:
        perm_butt.config(state='disabled')

def generateOTP(receiver,otp):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    password='urng vlrc gaeg sgqe'
    server.login("swd.demo69@gmail.com",password)
    msg='Hello, Your OTP is '+str(otp)
    sender='swd.demo69@gmail.com'
    server.sendmail(sender,receiver,msg)
    server.quit()

    return otp

def dumpinjson(dict_email, dict_perm):
    with open('data.json', 'r') as file:
        data = json.load(file)
    data[dict_email] = dict_perm
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)

window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - 600) // 2
y = (screen_height - 500) // 2
window.geometry(f"{600}x{500}+{x}+{y}")
window.title('Verification')
window.rowconfigure((0,2), weight=1)
window.rowconfigure((1,3), weight=5)
window.columnconfigure(0, weight=1)

def otpVerification(otp):
    global otp_var
    global dict_perm
    global email_var
    # global tempdict
    if otp_var.get() == otp:
        dict_perm = 1
        dumpinjson(email_var.get(), dict_perm)
        email_label.config(text='Verification Successful')
    else:
        email_label.config(text='OTP doesnt match')

def EmailPermSubmit():
    global correct_email
    global otp
    global otp_var
    global perm_bar
    global dict_email
    global dict_perm
    global tempdict
    email = email_var.get()
    email_label.config(text='')
    email_entry.destroy()
    perm_butt.destroy()
    perm_check.destroy()
    if email=='':
        messagebox.showinfo("Incorrect Email!", "Please Enter Correct Email!")
        window.destroy()
        
    else:
        if email[0] == 'f' and '@goa.bits-pilani.ac.in' in email:
            correct_email = True
            dict_email = email
            
            if perm_bar.get() == 1:
                generateOTP(email, otp)

                otp_window = tk.Toplevel(window)
                otp_window.title('Verification')
                otp_window.geometry(f"{600}x{500}+{x}+{y}")
                ttk.Label(otp_window, text='Enter OTP').pack()
                ttk.Entry(otp_window, text='four digit number sent to your mail', textvariable=otp_var).pack()
                ttk.Button(otp_window, text='Verify', command=lambda: (otpVerification(otp), otp_window.destroy())).pack()
            else:
                dict_perm = 0
                dumpinjson(email, dict_perm)
                email_label.config(text='Your permission has been recored!')
                

        else:
            correct_email = False
            messagebox.showinfo("Incorrect Email!", "Please Enter Correct Email!")
            window.destroy()
    # email_label.destroy()
    print(perm_bar.get())
    return correct_email

dict_email = None
dict_perm = None
otp=''.join([str(random.randint(0,9)) for i in range(4)])
correct_email = None
email_var = tk.StringVar()
perm_bar = tk.IntVar()
otp_var = tk.StringVar()


email_label = ttk.Label(master=window,text='Enter the email:', font=('Arial', 16), anchor='center')
email_label.grid(row=0, column=0, sticky='nsew', padx=50, pady=0, ipadx=50)

email_entry = ttk.Entry(master=window, textvariable=email_var, font=('Arial', 16))
email_entry.grid(row=1, column=0, sticky='ew', padx=30, ipadx=5,ipady=5)

perm_check = ttk.Checkbutton(window, text='Agreed to pay through SWD', variable=perm_bar, command=perm_butt_toggle)
perm_check.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=100)

perm_butt= ttk.Button(master=window, text='Submit', command=EmailPermSubmit, state='disabled')
perm_butt.grid(row=3, column=0, columnspan=2, sticky='nswe', padx=50, pady=50)

window.mainloop()