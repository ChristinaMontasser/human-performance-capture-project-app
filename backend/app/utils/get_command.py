import os, json
def get_command(model, file_extension, filename): 
    current_dir = os.path.dirname(__file__)
    json_file = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'database', 'command.json'))

    # Path to the uploads folder
    if file_extension in [".jpg", ".jpeg", ".png"]:
        data_type =  "image"
    elif file_extension in [".mp4", ".avi"]:
        data_type =  "video"
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    # Load the JSON commands
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            commands = json.load(f)
    else:
        raise FileNotFoundError(f"JSON file '{json_file}' does not exist.")

    # Generate key based on model and data_type
    model = model.split(':')[0]
    key = f'{model}_{data_type}'

    # Retrieve the command and replace the placeholder
    if key in commands:
        command = commands.get(key)
        if 'FILENAME' in command:
            # Replace placeholder with actual filename
            command = command.replace('FILENAME', filename)
            print(command)
            #return command
        if 'WithoutExte' in command:
            command = command.replace('WithoutExte', os.path.splitext(filename)[0])
        
        return command  # No placeholder, use as is
    else:
        raise KeyError(f"Command not found for {key} in {json_file}")
    
