class PassengerNode:
    def __init__(self, passenger_id, name, seat_number, boarding, destination, waiting_priority, is_waiting):
        self.passenger_id = passenger_id
        self.name = name
        self.seat_number = seat_number
        self.boarding = boarding
        self.destination = destination
        self.waiting_priority = waiting_priority
        self.is_waiting = is_waiting
        self.next = None


class CoachNode:
    def __init__(self, coach_id, coach_type, capacity):
        self.coach_id = coach_id
        self.coach_type = coach_type
        self.capacity = capacity
        self.passenger_head = None
        self.waiting_head = None
        self.next = None


class TrainNode:
    def __init__(self, train_id, train_name, source, destination):
        self.train_id = train_id
        self.train_name = train_name
        self.source = source
        self.destination = destination
        self.coach_head = None
        self.next = None


class RailwayReservationSystem:
    def __init__(self):
        self.train_head = None
        self.arrival_priority = 1
        self.split_counter = 1

    def process_command(self, line):
        parts = line.strip().split("::")
        if len(parts) == 0 or parts[0] == "":
            return ""

        command = parts[0]
        data = []
        if len(parts) > 1:
            data = parts[1].split(":")

        if command == "addTrain":
            if len(data) != 4:
                return "Invalid Command:\naddTrain requires TrainID:TrainName:Source:Destination"
            return self.add_train(data[0], data[1], data[2], data[3])

        if command == "removeTrain":
            if len(data) != 1:
                return "Invalid Command:\nremoveTrain requires TrainID"
            return self.remove_train(data[0])

        if command == "addCoach":
            if len(data) != 4:
                return "Invalid Command:\naddCoach requires TrainID:CoachID:CoachType:Capacity"
            return self.add_coach(data[0], data[1], data[2], data[3])

        if command == "detachCoach":
            if len(data) != 2:
                return "Invalid Command:\ndetachCoach requires TrainID:CoachID"
            return self.detach_coach(data[0], data[1])

        if command == "reserveTicket":
            if len(data) != 6 and len(data) != 7:
                return "Invalid Command:\nreserveTicket requires TrainID:CoachID:PassengerID:Name:Boarding:Destination"
            priority = None
            if len(data) == 7:
                priority = data[6]
            return self.reserve_ticket(data[0], data[1], data[2], data[3], data[4], data[5], priority)

        if command == "cancelTicket":
            if len(data) != 3:
                return "Invalid Command:\ncancelTicket requires TrainID:CoachID:PassengerID"
            return self.cancel_ticket(data[0], data[1], data[2])

        if command == "splitTrain":
            if len(data) != 2:
                return "Invalid Command:\nsplitTrain requires TrainID:CoachID"
            return self.split_train(data[0], data[1])

        if command == "displayTrain":
            if len(data) != 1:
                return "Invalid Command:\ndisplayTrain requires TrainID"
            return self.display_train(data[0])

        if command == "displayAll":
            if len(data) != 0:
                return "Invalid Command:\ndisplayAll does not take parameters"
            return self.display_all()

        if command == "detectCycle":
            if len(data) != 1:
                return "Invalid Command:\ndetectCycle requires TrainID"
            return self.detect_cycle_command(data[0])

        return "Invalid Command:\n" + command

    def add_train(self, train_id, train_name, source, destination):
        if self.find_train(train_id) is not None:
            return "Error:\nTrain already exists: " + train_id

        new_train = TrainNode(train_id, train_name, source, destination)
        if self.train_head is None:
            self.train_head = new_train
        else:
            current = self.train_head
            while current.next is not None:
                current = current.next
            current.next = new_train

        return "Train Added:\n(" + train_id + ", " + train_name + ")"

    def remove_train(self, train_id):
        previous = None
        current = self.train_head
        while current is not None:
            if current.train_id == train_id:
                if previous is None:
                    self.train_head = current.next
                else:
                    previous.next = current.next
                return "Train Removed:\n(" + train_id + ", " + current.train_name + ")"
            previous = current
            current = current.next
        return "Error:\nTrain not found: " + train_id

    def add_coach(self, train_id, coach_id, coach_type, capacity_text):
        train = self.find_train(train_id)
        if train is None:
            return "Error:\nTrain not found: " + train_id

        if self.find_coach(train, coach_id) is not None:
            return "Error:\nCoach already exists: " + coach_id

        capacity = self.parse_positive_integer(capacity_text)
        if capacity is None:
            return "Error:\nInvalid coach capacity: " + capacity_text

        new_coach = CoachNode(coach_id, coach_type, capacity)
        if train.coach_head is None:
            train.coach_head = new_coach
        else:
            current = train.coach_head
            while current.next is not None:
                current = current.next
            current.next = new_coach

        return "Coach Added:\n(" + coach_id + ", " + coach_type + ", Capacity=" + str(capacity) + ")"

    def detach_coach(self, train_id, coach_id):
        train = self.find_train(train_id)
        if train is None:
            return "Error:\nTrain not found: " + train_id

        previous = None
        current = train.coach_head
        while current is not None:
            if current.coach_id == coach_id:
                if current.passenger_head is not None or current.waiting_head is not None:
                    return "Error:\nCoach not empty, cannot detach: " + coach_id
                if previous is None:
                    train.coach_head = current.next
                else:
                    previous.next = current.next
                return "Coach Detached:\n(" + coach_id + ")"
            previous = current
            current = current.next
        return "Error:\nCoach not found: " + coach_id

    def reserve_ticket(self, train_id, coach_id, passenger_id, name, boarding, destination, priority_text):
        train = self.find_train(train_id)
        if train is None:
            return "Error:\nTrain not found: " + train_id

        coach = self.find_coach(train, coach_id)
        if coach is None:
            return "Error:\nCoach not found: " + coach_id

        if self.find_passenger_in_coach(coach, passenger_id) is not None:
            return "Error:\nPassenger already exists: " + passenger_id

        priority = self.arrival_priority
        if priority_text is not None:
            parsed_priority = self.parse_positive_integer(priority_text)
            if parsed_priority is None:
                return "Error:\nInvalid waiting list priority: " + priority_text
            priority = parsed_priority
        self.arrival_priority += 1

        if self.count_passengers(coach.passenger_head) < coach.capacity:
            seat_number = self.next_available_seat(coach)
            passenger = PassengerNode(passenger_id, name, seat_number, boarding, destination, priority, False)
            self.append_passenger(coach, passenger)
            return "Ticket Confirmed:\n(" + passenger_id + ", " + name + ", Seat No:" + str(seat_number) + ")"

        passenger = PassengerNode(passenger_id, name, 0, boarding, destination, priority, True)
        self.insert_waiting_by_priority(coach, passenger)
        return "Added to Waiting List:\n(" + passenger_id + ", " + name + ")"

    def cancel_ticket(self, train_id, coach_id, passenger_id):
        train = self.find_train(train_id)
        if train is None:
            return "Error:\nTrain not found: " + train_id

        coach = self.find_coach(train, coach_id)
        if coach is None:
            return "Error:\nCoach not found: " + coach_id

        removed = self.remove_confirmed_passenger(coach, passenger_id)
        if removed is not None:
            output = "Ticket Cancelled:\n(" + removed.passenger_id + ", " + removed.name + ")"
            promoted = self.promote_waiting_passenger(coach, removed.seat_number)
            if promoted is not None:
                output += "\nWaiting List Passenger Promoted:\n(" + promoted.passenger_id + ", " + promoted.name + ", Seat No:" + str(promoted.seat_number) + ")"
            merge_message = self.merge_underutilized_coaches(train)
            if merge_message != "":
                output += "\n" + merge_message
            return output

        removed = self.remove_waiting_passenger(coach, passenger_id)
        if removed is not None:
            return "Waiting List Ticket Cancelled:\n(" + removed.passenger_id + ", " + removed.name + ")"

        return "Error:\nPassenger not found: " + passenger_id

    def split_train(self, train_id, coach_id):
        train = self.find_train(train_id)
        if train is None:
            return "Error:\nTrain not found: " + train_id

        previous = None
        current = train.coach_head
        while current is not None:
            if current.coach_id == coach_id:
                if previous is None:
                    return "Error:\nCannot split from first coach: " + coach_id
                previous.next = None
                new_train_id = self.make_split_train_id(train_id)
                new_train = TrainNode(new_train_id, train.train_name + "_Split", train.source, train.destination)
                new_train.coach_head = current
                self.append_train_node(new_train)
                return "Train Split Successful:\nNew Train Created Starting From Coach " + coach_id
            previous = current
            current = current.next

        return "Error:\nCoach not found: " + coach_id

    def display_train(self, train_id):
        train = self.find_train(train_id)
        if train is None:
            return "Error:\nTrain not found: " + train_id

        if self.has_coach_cycle(train):
            return "Error:\nCycle detected in coach links for train " + train_id

        return "Train Details:\n" + self.train_details(train)

    def display_all(self):
        if self.train_head is None:
            return "Complete Railway Structure:\nEmpty"

        output = "Complete Railway Structure:\n"
        current = self.train_head
        while current is not None:
            if self.has_coach_cycle(current):
                output += "Error:\nCycle detected in coach links for train " + current.train_id
            else:
                output += self.train_details(current)
            if current.next is not None:
                output += "\n"
            current = current.next
        output += "\nComplete Railway Structure Displayed Successfully"
        return output

    def detect_cycle_command(self, train_id):
        train = self.find_train(train_id)
        if train is None:
            return "Error:\nTrain not found: " + train_id
        if self.has_coach_cycle(train):
            return "Cycle Detected:\nTrain " + train_id
        return "No Cycle Detected:\nTrain " + train_id

    def train_details(self, train):
        output = "Train: " + train.train_id + " - " + train.train_name + "\n"
        if train.coach_head is None:
            output += "Coaches:\nEmpty"
        else:
            output += self.display_coaches_recursive(train.coach_head)
        return output

    def display_coaches_recursive(self, coach):
        if coach is None:
            return ""
        output = "Coach: " + coach.coach_id + "\nPassengers:\n"
        if coach.passenger_head is None:
            output += "Empty\n"
        else:
            output += self.display_passengers_recursive(coach.passenger_head, False)
        if coach.waiting_head is not None:
            output += "Waiting List:\n"
            output += self.display_passengers_recursive(coach.waiting_head, True)
        if coach.next is not None:
            output += self.display_coaches_recursive(coach.next)
        return output

    def display_passengers_recursive(self, passenger, waiting):
        if passenger is None:
            return ""
        if waiting:
            output = "(" + passenger.passenger_id + ", " + passenger.name + ")\n"
        else:
            output = "(" + passenger.passenger_id + ", " + passenger.name + ", Seat " + str(passenger.seat_number) + ")\n"
        return output + self.display_passengers_recursive(passenger.next, waiting)

    def find_train(self, train_id):
        current = self.train_head
        while current is not None:
            if current.train_id == train_id:
                return current
            current = current.next
        return None

    def find_coach(self, train, coach_id):
        current = train.coach_head
        while current is not None:
            if current.coach_id == coach_id:
                return current
            current = current.next
        return None

    def find_passenger_in_coach(self, coach, passenger_id):
        found = self.find_passenger(coach.passenger_head, passenger_id)
        if found is not None:
            return found
        return self.find_passenger(coach.waiting_head, passenger_id)

    def find_passenger(self, head, passenger_id):
        current = head
        while current is not None:
            if current.passenger_id == passenger_id:
                return current
            current = current.next
        return None

    def append_train_node(self, train):
        if self.train_head is None:
            self.train_head = train
            return
        current = self.train_head
        while current.next is not None:
            current = current.next
        current.next = train

    def append_passenger(self, coach, passenger):
        if coach.passenger_head is None:
            coach.passenger_head = passenger
            return
        current = coach.passenger_head
        while current.next is not None:
            current = current.next
        current.next = passenger

    def insert_waiting_by_priority(self, coach, passenger):
        if coach.waiting_head is None or passenger.waiting_priority < coach.waiting_head.waiting_priority:
            passenger.next = coach.waiting_head
            coach.waiting_head = passenger
            return
        previous = coach.waiting_head
        current = coach.waiting_head.next
        while current is not None and current.waiting_priority <= passenger.waiting_priority:
            previous = current
            current = current.next
        previous.next = passenger
        passenger.next = current

    def remove_confirmed_passenger(self, coach, passenger_id):
        previous = None
        current = coach.passenger_head
        while current is not None:
            if current.passenger_id == passenger_id:
                if previous is None:
                    coach.passenger_head = current.next
                else:
                    previous.next = current.next
                current.next = None
                return current
            previous = current
            current = current.next
        return None

    def remove_waiting_passenger(self, coach, passenger_id):
        previous = None
        current = coach.waiting_head
        while current is not None:
            if current.passenger_id == passenger_id:
                if previous is None:
                    coach.waiting_head = current.next
                else:
                    previous.next = current.next
                current.next = None
                return current
            previous = current
            current = current.next
        return None

    def promote_waiting_passenger(self, coach, seat_number):
        if coach.waiting_head is None:
            return None
        promoted = coach.waiting_head
        coach.waiting_head = promoted.next
        promoted.next = None
        promoted.seat_number = seat_number
        promoted.is_waiting = False
        self.append_passenger(coach, promoted)
        return promoted

    def count_passengers(self, head):
        count = 0
        current = head
        while current is not None:
            count += 1
            current = current.next
        return count

    def next_available_seat(self, coach):
        seat = 1
        while seat <= coach.capacity:
            if not self.seat_exists(coach.passenger_head, seat):
                return seat
            seat += 1
        return coach.capacity

    def seat_exists(self, passenger, seat_number):
        current = passenger
        while current is not None:
            if current.seat_number == seat_number:
                return True
            current = current.next
        return False

    def merge_underutilized_coaches(self, train):
        current = train.coach_head
        while current is not None and current.next is not None:
            next_coach = current.next
            if self.can_merge_coaches(current, next_coach):
                self.move_confirmed_passengers(next_coach, current)
                self.move_waiting_passengers(next_coach, current)
                current.capacity += next_coach.capacity
                current.coach_type = current.coach_type + "+" + next_coach.coach_type
                current.next = next_coach.next
                return "Underutilized Coaches Merged:\n(" + current.coach_id + ", " + next_coach.coach_id + ")"
            current = current.next
        return ""

    def can_merge_coaches(self, first, second):
        first_count = self.count_passengers(first.passenger_head)
        second_count = self.count_passengers(second.passenger_head)
        first_waiting = self.count_passengers(first.waiting_head)
        second_waiting = self.count_passengers(second.waiting_head)
        if first_waiting != 0 or second_waiting != 0:
            return False
        if first_count == 0 or second_count == 0:
            return False
        return first_count * 2 < first.capacity and second_count * 2 < second.capacity

    def move_confirmed_passengers(self, source, target):
        current = source.passenger_head
        while current is not None:
            next_node = current.next
            current.next = None
            current.seat_number = self.next_available_seat(target)
            self.append_passenger(target, current)
            current = next_node
        source.passenger_head = None

    def move_waiting_passengers(self, source, target):
        current = source.waiting_head
        while current is not None:
            next_node = current.next
            current.next = None
            self.insert_waiting_by_priority(target, current)
            current = next_node
        source.waiting_head = None

    def has_coach_cycle(self, train):
        slow = train.coach_head
        fast = train.coach_head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    def make_split_train_id(self, train_id):
        while True:
            candidate = train_id + "_S" + str(self.split_counter)
            self.split_counter += 1
            if self.find_train(candidate) is None:
                return candidate

    def parse_positive_integer(self, text):
        try:
            value = int(text)
            if value <= 0:
                return None
            return value
        except ValueError:
            return None


def main():
    system = RailwayReservationSystem()
    output_blocks = []

    try:
        input_file = open("inputPS2.txt", "r")
    except IOError:
        output_file = open("outputPS2.txt", "w")
        output_file.write("Error:\ninputPS2.txt not found")
        output_file.close()
        return

    for line in input_file:
        stripped = line.strip()
        if stripped != "":
            output_blocks.append(system.process_command(stripped))
    input_file.close()

    output_file = open("outputPS2.txt", "w")
    output_file.write("\n".join(output_blocks))
    output_file.close()


if __name__ == "__main__":
    main()
