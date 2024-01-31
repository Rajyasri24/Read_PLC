import json
import snap7

def connect_plc():

    for plc in data:
        plc_value = plc.get("PLC", [])
        ip_address, rack, slot = plc_value[0], int(plc_value[1]), int(plc_value[2])
        plc_instance.connect(ip_address, rack, slot)
        print(ip_address, rack, slot)



def get_plc_data(tagname):


    DB_bytearray = plc_instance.db_read(2, 0, 250)
    tag_details = data[0]['Tags'][tagname]
    if tag_details['Type'] == "int":
        tag_value = snap7.util.get_int(DB_bytearray, tag_details['offset'])
    elif tag_details['Type'] == "real":
        tag_value = snap7.util.get_real(DB_bytearray, tag_details['offset'])
    elif tag_details['Type'] == "string":
        tag_value = snap7.util.get_string(DB_bytearray, tag_details['offset'])
    else:
        tag_value = None
    result_dict = {tagname: tag_value}
    return result_dict

#----------------------OPC-UA SERVER---------------------

import sys
sys.path.insert(0, "..")
import time
from opcua import ua, Server

if __name__ == "__main__":

    plc_instance = snap7.client.Client()
    json_file_path = "C:/Users/User/Downloads/Config.json"
    # Open and read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)


    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)
    objects = server.get_objects_node()
    myobj = objects.add_object(idx, "MyObject")
    connect_plc()
    #read_plc()
    #while True:
    for i in data[0]['Tags']:
        try:

            plc_data = get_plc_data(i)
            print(f'plc tag is {plc_data}')
        except:
            print(f"Tag not found for {i}")
    c = 0
    while True:
        if c == 0:
            for i in data[0]['Tags']:
                try:
                    res = get_plc_data(i)
                    globals()[i] = myobj.add_variable(idx, i, res[i])
                    globals()[i].set_writable()

                    print(f"{i} - Node Address: {globals()[i].nodeid} and data is {res}")
                except Exception as e:
                    print(e)
            server.start()
            c = 1
        for i in data[0]['Tags']:
            try:
                res = get_plc_data(i)
                globals()[i].set_value(res[i])

                print(f"{i}   and data is {res}")
            except Exception as e:
                print(e)

        time.sleep(2)


    # # Loop through the dictionary and create global variables
    # for tag_name, tag_value in plc_data.items():
    #     print(tag_name , tag_value )
    #     globals()[tag_name] = myobj.add_variable(idx, tag_name, tag_value)
    #     globals()[tag_name].set_writable()
    #     node_addresses[tag_name] = globals()[tag_name].nodeid
    #     print(f"{tag_name} - Node Address: {node_addresses[tag_name]}")

    # Starting the server

    #server.stop()
    #
    # try:
    #     while True:
    #         # Update tag values (for demonstration purposes)
    #         for tag_name in tag_values:
    #             tag_value = tag_values[tag_name] + 1
    #             var_name = f'{tag_name}'
    #             globals()[var_name].set_value(tag_value)
    #             tag_values[tag_name] = tag_value
    #
    # except KeyboardInterrupt:
    #     # Stop the server on keyboard interrupt


