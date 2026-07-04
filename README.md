# Railway Reservation System

A multi-level linked list implementation of a railway reservation system supporting confirmed passengers and waiting lists.

## Project Overview

This project implements a **Railway Reservation System** using a **multi-level linked list** data structure. It efficiently manages train information, coaches, confirmed passengers, and waiting-list passengers.

## Data Structure

The system uses a three-level linked list hierarchy:

1. **Train Level**: Head pointer to the train linked list
2. **Coach Level**: Each train contains a linked list of coaches
3. **Passenger Level**: Each coach contains two linked lists:
   - Confirmed passengers list
   - Waiting-list passengers list

## Key Features

- **Add Trains**: Register new trains with details (ID, name, source, destination)
- **Add Coaches**: Add coaches to trains with specified capacity and type
- **Book Seats**: Reserve seats for passengers with automatic waiting-list management
- **Cancel Bookings**: Remove passengers and promote waiting-list candidates
- **View Availability**: Check seat availability across coaches
- **Waiting List Management**: Automatic promotion from waiting list when seats become available

## Classes

- **PassengerNode**: Represents a passenger with booking details
- **CoachNode**: Represents a coach with passenger and waiting-list linked lists
- **TrainNode**: Represents a train with coach linked list
- **RailwayReservationSystem**: Main system managing all operations

## Usage

```python
# Initialize the system
system = RailwayReservationSystem()

# Process commands from input
# Commands format: command_name::param1::param2::...
```

## Testing

- `inputPS2.txt`: Sample test input
- `outputPS2.txt`: Expected output
- `edge_cases_inputPS2.txt`: Edge case test input
- `edge_cases_outputPS2.txt`: Edge case expected output

## Assignment

This is part of the **Data Structures and Algorithms (DSAD)** curriculum - Assignment PS2 (Problem Set 2)

**Group**: G003

## Files

- `railway_reservation_ps2.py`: Main implementation
- `designPS2_G003.docx`: Design documentation
- `G003_A1_PS2_Multi level linked list/`: Assignment details folder
