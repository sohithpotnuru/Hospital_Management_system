import heapq
from collections import deque, defaultdict
from datetime import datetime, timedelta
import uuid

class Patient:
    def __init__(self, patient_id, name, age, condition, priority=3):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.condition = condition
        self.priority = priority  # 1 = Critical, 2 = High, 3 = Medium, 4 = Low
        self.admission_time = datetime.now()
        self.medical_history = []
        self.assigned_doctor = None
        self.room_number = None
        self.status = "Waiting"  # Waiting, Admitted, Discharged
    
    def __lt__(self, other):
        # For priority queue - lower number = higher priority
        return self.priority < other.priority
    
    def add_medical_record(self, record):
        self.medical_history.append({
            'timestamp': datetime.now(),
            'record': record
        })
    
    def display_info(self):
        """Display patient information"""
        print(f"\n--- Patient Information ---")
        print(f"Patient ID: {self.patient_id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age} years")
        print(f"Medical Condition: {self.condition}")
        priority_text = {1: 'Critical', 2: 'High', 3: 'Medium', 4: 'Low'}
        print(f"Priority Level: {priority_text.get(self.priority, 'Unknown')} ({self.priority})")
        print(f"Current Status: {self.status}")
        print(f"Assigned Room: {self.room_number if self.room_number else 'Not assigned yet'}")
        print(f"Assigned Doctor: {self.assigned_doctor if self.assigned_doctor else 'Not assigned yet'}")
        if self.admission_time:
            print(f"Registration Time: {self.admission_time.strftime('%Y-%m-%d %H:%M:%S')}")

class Doctor:
    def __init__(self, doctor_id, name, specialization, max_patients=10):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.max_patients = max_patients
        self.current_patients = []
        self.schedule = {}  # date -> list of appointments
        self.availability = True
    
    def assign_patient(self, patient):
        if len(self.current_patients) < self.max_patients:
            self.current_patients.append(patient.patient_id)
            patient.assigned_doctor = self.doctor_id
            return True
        return False
    
    def discharge_patient(self, patient_id):
        if patient_id in self.current_patients:
            self.current_patients.remove(patient_id)
            return True
        return False
    
    def display_info(self):
        """Display doctor information"""
        print(f"\n--- Doctor Information ---")
        print(f"Doctor ID: {self.doctor_id}")
        print(f"Name: Dr. {self.name}")
        print(f"Specialization: {self.specialization}")
        print(f"Current Patient Load: {len(self.current_patients)} out of {self.max_patients}")
        availability_status = "Available" if len(self.current_patients) < self.max_patients else "Fully Booked"
        print(f"Availability Status: {availability_status}")

class Room:
    def __init__(self, room_number, room_type, capacity=1):
        self.room_number = room_number
        self.room_type = room_type  # ICU, General, Private, Emergency
        self.capacity = capacity
        self.occupied_beds = 0
        self.patients = []
        self.is_available = True
    
    def admit_patient(self, patient_id):
        if self.occupied_beds < self.capacity:
            self.patients.append(patient_id)
            self.occupied_beds += 1
            if self.occupied_beds == self.capacity:
                self.is_available = False
            return True
        return False
    
    def discharge_patient(self, patient_id):
        if patient_id in self.patients:
            self.patients.remove(patient_id)
            self.occupied_beds -= 1
            self.is_available = True
            return True
        return False
    
    def display_info(self):
        """Display room information"""
        print(f"\n--- Room Information ---")
        print(f"Room Number: {self.room_number}")
        print(f"Room Type: {self.room_type}")
        print(f"Total Capacity: {self.capacity} bed(s)")
        print(f"Currently Occupied: {self.occupied_beds} bed(s)")
        print(f"Available Space: {self.capacity - self.occupied_beds} bed(s)")
        status = "Available" if self.is_available else "Full"
        print(f"Room Status: {status}")

class Appointment:
    def __init__(self, patient_id, doctor_id, appointment_time, appointment_type="Consultation"):
        self.appointment_id = str(uuid.uuid4())[:8]  # Shorter ID for display
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_time = appointment_time
        self.appointment_type = appointment_type
        self.status = "Scheduled"  # Scheduled, Completed, Cancelled
        self.notes = ""
    
    def display_info(self):
        """Display appointment information"""
        print(f"\n--- Appointment Details ---")
        print(f"Appointment ID: {self.appointment_id}")
        print(f"Patient ID: {self.patient_id}")
        print(f"Doctor ID: {self.doctor_id}")
        print(f"Scheduled Date: {self.appointment_time.strftime('%A, %B %d, %Y')}")
        print(f"Scheduled Time: {self.appointment_time.strftime('%I:%M %p')}")
        print(f"Appointment Type: {self.appointment_type}")
        print(f"Current Status: {self.status}")

class BinarySearchTree:
    """BST for efficient patient search and retrieval"""
    class TreeNode:
        def __init__(self, patient):
            self.patient = patient
            self.left = None
            self.right = None
    
    def __init__(self):
        self.root = None
    
    def insert(self, patient):
        if not self.root:
            self.root = self.TreeNode(patient)
        else:
            self._insert_recursive(self.root, patient)
    
    def _insert_recursive(self, node, patient):
        if patient.patient_id < node.patient.patient_id:
            if not node.left:
                node.left = self.TreeNode(patient)
            else:
                self._insert_recursive(node.left, patient)
        else:
            if not node.right:
                node.right = self.TreeNode(patient)
            else:
                self._insert_recursive(node.right, patient)
    
    def search(self, patient_id):
        return self._search_recursive(self.root, patient_id)
    
    def _search_recursive(self, node, patient_id):
        if not node:
            return None
        if patient_id == node.patient.patient_id:
            return node.patient
        elif patient_id < node.patient.patient_id:
            return self._search_recursive(node.left, patient_id)
        else:
            return self._search_recursive(node.right, patient_id)
    
    def inorder_traversal(self):
        patients = []
        self._inorder_recursive(self.root, patients)
        return patients
    
    def _inorder_recursive(self, node, patients):
        if node:
            self._inorder_recursive(node.left, patients)
            patients.append(node.patient)
            self._inorder_recursive(node.right, patients)

class HospitalManagementSystem:
    def __init__(self):
        
        self.emergency_queue = []
        self.regular_queue = deque()
        self.patients = {}  
        self.doctors = {}   
        self.rooms = {}     
        self.appointments = {} 
        self.patient_bst = BinarySearchTree()
        self.department_graph = defaultdict(list)
        self.operation_history = []
        
        self._initialize_hospital()
    
    def _initialize_hospital(self):
        
        print("Initializing hospital system with default staff and facilities...")
        
        # Add some doctors
        doctors_data = [
            ("D001", "Dr. Sarah Smith", "Cardiology"),
            ("D002", "Dr. Michael Johnson", "Neurology"),
            ("D003", "Dr. Emily Williams", "Emergency Medicine"),
            ("D004", "Dr. David Brown", "Orthopedics"),
            ("D005", "Dr. Lisa Davis", "Pediatrics")
        ]
        
        for doctor_id, name, specialization in doctors_data:
            doctor = Doctor(doctor_id, name, specialization)
            self.doctors[doctor_id] = doctor
        
        # Add some rooms
        rooms_data = [
            ("R001", "ICU"), ("R002", "ICU"), ("R003", "General"),
            ("R004", "General"), ("R005", "Private"), ("R006", "Emergency")
        ]
        
        for room_number, room_type in rooms_data:
            room = Room(room_number, room_type)
            self.rooms[room_number] = room
        
        # Set up department connections
        self.department_graph["Emergency"].extend(["ICU", "General"])
        self.department_graph["ICU"].extend(["General", "Cardiology"])
        self.department_graph["General"].extend(["Discharge"])
        
        print("Hospital system initialized successfully!")
        print(f"Available: {len(self.doctors)} doctors, {len(self.rooms)} rooms")
    
    def get_user_input_for_patient(self):
        """Get patient information from user"""
        print("\n========== New Patient Registration ==========")
        
        # Generate patient ID
        patient_count = len(self.patients) + 1
        patient_id = f"P{patient_count:03d}"
        
        # Get patient details
        print(f"Generated Patient ID: {patient_id}")
        
        while True:
            name = input("\nPlease enter patient's full name: ").strip()
            if name and len(name) >= 2:
                break
            print("Error: Patient name must be at least 2 characters long!")
        
        while True:
            try:
                age = int(input("Please enter patient's age: "))
                if 0 < age <= 120:
                    break
                else:
                    print("Error: Age must be between 1 and 120 years!")
            except ValueError:
                print("Error: Please enter a valid number for age!")
        
        while True:
            condition = input("Please describe patient's condition or symptoms: ").strip()
            if condition and len(condition) >= 3:
                break
            print("Error: Condition description must be at least 3 characters long!")
        
        print("\n--- Priority Level Guidelines ---")
        print("1. Critical    - Life-threatening emergency (heart attack, severe trauma)")
        print("2. High        - Urgent care needed within hours (severe pain, high fever)")
        print("3. Medium      - Standard care needed today (routine illness)")
        print("4. Low         - Minor issues (check-ups, minor complaints)")
        
        while True:
            try:
                priority = int(input("\nSelect priority level (1-4): "))
                if 1 <= priority <= 4:
                    break
                else:
                    print("Error: Priority must be between 1 and 4!")
            except ValueError:
                print("Error: Please enter a valid number for priority level!")
        
        return patient_id, name, age, condition, priority
    
    def register_patient_interactive(self):
        """Register a new patient with user input"""
        patient_id, name, age, condition, priority = self.get_user_input_for_patient()
        
        patient = Patient(patient_id, name, age, condition, priority)
        self.patients[patient_id] = patient
        self.patient_bst.insert(patient)
        if priority <= 2:  
            heapq.heappush(self.emergency_queue, patient)
            print(f"\nPatient added to EMERGENCY QUEUE due to {('Critical' if priority == 1 else 'High')} priority")
        else:
            self.regular_queue.append(patient)
            print(f"\nPatient added to REGULAR QUEUE")
        self.operation_history.append(('register', patient_id))
        
        print(f"\nSUCCESS: Patient {name} has been registered successfully!")
        print(f"Patient ID: {patient_id}")
        patient.display_info()
        return patient
    
    def add_doctor_interactive(self):
        """Add a doctor with user input"""
        print("\n========== Add New Doctor to Staff ==========")
        
        # Generate doctor ID
        doctor_count = len(self.doctors) + 1
        doctor_id = f"D{doctor_count:03d}"
        print(f"Generated Doctor ID: {doctor_id}")
        
        while True:
            name = input("\nEnter doctor's full name: ").strip()
            if name and len(name) >= 2:
                break
            print("Error: Doctor name must be at least 2 characters long!")
        
        print("\nCommon Specializations:")
        print("- Cardiology (Heart specialist)")
        print("- Neurology (Brain and nervous system)")
        print("- Emergency Medicine (Emergency care)")
        print("- Orthopedics (Bones and joints)")
        print("- Pediatrics (Children's medicine)")
        print("- General Medicine")
        
        while True:
            specialization = input("\nEnter doctor's specialization: ").strip()
            if specialization and len(specialization) >= 3:
                break
            print("Error: Specialization must be at least 3 characters long!")
        
        while True:
            try:
                max_patients_input = input("\nEnter maximum patient capacity (press Enter for default 10): ").strip()
                if max_patients_input == "":
                    max_patients = 10
                else:
                    max_patients = int(max_patients_input)
                
                if 1 <= max_patients <= 50:
                    break
                else:
                    print("Error: Patient capacity must be between 1 and 50!")
            except ValueError:
                print("Error: Please enter a valid number!")
        
        doctor = Doctor(doctor_id, name, specialization, max_patients)
        self.doctors[doctor_id] = doctor
        
        print(f"\nSUCCESS: Dr. {name} has been added to the hospital staff!")
        doctor.display_info()
        return doctor
    
    def add_room_interactive(self):
        """Add a room with user input"""
        print("\n========== Add New Room to Hospital ==========")
        
        # Generate room number
        room_count = len(self.rooms) + 1
        room_number = f"R{room_count:03d}"
        print(f"Generated Room Number: {room_number}")
        
        print("\nAvailable Room Types:")
        print("1. ICU (Intensive Care Unit) - For critical patients")
        print("2. General Ward - For standard patient care")
        print("3. Private Room - For patients preferring privacy")
        print("4. Emergency Room - For emergency treatments")
        
        room_types = ["ICU", "General", "Private", "Emergency"]
        while True:
            try:
                choice = int(input("\nSelect room type (1-4): "))
                if 1 <= choice <= 4:
                    room_type = room_types[choice-1]
                    break
                else:
                    print("Error: Choice must be between 1 and 4!")
            except ValueError:
                print("Error: Please enter a valid number!")
        
        while True:
            try:
                capacity_input = input("\nEnter room capacity (press Enter for default 1 bed): ").strip()
                if capacity_input == "":
                    capacity = 1
                else:
                    capacity = int(capacity_input)
                
                if 1 <= capacity <= 10:
                    break
                else:
                    print("Error: Room capacity must be between 1 and 10 beds!")
            except ValueError:
                print("Error: Please enter a valid number!")
        
        room = Room(room_number, room_type, capacity)
        self.rooms[room_number] = room
        
        print(f"\nSUCCESS: Room {room_number} ({room_type}) has been added to the hospital!")
        room.display_info()
        return room
    
    def admit_next_patient(self):
        """Admit next patient using priority queue logic"""
        print("\n========== Processing Next Patient Admission ==========")
        
        patient = None
        queue_type = ""
        
        # Check emergency queue first (priority queue)
        if self.emergency_queue:
            patient = heapq.heappop(self.emergency_queue)
            queue_type = "Emergency"
        # Then check regular queue (FIFO)
        elif self.regular_queue:
            patient = self.regular_queue.popleft()
            queue_type = "Regular"
        
        if not patient:
            print("No patients are currently waiting for admission.")
            return None
        
        print(f"Processing patient from {queue_type} queue: {patient.name}")
        
        # Find available room
        available_room = self._find_available_room(patient.condition)
        if not available_room:
            print(f"\nERROR: No available rooms suitable for patient {patient.name}")
            print("Patient will be returned to the queue.")
            # Put patient back in queue
            if patient.priority <= 2:
                heapq.heappush(self.emergency_queue, patient)
            else:
                self.regular_queue.appendleft(patient)
            return None
        
        # Assign doctor using load balancing
        assigned_doctor = self._assign_doctor(patient)
        if not assigned_doctor:
            print(f"\nERROR: No available doctor for patient {patient.name}")
            print("All doctors are currently at maximum capacity.")
            return None
        
        # Admit patient
        available_room.admit_patient(patient.patient_id)
        patient.room_number = available_room.room_number
        patient.status = "Admitted"
        
        print(f"\nSUCCESS: Patient admission completed!")
        print(f"Patient Name: {patient.name}")
        print(f"Assigned Room: {available_room.room_number} ({available_room.room_type})")
        print(f"Assigned Doctor: {assigned_doctor.name} ({assigned_doctor.specialization})")
        print(f"Admission Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return patient
    
    def _find_available_room(self, condition):
        """Find available room based on patient condition using linear search"""
        # Priority: ICU for critical, then General, then Private
        room_priority = ["ICU", "Emergency", "General", "Private"]
        
        # Adjust priority based on condition keywords
        condition_lower = condition.lower()
        if any(keyword in condition_lower for keyword in ["critical", "emergency", "heart attack", "stroke", "trauma"]):
            room_priority = ["ICU", "Emergency", "General", "Private"]
        elif any(keyword in condition_lower for keyword in ["surgery", "operation", "serious"]):
            room_priority = ["ICU", "General", "Private", "Emergency"]
        
        for room_type in room_priority:
            for room in self.rooms.values():
                if room.room_type == room_type and room.is_available:
                    return room
        return None
    
    def _assign_doctor(self, patient):
        """Assign doctor using load balancing algorithm"""
        available_doctors = [doc for doc in self.doctors.values() 
                           if len(doc.current_patients) < doc.max_patients]
        
        if not available_doctors:
            return None
        
        # Find doctor with minimum current patients (load balancing)
        best_doctor = min(available_doctors, key=lambda doc: len(doc.current_patients))
        best_doctor.assign_patient(patient)
        
        return best_doctor
    
    def search_patient_interactive(self):
        """Search for a patient with user input"""
        print("\n========== Patient Search System ==========")
        
        if not self.patients:
            print("No patients are currently registered in the system.")
            return None
        
        patient_id = input("Enter Patient ID to search for: ").strip().upper()
        
        if not patient_id:
            print("Error: Patient ID cannot be empty!")
            return None
        
        print(f"Searching for patient with ID: {patient_id}...")
        
        # Search using BST
        patient = self.patient_bst.search(patient_id)
        
        if patient:
            print(f"\nPatient found in hospital database!")
            patient.display_info()
            
            # Show medical history if available
            if patient.medical_history:
                print(f"\n--- Medical History ---")
                for i, record in enumerate(patient.medical_history, 1):
                    print(f"{i}. {record['record']} (Date: {record['timestamp'].strftime('%Y-%m-%d %H:%M')})")
            else:
                print("\nNo medical history recorded yet.")
        else:
            print(f"\nPatient with ID '{patient_id}' was not found in the system.")
            print("Please check the Patient ID and try again.")
        
        return patient
    
    def discharge_patient_interactive(self):
        """Discharge patient with user input"""
        print("\n========== Patient Discharge System ==========")
        
        if not any(p.status == "Admitted" for p in self.patients.values()):
            print("No patients are currently admitted in the hospital.")
            return False
        
        # Show admitted patients
        print("\nCurrently Admitted Patients:")
        admitted_patients = [p for p in self.patients.values() if p.status == "Admitted"]
        for i, patient in enumerate(admitted_patients, 1):
            print(f"{i}. {patient.patient_id}: {patient.name} (Room: {patient.room_number})")
        
        patient_id = input("\nEnter Patient ID to discharge: ").strip().upper()
        
        if not patient_id:
            print("Error: Patient ID cannot be empty!")
            return False
        
        patient = self.patients.get(patient_id)
        if not patient:
            print(f"Error: Patient with ID '{patient_id}' not found in system.")
            return False
        
        if patient.status != "Admitted":
            print(f"Error: Patient {patient.name} is not currently admitted.")
            print(f"Current status: {patient.status}")
            return False
        
        # Confirm discharge
        print(f"\nPatient to be discharged:")
        print(f"Name: {patient.name}")
        print(f"Room: {patient.room_number}")
        print(f"Doctor: {patient.assigned_doctor}")
        
        confirm = input("\nAre you sure you want to discharge this patient? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("Discharge operation cancelled.")
            return False
        
        # Free up room
        if patient.room_number:
            room = self.rooms.get(patient.room_number)
            if room:
                room.discharge_patient(patient_id)
        
        # Free up doctor
        if patient.assigned_doctor:
            doctor = self.doctors.get(patient.assigned_doctor)
            if doctor:
                doctor.discharge_patient(patient_id)
        
        patient.status = "Discharged"
        old_room = patient.room_number
        old_doctor = patient.assigned_doctor
        patient.room_number = None
        patient.assigned_doctor = None
        
        # Record operation for undo functionality
        self.operation_history.append(('discharge', patient_id))
        
        print(f"\nSUCCESS: Patient {patient.name} has been discharged successfully!")
        print(f"Room {old_room} is now available for new patients.")
        print(f"Dr. {self.doctors[old_doctor].name} now has additional capacity.")
        print(f"Discharge Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
    
    def schedule_appointment_interactive(self):
        """Schedule appointment with user input"""
        print("\n========== Appointment Scheduling System ==========")
        
        if not self.patients:
            print("No patients are registered in the system yet.")
            return None
        
        # Show available patients
        print("\nRegistered Patients:")
        for i, (patient_id, patient) in enumerate(self.patients.items(), 1):
            print(f"{i}. {patient_id}: {patient.name} (Status: {patient.status})")
        
        # Get patient ID
        patient_id = input("\nEnter Patient ID for appointment: ").strip().upper()
        if patient_id not in self.patients:
            print(f"Error: Patient with ID '{patient_id}' not found.")
            return None
        
        # Display available doctors
        print(f"\nAvailable Doctors:")
        for i, (doc_id, doctor) in enumerate(self.doctors.items(), 1):
            availability = f"({len(doctor.current_patients)}/{doctor.max_patients} patients)"
            print(f"{i}. Dr. {doctor.name} - {doctor.specialization} {availability}")
        
        # Get doctor choice
        while True:
            try:
                choice = int(input(f"\nSelect doctor (1-{len(self.doctors)}): "))
                if 1 <= choice <= len(self.doctors):
                    doctor_id = list(self.doctors.keys())[choice-1]
                    break
                else:
                    print(f"Error: Choice must be between 1 and {len(self.doctors)}!")
            except ValueError:
                print("Error: Please enter a valid number!")
        
        # Get appointment date and time
        print(f"\nScheduling appointment for {self.patients[patient_id].name} with Dr. {self.doctors[doctor_id].name}")
        print("Enter appointment date and time:")
        
        while True:
            try:
                print("\nDate format: YYYY-MM-DD (example: 2024-12-25)")
                date_str = input("Enter appointment date: ").strip()
                
                print("Time format: HH:MM (24-hour format, example: 14:30)")
                time_str = input("Enter appointment time: ").strip()
                
                datetime_str = f"{date_str} {time_str}"
                appointment_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                
                if appointment_time < datetime.now():
                    print("Error: Cannot schedule appointment in the past!")
                    continue
                
                if appointment_time < datetime.now() + timedelta(hours=1):
                    print("Error: Appointment must be scheduled at least 1 hour in advance!")
                    continue
                
                break
            except ValueError:
                print("Error: Invalid date/time format! Please use YYYY-MM-DD HH:MM")
        
        # Get appointment type
        print("\nCommon Appointment Types:")
        print("- Consultation")
        print("- Follow-up")
        print("- Check-up")
        print("- Treatment")
        print("- Surgery")
        
        appointment_type = input("\nEnter appointment type (press Enter for 'Consultation'): ").strip()
        if not appointment_type:
            appointment_type = "Consultation"
        
        appointment = Appointment(patient_id, doctor_id, appointment_time, appointment_type)
        self.appointments[appointment.appointment_id] = appointment
        
        # Add to doctor's schedule
        doctor = self.doctors[doctor_id]
        date_str = appointment_time.strftime("%Y-%m-%d")
        if date_str not in doctor.schedule:
            doctor.schedule[date_str] = []
        doctor.schedule[date_str].append(appointment.appointment_id)
        
        print(f"\nSUCCESS: Appointment has been scheduled successfully!")
        appointment.display_info()
        
        return appointment
    
    def get_patient_queue_status(self):
        """Get current queue status"""
        emergency_count = len(self.emergency_queue)
        regular_count = len(self.regular_queue)
        total_waiting = emergency_count + regular_count
        
        print(f"\n========== Patient Queue Status ==========")
        print(f"Emergency Queue (High Priority): {emergency_count} patients")
        print(f"Regular Queue (Standard Priority): {regular_count} patients")
        print(f"Total Patients Waiting: {total_waiting}")
        
        if self.emergency_queue:
            next_emergency = self.emergency_queue[0]
            priority_text = "Critical" if next_emergency.priority == 1 else "High"
            print(f"\nNext Emergency Patient: {next_emergency.name}")
            print(f"  - Priority Level: {priority_text}")
            print(f"  - Condition: {next_emergency.condition}")
            print(f"  - Waiting Since: {next_emergency.admission_time.strftime('%H:%M:%S')}")
        
        if self.regular_queue:
            next_regular = self.regular_queue[0]
            print(f"\nNext Regular Patient: {next_regular.name}")
            print(f"  - Condition: {next_regular.condition}")
            print(f"  - Waiting Since: {next_regular.admission_time.strftime('%H:%M:%S')}")
        
        if total_waiting == 0:
            print("\nGood news: No patients are currently waiting for admission!")
        else:
            print(f"\nNote: Emergency patients are given priority over regular patients.")
    
    def get_hospital_statistics(self):
        """Generate hospital statistics using various data structures"""
        total_patients = len(self.patients)
        admitted_patients = sum(1 for p in self.patients.values() if p.status == "Admitted")
        discharged_patients = sum(1 for p in self.patients.values() if p.status == "Discharged")
        waiting_patients = len(self.emergency_queue) + len(self.regular_queue)
        
        total_rooms = len(self.rooms)
        occupied_rooms = sum(1 for r in self.rooms.values() if not r.is_available)
        available_rooms = total_rooms - occupied_rooms
        
        total_doctors = len(self.doctors)
        busy_doctors = sum(1 for d in self.doctors.values() if d.current_patients)
        available_doctors = total_doctors - busy_doctors
        
        scheduled_appointments = len([a for a in self.appointments.values() if a.status == "Scheduled"])
        
        print(f"\n========== Hospital Statistics Dashboard ==========")
        print(f"\nPatient Statistics:")
        print(f"  Total Patients Registered: {total_patients}")
        print(f"  Currently Admitted: {admitted_patients}")
        print(f"  Successfully Discharged: {discharged_patients}")
        print(f"  Waiting for Admission: {waiting_patients}")
        
        print(f"\nFacility Statistics:")
        print(f"  Total Rooms Available: {total_rooms}")
        print(f"  Rooms Currently Occupied: {occupied_rooms}")
        print(f"  Rooms Available for New Patients: {available_rooms}")
        
        print(f"\nStaff Statistics:")
        print(f"  Total Doctors on Staff: {total_doctors}")
        print(f"  Doctors Currently Treating Patients: {busy_doctors}")
        print(f"  Doctors Available for New Patients: {available_doctors}")
        
        print(f"\nAppointment Statistics:")
        print(f"  Total Appointments Scheduled: {len(self.appointments)}")
        print(f"  Upcoming Appointments: {scheduled_appointments}")
        
        # Calculate occupancy rates
        if total_rooms > 0:
            room_occupancy_rate = (occupied_rooms / total_rooms) * 100
            print(f"\nOccupancy Rates:")
            print(f"  Room Occupancy Rate: {room_occupancy_rate:.1f}%")
        
        if total_doctors > 0:
            doctor_utilization = (busy_doctors / total_doctors) * 100
            print(f"  Doctor Utilization Rate: {doctor_utilization:.1f}%")
    
    def view_all_patients(self):
        """View all patients in sorted order"""
        patients = self.patient_bst.inorder_traversal()
        
        if not patients:
            print("\nNo patients are currently registered in the system.")
            return
        
        print(f"\n========== All Registered Patients ({len(patients)} total) ==========")
        
        for i, patient in enumerate(patients, 1):
            print(f"\n{i}. Patient ID: {patient.patient_id}")
            print(f"   Name: {patient.name}")
            print(f"   Age: {patient.age} years")
            print(f"   Medical Condition: {patient.condition}")
            print(f"   Current Status: {patient.status}")
            
            if patient.status == "Admitted":
                print(f"   Assigned Room: {patient.room_number}")
                if patient.assigned_doctor and patient.assigned_doctor in self.doctors:
                    doctor = self.doctors[patient.assigned_doctor]
                    print(f"   Attending Doctor: Dr. {doctor.name} ({doctor.specialization})")
            
            priority_text = {1: 'Critical', 2: 'High', 3: 'Medium', 4: 'Low'}
            print(f"   Priority Level: {priority_text.get(patient.priority, 'Unknown')}")
            print(f"   Registration Date: {patient.admission_time.strftime('%Y-%m-%d %H:%M')}")
    
    def view_all_doctors(self):
        """View all doctors"""
        if not self.doctors:
            print("\nNo doctors are currently registered in the system.")
            return
        
        print(f"\n========== Medical Staff Directory ({len(self.doctors)} doctors) ==========")
        
        for i, doctor in enumerate(self.doctors.values(), 1):
            print(f"\n{i}. Doctor ID: {doctor.doctor_id}")
            print(f"   Name: Dr. {doctor.name}")
            print(f"   Specialization: {doctor.specialization}")
            print(f"   Patient Load: {len(doctor.current_patients)} out of {doctor.max_patients}")
            
            if len(doctor.current_patients) < doctor.max_patients:
                available_slots = doctor.max_patients - len(doctor.current_patients)
                print(f"   Status: Available ({available_slots} slots free)")
            else:
                print(f"   Status: Fully booked")
            
            if doctor.current_patients:
                print(f"   Currently treating patients: {', '.join(doctor.current_patients)}")
    
    def view_all_rooms(self):
        """View all rooms"""
        if not self.rooms:
            print("\nNo rooms are currently available in the system.")
            return
        
        print(f"\n========== Hospital Room Directory ({len(self.rooms)} rooms) ==========")
        
        # Group rooms by type for better organization
        room_types = {}
        for room in self.rooms.values():
            if room.room_type not in room_types:
                room_types[room.room_type] = []
            room_types[room.room_type].append(room)
        
        for room_type, rooms in room_types.items():
            print(f"\n--- {room_type} Rooms ---")
            for room in sorted(rooms, key=lambda x: x.room_number):
                print(f"  Room {room.room_number}:")
                print(f"    Capacity: {room.capacity} bed(s)")
                print(f"    Currently Occupied: {room.occupied_beds} bed(s)")
                print(f"    Available Space: {room.capacity - room.occupied_beds} bed(s)")
                status = "Available" if room.is_available else "Full"
                print(f"    Status: {status}")
                
                if room.patients:
                    print(f"    Current Patients: {', '.join(room.patients)}")
    
    def view_all_appointments(self):
        """View all appointments"""
        if not self.appointments:
            print("\nNo appointments are currently scheduled.")
            return
        
        print(f"\n========== Appointment Schedule ({len(self.appointments)} total) ==========")
        
        # Sort appointments by date and time
        sorted_appointments = sorted(
            self.appointments.values(), 
            key=lambda x: x.appointment_time
        )
        
        for i, appointment in enumerate(sorted_appointments, 1):
            print(f"\n{i}. Appointment ID: {appointment.appointment_id}")
            
            # Get patient and doctor names
            patient = self.patients.get(appointment.patient_id)
            doctor = self.doctors.get(appointment.doctor_id)
            
            patient_name = patient.name if patient else "Unknown Patient"
            doctor_name = f"Dr. {doctor.name}" if doctor else "Unknown Doctor"
            
            print(f"   Patient: {patient_name} (ID: {appointment.patient_id})")
            print(f"   Doctor: {doctor_name} (ID: {appointment.doctor_id})")
            print(f"   Date: {appointment.appointment_time.strftime('%A, %B %d, %Y')}")
            print(f"   Time: {appointment.appointment_time.strftime('%I:%M %p')}")
            print(f"   Type: {appointment.appointment_type}")
            print(f"   Status: {appointment.status}")
    
    def undo_last_operation(self):
        """Undo last operation using stack"""
        if not self.operation_history:
            print("No recent operations available to undo.")
            return False
        
        operation, patient_id = self.operation_history.pop()
        
        if operation == 'register':
            # Remove patient from all data structures
            if patient_id in self.patients:
                patient_name = self.patients[patient_id].name
                
                # Remove from queues if still waiting
                # This is a simplified approach - in a real system you'd need more sophisticated queue management
                self.emergency_queue = [p for p in self.emergency_queue if p.patient_id != patient_id]
                heapq.heapify(self.emergency_queue)  # Restore heap property
                
                # Remove from regular queue
                new_regular_queue = deque()
                for p in self.regular_queue:
                    if p.patient_id != patient_id:
                        new_regular_queue.append(p)
                self.regular_queue = new_regular_queue
                
                # Remove from patients dictionary
                del self.patients[patient_id]
                
                print(f"SUCCESS: Undid registration of patient {patient_name} (ID: {patient_id})")
                print("Patient has been removed from all hospital records and queues.")
                
        elif operation == 'discharge':
            print(f"INFO: Discharge operation for patient {patient_id} has been noted.")
            print("Note: Full undo of discharge would require complex state restoration.")
        
        return True

def display_menu():
    """Display the main menu"""
    print("\n" + "="*65)
    print("           HOSPITAL MANAGEMENT SYSTEM")
    print("="*65)
    print("PATIENT MANAGEMENT:")
    print("  1.  Register New Patient")
    print("  2.  Admit Next Waiting Patient")
    print("  3.  Search for Patient")
    print("  4.  Discharge Patient")
    print("  5.  Schedule Patient Appointment")
    print("")
    print("INFORMATION & REPORTS:")
    print("  6.  View Patient Queue Status")
    print("  7.  View Hospital Statistics")
    print("  8.  View All Patients")
    print("  9.  View All Doctors")
    print("  10. View All Rooms")
    print("  11. View All Appointments")
    print("")
    print("SYSTEM MANAGEMENT:")
    print("  12. Add New Doctor to Staff")
    print("  13. Add New Room to Hospital")
    print("  14. Undo Last Operation")
    print("  15. Exit System")
    print("="*65)

def main():
    """Main function with interactive menu"""
    print("="*65)
    print("    WELCOME TO THE HOSPITAL MANAGEMENT SYSTEM")
    print("="*65)
    print("Initializing system, please wait...")
    
    try:
        hms = HospitalManagementSystem()
        print("System initialization completed successfully!")
        
        while True:
            display_menu()
            
            try:
                choice = input("\nPlease enter your choice (1-15): ").strip()
                
                if choice == '1':
                    hms.register_patient_interactive()
                
                elif choice == '2':
                    hms.admit_next_patient()
                
                elif choice == '3':
                    hms.search_patient_interactive()
                
                elif choice == '4':
                    hms.discharge_patient_interactive()
                
                elif choice == '5':
                    hms.schedule_appointment_interactive()
                
                elif choice == '6':
                    hms.get_patient_queue_status()
                
                elif choice == '7':
                    hms.get_hospital_statistics()
                
                elif choice == '8':
                    hms.view_all_patients()
                
                elif choice == '9':
                    hms.view_all_doctors()
                
                elif choice == '10':
                    hms.view_all_rooms()
                
                elif choice == '11':
                    hms.view_all_appointments()
                
                elif choice == '12':
                    hms.add_doctor_interactive()
                
                elif choice == '13':
                    hms.add_room_interactive()
                
                elif choice == '14':
                    hms.undo_last_operation()
                
                elif choice == '15':
                    print("\n" + "="*50)
                    print("Thank you for using Hospital Management System!")
                    print("System shutting down safely...")
                    print("Goodbye!")
                    print("="*50)
                    break
                
                else:
                    print("ERROR: Invalid choice! Please select a number between 1 and 15.")
            
            except KeyboardInterrupt:
                print("\n\nSystem interrupted by user.")
                print("Thank you for using Hospital Management System!")
                break
            except Exception as e:
                print(f"ERROR: An unexpected error occurred: {str(e)}")
                print("Please try again or contact system administrator.")
            
            # Wait for user to continue
            input("\nPress Enter to continue to main menu...")
    
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to initialize system: {str(e)}")
        print("Please contact system administrator.")

if __name__ == "__main__":
    main()