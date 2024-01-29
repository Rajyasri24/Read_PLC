import snap7

#Creating the Snap7 client (PLC interface)
plc = snap7.client.Client()

#Connecting to the PLC
plc.connect('192.168.0.5', 0, 1)  # Replace with your PLC's IP address, rack, and slot

#Reading 50 bytes from DB1
DB_bytearray = plc.db_read(1, 0, 50)

#Creating a dictionary to store names and their associated values
data = {
    'total_prod': snap7.util.get_int(DB_bytearray, 0),
    'prod_rate': snap7.util.get_real(DB_bytearray, 2),
    'message': snap7.util.get_string(DB_bytearray, 6),
}

#Print the extracted values using the dictionary
for name, value in data.items():
    print(f'{name}: {value}')

request = input("Enter the name of the value you want to extract: ")
if request in data:
    value = data[request]
    print(f'{request}: {value}')
else:
    print(f'Error: Value with name "{request}" not found in the dictionary.')

#Ensure to disconnect from the PLC
plc.disconnect()
