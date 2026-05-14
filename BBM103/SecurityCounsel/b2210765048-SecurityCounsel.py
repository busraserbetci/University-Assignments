#Büşra Şerbetci - 2210765048

# Function to calculate the counsel risk
def calculate_risk(core_accuracy, incidence, counsel):
    base_rate = core_accuracy / 100
    x = int(incidence.split("/")[0])
    y = int(incidence.split("/")[1])

    numerator = ((y - x) * (1 - base_rate))
    denominator = (x * base_rate) + numerator
    calculated_risk = (numerator / denominator)
    risk = calculated_risk * 100

    if counsel == "0":
        risk = "No Risk"
    else:
        return risk

    return risk

# Function to recommend action based on counsel and risk
def recommend_action(counsel, risk, name):
    if counsel == "Not Bomber":
        if risk > 40:
            return f"System suggests to arrest {name}."
        else:
            return f"System suggests to release {name}."
    else:
        if risk > 40:
            return f"System suggests to release {name}."
        else:
            return f"System suggests to arrest {name}."

# Function to create a new interrogee
def create_interrogee(data, interrogees):
    name, core_accuracy, counsel, incidence = data
    counsel_description = "Bomber" if counsel == "1" else "Not Bomber"
    if name not in interrogees:
        core_accuracy = float(core_accuracy) * 100  # Convert to percentage
        risk = calculate_risk(float(core_accuracy), incidence, counsel)
        if isinstance(risk, float):
            risk = "{:.2f}%".format(risk)  # Format as percentage with two decimal places
        interrogees[name] = {
            "Interrogee Name": name,
            "Core Accuracy": f"{core_accuracy:.2f}%",  # Format as percentage
            "Counsel": counsel_description,
            "Local Bomber Incidence": incidence,
            "Counsel Risk": risk
        }
        return f"Interrogee {name} is recorded."
    else:
        return f"Interrogee {name} cannot be recorded due to duplication."

# Function to remove an interrogee
def remove_interrogee(name, interrogees):
    if name in interrogees:
        del interrogees[name]
        return f"Interrogee {name} is removed."
    else:
        return f"Interrogee {name} cannot be removed due to absence."

# Function to list all interrogees
def list_interrogees(interrogees):
    header = "Interrogee Name\t\tCore Accuracy\tCounsel\t\tLocal Bomber Incidence\tCounsel Risk"
    separator = "-" * (len(header) + 20)
    output = [header, separator]

    for interrogee in interrogees.values():
        name = interrogee["Interrogee Name"]
        core_accuracy = interrogee["Core Accuracy"]
        counsel = interrogee["Counsel"]
        incidence = interrogee["Local Bomber Incidence"]
        counsel_risk = interrogee["Counsel Risk"]

        if counsel == "Not Bomber":
            info = f"{name}\t\t\t{core_accuracy}\t\t{counsel}\t{incidence}\t\t{counsel_risk}"
            output.append(info)
        else:
            info = f"{name}\t\t\t{core_accuracy}\t\t{counsel}\t\t{incidence}\t\t{counsel_risk}"
            output.append(info)

    return "\n".join(output)

# Function to handle risk command
def handle_risk(name, interrogees):
    if name in interrogees:
        if interrogees[name]["Counsel"] == "Not Bomber":
            return f"Interrogee {name} has no counsel risk."
        else:
            return f"Interrogee {name} has a counsel risk of {interrogees[name]['Counsel Risk']}."
    else:
        return f"Risk for {name} cannot be calculated due to absence."

# Function to handle recommendation command
def handle_recommendation(name, interrogees):
    if name in interrogees:
        counsel = interrogees[name]["Counsel"]
        counsel_risk = float(interrogees[name]["Counsel Risk"][:-1])
        return recommend_action(counsel, counsel_risk, name)
    else:
        return f"Recommendation for {name} cannot be calculated due to absence."

# Function to read commands from input file
def read_commands(filename):
    commands = []
    with open(filename, 'r') as file:
        for line in file:
            split_line = line.strip().split(' ', 1)
            if len(split_line) == 2:
                commands.append((split_line[0], split_line[1].strip()))
            elif len(split_line) == 1:
                commands.append((split_line[0], ''))
    return commands

# Function to save outputs to output file
def save_outputs(outputs, filename):
    with open(filename, 'w') as file:
        file.write(outputs)

# Main function to execute commands
def execute_commands(input_filename, output_filename):
    interrogees = {}
    commands = read_commands(input_filename)
    outputs = []

    for command, data in commands:
        if command == "create":
            output = create_interrogee(data.split(", "), interrogees)
        elif command == "remove":
            output = remove_interrogee(data, interrogees)
        elif command == "list":
            output = list_interrogees(interrogees)
        elif command == "risk":
            output = handle_risk(data, interrogees)
        elif command == "recommendation":
            output = handle_recommendation(data, interrogees)
        else:
            output = "Invalid command"

        outputs.append(output)

    save_outputs("\n".join(outputs), output_filename)

# Run the program
if __name__ == "__main__":
    execute_commands("agents_aid_inputs.txt", "agents_aid_outputs.txt")
