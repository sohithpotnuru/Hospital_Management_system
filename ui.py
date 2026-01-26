# ui.py
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import heapq

# Import backend classes from your main.py
from main import (
    HospitalManagementSystem,
    Patient,
    Doctor,
    Room,
    Appointment
)

class HospitalUI:
    def __init__(self, root):
        self.hms = HospitalManagementSystem()
        self.root = root
        self.root.title("🏥 Hospital Management System — UI")
        self.root.geometry("1000x700")
        self.root.config(bg="#f4f7fb")

        title = tk.Label(root, text="🏥 Hospital Management System",
                         font=("Segoe UI", 20, "bold"), bg="#1976D2", fg="white", pady=10)
        title.pack(fill="x")

        # Top controls frame
        ctrl_frame = tk.Frame(root, bg="#f4f7fb")
        ctrl_frame.pack(pady=12, padx=12, fill="x")

        left_frame = tk.Frame(ctrl_frame, bg="#f4f7fb")
        left_frame.pack(side="left", anchor="n")

        right_frame = tk.Frame(ctrl_frame, bg="#f4f7fb")
        right_frame.pack(side="right", anchor="n")

        buttons = [
            ("Register Patient", self.register_patient_ui),
            ("Admit Next Patient", self.admit_patient_ui),
            ("Discharge Patient", self.discharge_patient_ui),
            ("Schedule Appointment", self.schedule_appointment_ui),
            ("Add Doctor", self.add_doctor_ui),
            ("Add Room", self.add_room_ui),
            ("View Patients", self.view_patients_ui),
            ("View Doctors", self.view_doctors_ui),
            ("View Rooms", self.view_rooms_ui),
            ("View Appointments", self.view_appointments_ui),
            ("View Statistics", self.view_stats_ui),
            ("Clear Output", self.clear_output)
        ]

        for i, (text, cmd) in enumerate(buttons):
            b = tk.Button(left_frame if i < 6 else right_frame, text=text, width=20, height=2,
                          bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold"), command=cmd)
            b.grid(row=i % 6, column=0, padx=8, pady=6)

        # Output area (scrollable)
        out_frame = tk.Frame(root, bg="#f4f7fb")
        out_frame.pack(padx=12, pady=(0,12), fill="both", expand=True)

        self.output = tk.Text(out_frame, wrap="word", font=("Consolas", 11), bg="white")
        self.output.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(out_frame, command=self.output.yview)
        scrollbar.pack(side="right", fill="y")
        self.output.config(yscrollcommand=scrollbar.set)

        # initial welcome message
        self.output.insert(tk.END, "Welcome! Use the buttons to operate the Hospital Management System.\n")
        self.output.insert(tk.END, "All actions use GUI forms — no terminal input required.\n\n")

    def clear_output(self):
        self.output.delete(1.0, tk.END)

    # ---------- Patient Registration ----------
    def register_patient_ui(self):
        win = tk.Toplevel(self.root)
        win.title("Register New Patient")
        win.geometry("420x420")
        win.resizable(False, False)

        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Name:", anchor="w").pack(fill="x")
        name_e = tk.Entry(frame)
        name_e.pack(fill="x", pady=6)

        tk.Label(frame, text="Age:", anchor="w").pack(fill="x")
        age_e = tk.Entry(frame)
        age_e.pack(fill="x", pady=6)

        tk.Label(frame, text="Condition / Symptoms:", anchor="w").pack(fill="x")
        cond_e = tk.Entry(frame)
        cond_e.pack(fill="x", pady=6)

        tk.Label(frame, text="Priority (1=Critical, 4=Low):", anchor="w").pack(fill="x")
        priority_cb = ttk.Combobox(frame, values=[1,2,3,4], state="readonly")
        priority_cb.set(3)
        priority_cb.pack(fill="x", pady=6)

        def submit():
            name = name_e.get().strip()
            age_str = age_e.get().strip()
            condition = cond_e.get().strip()
            try:
                if not name or len(name) < 2:
                    raise ValueError("Name must be at least 2 characters.")
                age = int(age_str)
                if not (1 <= age <= 120):
                    raise ValueError("Age must be between 1 and 120.")
                if not condition or len(condition) < 3:
                    raise ValueError("Condition description must be at least 3 characters.")
                priority = int(priority_cb.get())
                if priority < 1 or priority > 4:
                    raise ValueError("Priority must be 1-4.")

                patient_id = f"P{len(self.hms.patients)+1:03d}"
                patient = Patient(patient_id, name, age, condition, priority)
                self.hms.patients[patient_id] = patient
                self.hms.patient_bst.insert(patient)

                if priority <= 2:
                    heapq.heappush(self.hms.emergency_queue, patient)
                    qtxt = "Emergency Queue"
                else:
                    self.hms.regular_queue.append(patient)
                    qtxt = "Regular Queue"

                self.output.insert(tk.END, f"✅ Registered patient {name} (ID: {patient_id}) → {qtxt}\n")
                messagebox.showinfo("Success", f"Patient {name} registered (ID: {patient_id}).")
                win.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(frame, text="Register", bg="#4CAF50", fg="white", command=submit).pack(pady=12)

    # ---------- Admit Next Patient ----------
    def admit_patient_ui(self):
        patient = self.hms.admit_next_patient()
        if patient:
            self.output.insert(tk.END, f"✅ Admitted: {patient.name} (ID: {patient.patient_id}) to {patient.room_number} — Doctor: {patient.assigned_doctor}\n")
        else:
            self.output.insert(tk.END, "⚠️ No patients available to admit.\n")

    # ---------- Discharge ----------
    def discharge_patient_ui(self):
        admitted = [p for p in self.hms.patients.values() if p.status == "Admitted"]
        if not admitted:
            messagebox.showinfo("Info", "No patients are currently admitted.")
            return

        win = tk.Toplevel(self.root)
        win.title("Discharge Patient")
        win.geometry("420x220")
        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Select patient to discharge:", anchor="w").pack(fill="x")
        combo = ttk.Combobox(frame, values=[f"{p.patient_id} - {p.name}" for p in admitted], width=40, state="readonly")
        combo.pack(pady=10)

        def do_discharge():
            sel = combo.get()
            if not sel:
                messagebox.showwarning("Warning", "Select a patient.")
                return
            pid = sel.split(" - ")[0]
            patient = self.hms.patients.get(pid)
            if not patient:
                messagebox.showerror("Error", "Patient not found.")
                return

            # free room
            if patient.room_number and patient.room_number in self.hms.rooms:
                room = self.hms.rooms[patient.room_number]
                room.discharge_patient(pid)

            # free doctor
            if patient.assigned_doctor and patient.assigned_doctor in self.hms.doctors:
                doc = self.hms.doctors[patient.assigned_doctor]
                doc.discharge_patient(pid)

            patient.status = "Discharged"
            old_room = patient.room_number
            old_doc = patient.assigned_doctor
            patient.room_number = None
            patient.assigned_doctor = None

            self.hms.operation_history.append(('discharge', pid))
            messagebox.showinfo("Success", f"{patient.name} discharged.")
            self.output.insert(tk.END, f"✅ Discharged: {patient.name} (ID: {pid}) — freed Room: {old_room}, Doctor: {old_doc}\n")
            win.destroy()

        tk.Button(frame, text="Discharge", bg="#E91E63", fg="white", command=do_discharge).pack(pady=8)

    # ---------- Add Doctor ----------
    def add_doctor_ui(self):
        win = tk.Toplevel(self.root)
        win.title("Add Doctor")
        win.geometry("420x300")
        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Doctor Name:", anchor="w").pack(fill="x")
        name_e = tk.Entry(frame)
        name_e.pack(fill="x", pady=6)

        tk.Label(frame, text="Specialization:", anchor="w").pack(fill="x")
        spec_e = tk.Entry(frame)
        spec_e.pack(fill="x", pady=6)

        tk.Label(frame, text="Max Patients (default 10):", anchor="w").pack(fill="x")
        max_e = tk.Entry(frame)
        max_e.insert(0, "10")
        max_e.pack(fill="x", pady=6)

        def submit():
            name = name_e.get().strip()
            spec = spec_e.get().strip()
            try:
                if not name or len(name) < 2:
                    raise ValueError("Name must be at least 2 characters.")
                if not spec or len(spec) < 3:
                    raise ValueError("Specialization must be at least 3 characters.")
                max_p = int(max_e.get())
                if max_p < 1 or max_p > 100:
                    raise ValueError("Max patients must be between 1 and 100.")

                doc_id = f"D{len(self.hms.doctors)+1:03d}"
                doctor = Doctor(doc_id, name, spec, max_p)
                self.hms.doctors[doc_id] = doctor

                self.output.insert(tk.END, f"✅ Added Doctor: Dr. {name} (ID: {doc_id}) — {spec}, max {max_p}\n")
                messagebox.showinfo("Success", f"Doctor {name} added (ID: {doc_id}).")
                win.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(frame, text="Add Doctor", bg="#4CAF50", fg="white", command=submit).pack(pady=10)

    # ---------- Add Room ----------
    def add_room_ui(self):
        win = tk.Toplevel(self.root)
        win.title("Add Room")
        win.geometry("420x330")
        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Room Type:", anchor="w").pack(fill="x")
        rt_cb = ttk.Combobox(frame, values=["ICU", "General", "Private", "Emergency"], state="readonly")
        rt_cb.set("General")
        rt_cb.pack(fill="x", pady=6)

        tk.Label(frame, text="Capacity (beds):", anchor="w").pack(fill="x")
        cap_e = tk.Entry(frame)
        cap_e.insert(0, "1")
        cap_e.pack(fill="x", pady=6)

        def submit():
            rtype = rt_cb.get().strip()
            try:
                cap = int(cap_e.get())
                if cap < 1 or cap > 20:
                    raise ValueError("Capacity must be 1-20 beds.")
                room_id = f"R{len(self.hms.rooms)+1:03d}"
                room = Room(room_id, rtype, cap)
                self.hms.rooms[room_id] = room
                self.output.insert(tk.END, f"✅ Added Room: {room_id} — {rtype}, capacity {cap}\n")
                messagebox.showinfo("Success", f"Room {room_id} added.")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(frame, text="Add Room", bg="#4CAF50", fg="white", command=submit).pack(pady=10)

    # ---------- Schedule Appointment ----------
    def schedule_appointment_ui(self):
        if not self.hms.patients:
            messagebox.showinfo("Info", "No patients registered yet.")
            return
        if not self.hms.doctors:
            messagebox.showinfo("Info", "No doctors available.")
            return

        win = tk.Toplevel(self.root)
        win.title("Schedule Appointment")
        win.geometry("520x420")
        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Select Patient:", anchor="w").pack(fill="x")
        pat_cb = ttk.Combobox(frame, values=[f"{p.patient_id} - {p.name}" for p in self.hms.patients.values()], state="readonly")
        pat_cb.pack(fill="x", pady=6)

        tk.Label(frame, text="Select Doctor:", anchor="w").pack(fill="x")
        doc_cb = ttk.Combobox(frame, values=[f"{d.doctor_id} - {d.name}" for d in self.hms.doctors.values()], state="readonly")
        doc_cb.pack(fill="x", pady=6)

        tk.Label(frame, text="Date (YYYY-MM-DD):", anchor="w").pack(fill="x")
        date_e = tk.Entry(frame)
        date_e.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_e.pack(fill="x", pady=6)

        tk.Label(frame, text="Time (HH:MM 24hr):", anchor="w").pack(fill="x")
        time_e = tk.Entry(frame)
        time_e.insert(0, "09:30")
        time_e.pack(fill="x", pady=6)

        tk.Label(frame, text="Type (Consultation / Follow-up):", anchor="w").pack(fill="x")
        type_e = tk.Entry(frame)
        type_e.insert(0, "Consultation")
        type_e.pack(fill="x", pady=6)

        def submit():
            sel_patient = pat_cb.get()
            sel_doc = doc_cb.get()
            dt = date_e.get().strip()
            tm = time_e.get().strip()
            atype = type_e.get().strip() or "Consultation"

            if not sel_patient or not sel_doc:
                messagebox.showwarning("Warning", "Select both patient and doctor.")
                return
            pid = sel_patient.split(" - ")[0]
            did = sel_doc.split(" - ")[0]

            try:
                appointment_time = datetime.strptime(f"{dt} {tm}", "%Y-%m-%d %H:%M")
                if appointment_time < datetime.now():
                    raise ValueError("Appointment time must be in the future.")

                appt = Appointment(pid, did, appointment_time, atype)
                self.hms.appointments[appt.appointment_id] = appt

                # add to doctor's schedule
                doctor = self.hms.doctors.get(did)
                if doctor:
                    date_str = appointment_time.strftime("%Y-%m-%d")
                    if date_str not in doctor.schedule:
                        doctor.schedule[date_str] = []
                    doctor.schedule[date_str].append(appt.appointment_id)

                self.output.insert(tk.END, f"✅ Scheduled appointment {appt.appointment_id} — Patient {pid}, Doctor {did} at {appointment_time.strftime('%Y-%m-%d %H:%M')}\n")
                messagebox.showinfo("Success", f"Appointment scheduled (ID: {appt.appointment_id}).")
                win.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(frame, text="Schedule", bg="#4CAF50", fg="white", command=submit).pack(pady=12)

    # ---------- Viewing helpers ----------
    def view_patients_ui(self):
        patients = sorted(self.hms.patient_bst.inorder_traversal(), key=lambda p: p.patient_id)
        if not patients:
            self.output.insert(tk.END, "No patients registered.\n")
            return
        self.output.insert(tk.END, f"\n--- All Patients ({len(patients)}) ---\n")
        for p in patients:
            self.output.insert(tk.END,
                f"{p.patient_id} | {p.name} | Age: {p.age} | Condition: {p.condition} | Status: {p.status} | Room: {p.room_number or 'N/A'} | Doctor: {p.assigned_doctor or 'N/A'}\n"
            )

    def view_doctors_ui(self):
        docs = sorted(self.hms.doctors.values(), key=lambda d: d.doctor_id)
        if not docs:
            self.output.insert(tk.END, "No doctors in system.\n")
            return
        self.output.insert(tk.END, f"\n--- Doctors ({len(docs)}) ---\n")
        for d in docs:
            self.output.insert(tk.END,
                f"{d.doctor_id} | Dr. {d.name} | {d.specialization} | Load: {len(d.current_patients)}/{d.max_patients}\n"
            )

    def view_rooms_ui(self):
        rooms = sorted(self.hms.rooms.values(), key=lambda r: r.room_number)
        if not rooms:
            self.output.insert(tk.END, "No rooms defined.\n")
            return
        self.output.insert(tk.END, f"\n--- Rooms ({len(rooms)}) ---\n")
        for r in rooms:
            status = "Available" if r.is_available else "Full"
            self.output.insert(tk.END,
                f"{r.room_number} | {r.room_type} | Capacity: {r.capacity} | Occupied: {r.occupied_beds} | Status: {status}\n"
            )

    def view_appointments_ui(self):
        apps = sorted(self.hms.appointments.values(), key=lambda a: a.appointment_time)
        if not apps:
            self.output.insert(tk.END, "No appointments scheduled.\n")
            return
        self.output.insert(tk.END, f"\n--- Appointments ({len(apps)}) ---\n")
        for a in apps:
            patient_name = self.hms.patients.get(a.patient_id).name if a.patient_id in self.hms.patients else "Unknown"
            doctor_name = self.hms.doctors.get(a.doctor_id).name if a.doctor_id in self.hms.doctors else "Unknown"
            self.output.insert(tk.END,
                f"{a.appointment_id} | {a.appointment_time.strftime('%Y-%m-%d %H:%M')} | Patient: {patient_name} ({a.patient_id}) | Doctor: Dr. {doctor_name} ({a.doctor_id}) | Type: {a.appointment_type} | Status: {a.status}\n"
            )

    def view_stats_ui(self):
        total_patients = len(self.hms.patients)
        admitted = sum(1 for p in self.hms.patients.values() if p.status == "Admitted")
        discharged = sum(1 for p in self.hms.patients.values() if p.status == "Discharged")
        waiting = len(self.hms.emergency_queue) + len(self.hms.regular_queue)
        total_rooms = len(self.hms.rooms)
        occupied_rooms = sum(1 for r in self.hms.rooms.values() if not r.is_available)
        total_doctors = len(self.hms.doctors)
        busy_doctors = sum(1 for d in self.hms.doctors.values() if d.current_patients)
        scheduled_appointments = len([a for a in self.hms.appointments.values() if a.status == "Scheduled"])

        self.output.insert(tk.END, "\n--- Hospital Statistics ---\n")
        self.output.insert(tk.END, f"Total Patients Registered: {total_patients}\n")
        self.output.insert(tk.END, f"  Admitted: {admitted}\n")
        self.output.insert(tk.END, f"  Discharged: {discharged}\n")
        self.output.insert(tk.END, f"  Waiting: {waiting}\n\n")
        self.output.insert(tk.END, f"Total Rooms: {total_rooms} | Occupied Rooms: {occupied_rooms}\n")
        self.output.insert(tk.END, f"Total Doctors: {total_doctors} | Busy Doctors: {busy_doctors}\n")
        self.output.insert(tk.END, f"Scheduled Appointments: {len(self.hms.appointments)} | Upcoming: {scheduled_appointments}\n\n")

# Run the UI
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalUI(root)
    root.mainloop()
