#Create a contact management system using sqlite3 and python using user define function.
import sqlite3 as sq
def Connect():
    con=sq.connect("c:\\sqlite3\\contactmgmt.db")
    cur=con.cursor()
    con.commit()


# Create table contact(fname,lname,contact,email,city).Perform following operation on it.
def createTable():
    cur=con.cursor()
    cur.execute("CREATE TABLE CONTACT(fname text, lname text, contact numeric, email text, city text);")
    con.commit()

# log table create 
def createLog():
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS CONTACT_log
        (
        fname text,
        lname text,
        contact integer,
        datetime text,
        operation_performed text
        );""")             
    con.commit()

# creating trigger for log table 
def logTrigger():
    cur=con.cursor()
    cur.execute("""CREATE TRIGGER IF NOT EXISTS insertLogTrigger
                        after insert
                        on contact
                        BEGIN
                            INSERT INTO CONTACT_log
                            VALUES(new.fname,new.laname,new.contact,datetime('now','localtime'),'INSERT');
                        END;""")
    cur.execute("""CREATE TRIGGER IF NOT EXISTS deleteLogTrigger
                        after delete 
                        on contact
                        BEGIN
                            INSERT INTO CONTACT_log
                            VALUES(old.fname,old.lname,old.contact,datetime('now','localtime'),'DELETE');
                        END;""")
    cur.execute("""CREATE TRIGGER IF NOT EXISTS updateLogTrigger
                        after update
                        on contact
                        BEGIN
                            INSERT INTO CONTACT_log
                            VALUES(new.fname,new.lname,new.contact,datetime('now','localtime'),'After UPDATE');
                            INSERT INTO CONTACT_log
                            VALUES(old.fname,old.lname,old.contact,datetime('now','localtime'),'Before UPDATE');
                        END;""")
    con.commit()

# validate record 
def createTrigger():
    cur=con.cursor()
    con.execute("""CREATE TRIGGER validate_field 
    BEFORE INSERT
    ON CONTACT
    BEGIN
    SELECT
    CASE
    WHEN new.email NOT LIKE '%_@_%_.%' THEN
        RAISE(ABORT,'Please enter email in correct format')
    WHEN length(new.contact)<10 THEN
        RAISE(ABORT,'please enter valid contact no.')\
    END;
    END;""")           
    con.commit()

# insert record 
def insertRecords():
    cur=con.cursor()
    fname=input("\n\nEnter first name: ")
    lname=input("Enter last name: ")
    contact=int(input("Enter contact: "))
    email=input("Enter email:")
    city=input("Enter city: ")
    L=[fname,lname,contact,email,city]
    conn.execute("INSERT INTO CONTACT VALUES(?,?,?,?,?);",L)
    print('\n\nContact inserted sucessfully.\n')
    con.commit()

# updating record 
def updateContacts():
    cur=con.cursor()
    name_search=input("\n\nEnter their First name: ")
    new_contact=input("Enter New Contact No :")
    cur.execute(f"update CONTACT set contact='{new_contact}' where fname='{name_search}'")
    print("\n\nContact updated successfully.\n")
    con.commit()

#deleting record 
def deleteContacts():
    cur=con.cursor()
    name_search=input("\n\nEnter their First Name: ")
    cur.execute(f"delete from CONTACT where fname='{name_search}'")
    print("\n\nContact deleted successfully.\n")
    con.commit()

# searching record
def searchContacts():
    cur=con.cursor()
    name_search=input("\n\nEnter their First Name: ")
    cur.execute(f"select * from CONTACT where fname='{name_search}'")
    records=cur.fetchall()
    print('\n')
    print('Fname\tLaname\tContact\t\tEmail\t\t\tCity')
    for rows in records:
        print('{}\t{}\t{}\t{}\t{}'.format(rows[0],rows[1],rows[2],rows[3],rows[4]))     
    print('\n\n This are all available records \n')
    con.commit()

# def viewRecords():
    cur=con.cursor()
    cur.execute('select * from CONTACT')
    records=cur.fetchall()
    print('\n')
    print('Fname\tLaname\tContact\t\tEmail\t\t\tCity')
    for rows in records:
        print('{}\t{}\t{}\t{}\t{}'.format(rows[0],rows[1],rows[2],rows[3],rows[4]))       
    print('\n\nThis are all available records')
    con.commit()

# operation function 
def operationFunct():
    con=createConnect()
    tablecreate(con)
    createLog(con)
    createTrigger(con)
    logTrigger(con)
    choice=1
    while choice!=0:
        print('\n')
        print('1- Insert contacts')
        print('2- Update contacts')
        print('3- Delete contacts')
        print('4- Search contacts')
        print('5- View all records')
        print('0- Exit the program')
        choice=int(input('\nEnter your choice: '))     
        if choice==1:
            insertRecords(con)      
        elif choice==2:
            updateContacts(con)     
        elif choice==3:
            deleteContacts(con)     
        elif choice==4:
            searchContacts(con)     
        elif choice==5:
            viewRecords(con)       
    con.close()
      
