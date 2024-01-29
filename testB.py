import json
import snap7

#Creating the Snap7 client (PLC interface)
plc_instance = snap7.client.Client()
json_file_path = "C:/Users/rajyasri/PycharmProjects/Config.json"
# Open and read the JSON file
with open(json_file_path, 'r') as file: data = json.load(file)

for plc in data:
    plc_value = plc.get("PLC", [])
    ip_address, rack, slot = plc_value[0], int(plc_value[1]), int(plc_value[2])
    # plc_instance.connect(ip_address, rack, slot)
    db_number = plc_value[3]
    print(ip_address, rack, slot , db_number)
    # DB_bytearray = plc_instance.db_read(db_number, 0, 50)

def get_plc_data(tagname):
    tag_details = data[0]['Tags'][tagname]
    if tag_details['Type'] == "int":
        tag_value = snap7.util.get_int(db_bytearray, tag_deatils['offset'])
    elif tag_details['Type'] == "real":
        tag_value = snap7.util.get_real(db_bytearray, tag_deatils['offset'])
    elif tag_details['Type'] == "string":
        tag_value = snap7.util.get_string(db_bytearray, tag_deatils['offset'])
    else:
        tag_value = None


# while True:
#     req = input('Give Tag')
#     try:
#         get_plc_data(req)
#     except:
#         print("Tag not found")

while True:
  for i in data[0]['Tags']:
    try:
        plc_data = get_plc_data(i)
        print(plc_data)
    except:
        print(f"Tag not found for {i}")
    time.sleep(2)


# read_value('prod')