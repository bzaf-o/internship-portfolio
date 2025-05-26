from reservation import LibREST
from gui import run_gui

def main():
    reservation_system = LibREST()

    while True:
        print("\n########## LibREST (Library Room Reservation System) ##########")
        print("\n1. Check available types of rooms")
        print("2. Check room availability")
        print("3. Create a reservation")
        print("4. Edit an existing reservation")
        print("5. Cancel an existing reservation")
        print("6. View existing reservation details")
        print("7. Exit")

        try:
            choice = int(input("\nEnter your choice (1-7): \n>> "))

            if choice == 1:
                print("\nLibREST is a library room reservation system that creates a seamless experience for users to book one of the library's 10 meeting rooms in advance.\nLibREST offers:\n")
                print("- 5 Small Rooms (Room 1 - 5)")
                print("- 5 Large Rooms (Room 6 - 10)")
                print("- Reservations available Monday to Friday")
                print("- Reservation hours: 8am to 8pm")
                print("- Note: Reservations can only start from 8am to 7pm and end from 9am to 8pm")

            elif choice == 2:
                day = input("Enter day to check availability (Monday - Friday): ")
                reservation_system.check_availablitiy(day)

            elif choice == 3:
                room_type = input("Enter room type (Small/Large): ")
                day = input("Enter day (Monday - Friday): ")
                start_time = int(input("Enter start time (HHMM, e.g., 900 for 9:00 AM): "))
                end_time = int(input("Enter end time (HHMM, e.g., 1500 for 3:00 PM): "))
                student_name = input("Enter your name: ")
                student_id = input("Enter your student ID: ")
                phone = input("Enter your phone number: ")

                if reservation_system.create_reservation(room_type, day, start_time, end_time, 
                                                 student_name, student_id, phone):
                    print("Reservation created successfully!")
                else:
                    print("Reservation failed. Please check your details.")

            elif choice == 4:
                student_id = input("Enter your student ID: ")
                phone = input("Enter your phone number: ")
                
                # First, show existing reservations
                user_reservations = reservation_system.find_user_reservations(student_id, phone)
                if not user_reservations:
                    print("No reservations found for this student.")
                    continue

                print("Your current reservations:")
                for i, reservation in enumerate(user_reservations, 1):
                    print(f"{i}. {reservation['room_type']} Room {reservation['room_number']} on {reservation['day']} "
                          f"from {reservation['start_time']} to {reservation['end_time']}")

                # Get new reservation details
                new_details = {}
                edit_choice = input("Do you want to edit this reservation? (y/n): ").lower()
                if edit_choice == 'y':
                    new_details['start_time'] = int(input("Enter new start time (HHMM): "))
                    new_details['end_time'] = int(input("Enter new end time (HHMM): "))

                    if reservation_system.edit_reservation(student_id, phone, new_details):
                        print("Reservation updated successfully!")
                    else:
                        print("Failed to update reservation.")

            elif choice == 5:
                student_id = input("Enter your student ID: ")
                phone = input("Enter your phone number: ")

                if reservation_system.cancel_reservation(student_id, phone):
                    print("Reservation cancelled successfully!")
                else:
                    print("No reservation found to cancel.")

            elif choice == 6:
                student_id = input("Enter your student ID: ")
                phone = input("Enter your phone number: ")

                user_reservations = reservation_system.find_user_reservations(student_id, phone)
                if user_reservations:
                    print("Your reservations:")
                    for reservation in user_reservations:
                        print(f"{reservation['room_type']} Room {reservation['room_number']} on {reservation['day']} "
                              f"from {reservation['start_time']} to {reservation['end_time']}")
                else:
                    print("No reservations found.")

            elif choice == 7:
                print("Exiting Library Room reservation System. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    run_gui()