import ctypes, json

def jsonToRawData(json_dict):
    """
    Converts a JSON dictionary into a raw byte array (c_ubyte array) that can be used for low-level data operations.

    Parameters:
        json_dict (dict): A Python dictionary to be converted into JSON format and then into raw bytes.

    Returns:
        tuple: A tuple containing:
            - json_data_raw (ctypes.c_ubyte array): The raw byte array representation of the JSON data.
            - json_data_size (int): The size of the JSON data in bytes.
    """    
    json_str = json.dumps(json_dict)
    json_data = bytearray(json_str.encode("utf-8"))
    json_data_size = len(json_str)
    json_data_raw = (ctypes.c_ubyte * json_data_size).from_buffer(json_data)
    return json_data_raw, json_data_size

