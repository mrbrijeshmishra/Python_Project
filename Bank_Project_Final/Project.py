from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox,Treeview,Style,Scrollbar
from PIL import Image,ImageTk
from datetime import datetime
import sqlite3

con=sqlite3.connect(database="bank.sqlite")
cur=con.cursor()
table1="create table accounts(account_no integer primary key autoincrement,account_name text,account_password text,account_email text,account_mob text,account_type text,account_bal float,account_opendate text)"
table2="create table txn(txn_account_no int,txn_amt float,txn_update_bal float,txn_date text,txn_type text)"
try:
    cur.execute(table1)
    cur.execute(table2)
    print("Tables Created")
except:
    print("something went wrong in database, table might exist.")
    
con.commit()
con.close()

win=Tk()
win.state("zoomed")
win.configure(bg="powder Blue")


lbl_title=Label(win,text="Banking Automation",fg="red",bg="powder blue",font=("arial",55,"bold","underline"))
lbl_title.place(relx=.25,rely=.0)

img=Image.open("download.jpg").resize((300,90))
imgtk=ImageTk.PhotoImage(img,master=win)

lbl_logo=Label(win,image=imgtk)
lbl_logo.place(x=0,y=0)

def login_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)
    
    def newuser():
        frm.destroy()
        newuser_screen()
        
    def forgot():
        frm.destroy()
        forgotpass_screen()
        
    def reset():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()
        
    def login_db():
        acn=e_acn.get()
        pwd=e_pass.get()
        if (acn=="" or pwd==""):
            messagebox.showwarning("login","Please fill all fields")
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from accounts where account_no=? and account_password=?",(acn,pwd))
            global tup
            tup=cur.fetchone()
        
            if(tup==None):
                messagebox.showerror("login","invalid ACN or PASSWORD")
            else:
                frm.destroy()
                welcome_screen()
            
    lbl_acn=Label(frm,text="Account No",bg="pink",font=("arial",20,"bold"))
    lbl_acn.place(relx=.3,rely=.1)

    e_acn=Entry(frm,font=('arial',20,"bold"),bd=5)
    e_acn.place(relx=.45,rely=.1)
    e_acn.focus() #used to set pointer default location
    
    lbl_pass=Label(frm,text="Password",bg="pink",font=("arial",20,"bold"))
    lbl_pass.place(relx=.3,rely=.2)

    e_pass=Entry(frm,font=('arial',20,"bold"),bd=5,show="*")
    #here show is used to hide the passwrord. When user will write it will display *
    e_pass.place(relx=.45,rely=.2)
    
    btn_login=Button(frm,text="Login",command=login_db,font=("Arial",20,"bold"),bg="powder blue")
    btn_login.place(relx=.45,rely=.4)
    
    btn_reset=Button(frm,text="Reset",command=reset,font=("Arial",20,"bold"),bg="powder blue")
    btn_reset.place(relx=.55,rely=.4)
    
    btn_fp=Button(frm,text="Forgot Password",command=forgot,font=("Arial",20,"bold"),bg="powder blue")
    btn_fp.place(relx=.45,rely=.52)
    
    btn_nu=Button(frm,text="Open New Account",command=newuser,font=("Arial",20,"bold"),bg="powder blue")
    btn_nu.place(relx=.44,rely=.63)
    

def newuser_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)
    
    def back():
        frm.destroy()
        login_screen()
        
    def openacn_db():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        acn_type=cb_type.get()
        
        if (acn_type=="Saving"):
            bal=1000
        else:
            bal=10000
        opendate=str(datetime.now().date())
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("insert into accounts(account_name,account_password,account_email,account_mob,account_type,account_bal,account_opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,acn_type,bal,opendate))
        con.commit()
        con.close()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select max(account_no) from accounts ")
        tup=cur.fetchone()
        con.close()
        
        messagebox.showinfo("Success",f"Account opened with ACN :{tup[0]}")
        frm.destroy()
        login_screen()
        
    btn_back=Button(frm,text="Back",command=back,font=("Arial",20,"bold"),bg="powder blue")
    btn_back.place(relx=0,rely=0)
    
    lbl_name=Label(frm,text="Name",bg="pink",font=("arial",20,"bold"))
    lbl_name.place(relx=.3,rely=.2)
    
    e_name=Entry(frm,font=('arial',20,"bold"),bd=5)
    e_name.place(relx=.4,rely=.2)
    e_name.focus()    
    
    lbl_pass=Label(frm,text="Password",bg="pink",font=("arial",20,"bold"))
    lbl_pass.place(relx=.3,rely=.3)
    
    e_pass=Entry(frm,show="*",font=('arial',20,"bold"),bd=5)
    e_pass.place(relx=.4,rely=.3)
    
    lbl_mob=Label(frm,text="Mobile No",bg="pink",font=("arial",20,"bold"))
    lbl_mob.place(relx=.3,rely=.4)
    
    e_mob=Entry(frm,font=('arial',20,"bold"),bd=5)
    e_mob.place(relx=.4,rely=.4)
    
    lbl_email=Label(frm,text="Email Id",bg="pink",font=("arial",20,"bold"))
    lbl_email.place(relx=.3,rely=.5)
    
    e_email=Entry(frm,font=('arial',20,"bold"),bd=5)
    e_email.place(relx=.4,rely=.5)
    
    lbl_type=Label(frm,text="Account Type",bg="pink",font=("arial",20,"bold"))
    lbl_type.place(relx=.27,rely=.6)
    
    cb_type=Combobox(frm,values=['Savings','Current'],font=("arial",19,"bold"))
    cb_type.current(0)
    cb_type.place(relx=.4,rely=.6)
    
    btn_nu=Button(frm,text="Open",command=openacn_db,font=("Arial",20,"bold"),bg="powder blue")
    btn_nu.place(relx=.42,rely=.72)
    
    btn_nu=Button(frm,text="Reset",font=("Arial",20,"bold"),bg="powder blue")
    btn_nu.place(relx=.52,rely=.72)
    
def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)
    
    def back():
        frm.destroy()
        login_screen()
        
    def reset_pass():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()
        
    def get_db():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()
        
        if (acn=="" or email=="" or mob==""):
            messagebox.showwarning("Validation","Please fill all fields")
            return
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select account_password from accounts where account_no=? and account_email=? and account_mob=?",(acn,email,mob))
            tup=cur.fetchone()
            
            if (tup==None):
                messagebox.showerror("Forgot","Invalid Details")
            else:
                messagebox.showinfo("Forgot",f"Your password is: {tup[0]}")
            
    btn_back=Button(frm,text="Back",command=back,font=("Arial",20,"bold"),bg="powder blue")
    btn_back.place(relx=0,rely=0)
    
    lbl_acn=Label(frm,text="Account No",bg="pink",font=("arial",20,"bold"))
    lbl_acn.place(relx=.29,rely=.1)
    
    e_acn=Entry(frm,font=('arial',20,"bold"),bd=5)
    e_acn.place(relx=.4,rely=.1)
    e_acn.focus()    
    
    lbl_mob=Label(frm,text="Mobile No",bg="pink",font=("arial",20,"bold"))
    lbl_mob.place(relx=.3,rely=.2)
    
    e_mob=Entry(frm,font=('arial',20,"bold"),bd=5)
    e_mob.place(relx=.4,rely=.2)
    
    lbl_email=Label(frm,text="Email ID",bg="pink",font=("arial",20,"bold"))
    lbl_email.place(relx=.3,rely=.3)
    
    e_email=Entry(frm,font=('arial',20,"bold"),bd=5)
    e_email.place(relx=.4,rely=.3)
    
    btn_get=Button(frm,text="Get",command=get_db,font=("Arial",20,"bold"),bg="powder blue")
    btn_get.place(relx=.42,rely=.4)
    
    btn_nu=Button(frm,text="Reset",command=reset_pass,font=("Arial",20,"bold"),bg="powder blue")
    btn_nu.place(relx=.52,rely=.4)
    
def welcome_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.8)
    
    def logout():
        frm.destroy()
        login_screen()
        
    def checkbal():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=5,highlightcolor="brown")
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        lbl_page.configure(text="Check Balance Page")
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select account_name,account_bal,account_opendate from accounts where account_no=?",(tup[0],))
        row=cur.fetchone()
        
        lbl_acn=Label(ifrm,text=f"Account Number\t{tup[0]}",bg="white",font=("arial",15,"bold"),fg="red")
        lbl_acn.place(relx=.3,rely=.1)
        
        lbl_name=Label(ifrm,text=f"Account Holder\t{row[0]}",bg="white",font=("arial",15,"bold"),fg="red")
        lbl_name.place(relx=.3,rely=.3)
        
        lbl_bal=Label(ifrm,text=f"Available Balance\t{row[1]}",bg="white",font=("arial",15,"bold"),fg="red")
        lbl_bal.place(relx=.3,rely=.5)
        
        lbl_date=Label(ifrm,text=f"Acn Open Date\t{row[2]}",bg="white",font=("arial",15,"bold"),fg="red")
        lbl_date.place(relx=.3,rely=.7) 
        
    def deposit():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=5,highlightcolor="brown")
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        lbl_page.configure(text="Deposit Page")
        
        def deposit_db():
            amt=float(e_amt.get())
            acn=tup[0]
            txn_type="CR."
            dt=str(datetime.now())
            
            if(amt<0):
                messagebox.showerror("Deposit", "Amount cant be nagtive")
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(acn,))
                bal=cur.fetchone()[0]
                con.close()
            
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("insert into txn values(?,?,?,?,?)",(acn,amt,bal+amt,dt,txn_type))
                cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(amt,acn))
                con.commit()
                con.close()
                
                messagebox.showinfo("Deposit","Amount deposited")
        
        lbl_amt=Label(ifrm,text="Enter Amount to Deposit",bg="white",font=("arial",18,"bold"),fg="red")
        lbl_amt.place(relx=.15,rely=.25)
        
        e_amt=Entry(ifrm,font=('arial',20,"bold"),bd=5)
        e_amt.place(relx=.5,rely=.25)
        e_amt.focus()
        
        btn_deposit=Button(frm,text="Deposit",command=deposit_db,font=("Arial",20,"bold"),bg="powder blue")
        btn_deposit.place(relx=.5,rely=.5)
        
    def withdraw():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=5,highlightcolor="brown")
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        lbl_page.configure(text="Withdraw Page") 
        
        def withdraw_db():
            amt=float(e_amt.get())
            acn=tup[0]
            txn_type="DR."
            dt=str(datetime.now())
            
            if(amt<0):
                messagebox.showerror("Deposit", "Amount can't be nagtive")
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(acn,))
                bal=cur.fetchone()[0]
                con.close()
                
                if(bal>=amt):            
                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    cur.execute("insert into txn values(?,?,?,?,?)",(acn,amt,bal+amt,dt,txn_type))
                    cur.execute("update accounts set account_bal=account_bal-? where account_no=?",(amt,acn))
                    con.commit()
                    con.close()
                
                    messagebox.showinfo("Withdraw","Amount withdrawn")
                else:
                    messagebox.showwarning("Withdraw","Insufficient balance")
        
        lbl_amt=Label(ifrm,text="Enter Amount to Withdraw",bg="white",font=("arial",18,"bold"),fg="red")
        lbl_amt.place(relx=.14,rely=.25)
        
        e_amt=Entry(ifrm,font=('arial',20,"bold"),bd=5)
        e_amt.place(relx=.5,rely=.25)
        e_amt.focus()
        
        btn_withdraw=Button(frm,text="Withdraw",command=withdraw_db,font=("Arial",20,"bold"),bg="powder blue")
        btn_withdraw.place(relx=.5,rely=.5)
        
    def transfer():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=5,highlightcolor="brown")
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        lbl_page.configure(text="Transfer Page") 
        
        
        def transfer_db():
            t_acn=e_to.get()
            amt=float(e_amt.get())
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from accounts where account_no=?",(t_acn,))
            row=cur.fetchone()
            con.close()
            
            if (row==None):
                messagebox.showerror("Transfer","To account doesn't exists")
            else:
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(tup[0],))
                bal=cur.fetchone()[0]
                con.close()
                
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(t_acn,))
                t_bal=cur.fetchone()[0]
                con.close()
                
                if(bal>=amt):
                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    dt=str(datetime.now())
                    cur.execute("update accounts set account_bal=account_bal-? where account_no=?",(amt,tup[0]))
                    cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(amt,tup[0]))
                    cur.execute("insert into txn values(?,?,?,?,?)",(tup[0],amt,bal-amt,dt,"DR."))
                    cur.execute("insert into txn values(?,?,?,?,?)",(t_acn,amt,bal+amt,dt,"CR."))
                    con.commit()
                    con.close()
                    
                    messagebox.showinfo("Transfer","Txn Done")
                    
                else:
                    messagebox.showwarning("Transfer","Insufficient Balance")
        
        lbl_to=Label(ifrm,text="Enter Account Number",bg="white",font=("arial",18,"bold"),fg="red")
        lbl_to.place(relx=.20,rely=.2)
        
        e_to=Entry(ifrm,font=('arial',20,"bold"),bd=5)
        e_to.place(relx=.5,rely=.2)
        e_to.focus()
        
        lbl_amt=Label(ifrm,text="Enter Amount",bg="white",font=("arial",18,"bold"),fg="red")
        lbl_amt.place(relx=.20,rely=.4)
        
        e_amt=Entry(ifrm,font=('arial',20,"bold"),bd=5)
        e_amt.place(relx=.5,rely=.4)
        
        
        btn_deposit=Button(frm,text="Transfer",command=transfer_db,font=("Arial",20,"bold"),bg="powder blue")
        btn_deposit.place(relx=.5,rely=.6)
        
        
    def update():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=5,highlightcolor="brown")
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        lbl_page.configure(text="Update Profile Page")
        
        def update_profile():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mob.get()
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("update accounts set account_name=?,account_password=?,account_email=?,account_mob=? where account_no=?",(name,pwd,email,mob,tup[0]))
            con.commit()
            con.close()
            messagebox.showinfo("Update","Info updated successfully")
            
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select * from accounts where account_no=?",(tup[0],))
        row=cur.fetchone()
        con.close()
        
        lbl_name=Label(ifrm,text="Name",bg="white",font=("arial",15,"bold"),fg="green")
        lbl_name.place(relx=.05,rely=.2)
        
        e_name=Entry(ifrm,font=('arial',15,"bold"),bd=5)
        e_name.place(relx=.15,rely=.2)
        e_name.insert(0,row[1])
        e_name.focus()
        
        lbl_pass=Label(ifrm,text="Pass",bg="white",font=("arial",15,"bold"),fg="green")
        lbl_pass.place(relx=.53,rely=.2)
        
        e_pass=Entry(ifrm,font=('arial',15,"bold"),bd=5)
        e_pass.place(relx=.62,rely=.2)
        e_pass.insert(0,row[2])
        
        lbl_email=Label(ifrm,text="Email",bg="white",font=("arial",15,"bold"),fg="green")
        lbl_email.place(relx=.05,rely=.4)
        
        e_email=Entry(ifrm,font=('arial',15,"bold"),bd=5)
        e_email.place(relx=.15,rely=.4)
        e_email.insert(0,row[3])
        
        lbl_mob=Label(ifrm,text="Mobile",bg="white",font=("arial",15,"bold"),fg="green")
        lbl_mob.place(relx=.53,rely=.4)
        
        e_mob=Entry(ifrm,font=('arial',15,"bold"),bd=5)
        e_mob.place(relx=.62,rely=.4)
        e_mob.insert(0,row[4])
        
        btn_update=Button(frm,text="Update",command=update_profile,font=("Arial",20,"bold"),bg="powder blue")
        btn_update.place(relx=.5,rely=.6)
        
    def txn():
        ifrm=Frame(frm,highlightbackground="brown",highlightthickness=5,highlightcolor="brown")
        ifrm.configure(bg="white")
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        
        lbl_page.configure(text="Transaction History Page") 
    
        tv=Treeview(ifrm)
        tv.place(x=0,y=0,relheight=1,relwidth=1)
        
        style=Style()
        style.configure("Treeview.Heading",font=('arial',10,"bold"),foreground="brown")
        
        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(relx=.98,y=0,relheight=1)
        
        sb=Scrollbar(ifrm,orient='horizontal',command=tv.xview)
        sb.pack(side=BOTTOM,fill=Y)
        
        tv['columns']=('Txn date','Txn amount','Txn type','Updated bal')
        
        tv.column('Txn date',width=150,anchor='c')
        tv.column('Txn amount',width=100,anchor='c')
        tv.column('Txn type',width=100,anchor='c')
        tv.column('Updated bal',width=100,anchor='c')
        
        tv.heading('Txn date',text="Txn date")
        tv.heading('Txn amount',text='Txn amount')
        tv.heading('Txn type',text='Txn type')
        tv.heading('Updated bal',text='Updated bal')
        
        tv['show']='headings'
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select txn_date,txn_amt,txn_type,txn_update_bal from txn where txn_account_no=?",(tup[0],))
        
        for row in cur:
            tv.insert("","end",values=(row[0],row[1],row[2],row[3]))
    
    btn_back=Button(frm,text="logout",command=logout,font=("Arial",20,"bold"),bg="powder blue")
    btn_back.place(relx=.9,rely=.01)
    
    lbl_wel=Label(frm,text=f"Welcome,{tup[1]}",bg="pink",font=("arial",20,"bold"),fg="green")
    lbl_wel.place(relx=0,rely=0)
    
    lbl_page=Label(frm,text="This is Home Page",bg="pink",font=("arial",20,"bold","underline"),fg="blue")
    lbl_page.place(relx=.4,rely=0)
    
    btn_checkbal=Button(frm,text="Check Balance",command=checkbal,width=12,font=("Arial",20,"bold"),bg="powder blue")
    btn_checkbal.place(relx=.0,rely=.1)
    
    btn_deposit=Button(frm,text="Deposit",command=deposit,width=12,font=("Arial",20,"bold"),bg="powder blue")
    btn_deposit.place(relx=.0,rely=.25)
    
    btn_withdraw=Button(frm,text="Withdraw",command=withdraw,width=12,font=("Arial",20,"bold"),bg="powder blue")
    btn_withdraw.place(relx=.0,rely=.4)
    
    btn_transfer=Button(frm,text="Transfer",command=transfer,width=12,font=("Arial",20,"bold"),bg="powder blue")
    btn_transfer.place(relx=.0,rely=.55)
    
    btn_update=Button(frm,text="Update Profile",command=update,width=12,font=("Arial",20,"bold"),bg="powder blue")
    btn_update.place(relx=.0,rely=.7)
    
    btn_txnhist=Button(frm,text="Trxn History",command=txn,width=12,font=("Arial",20,"bold"),bg="powder blue")
    btn_txnhist.place(relx=.0,rely=.85)
    
login_screen()
win.mainloop()


# In[ ]:





# In[ ]:




