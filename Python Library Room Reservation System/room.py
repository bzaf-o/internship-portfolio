from typing import List, Dict

class Room:
    def __init__(self, room_number: int, room_type: str):
        self._room_number = room_number
        self._room_type = room_type
        self._reservations: Dict[str, List[Dict]] = {
            'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []
        }

    @property
    def room_number(self) -> int:
        return self._room_number

    @property
    def room_type(self) -> str:
        return self._room_type
    
    def check_availability(self, day: str, start_time: int, end_time: int) -> bool:
        # Check if room is available for reservation
        for reservation in self._reservations[day]:
            if not (end_time <= reservation['start_time'] or start_time >= reservation['end_time']):
                return False
        return True

    def add_reservation(self, day: str, start_time: int, end_time: int, reservation_details: Dict) -> bool:
        # Add a reservation to the room's dictionary
        if self.check_availability(day, start_time, end_time):
            self._reservations[day].append({
                'start_time': start_time,
                'end_time': end_time,
                **reservation_details
            })
            return True
        return False

    def get_reservations(self, day: str) -> List[Dict]:
        # Get all reservations for a specific day
        return self._reservations[day]

    def remove_reservation(self, day: str, student_id: str):
        # Remove a reservation for a specific student
        self._reservations[day] = [
            reservation for reservation in self._reservations[day] 
            if reservation['student_id'] != student_id
        ]

class SmallRoom(Room):
    # Represents a small room in the library
    def __init__(self, room_number: int):
        super().__init__(room_number, "Small")

class LargeRoom(Room):
    # Represents a large room in the library"""
    def __init__(self, room_number: int):
        super().__init__(room_number, "Large")