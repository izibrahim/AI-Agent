from netmiko import ConnectHandler

def connect_to_node(nodename, command):
    # Define device details
    device = {
        'device_type': 'cisco_ios',  # or the appropriate device type
        'host': nodename,
        'username': 'admin',
        'password': 'C1sco54321', #C1sco12345
    }
    
    # Establish SSH connection to the device
    try:
        connection = ConnectHandler(**device)
        # Send the command
        output = connection.send_command(command,expect_string=r'#')
        # Close the connection
        connection.disconnect()
        return output
    except Exception as e:
        return f"Failed to execute command: {str(e)}"


