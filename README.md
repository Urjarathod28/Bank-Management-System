# Bank-Management-System

Class Structure:
The Bank class encapsulates the entire banking system, including user management, account operations, transaction recording, and various banking functionalities.

User Registration and Login:
Methods like register, validate_username, validate_email, and validate_password facilitate user registration with validation checks for username, email, and password formats.
Users can log in using either a username and password or an MPIN, with corresponding methods like login_username_password and login_mpin.

Account Management:
Users can create accounts (create_account), deposit money (deposit), withdraw money (withdraw), and check their account balances (check_balance).
Account information such as holder's name, type, and balance can be viewed using view_account_info.

Transaction Handling:
The system records transactions for each account, including details like timestamp, transaction type, and amount. Methods like record_transaction manage this functionality.

Fund Transfer:
Users can transfer funds between accounts within the bank using the transfer_funds method.

Bill Payment:
Methods like pay_gas_bill, pay_electricity_bill, pay_cable_tv_bill, and recharge enable users to pay various bills and recharge mobile accounts.

Train Ticket Booking:
Users can book and cancel train tickets using methods like book_train_ticket, cancel_train_ticket, and view_train_ticket_details.

Error Handling:
The system incorporates error handling mechanisms to deal with invalid inputs, insufficient balances, and other exceptional scenarios during operations.

User Interface:
The program offers a command-line interface (CLI) for users to interact with the banking system, providing options for registration, login, account management, transactions, bill payments, and train ticket bookings.

Main Execution:
The main execution loop allows users to choose between registration, login, or exiting the system, with subsequent navigation through various banking functionalities.
