import sqlite3
from datetime import datetime
import streamlit as st

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("rehabilitation.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):

        # Clients
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            addiction TEXT,
            admission_date TEXT,
            completed_sessions INTEGER DEFAULT 0,
            total_sessions INTEGER
        )
        """)

        # Therapists
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS therapists(
            therapist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            specialization TEXT,
            phone TEXT
        )
        """)

        # Therapy Appointments
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments(
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            therapist_id INTEGER,
            visit_date TEXT,
            visit_time TEXT,
            status TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(client_id),
            FOREIGN KEY(therapist_id) REFERENCES therapists(therapist_id)
        )
        """)

        self.conn.commit()


class Client(Database):

    def add_client(self):

        name = input("Client Name: ")
        age = int(input("Age: "))
        gender = input("Gender: ")
        addiction = input("Addiction Type: ")
        admission = input("Admission Date (YYYY-MM-DD): ")
        sessions = int(input("Total Therapy Sessions: "))

        self.cursor.execute("""
        INSERT INTO clients(name,age,gender,addiction,admission_date,total_sessions)
        VALUES(?,?,?,?,?,?)
        """,
        (name,age,gender,addiction,admission,sessions))

        self.conn.commit()
        print("Client added successfully.")

    def delete_client(self):

        cid = int(input("Enter Client ID: "))

        self.cursor.execute("DELETE FROM appointments WHERE client_id=?", (cid,))
        self.cursor.execute("DELETE FROM clients WHERE client_id=?", (cid,))

        self.conn.commit()

        print("Client deleted.")

    def view_clients(self):

        self.cursor.execute("SELECT * FROM clients")

        rows = self.cursor.fetchall()

        print("\nCLIENT LIST\n")

        for row in rows:
            print(row)


class Therapist(Database):

    def add_therapist(self):

        name = input("Therapist Name: ")
        specialization = input("Specialization: ")
        phone = input("Phone: ")

        self.cursor.execute("""
        INSERT INTO therapists(name,specialization,phone)
        VALUES(?,?,?)
        """,(name,specialization,phone))

        self.conn.commit()

        print("Therapist added.")

    def view_therapists(self):

        self.cursor.execute("SELECT * FROM therapists")

        rows=self.cursor.fetchall()

        print("\nTHERAPISTS\n")

        for row in rows:
            print(row)


class Appointment(Database):

    def book_visit(self):

        client = int(input("Client ID: "))
        therapist = int(input("Therapist ID: "))
        date = input("Visit Date (YYYY-MM-DD): ")
        time = input("Visit Time (HH:MM): ")

        self.cursor.execute("""
        INSERT INTO appointments(client_id,therapist_id,visit_date,visit_time,status)
        VALUES(?,?,?,?,?)
        """,(client,therapist,date,time,"Booked"))

        self.conn.commit()

        print("Therapy Visit Booked.")

    def cancel_visit(self):

        appointment = int(input("Appointment ID: "))

        self.cursor.execute("""
        UPDATE appointments
        SET status='Cancelled'
        WHERE appointment_id=?
        """,(appointment,))

        self.conn.commit()

        print("Appointment Cancelled.")

    def view_visits(self):

        self.cursor.execute("""
        SELECT
        appointment_id,
        client_id,
        therapist_id,
        visit_date,
        visit_time,
        status
        FROM appointments
        """)

        rows=self.cursor.fetchall()

        print("\nAPPOINTMENTS\n")

        for row in rows:
            print(row)


class Progress(Database):

    def update_progress(self):

        cid = int(input("Client ID: "))
        completed = int(input("Completed Sessions: "))

        self.cursor.execute("""
        UPDATE clients
        SET completed_sessions=?
        WHERE client_id=?
        """,(completed,cid))

        self.conn.commit()

        print("Progress Updated.")

    def calculate_progress(self):

        cid=int(input("Client ID: "))

        self.cursor.execute("""
        SELECT
        name,
        completed_sessions,
        total_sessions
        FROM clients
        WHERE client_id=?
        """,(cid,))

        row=self.cursor.fetchone()

        if row:

            name=row[0]
            completed=row[1]
            total=row[2]

            progress=(completed/total)*100

            print("\nTreatment Progress")
            print("----------------------")
            print("Name:",name)
            print("Completed:",completed)
            print("Total:",total)
            print(f"Progress: {progress:.2f}%")

        else:
            print("Client not found.")


class RehabilitationSystem:

    def __init__(self):

        self.client=Client()
        self.therapist=Therapist()
        self.appointment=Appointment()
        self.progress=Progress()

    def menu(self):

        while True:

            print("""
==============================
 REHABILITATION MANAGEMENT
==============================

1.Add Client
2.Delete Client
3.View Clients

4.Add Therapist
5.View Therapists

6.Book Therapy Visit
7.Cancel Therapy Visit
8.View Therapy Visits

9.Update Treatment Progress
10.Calculate Progress

0.Exit
""")

            choice=input("Choice: ")

            if choice=="1":
                self.client.add_client()

            elif choice=="2":
                self.client.delete_client()

            elif choice=="3":
                self.client.view_clients()

            elif choice=="4":
                self.therapist.add_therapist()

            elif choice=="5":
                self.therapist.view_therapists()

            elif choice=="6":
                self.appointment.book_visit()

            elif choice=="7":
                self.appointment.cancel_visit()

            elif choice=="8":
                self.appointment.view_visits()

            elif choice=="9":
                self.progress.update_progress()

            elif choice=="10":
                self.progress.calculate_progress()

            elif choice=="0":
                print("Goodbye")
                break

            else:
                print("Invalid choice")


if __name__=="__main__":
    RehabilitationSystem().menu()