from typing import List, Dict, Optional
from room import Room, SmallRoom, LargeRoom

class LibREST:
    # Main library room management method
    def __init__(self):
        # Create 5 small and 5 large rooms
        self._rooms: List[Room] = [
            SmallRoom(i+1) for i in range(5)
        ] + [
            LargeRoom(i+6) for i in range(5)
        ]
        
        # Valid days for booking
        self._valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    def validate_reservation_time(self, start_time: int, end_time: int) -> bool:
        # Makes sure the reservations are made within valid times (8am - 8pm)
        return (
            800 <= start_time < 1900 and  # Start time between 8am and 7pm
            900 <= end_time <= 2000 and   # End time between 9am and 8pm
            start_time < end_time          # End time after start time
        )

    def availability(self, day: str):
        # View availability of all rooms for a specific day
        if day not in self._valid_days:
            print(f"Invalid day. Choose from {', '.join(self._valid_days)}")
            return
            
        print(f"\nRoom Availability for {day}:")
        for room in self._rooms:
            reservations = room.get_reservations(day)
            print(f"{room.room_type} Room {room.room_number}:")
            if not reservations:
                print("No reservations yet")
            else:
                for reservation in reservations:
                    print(f"  Booked from {reservation['start_time']} to {reservation['end_time']}")
    
class LibRESTManager(LibREST):
    def find_available_room(self, room_type: str, day: str, start_time: int, end_time: int) -> Optional[Room]:
        # Find an available room of specified type
        for room in self._rooms:
            if room.room_type.lower() == room_type.lower():
                if room.check_availability(day, start_time, end_time):
                    return room
        return None

    def create_reservation(self, room_type: str, day: str, start_time: int, end_time: int, student_name: str, student_id: str, phone: str) -> bool:
        # Create a new reservation with required details: room type, start & end time, name, student ID and contact number
        # Validate day and time
        if day not in self._valid_days:
            print(f"Invalid day. Choose from {', '.join(self._valid_days)}")
            return False

        if not self.validate_reservation_time(start_time, end_time):
            print("Invalid reservation time. Must be between 8am-7pm, with end time between 9am-8pm.")
            return False

        # Find available room
        room = self.find_available_room(room_type, day, start_time, end_time)
        if not room:
            print(f"No {room_type.lower()} room available for the specified time.")
            return False

        # Add reservation
        reservation_details = {
            'student_name': student_name,
            'student_id': student_id,
            'phone': phone
        }
        return room.add_reservation(day, start_time, end_time, reservation_details)

    def check_availability(self, day: str):
        # View availability of all rooms for a specific day
        print(f"\nRoom Availability for {day}:")
        for room in self._rooms:
            reservations = room.get_reservations(day)
            print(f"{room.room_type} Room {room.room_number}:")
            if not reservations:
                print("No reservations yet")
            else:
                for reservation in reservations:
                    print(f"  Booked from {reservation['start_time']} to {reservation['end_time']}")

    def find_user_reservations(self, student_id: str, phone: str) -> List[Dict]:
        # Find all reservations for a specific user
        user_reservations = []
        for room in self._rooms:
            for day, day_reservations in room._reservations.items():
                user_reservations.extend([
                    {**reservation, 'room_type': room.room_type, 'room_number': room.room_number, 'day': day}
                    for reservation in day_reservations 
                    if reservation['student_id'] == student_id and reservation['phone'] == phone
                ])
        return user_reservations

    def edit_reservation(self, student_id: str, phone: str, new_details: Dict) -> bool:
        # Edit an existing reservation after student info has been verified
        for room in self._rooms:
            for day in self._valid_days:
                reservations = room.get_reservations(day)
                for reservation in reservations:
                    if reservation['student_id'] == student_id and reservation['phone'] == phone:
                        # Remove old reservation
                        room.remove_reservation(day, student_id)
                        
                        # Try to create new reservation with updated details
                        try:
                            result = self.create_reservation(
                                room.room_type, 
                                day, 
                                new_details.get('start_time', reservation['start_time']),
                                new_details.get('end_time', reservation['end_time']),
                                new_details.get('student_name', reservation['student_name']),
                                student_id, 
                                phone
                            )
                            return result
                        except Exception:
                            # If new reservation fails, restore the original reservation
                            room.add_reservation(day, reservation['start_time'], reservation['end_time'], reservation)
                            return False
        return False

    def cancel_reservation(self, student_id: str, phone: str) -> bool:
        # Cancel a reservation
        for room in self._rooms:
            for day in self._valid_days:
                original_reservations = room.get_reservations(day)
                room.remove_reservation(day, student_id)
                
                # Check if any reservation was actually removed
                if len(room.get_reservations(day)) < len(original_reservations):
                    return True
        return False