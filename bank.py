from datetime import datetime

class Bank:
    def __init__(self):
        self.accounts = {}
        self.users = {}
        self.transaction_history = {}
        self.train_tickets = {}

    def validate_username(self, username):
        if username in self.users:
            return False, "Username already exists"
        if not username[0].isalpha():
            return False, "Username must be start with a letter"
        if not any(char.isdigit() for char in username):
            return False, "Username must contain at least one number"
        if '_' not in username:
            return False, "Username must contain an underscore"
        if not 6 <= len(username) <= 20:
            return False, "Username length must be between 6 and 20 characters"
        return True, ""

    def validate_email(self, email):
        if '@' not in email:
            return False, "Invalid email format. Email must be contain '@'"
        if not email.endswith('.com'):
            return False, "Invalid email format. Email must be end with '.com'"
        if not any(char.isalpha() for char in email):
            return False, "Email must contain at least one letter"
        if not any(char.isdigit() for char in email):
            return False, "Email must contain at least one digit"
        if not any(char.islower() or char.isupper() for char in email): 
            return False, "Email must contain at least one upper or lower case letter"
        return True, ""

    def validate_password(self, password):
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(char.islower() for char in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        if not 8 <= len(password) <= 15:
            return False, "Password length must be between 8 and 15 characters"
        return True, ""

    
    def register(self):
        try:
            username = input("Enter Username: ")
            valid, message = self.validate_username(username)
            if not valid:
                return message

            email = input("Enter Email Address: ")
            valid, message = self.validate_email(email)
            if not valid:
                return message

            password = input("Enter Password: ")
            valid, message = self.validate_password(password)
            if not valid:
                return message

            self.users[username] = {'email': email, 'password': password}
            return "Registration successfully done!!!"
        except Exception as e:
            return "Error occurred during registration: " + str(e)

    def login_username_password(self, username, password):
        try:
            if username not in self.users:
                return "Username does not exist"

            if self.users[username]['password'] != password:
                return "Incorrect password"

            return "Login successful: Welcome " + username
        except Exception as e:
            return "Error occurred during login: " + str(e)

    def login_mpin(self, username, mpin):
        try:
            if username not in self.users:
                return "Username does not exist"

            if not mpin.isdigit() or len(mpin) != 6:
                return "MPIN must be a 6-digit number"
            return "Login successful: Welcome " + username
        except Exception as e:
            return "Error occurred during login: " + str(e)

    def validate_account_number(self, account_number):
        if account_number in self.accounts:
            return False, "Account number already exists"
        if not account_number.isdigit():
            return False, "Account number must contain only digits"
        if len(account_number) < 9 or len(account_number) > 18:
            return False, "Account number length must be between 9 and 18 digits"
        return True, ""

    def validate_account_holder(self, account_holder):
        if not account_holder.replace(" ", "").isalpha():
            return False, "Account holder's name must contain only alphabets"
        return True, ""

    def validate_initial_balance(self, initial_balance):
        try:
            initial_balance = float(initial_balance)
            if initial_balance < 100:
                return False, "Initial balance must be at least 100"
            return True, ""
        except ValueError:
            return False, "Initial balance must be a number"


    def record_transaction(self, account_number, transaction_type, amount):
        """Record a transaction in the transaction history."""
        try:
            timestamp = datetime.now()
            if account_number not in self.transaction_history:
                self.transaction_history[account_number] = []
            self.transaction_history[account_number].append({
                'timestamp': timestamp,
                'type': transaction_type,
                'amount': amount
            })
        except KeyError:
            raise ValueError("Invalid account number")
        except Exception as e:
            raise RuntimeError(f"Error occurred while recording transaction: {e}")


    def create_account(self):
        try:
            account_number = input("Enter Account Number : ")
            # Validate account number
            valid, message = self.validate_account_number(account_number)
            if not valid:
                return message

            account_holder = input("Enter Account Holder's Name : ")
            # Validate account holder
            valid, message = self.validate_account_holder(account_holder)
            if not valid:
                return message

            account_type = input("Enter Account Type (savings/checking/investment): ").lower()
            if account_type not in ['savings', 'checking', 'investment']:
                return "Invalid account type"

            initial_balance_str = input("Enter Initial Balance : ") 
            valid, message = self.validate_initial_balance(initial_balance_str) 
            if not valid:
                return message

            initial_balance = float(initial_balance_str)  
            if account_number in self.accounts:
                return "Account already exists"
            if initial_balance < 0:
                return "Initial balance must be non-negative"

            self.accounts[account_number] = {
                'account_holder': account_holder,
                'balance': initial_balance,
                'type': account_type
            }
            return "Account created successfully"
        except Exception as e:
            return "Error occurred during account creation: " + str(e)


    def deposit(self, account_number, amount):
        try:
            if account_number not in self.accounts:
                return "Account does not exist"
            if amount <= 0:
                return "Amount to deposit must be positive"

            self.accounts[account_number]['balance'] += amount
            self.record_transaction(account_number, 'deposit', amount)  
            return "Deposited " + str(amount) + " successfully. New balance : " + str(
                self.accounts[account_number]['balance'])
        except Exception as e:
            return "Error occurred during deposit: " + str(e)

    def withdraw(self, account_number, amount):
        try:
            if account_number not in self.accounts:
                return "Account does not exist"
            if amount <= 0:
                return "Amount to withdraw must be positive"

            if self.accounts[account_number]['balance'] < amount:
                return "Insufficient balance."

            self.accounts[account_number]['balance'] -= amount
            self.record_transaction(account_number, 'withdrawal', amount)  
            return "Withdrew " + str(amount) + " successfully. New balance : " + str(
                self.accounts[account_number]['balance'])
        except Exception as e:
            return "Error occurred during withdrawal: " + str(e)

    def check_balance(self, account_number):
        try:
            if account_number not in self.accounts:
                return "Account does not exist"

            return "Account Holder : " + self.accounts[account_number]['account_holder'] + "\nBalance : " + str(
                self.accounts[account_number]['balance'])
        except Exception as e:
            return "Error occurred while checking balance: " + str(e)

    def view_account_info(self, account_number):
        try:
            if account_number not in self.accounts:
                return "Account does not exist"
            
            account_info = self.accounts[account_number]
            account_holder = account_info['account_holder']
            account_type = account_info['type']
            balance = account_info['balance']
            
            info_str = f"Account Number: {account_number}\n"
            info_str += f"Account Holder: {account_holder}\n"
            info_str += f"Account Type: {account_type.capitalize()}\n"
            info_str += f"Balance: {balance}"
            
            return info_str
        except Exception as e:
            return "Error occurred while retrieving account info: " + str(e)

    def view_transaction_history(self, account_number):
        try:
            if account_number not in self.transaction_history:
                return "No transaction history available for this account"
            transactions = self.transaction_history[account_number]
            history_str = "Transaction History:\n"
            for transaction in transactions:
                history_str += f"Timestamp: {transaction['timestamp']}, Type: {transaction['type']}, Amount: {transaction['amount']}\n"
            return history_str
        except Exception as e:
            return "Error occurred while retrieving transaction history: " + str(e)
    
    def transfer_funds(self):
        try:
            from_account = input("Enter Your Account Number : ")
            
          
            if from_account not in self.accounts:
                print("Error: Sender account does not exist")
                return 

            to_account = input("Enter Recipient's Account Number : ")
            
            
            if to_account not in self.accounts:
                print("Error: Recipient account does not exist")
                return 

            amount = float(input("Enter Amount to Transfer : "))
             
            
            if amount <= 0:
                print("Error: Amount to transfer must be positive")
                return 
            
           
            if self.accounts[from_account]['balance'] < amount:
                print("Error: Insufficient balance for transfer")
                return 

           
            self.accounts[from_account]['balance'] -= amount
            self.accounts[to_account]['balance'] += amount 
            self.record_transaction(from_account, 'transfer_out', amount)
            self.record_transaction(to_account, 'transfer_in', amount)

        
            print(f"Transferred {amount} successfully from account {from_account} to account {to_account}. Sender's balance: {self.accounts[from_account]['balance']}, Recipient's balance: {self.accounts[to_account]['balance']}")
        except Exception as e:
            print(f"Error occurred during fund transfer: {e}")

    
    def validate_operator(self, operator):
        valid_operators = ["jio", "bsnl", "idea", "airtel"]
        
        return operator.lower() in valid_operators
   
    def validate_mobile_number(self, mobile_number):
    
        if len(mobile_number) != 10:
            return False
        if not mobile_number.isdigit():
            return False
        return True
    
    def validate_recharge_amount(self, amount):
    
        return amount > 0

    def validate_transaction_account(self, transaction_account):
       
        return transaction_account in self.accounts

    def recharge(self):
        try:
           
            operator = input("Enter operator (jio, bsnl, idea, airtel): ")
            if not self.validate_operator(operator):
                return "Invalid operator"

    
            mobile_number = input("Enter mobile number: ")
            if not self.validate_mobile_number(mobile_number):
                return "Invalid mobile number"

            amount = float(input("Enter recharge amount: "))
            if not self.validate_recharge_amount(amount):
                return "Invalid recharge amount"

            # Validate transaction account
            transaction_account = input("Enter transaction account: ")
            if not self.validate_transaction_account(transaction_account):
                return "Invalid transaction account"

            # Deduct amount from transaction account
            if self.accounts[transaction_account]['balance'] < amount:
                return "Insufficient balance in transaction account"
            self.accounts[transaction_account]['balance'] -= amount

            # Record recharge transaction
            self.record_transaction(transaction_account, 'recharge', amount)
            recharge_details = {
                'operator': operator,
                'mobile_number': mobile_number,
                'amount': amount,
                'transaction_account': transaction_account
            }
            recharge_message = f"Recharged {operator} number {mobile_number} with {amount} successfully."
            print("Recharge Details:")
            print("Operator:", operator)
            print("Mobile Number:", mobile_number)
            print("Recharge Amount:", amount)
            print("Transaction Account:", transaction_account)
            return recharge_message
        except Exception as e:
            return f"Error occurred during recharge: {e}"

    def pay_gas_bill(self):
        try:
            # Validate customer ID
            customer_id = input("Enter customer ID: ")
            if not self.validate_customer_id(customer_id):
                return "Invalid Customer ID"

            # Validate transaction account
            transaction_account = input("Enter transaction account: ")
            if not self.validate_transaction_account(transaction_account):
                return "Invalid transaction account"

            # Check if the amount is non-negative
            amount = float(input("Enter gas bill amount: "))
            if amount < 0:
                return "Amount cannot be negative"

            # Deduct bill amount from account balance
            if self.accounts[transaction_account]['balance'] < amount:
                return "Insufficient balance in transaction account"
            self.accounts[transaction_account]['balance'] -= amount

            # Record gas bill payment transaction
            self.record_transaction(transaction_account, 'gas_bill_payment', amount)

            return f"Gas bill payment of {amount} successful. New balance: {self.accounts[transaction_account]['balance']}"

        except Exception as e:
            return f"Error occurred during gas bill payment: {e}"

    def validate_customer_id(self, customer_id):
        # # Check if customer ID length is exactly 8 characters
        # if len(customer_id) != 8:
        #     return "Customer ID must be exactly 8 characters long."

        # Check if first 3 characters are alphabets and the last character is a digit
        if not customer_id[:3].isalpha() or not customer_id[3:].isdigit():
            return "Customer ID must start with 3 alphabetic characters followed by 5 digits."

        return True

    def pay_electricity_bill(self):
        try:
            # Validate customer ID
            customer_id = input("Enter customer ID: ")
            if not self.validate_customer_id(customer_id):
                return "Invalid Customer ID"

            # Validate transaction account
            transaction_account = input("Enter transaction account: ")
            if not self.validate_transaction_account(transaction_account):
                return "Invalid transaction account"

            # Check if the amount is non-negative
            amount = float(input("Enter electricity bill amount: "))
            if amount < 0:
                return "Amount cannot be negative"

            # Deduct bill amount from account balance
            if self.accounts[transaction_account]['balance'] < amount:
                return "Insufficient balance in transaction account"
            self.accounts[transaction_account]['balance'] -= amount

            # Record electricity bill payment transaction
            self.record_transaction(transaction_account, 'electricity_bill_payment', amount)

            return f"Electricity bill payment of {amount} successful. New balance: {self.accounts[transaction_account]['balance']}"

        except Exception as e:
            return f"Error occurred during electricity bill payment: {e}"


    def pay_cable_tv_bill(self):
        try:
            # Validate customer ID
            customer_id = input("Enter customer ID: ")
            if not self.validate_customer_id(customer_id):
                return "Invalid Customer ID"

            # Validate transaction account
            transaction_account = input("Enter transaction account: ")
            if not self.validate_transaction_account(transaction_account):
                return "Invalid transaction account"

            # Check if the amount is non-negative
            amount = float(input("Enter cable TV bill amount: "))
            if amount < 0:
                return "Amount cannot be negative"

            # Deduct bill amount from account balance
            if self.accounts[transaction_account]['balance'] < amount:
                return "Insufficient balance in transaction account"
            self.accounts[transaction_account]['balance'] -= amount

            # Record cable TV bill payment transaction
            self.record_transaction(transaction_account, 'cable_tv_bill_payment', amount)

            return f"Cable TV bill payment of {amount} successful. New balance: {self.accounts[transaction_account]['balance']}"

        except Exception as e:
            return f"Error occurred during cable TV bill payment: {e}"

    def bill_payment(self):
        print("\nChoose Bill Payment Option:")
        print("1. Recharge")
        print("2. Gas Bill")
        print("3. Electricity Bill")
        print("4. Cable-TV Bill")
        
        bill_choice = input("Enter your Choice (1 to 6): ")

        if bill_choice == '1':
            result = self.recharge()
            print(result)
        
        elif bill_choice == '2':
            result = self.pay_gas_bill()
            print(result)

        elif bill_choice == '3':
            result = self.pay_electricity_bill()  
            print(result)
        elif bill_choice == '4':
            result = self.pay_cable_tv_bill()  
            print(result)
        else:
            print("Invalid Choice. Please Try Again !!!")

    def validate_station_name(self, station_name):
        # Example validation: Ensure station name is not empty
        if not station_name.strip():
            return False
        return True

    def validate_travel_date(self, travel_date):
        try:
            
            travel_date_obj = datetime.strptime(travel_date, '%Y-%m-%d')
            current_date = datetime.now()
            if travel_date_obj < current_date:
                return False
            return True
        except ValueError:
            return False

    def validate_travel_class(self, travel_class):
  
        valid_classes = ['1', '2', '3', '4']
        return travel_class in valid_classes

    def validate_quota(self, quota):
       
        valid_quotas = ['1', '2', '3', '4', '5']
        return quota in valid_quotas

    def book_train_ticket(self, account_number):
        try:
            if account_number not in self.accounts:
                return "Account does not exist"

            from_station = input("Enter the departure station: ")
            if not self.validate_station_name(from_station):
                return "Invalid departure station name"

            to_station = input("Enter the destination station: ")
            if not self.validate_station_name(to_station):
                return "Invalid destination station name"

            travel_date = input("Enter the travel date (YYYY-MM-DD): ")
            if not self.validate_travel_date(travel_date):
                return "Invalid travel date"

            travel_class = input("Enter the travel class (1. Sleeper, 2. First AC, 3. Second AC, 4. Third AC): ")
            if not self.validate_travel_class(travel_class):
                return "Invalid travel class"

            quota = input("(1. General, 2. Ladies, 3. Sr. Citizen, 4. Physically Handicapped, 5. Tatkal): ")
            if not self.validate_quota(quota):
                return "Invalid quota"

          
            if travel_class == '1':
                fare = 500  
            elif travel_class == '2':
                fare = 1500  
            elif travel_class == '3':
                fare = 1000  
            elif travel_class == '4':
                fare = 800  
            else:
                return "Invalid travel class"

            if quota == '5':
                fare += 500 
            if self.accounts[account_number]['balance'] < fare:
                return "Insufficient balance to book ticket"
            self.accounts[account_number]['balance'] -= fare

            # Record the transaction
            self.record_transaction(account_number, 'train_ticket_booking', fare)

            # Store ticket details
            self.train_tickets[account_number] = {
                'from_station': from_station,
                'to_station': to_station,
                'travel_date': travel_date,
                'travel_class': travel_class,
                'quota': quota,
                'fare': fare
            }
            
            return "Train ticket booked successfully"

        except Exception as e:
            return f"Error occurred during train ticket booking: {e}"

    def view_train_ticket_details(self, account_number):
        try:
            if account_number not in self.train_tickets:
                return "No train ticket booked for this account"

            ticket_details = self.train_tickets[account_number]
            details_str = "Train Ticket Details:\n"
            details_str += f"From Station: {ticket_details['from_station']}\n"
            details_str += f"To Station: {ticket_details['to_station']}\n"
            details_str += f"Travel Date: {ticket_details['travel_date']}\n"
            details_str += f"Travel Class: {ticket_details['travel_class']}\n"
            details_str += f"Quota: {ticket_details['quota']}\n"
            details_str += f"Fare: {ticket_details['fare']}\n"
            return details_str
        except Exception as e:
            return f"Error occurred while retrieving train ticket details: {e}"
    def cancel_train_ticket(self, account_number):
        try:
            if account_number not in self.train_tickets:
                return "No train ticket booked for this account"

            ticket_details = self.train_tickets[account_number]

            self.accounts[account_number]['balance'] += ticket_details['fare']

            del self.train_tickets[account_number]

            self.record_transaction(account_number, 'train_ticket_cancellation', ticket_details['fare'])

            return "Train ticket canceled successfully"
        except Exception as e:
            return f"Error occurred during train ticket cancellation: {e}"
    
    def perform_operations(self, username):
        if username not in self.users:
            print("You need to register first.")
            return
        while True:
            print("\n1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Check Balance")
            print("5. View Account Information")
            print("6. View Transaction History")
            print("7. Transfer Funds")
            print("8. Bill Payment")
            print("9. Train Ticket booking")
            print("10. Logout")
            operation_choice = input("\nEnter your Choice (1 to 9): ")

            if operation_choice == '1':
                result = self.create_account()
                print(result)

            elif operation_choice == '2':
                account_number = input("Enter Account Number : ")
                amount = float(input("Enter Amount to Deposit : "))
                result = self.deposit(account_number, amount)
                print(result)

            elif operation_choice == '3':
                account_number = input("Enter Account Number : ")
                amount = float(input("Enter Amount to Withdraw : "))
                result = self.withdraw(account_number, amount)
                print(result)

            elif operation_choice == '4':
                account_number = input("Enter Account Number : ")
                result = self.check_balance(account_number)
                print(result)

            elif operation_choice == '5':
                account_number = input("Enter Account Number: ")
                result = self.view_account_info(account_number)
                print(result)

            elif operation_choice == '6':
                account_number = input("Enter Account Number: ")
                result = self.view_transaction_history(account_number)
                print(result)

            elif operation_choice == '7':
                result = self.transfer_funds()
                print(result)

            elif operation_choice == '8':
                self.bill_payment()

            elif operation_choice == '9':
                while True:
                    print("\nTrain Ticket Options:")
                    print("1. Book Train Ticket")
                    print("2. Cancel Train Ticket")
                    print("3. View Details of Ticket")
                    print("4. Exit")

                    ticket_choice = input("Enter your Choice (1, 2, or 3): ")
                    
                    if ticket_choice == '1':
                        account_number = input("Enter Account Number: ")
                        result = self.book_train_ticket(account_number)
                        print(result)
                    elif ticket_choice == '2':
                        account_number = input("Enter Account Number: ")
                        result = self.cancel_train_ticket(account_number)
                        print(result)
                    elif ticket_choice == '3':
                        account_number = input("Enter Account Number: ")
                        result = self.view_train_ticket_details(account_number)
                        print(result)
                    elif ticket_choice == '4':
                        print("Exiting train ticket operations.")
                        break 
                    else:
                        print("Invalid Choice. Please Try Again !!!")

            elif operation_choice == '10':
                print("Logging out...")
                break

            else:
                print("Invalid Choice. Please Try Again !!!")


bank = Bank()  # This is a Bank object
print("============================================================================================")
print("                           \n****** Bank Management System ******                           ")
print("============================================================================================")

try:
    while True:
        print("\n1. Registration")
        print("2. Login")
        print("3. Exit")
        choice = input("\nEnter your Choice (1 to 3): ")

        if choice == '1':
            result = bank.register()
            print(result)

        elif choice == '2':
            print("1. Login with Username and Password")
            print("2. Login with MPIN")
            login_choice = input("Enter your Choice (1 or 2): ")

            if login_choice == '1':
                username = input("Enter Username: ")
                password = input("Enter Password: ")
                result = bank.login_username_password(username, password)
                print(result)
                if "Login successful" in result:
                    bank.perform_operations(username)

            elif login_choice == '2':
                username = input("Enter Username: ")
                mpin = input("Enter MPIN: ")
                result = bank.login_mpin(username, mpin)
                print(result)
                if "Login successful" in result:
                    bank.perform_operations(username)


            else:
                print("Invalid Choice. Please Try Again !!!")

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid Choice. Please Try Again !!!")

except Exception as e:
    print("An error occurred:", e)