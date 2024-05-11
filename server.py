from socket import *
import json

SERVER_PORT = 12000
MENU_FILE = 'menu.json'
def load_menu():
    try:
        with open(MENU_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def save_menu(menu):
    with open(MENU_FILE, 'w') as file:
        json.dump(menu, file)

# Initialize menu
menu = load_menu()

# Create and bind the server socket
server = gethostbyname(gethostname())
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((server, SERVER_PORT))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection established with {addr}")

    try:
        while True:
            # Send initial prompt to the client
            connectionSocket.sendall('Owner Enter 1, Customer Enter 2, Quit Enter 0:'.encode())

            # Wait for the response from the client
            clientChoice = connectionSocket.recv(1024).decode().strip()

            if clientChoice == '1':
                connectionSocket.sendall('Enter username:'.encode())
                username = connectionSocket.recv(1024).decode().strip()

                connectionSocket.sendall('Enter password:'.encode())
                password = connectionSocket.recv(1024).decode().strip()

                if username == 'admin' and password == 'passadmin':
                    connectionSocket.sendall('Login successful. Enter "add", "edit", "delete", or "logout":'.encode())
                    while True:
                        adminAction = connectionSocket.recv(1024).decode().strip()

                        if adminAction == 'logout':
                            connectionSocket.sendall('Logged out. to Return to main menu press enter'.encode())
                            break  # Exit admin loop
                        elif adminAction == 'add':
                            connectionSocket.sendall('Enter item name:'.encode())
                            itemName = connectionSocket.recv(1024).decode().strip()
                            connectionSocket.sendall('Enter item price:'.encode())
                            itemPrice = connectionSocket.recv(1024).decode().strip()
                            menu[itemName] = float(itemPrice)
                            save_menu(menu)
                            connectionSocket.sendall(f'Item {itemName} added with price ${itemPrice}'.encode())
                        elif adminAction == 'edit':
                            connectionSocket.sendall('Enter item name to edit:'.encode())
                            itemName = connectionSocket.recv(1024).decode().strip()
                            if itemName in menu:
                                connectionSocket.sendall('Enter new price:'.encode())
                                itemPrice = connectionSocket.recv(1024).decode().strip()
                                menu[itemName] = float(itemPrice)
                                save_menu(menu)
                                connectionSocket.sendall(f'Item {itemName} updated with new price ${itemPrice}'.encode())
                            else:
                                connectionSocket.sendall(f'Item {itemName} not found.'.encode())
                        elif adminAction == 'delete':
                            connectionSocket.sendall('Enter item name to delete:'.encode())
                            itemName = connectionSocket.recv(1024).decode().strip()
                            if itemName in menu:
                                del menu[itemName]
                                save_menu(menu)
                                connectionSocket.sendall(f'Item {itemName} deleted.'.encode())
                            else:
                                connectionSocket.sendall(f'Item {itemName} not found.'.encode())
                        else:
                            connectionSocket.sendall('Invalid action. Enter "add", "edit", "delete", or "logout":'.encode())
                else:
                    connectionSocket.sendall('Login failed. Invalid username or password,to Return to main menu press enter.'.encode())

            elif clientChoice == '2':
                if menu:
                    menuStr = ', '.join(f"{item}: ${price}" for item, price in menu.items())
                    connectionSocket.sendall(f"Menu: {menuStr}".encode())
                else:
                    connectionSocket.sendall("Menu is currently empty. Returning to main menu.".encode())
                    continue  # Skip further steps if the menu is empty

                connectionSocket.sendall('Enter your order in the format item1,quantity1 item2,quantity2:'.encode())
                orderDetails = connectionSocket.recv(1024).decode().strip()

                totalPrice = 0
                orderItems = orderDetails.split()
                validOrder = True
                for order in orderItems:
                    try:
                        item, quantity = order.split(',')
                        if item in menu:
                            totalPrice += menu[item] * int(quantity)
                        else:
                            connectionSocket.sendall(f'Error: {item} is not on the menu. Returning to main menu.'.encode())
                            validOrder = False
                            break
                    except ValueError:
                        connectionSocket.sendall('Error: Incorrect order format. Please use item,quantity format. Returning to main menu.'.encode())
                        validOrder = False
                        break

                if validOrder:
                    connectionSocket.sendall(f'Total price: ${totalPrice}. Enter your delivery address:'.encode())
                    deliveryAddress = connectionSocket.recv(1024).decode().strip()
                    connectionSocket.sendall(f'Order confirmed! Your order will be delivered to {deliveryAddress}. Thank you!'.encode())

            elif clientChoice == '0':
                connectionSocket.sendall('Goodbye!'.encode())
                break
            else:
                connectionSocket.sendall('Invalid option, please try again.'.encode())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connectionSocket.close()
        print("Connection closed.")
