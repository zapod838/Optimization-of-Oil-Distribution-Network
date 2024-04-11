
import cplex
import sys
import itertools
from cplex.exceptions import CplexError
from cplex import SparsePair
from cplex.exceptions import CplexError, CplexSolverError


# Example crude oil costs per barrel (you should replace these with your actual costs)
crude_oil_costs_per_barrel = {
    "Azeri BTC": 57,  
    "Poseidon Streams": 48,  
    "Laguna": 35,  
    "Snøhvit Condensate": 71  
}

#Additional data for transportation
tanker_rates = {
    'GPT': {
        'Gudrun': 13000, 'Ingeborg': 22000, 'Valborg': 20000, 'Estrid': 15000, 'Rose': 14000,
        'Cork Cat': 23000, 'Guam': 21000, 'Chance': 16000
    },
    'MRT': {
        'Ismine': 25000, 'Signe': 27000, 'Venture': 23000, 'Pretty World': 25000, 'Viking': 26000,
        'Limerick': 28000, 'York Gulls': 25000, 'Lancaster': 26000
    },
    'LR1': {
        'PTI Volans': 30000, 'Trinity': 32000, 'Galway': 31000, 'Glasgow': 33000
    },
    'LR2': {
        'Garonne': 41000, 'Torm Rhone': 44000, 'Thorpe': 51000, 'Venus': 56000
    }
}

tankers_capicity_in_barrels = {'GPT': {'Gudrun': 84500,
  'Ingeborg': 205334,
  'Valborg': 173224,
  'Estrid': 141115,
  'Rose': 101399,
  'Cork Cat': 211249,
  'Guam': 188857,
  'Chance': 146523},
 'MRT': {'Ismine': 270400,
  'Signe': 358279,
  'Venture': 226459,
  'Pretty World': 316452,
  'Viking': 287300,
  'Limerick': 377714,
  'York Gulls': 242092,
  'Lancaster': 332211},
 'LR1': {'PTI Volans': 515449,
  'Trinity': 574600,
  'Galway': 557700,
  'Glasgow': 650650},
 'LR2': {'Garonne': 929499,
  'Torm Rhone': 1153425,
  'Thorpe': 1309750,
  'Venus': 1352000}}

port_charges = {
    'Ceyhan': {
        'GPT': 109000, 'MRT': 112000, 'LR1': 124000, 'LR2': 135000
    },
    'Houma': {
        'GPT': 111000, 'MRT': 114000, 'LR1': 138000, 'LR2': 159000
    },
    'Puerto Miranda': {
        'GPT': 135000, 'MRT': 147000, 'LR1': 158000, 'LR2': 169000  
    },
    'Melkoya': {
        'GPT': 136000, 'MRT': 147000, 'LR1': 156000, 'LR2': 177000
    }
}

# Cost per hour
fuel_costs = {
    "GPT": 2500,
    "MRT": 2750,
    'LR1': 3000, 
    'LR2': 3250,
}
# Times in days from port to refinery
shipping_times_in_days = {
    'Ceyhan': {'Greece': 2, 'Poland': 15, 'Spain': 8, 'UK': 12},
    'Houma': {'Greece': 20, 'Poland': 18, 'Spain': 16, 'UK': 15},
    'Puerto Miranda': {'Greece': 19, 'Poland': 20, 'Spain': 14, 'UK': 15},
    'Melkoya': {'Greece': 11, 'Poland': 3, 'Spain': 4, 'UK': 3}
}
# Hypothetical mapping from crude oil types to ports
crude_to_port = {
    "Azeri BTC": "Ceyhan",
    "Poseidon Streams": "Houma",
    "Laguna": "Puerto Miranda",
    "Snøhvit Condensate": "Melkoya"
}
crude_to_tanker_type = {
    "Azeri BTC": "GPT",
    "Poseidon Streams": "MRT",
    "Laguna": "LR1",
    "Snøhvit Condensate": "LR2"
}
# New quantities per destination
quantities_per_destination = {
    "UK": 183750,
    "Spain": 156250,
    "Poland": 135000,
    "Greece": 75000
}

# Invert the crude_to_tanker_type dictionary
tanker_type_to_crude = {v: k for k, v in crude_to_tanker_type.items()}
# Constants
#QUANTITY_PER_TYPE_PER_DESTINATION = 137500  # 550,000 barrels divided by 4

# Create a list of ports, tankers, and destinations
ports = list(port_charges.keys())
tankers = [tanker for sublist in tankers_capicity_in_barrels.values() for tanker in sublist]
destinations = ["Greece", "Poland", "Spain", "UK"]

# Correct instantiation of a Cplex object
model = cplex.Cplex()

# Variables: binary decision for each port, tanker, destination
# Format: "Port_Tanker_Destination"
variables = ["{}_{}_{}".format(port, tanker, destination) 
             for port, tanker, destination in itertools.product(ports, tankers, destinations)]

# Add variables to the model
model.variables.add(names=variables, types=["B"] * len(variables))

# Function to create consistent variable names 
def create_var_name(port, tanker, destination):
    return f"{port}_{tanker}_{destination}"

# Adjust the objective function calculation
objective = []
for tanker_type in tankers_capicity_in_barrels:
    crude_type = tanker_type_to_crude[tanker_type]  # Get the crude type for this tanker type
    port = crude_to_port[crude_type]  # Get the port for this crude type
    for tanker in tankers_capicity_in_barrels[tanker_type]:
        for destination in destinations:
            quantity = quantities_per_destination[destination]
            var_name = create_var_name(port, tanker, destination)
            rate = tanker_rates[tanker_type].get(tanker, 0)
            port_charge = port_charges[port].get(tanker_type, 0)
            fuel_cost_per_hour = fuel_costs[tanker_type]
            shipping_days = shipping_times_in_days[port].get(destination, 0)
            fuel_cost = fuel_cost_per_hour * shipping_days * 24
            crude_oil_cost = crude_oil_costs_per_barrel[crude_type] * quantity
            total_cost = rate + port_charge + fuel_cost + crude_oil_cost
            objective.append((var_name, total_cost))

model.objective.set_sense(model.objective.sense.minimize)
model.objective.set_linear(objective)

# Step 1: Create a dictionary for costs and capacities
costs_and_capacities = {}
for tanker_type in tankers_capicity_in_barrels:
    for tanker in tankers_capicity_in_barrels[tanker_type]:
        tanker_capacity = tankers_capicity_in_barrels[tanker_type][tanker]
        for port in ports:
            for destination in destinations:
                var_name = "{}_{}_{}".format(port, tanker, destination)
                rate = tanker_rates[tanker_type].get(tanker, 0)
                port_charge = port_charges[port].get(tanker_type, 0)
                fuel_cost_per_hour = fuel_costs[tanker_type]
                shipping_days = shipping_times_in_days[port].get(destination, 0)
                fuel_cost = fuel_cost_per_hour * shipping_days * 24
                total_cost = rate + port_charge + fuel_cost
                costs_and_capacities[var_name] = (total_cost, tanker_capacity)
                

allocated_boats = set()

sorted_boats_by_route = {}
for port in ports:
    for destination in destinations:
        required_quantity = quantities_per_destination[destination]

        # Filter boats that are not already allocated and have sufficient capacity for the required quantity
        eligible_boats = [(var_name, cost) for var_name, (cost, capacity) in costs_and_capacities.items()
                          if var_name.split('_')[1] not in allocated_boats and capacity >= required_quantity and var_name.startswith(port + "_")]
        
        if eligible_boats:
            # Sort by cost and select the cheapest boat
            sorted_boats = sorted(eligible_boats, key=lambda x: x[1])
            cheapest_boat = sorted_boats[0][0]
            sorted_boats_by_route[(port, destination)] = [cheapest_boat]

            # Add the selected boat to the allocated set
            allocated_boats.add(cheapest_boat.split('_')[1])
        else:
            # No eligible boats available for this route
            sorted_boats_by_route[(port, destination)] = []

# Rest of the constraints and model solving remains the same


# Constraint: Each boat can only be assigned to one route
for tanker in tankers:
    vars_for_tanker = [create_var_name(port, tanker, destination) for port in ports for destination in destinations]
    model.linear_constraints.add(
        lin_expr=[ [vars_for_tanker, [1] * len(vars_for_tanker)] ],
        senses=["L"],
        rhs=[1]
    )

for port in ports:
    for destination in destinations:
        quantity = quantities_per_destination[destination]
        vars_for_port_destination = []

        # Capacity coefficients for each variable
        capacity_coefficients = []

        for tanker in tankers:
            var_name = create_var_name(port, tanker, destination)
            vars_for_port_destination.append(var_name)

            # Determine the tanker type based on the tanker's name
            for tanker_type, tankers_list in tankers_capicity_in_barrels.items():
                if tanker in tankers_list:
                    # Get the capacity of the tanker
                    capacity = tankers_capicity_in_barrels[tanker_type][tanker]
                    break

            capacity_coefficients.append(capacity)

        # Adjust the right-hand side of the constraint to match the new quantity
        model.linear_constraints.add(
            lin_expr=[ [vars_for_port_destination, capacity_coefficients] ],
            senses=["G"],  # Greater than or equal to, to ensure enough capacity
            rhs=[quantity]
        )

# Existing constraints are defined here...
print(allocated_boats)
# Additional Constraint: Each port-destination pair should have exactly one tanker assigned
for port in ports:
    for destination in destinations:
        vars_for_port_destination = [create_var_name(port, tanker, destination) for tanker in tankers]
        # Add constraint for each port-destination pair
        model.linear_constraints.add(
            lin_expr=[[vars_for_port_destination, [1] * len(vars_for_port_destination)]],
            senses=["E"],  # "E" stands for equality
            rhs=[1]
        )


# Solve the model
try:
    model.solve()
    print("Model solved successfully.")
except CplexError as exc:
    print("Error solving model:", exc)
    sys.exit(1)  # Exit if model couldn't be solved

# Initialize total cost
total_cost = 0

# Retrieve and print the solution
solution_values = model.solution.get_values()
for var_name, value in zip(variables, solution_values):
    if value > 0.5:  # If the variable is part of the solution
        route_cost = costs_and_capacities[var_name][0]
        total_cost += route_cost  # Add the cost of this route to the total cost
        # print(f"{var_name} selected with a cost of {route_cost}")

# Print the total cost
print(f"Total cost of the solution: {total_cost}")

#print(allocated_boats)
# Check the solution status

# Check the solution status
solution = model.solution
if solution.is_primal_feasible():
    print("Solution status = ", solution.get_status())
    found_solution = False
    for tanker_type in tankers_capicity_in_barrels:
        for tanker in tankers_capicity_in_barrels[tanker_type]:
            for port in crude_to_port.values():
                for destination in destinations:
                    var_name = create_var_name(port, tanker, destination)
                    try:
                        if solution.get_values(var_name) > 0.5:
                            # Quantity required for the destination
                            quantity = quantities_per_destination[destination]
                            route_cost = costs_and_capacities[var_name][0]  # Get the route cost from the dictionary
                            print(f"From {port}, Tanker {tanker} to {destination}, transporting {quantity} barrels. Cost: {route_cost}")
                            found_solution = True
                    except CplexSolverError as e:
                        print(f"Error accessing variable '{var_name}': {e}")
    if not found_solution:
        print("No routes selected in the solution.")
else:
    print("No solution available.")
