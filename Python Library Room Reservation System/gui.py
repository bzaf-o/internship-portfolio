import tkinter as tk
from tkinter import ttk, messagebox
from reservation import LibREST, LibRESTManager
import sv_ttk



"""

To Do:

[X] Add edit and cancel reservation functions in manage reservations

[X] Move "make a reservation" button above the exit button

[ ] Error warnings: invalid day, invalid time, clashing time, room not available

"""

class LibRESTInfo:
    def setup_info_tab(self):
        self.clear_main_frame()
        info_text = """
        LibREST offers:

        - 5 Small Rooms (Room 1 - 5)

        - 5 Large Rooms (Room 6 - 10)

        - Reservations available Monday to Friday

        - Reservation hours: 8am to 8pm

        - Note: Reservations can only start from 8am to 7pm and end from 9am to 8pm

        """

        info_label = ttk.Label(self.main_frame, text=info_text, wraplength=400, font=('Segoe UI', 13))
        info_label.pack(expand=True, fill='both', padx=20, pady=20)
        self.add_return_button()

class AvailabilityTab:
    def setup_check_tab(self):
        self.clear_main_frame()
        # Day selection
        frame = ttk.Frame(self.main_frame)
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        ttk.Label(frame, text="Select Day:", font=('Segoe UI', 13)).pack(pady=10)
        
        self.check_day_var = tk.StringVar()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] 
        day_combo = ttk.Combobox(frame, textvariable=self.check_day_var, values=days, font=('Segoe UI', 13))
        day_combo.pack(pady=10)
        ttk.Button(frame, text="Check Availability", command=self.check_availability, style='Large.TButton').pack(pady=20)
        
        self.availability_text = tk.Text(frame, height=15, width=50, font=('TkDefaultFont', 15))
        self.availability_text.pack(expand=True, fill='both', pady=10)
        self.add_return_button()

    def check_availability(self):
        day = self.check_day_var.get()
        if not day:
            messagebox.showerror("Error", "Please select a day")
            return
        self.availability_text.delete(1.0, tk.END)
        self.reservation_system.availability(day)

        # Redirect output to text widget
        self.availability_text.insert(tk.END, f"Room Availability for {day}:\n")
        for room in self.reservation_system._rooms:
            reservations = room.get_reservations(day)
            self.availability_text.insert(tk.END, f"\n{room.room_type} Room {room.room_number}:\n")
            if not reservations:
                self.availability_text.insert(tk.END, "No reservations yet\n")
            else:
                for reservation in reservations:
                    self.availability_text.insert(tk.END, 
                        f"  Booked from {reservation['start_time']} to {reservation['end_time']}\n")

class ReservationTab:
    def setup_reserve_tab(self):
        self.clear_main_frame()
        frame = ttk.Frame(self.main_frame)
        frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Create left and right frames
        left_frame = ttk.Frame(frame)
        right_frame = ttk.Frame(frame)
        left_frame.pack(side='left', expand=True, fill='both', padx=10)
        right_frame.pack(side='right', expand=True, fill='both', padx=10)

        # Room Details (Left Column)
        ttk.Label(left_frame, text="Room Details", font=('Segoe UI', 13, 'bold')).pack(pady=(0,10))

        # Room Type as radio buttons

        ttk.Label(left_frame, text="Room Type:", font=('Segoe UI', 13)).pack(pady=5)
        self.room_type_var = tk.StringVar(value="Small")
        ttk.Radiobutton(left_frame, text="Small", variable=self.room_type_var, value="Small").pack()
        ttk.Radiobutton(left_frame, text="Large", variable=self.room_type_var, value="Large").pack()

        # Day as dropdown
        ttk.Label(left_frame, text="Day:", font=('Segoe UI', 13)).pack(pady=5)
        self.day_var = tk.StringVar()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        ttk.Combobox(left_frame, textvariable=self.day_var, values=days, font=('Segoe UI', 13)).pack(pady=5)

        # Time inputs
        self.start_time_var = tk.StringVar()
        self.end_time_var = tk.StringVar()
        time_inputs = [
            ('Start Time (HHMM):', self.start_time_var),
            ('End Time (HHMM):', self.end_time_var)
        ]

        for label, var in time_inputs:
            ttk.Label(left_frame, text=label, font=('Segoe UI', 13)).pack(pady=5)
            ttk.Entry(left_frame, textvariable=var, font=('Segoe UI', 13)).pack(pady=5)

        # Personal Details (Right Column)
        ttk.Label(right_frame, text="Personal Details", font=('Segoe UI', 13, 'bold')).pack(pady=(0,10))
        labels_right = ['Name:', 'Student ID:', 'Phone:']
        vars_right = [self.name_var, self.student_id_var, self.phone_var] = [tk.StringVar() for _ in range(3)]

        for label, var in zip(labels_right, vars_right):
            ttk.Label(right_frame, text=label, font=('Segoe UI', 13)).pack(pady=5)
            ttk.Entry(right_frame, textvariable=var, font=('Segoe UI', 13)).pack(pady=5)

        # Submit & return button
        ttk.Button(self.main_frame, text="Create Reservation", command=self.create_reservation,style='Large.TButton').pack(pady=10)
        self.add_return_button()

    def create_reservation(self):
        try:
            success = self.reservation_system.create_reservation(
                self.room_type_var.get(),
                self.day_var.get(),
                int(self.start_time_var.get()),
                int(self.end_time_var.get()),
                self.name_var.get(),
                self.student_id_var.get(),
                self.phone_var.get()
            )

            if success:
                messagebox.showinfo("Success", "Reservation created successfully!")

                # Clear fields
                for var in [self.room_type_var, self.day_var, self.start_time_var, self.end_time_var, self.name_var, self.student_id_var, self.phone_var]:
                    var.set("")

            else:
                messagebox.showerror("Error", "Failed to create reservation")
        except ValueError:
            messagebox.showerror("Error", "Please check your input values")



class ManageReservationsTab:
    def setup_manage_tab(self):
        self.clear_main_frame()
        frame = ttk.Frame(self.main_frame)
        frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Student verification section
        verify_frame = ttk.Frame(frame)
        verify_frame.pack(fill='x', pady=20)
        ttk.Label(verify_frame, text="Student ID:", font=('Segoe UI', 13)).pack(pady=5)
        self.manage_id_var = tk.StringVar()
        ttk.Entry(verify_frame, textvariable=self.manage_id_var, font=('Segoe UI', 13)).pack(pady=5)
        ttk.Label(verify_frame, text="Phone:", font=('Segoe UI', 13)).pack(pady=5)
        self.manage_phone_var = tk.StringVar()
        ttk.Entry(verify_frame, textvariable=self.manage_phone_var, font=('Segoe UI', 13)).pack(pady=5)
        ttk.Button(verify_frame, text="Verify", command=self.verify_user, style='Large.TButton').pack(pady=20)

        # Add return button below verify
        ttk.Button(verify_frame, text="Return to Main Menu", command=self.show_main_menu, style='Large.TButton').pack(pady=10)

        # Results area (hidden initially)
        self.manage_text = tk.Text(frame, height=10, width=50, font=('Segoe UI', 11))
        self.manage_text.pack_forget()

        # Configure tag for selection border
        self.manage_text.tag_configure('selected', borderwidth=2, relief='solid')

        # Create hover tag with light blue background
        self.manage_text.tag_configure('hover', background='#e6f3ff')

        # Action buttons frame (hidden initially)
        self.action_frame = ttk.Frame(frame)

        # Edit button
        self.edit_button = ttk.Button(self.action_frame, text="Edit Reservation", command=self.show_edit_dialog, style='Large.TButton')
        self.edit_button.grid(row=0, column=0, padx=10)

        # Delete button
        self.delete_button = ttk.Button(self.action_frame, text="Delete Reservation", command=self.delete_reservation, style='Large.TButton')
        self.delete_button.grid(row=0, column=1, padx=10)

    def verify_user(self):
        student_id = self.manage_id_var.get()
        phone = self.manage_phone_var.get()
        reservations = self.reservation_system.find_user_reservations(student_id, phone)

        if not reservations:
            messagebox.showerror("Error", "No reservations found for this user")
            return

        # Show reservations and action buttons
        self.manage_text.pack(expand=True, fill='both', pady=10)
        self.action_frame.pack(pady=20)

        # Display reservations and make them selectable
        self.manage_text.config(state='normal')
        self.manage_text.delete(1.0, tk.END)
        self.manage_text.insert(tk.END, "Click on a reservation to select it:\n\n")

        # Store reservations for reference
        self.current_reservations = reservations
        self.selected_reservation = None

        for i, reservation in enumerate(reservations):
            tag_name = f"reservation_{i}"
            line_start = self.manage_text.index("end-1c")

            # Insert reservation text
            self.manage_text.insert(tk.END,
                f"{reservation['room_type']} Room {reservation['room_number']} on {reservation['day']} " f"from {reservation['start_time']} to {reservation['end_time']}\n", tag_name)

            line_end = self.manage_text.index("end-1c")

            # Bind mouse events for hover and click
            self.manage_text.tag_bind(tag_name, '<Enter>', lambda e, start=line_start, end=line_end: self.on_reservation_hover(start, end))
            self.manage_text.tag_bind(tag_name, '<Leave>', lambda e, start=line_start, end=line_end: self.on_reservation_leave(start, end))
            self.manage_text.tag_bind(tag_name, '<Button-1>', lambda e, r=reservation, start=line_start, end=line_end: self.select_reservation(r, start, end))

        # Disable text editing but allow selection
        self.manage_text.config(state='disabled')

    def on_reservation_hover(self, start, end):
        self.manage_text.tag_add('hover', start, end)

    def on_reservation_leave(self, start, end):
        self.manage_text.tag_remove('hover', start, end)   

    def view_reservations(self):
        student_id = self.manage_id_var.get()
        phone = self.manage_phone_var.get()
        reservations = self.reservation_system.find_user_reservations(student_id, phone)
        self.manage_text.delete(1.0, tk.END)

        if reservations:
            self.manage_text.insert(tk.END, "Your reservations:\n")
            for reservation in reservations:
                self.manage_text.insert(tk.END, f"{reservation['room_type']} Room {reservation['room_number']} on {reservation['day']} " f"from {reservation['start_time']} to {reservation['end_time']}\n")
        else:
            self.manage_text.insert(tk.END, "No reservations found.")

    def cancel_reservation(self):
        student_id = self.manage_id_var.get()
        phone = self.manage_phone_var.get()

        if self.reservation_system.cancel_reservation(student_id, phone):
            messagebox.showinfo("Success", "Reservation cancelled successfully!")
            self.view_reservations()  # Refresh the view
        else:
            messagebox.showerror("Error", "No reservation found to cancel")

    def select_reservation(self, reservation, start, end):
        # Remove previous selection border
        self.manage_text.tag_remove('selected', '1.0', 'end')

        # Add border to new selection
        self.manage_text.tag_add('selected', start, end)

        # Store selected reservation
        self.selected_reservation = reservation

    def show_edit_dialog(self):

        if not self.selected_reservation:
            messagebox.showerror("Error", "Please select a reservation to edit")
            return

        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Reservation")
        dialog.geometry("400x300")

        # Add time input fields
        ttk.Label(dialog, text="New Start Time (HHMM):", font=('Segoe UI', 13)).pack(pady=10)
        new_start_time = tk.StringVar(value=str(self.selected_reservation['start_time']))
        ttk.Entry(dialog, textvariable=new_start_time, font=('Segoe UI', 13)).pack(pady=5)
        ttk.Label(dialog, text="New End Time (HHMM):", font=('Segoe UI', 13)).pack(pady=10)
        new_end_time = tk.StringVar(value=str(self.selected_reservation['end_time']))
        ttk.Entry(dialog, textvariable=new_end_time, font=('Segoe UI', 13)).pack(pady=5)

        def save_changes():
            try:
                new_details = {
                    'start_time': int(new_start_time.get()),
                    'end_time': int(new_end_time.get())

                }

                if self.reservation_system.edit_reservation(
                    self.manage_id_var.get(),
                    self.manage_phone_var.get(),
                    new_details
                ):
                    messagebox.showinfo("Success", "Reservation updated successfully!")
                    dialog.destroy()
                    self.verify_user()  # Refresh the display
                else:
                    messagebox.showerror("Error", "Failed to update reservation")

            except ValueError:
                messagebox.showerror("Error", "Please enter valid times")

        ttk.Button(dialog, text="Save Changes", 
                    command=save_changes, style='Large.TButton').pack(pady=20)

    def delete_reservation(self):
        if not self.selected_reservation:
            messagebox.showerror("Error", "Please select a reservation to delete")
            return

        if messagebox.askyesno("Confirm Delete", 
            "Are you sure you want to delete this reservation?"):

            if self.reservation_system.cancel_reservation(
                self.manage_id_var.get(),
                self.manage_phone_var.get()
            ):
                messagebox.showinfo("Success", "Reservation deleted successfully!")
                self.verify_user()  # Refresh the display

            else:
                messagebox.showerror("Error", "Failed to delete reservation")
                
class LibRESTGUI(LibRESTInfo, AvailabilityTab, ReservationTab, ManageReservationsTab):
    def __init__(self, root):
        self.root = root
        self.root.title("LibREST - Library Room Reservation System")
        self.reservation_system = LibRESTManager()
        self.reservation_main = LibREST()

        # Configure weight for dynamic resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create and show main menu
        self.show_main_menu()

    def show_main_menu(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Configure weights for dynamic resizing
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # Center frame for image and buttons
        center_frame = ttk.Frame(self.main_frame)
        center_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_rowconfigure(0, weight=1)

        # Title image
        try:
            self.title_image = tk.PhotoImage(file="title.png")
            image_frame = ttk.Frame(center_frame)
            image_frame.grid(row=0, column=0, sticky='nsew')
            image_frame.grid_columnconfigure(0, weight=1)
            image_label = ttk.Label(image_frame, image=self.title_image)
            image_label.grid(row=0, column=0, pady=20)
        except:
            print("Warning: title.png not found")

        # Configure button style
        style = ttk.Style()
        style.configure('Large.TButton', font=('Segoe UI', 13))
        style.configure('Exit.TButton', font=('Segoe UI', 13))

        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Create buttons with consistent width

        buttons = [
            ("About This System", self.setup_info_tab, 0, 0),
            ("Check Room Availability", self.setup_check_tab, 1, 0),
            ("Make A Reservation", self.setup_reserve_tab, 0, 1),
            ("Manage Existing Reservations", self.setup_manage_tab, 1, 1)
        ]

        # Calculate max button width based on longest text
        max_text = max(buttons, key=lambda x: len(x[0]))[0]
        button_width = len(max_text) + 4  # Add padding

        # Create main menu buttons
        for text, command, row, col in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, style='Large.TButton', width=button_width)
            btn.grid(row=row, column=col, pady=10, padx=10, sticky='nsew')

        # Exit button (smaller width)
        exit_btn = ttk.Button(self.main_frame, text="Exit", command=self.root.quit, style='Exit.TButton', width=10)
        exit_btn.grid(row=2, column=0, columnspan=2, pady=20)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def add_return_button(self):
        ttk.Button(self.main_frame, text="Return to Main Menu", command=self.show_main_menu, style='Large.TButton').pack(side='bottom', pady=20)

def run_gui():
    root = tk.Tk()
    app = LibRESTGUI(root)
    sv_ttk.set_theme("dark")
    root.mainloop()