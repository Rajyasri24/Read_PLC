from opcua import Client

if __name__ == "__main__":
    # Create an OPC UA client
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")

    try:
        # Connect to the OPC UA server
        client.connect()
        print("Connected to OPC UA server")

        # Specify the node ID you want to retrieve (ns=4;i=2 in this case)
        node_id = "ns=2;i=2"

        # Get the specified node
        desired_node = client.get_node(node_id)

        # Read the current value of the node
        current_value = desired_node.get_value()
        print(f"Current value of node {node_id}: {current_value}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Disconnect from the OPC UA server
        client.disconnect()
        print("Disconnected from OPC UA server")
