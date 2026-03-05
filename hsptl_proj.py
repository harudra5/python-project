# Import necessary modules
import json  # For reading and writing data in JSON format
import os    # For checking file existence and file operations
from datetime import datetime  # For handling dates

# -----------------------------
# Base class
# -----------------------------
class Person:
    # Constructor to initialize name and age
    def __init__(self, name: str, age: int):
        self.name = name  # store name
        self.age = age    # store age

    # Method to return basic information
    def basic_info(self):
        return f"Name: {self.name}, age: {self.age}"


# -----------------------------
# Patient class (Inheritance + Encapsulation)
# -----------------------------
class Patient(Person):
    def __init__(self, patient_id: int, name: str, age: int, gender: str):
        super().__init__(name, age)  # Call parent constructor (Person)
        self.__patient_id = patient_id  # Private attribute for patient ID
        self.gender = gender            # Gender is public

    # Getter method for private patient ID
    def get_id(self):
        return self.__patient_id

    # Convert patient object to dictionary (for JSON storage)
    def to_dict(self):
        return {
            "id": self.__patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }


# -----------------------------
# Doctor class
# -----------------------------
class Doctor(Person):
    def __init__(self, doctor_id: int, name: str, age: int, specialization: str):
        super().__init__(name, age)  # Inherit name and age from Person
        self.doctor_id = doctor_id    # Unique doctor ID
        self.specialization = specialization  # Doctor specialization

    # Getter method for doctor ID
    def get_id(self):
        return self.doctor_id

    # Convert doctor object to dictionary
    def to_dict(self):
        return {
            "id": self.doctor_id,
            "name": self.name,
            "age": self.age,
            "specialization": self.specialization
        }


# -----------------------------
# Appointment class (Composition)
# -----------------------------
class Appointment:
    # Constructor with patient ID, doctor ID, and appointment date
    def __init__(self, patient_id: int, doctor_id: int, date: str):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date

    # Convert appointment object to dictionary
    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date
        }


# -----------------------------
# Billing class
# -----------------------------
class Bill:
    CONSULTATION_FEE = 500         # Fixed consultation fee
    ROOM_CHARGE_PER_DAY = 2000     # Fixed room charge per day

    # Constructor with patient ID and number of days admitted
    def __init__(self, patient_id: int, days_admitted: int):
        self.patient_id = patient_id
        self.days_admitted = days_admitted

    # Calculate total bill
    def calculate_total_bill(self):
        return self.CONSULTATION_FEE + (self.days_admitted * self.ROOM_CHARGE_PER_DAY)

    # Generate bill dictionary
    def generate_bill(self):
        return {
            "patient_id": self.patient_id,
            "days_admitted": self.days_admitted,
            "total_bill": self.calculate_total_bill()
        }


# -----------------------------
# Hospital Management System
# -----------------------------
class Hospital:
    def __init__(self):
        self.file_name = "hospital_data.json"  # JSON file to store data
        self.patients = []       # List to store patients
        self.doctors = []        # List to store doctors
        self.appointments = []   # List to store appointments
        self.bills = []          # List to store bills
        self.load_data()         # Load existing data from file (if exists)

    # -----------------------------
    # File Handling Methods
    # -----------------------------
    def load_data(self):
        # Check if the JSON file exists
        if os.path.exists(self.file_name):
            # Open the file and read JSON data
            with open(self.file_name, "r") as file:
                data = json.load(file)
                # Load each section into memory (patients, doctors, appointments, bills)
                self.patients = data.get("patients", [])
                self.doctors = data.get("doctors", [])
                self.appointments = data.get("appointments", [])
                self.bills = data.get("bills", [])

    def save_data(self):
        # Prepare dictionary to save all data
        data = {
            "patients": self.patients,
            "doctors": self.doctors,
            "appointments": self.appointments,
            "bills": self.bills,
        }
        # Write data to JSON file
        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    # -----------------------------
    # Validation Methods
    # -----------------------------
    def validate_age(self):
        # Ensure age is a positive integer
        while True:
            try:
                age = int(input("Enter age: "))
                if age <= 0:
                    raise ValueError
                return age
            except ValueError:
                print("Invalid age. Enter positive number.")

    def validate_date(self):
        # Ensure date is in correct YYYY-MM-DD format
        while True:
            date = input("Enter appointment date (YYYY-MM-DD): ")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                return date
            except ValueError:
                print("Invalid date format.")

    # -----------------------------
    # Patient Methods
    # -----------------------------
    def add_patient(self):
        name = input("Enter patient name: ")  # Input patient name
        age = self.validate_age()             # Input and validate age
        gender = input("Enter gender: ")      # Input gender

        patient_id = len(self.patients) + 1   # Generate patient ID
        patient = Patient(patient_id, name, age, gender)  # Create Patient object

        self.patients.append(patient.to_dict())  # Add patient to list
        self.save_data()                         # Save to file
        print("Patient added successfully!")     # Confirmation message

    def view_patients(self):
        if not self.patients:
            print("No patients found.")          # No patients message
            return
        # Print all patients
        for p in self.patients:
            print(p)

    # -----------------------------
    # Doctor Methods
    # -----------------------------
    def add_doctor(self):
        name = input("Enter doctor name: ")     # Input doctor name
        age = self.validate_age()               # Input and validate age
        specialization = input("Enter specialization: ")  # Input specialization

        doctor_id = len(self.doctors) + 1      # Generate doctor ID
        doctor = Doctor(doctor_id, name, age, specialization)  # Create Doctor object

        self.doctors.append(doctor.to_dict())  # Add doctor to list
        self.save_data()                       # Save to file
        print("Doctor added successfully!")    # Confirmation

    def view_doctors(self):
        if not self.doctors:
            print("No doctors found.")         # No doctors message
            return
        # Print all doctors
        for d in self.doctors:
            print(d)

    # -----------------------------
    # Appointment Methods
    # -----------------------------
    def book_appointment(self):
        if not self.patients or not self.doctors:
            print("Add patient and doctor first.")  # Cannot book without patients or doctors
            return

        try:
            patient_id = int(input("Enter patient ID: "))  # Input patient ID
            doctor_id = int(input("Enter doctor ID: "))    # Input doctor ID

            # Check if patient ID exists
            if not any(p["id"] == patient_id for p in self.patients):
                print("Invalid patient ID.")
                return

            # Check if doctor ID exists
            if not any(d["id"] == doctor_id for d in self.doctors):
                print("Invalid doctor ID.")
                return

            date = self.validate_date()                       # Input and validate date
            appointment = Appointment(patient_id, doctor_id, date)  # Create appointment object

            self.appointments.append(appointment.to_dict())   # Add appointment to list
            self.save_data()                                  # Save to file
            print("Appointment booked successfully!")        # Confirmation

        except ValueError:
            print("Invalid input.")  # If user enters invalid number

    def view_appointments(self):
        if not self.appointments:
            print("No appointments found.")  # No appointments message
            return
        # Print all appointments
        for a in self.appointments:
            print(a)

    # -----------------------------
    # Billing Methods
    # -----------------------------
    def generate_bill(self):
        try:
            patient_id = int(input("Enter patient Id: "))  # Input patient ID
            days = int(input("Enter number of days admitted: "))  # Input days

            # Check if patient exists
            if not any(p["id"] == patient_id for p in self.patients):
                print("Invalid patient ID.")
                return

            bill = Bill(patient_id, days)          # Create Bill object
            bill_data = bill.generate_bill()       # Generate bill dictionary

            self.bills.append(bill_data)           # Add to bills list
            self.save_data()                       # Save to file

            # Print bill details
            print("\n======= BILL DETAILS ======")
            print("Patient ID:", bill_data["patient_id"])
            print("Days admitted:", bill_data["days_admitted"])
            print("Total Amount:", bill_data["total_bill"])

        except ValueError:
            print("Invalid Input.")  # If input is not valid number

    def view_bill(self):
        if not self.bills:
            print("No bills found.")  # No bills message
            return
        # Print all bills
        for b in self.bills:
            print(b)


# -----------------------------
# Main Menu
# -----------------------------
def main():
    hospital = Hospital()  # Create hospital management system object

    while True:
        # Display menu
        print("\n====== Hospital Management System ====")
        print("1 Add Patient")
        print("2 view Patients")
        print("3 Add Doctor")
        print("4 view Doctors")
        print("5 Book Appointment")
        print("6 View Appointments")
        print("7 Generate Bill")
        print("8 View Bills")
        print("9 Exit")

        choice = input("Enter your choice: ")  # Input menu choice

        # Handle menu choices
        if choice == "1":
            hospital.add_patient()
        elif choice == "2":
            hospital.view_patients()
        elif choice == "3":
            hospital.add_doctor()
        elif choice == "4":
            hospital.view_doctors()
        elif choice == "5":
            hospital.book_appointment()
        elif choice == "6":
            hospital.view_appointments()
        elif choice == "7":
            hospital.generate_bill()
        elif choice == "8":
            hospital.view_bill()
        elif choice == "9":
            print("Exiting system...")  # Exit message
            break
        else:
            print("Invalid choice. Try again.")  # Invalid input message


# Run the program
if __name__ == "__main__":
    main()