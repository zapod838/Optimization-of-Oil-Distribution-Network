from cplex import Cplex
from cplex.exceptions import CplexError
from cplex import SparsePair
from cplex.exceptions import CplexError, CplexSolverError


# Example crude oil costs per barrel (you should replace these with your actual costs)
crude_oil_costs_per_barrel = {
    "Azeri BTC": 57,  # replace with actual cost
    "Poseidon Streams": 48,  # replace with actual cost
    "Laguna": 35,  # replace with actual cost
    "Snøhvit Condensate": 71  # replace with actual cost
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

tankers_barrels = {'GPT': {'Gudrun': 84500.0,
  'Ingeborg': 205334.99999999997,
  'Valborg': 173224.99999999997,
  'Estrid': 141115.0,
  'Rose': 101399.99999999999,
  'Cork Cat': 211249.99999999997,
  'Guam': 188857.49999999997,
  'Chance': 146523.0},
 'MRT': {'Ismine': 270400.0,
  'Signe': 358279.99999999994,
  'Venture': 226459.99999999997,
  'Pretty World': 316452.5,
  'Viking': 287300.0,
  'Limerick': 377714.99999999994,
  'York Gulls': 242092.49999999997,
  'Lancaster': 332211.75},
 'LR1': {'PTI Volans': 515449.99999999994,
  'Trinity': 574600.0,
  'Galway': 557700.0,
  'Glasgow': 650650.0},
 'LR2': {'Garonne': 929499.9999999999,
  'Torm Rhone': 1153425.0,
  'Thorpe': 1309750.0,
  'Venus': 1352000.0}}

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


fuel_costs = {
    "GPT": 2500,
    "MRT": 2750,
    'LR1': 3000, # Cost per hour
    'LR2': 3250,
}
# Times in days from port to refinery
shipping_times = {
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

# Invert the crude_to_tanker_type dictionary
tanker_type_to_crude = {v: k for k, v in crude_to_tanker_type.items()}

# Constants
QUANTITY_PER_TYPE_PER_DESTINATION = 137500  # 550,000 barrels divided by 4

# Create a list of ports, tankers, and destinations
ports = list(port_charges.keys())
tankers = [tanker for sublist in tankers_barrels.values() for tanker in sublist]
destinations = ["Greece", "Poland", "Spain", "UK"]

# Initialize CPLEX model
model = Cplex()

# Function to create consistent variable names
def create_var_name(tanker_type, tanker, destination):
    return f"{tanker_type}_{tanker}_{destination}"

# Decision variables: 1 if tanker t from tanker_type tt is used for destination d, 0 otherwise
for tanker_type in tankers_barrels:
    for tanker in tankers_barrels[tanker_type]:
        for destination in destinations:
            var_name = create_var_name(tanker_type, tanker, destination)
            model.variables.add(names=[var_name], types=["B"])  # Binary variable

# Objective function: minimize total cost
objective = []
# ...
for tanker_type in tankers_barrels:
    crude_type = tanker_type_to_crude[tanker_type]  # Get the crude type for this tanker type
    port = crude_to_port[crude_type]  # Get the port for this crude type
    for tanker in tankers_barrels[tanker_type]:
        for destination in destinations:
            var_name = create_var_name(tanker_type, tanker, destination)
            rate = tanker_rates[tanker_type].get(tanker, 0)
            port_charge = port_charges[port].get(tanker_type, 0)
            fuel_cost_per_hour = fuel_costs[tanker_type]
            shipping_days = shipping_times[port].get(destination, 0)
            fuel_cost = fuel_cost_per_hour * shipping_days * 24
            
            crude_oil_cost = crude_oil_costs_per_barrel[crude_type] * tankers_barrels[tanker_type][tanker]
            total_cost = rate + port_charge + fuel_cost + crude_oil_cost
            objective.append((var_name, total_cost))

model.objective.set_sense(model.objective.sense.minimize)
model.objective.set_linear(objective)


# ...

# Constraints
# Each destination receives a quarter of each type of crude oil
for destination in destinations:
    for oil_type, tanker_type in crude_to_tanker_type.items():
        vars_and_coeffs = [(create_var_name(tanker_type, tanker, destination), tankers_barrels[tanker_type][tanker])
                           for tanker in tankers if tanker in tankers_barrels[tanker_type]]
        constraint = SparsePair(ind=[var for var, coeff in vars_and_coeffs], 
                                val=[coeff for var, coeff in vars_and_coeffs])
        model.linear_constraints.add(lin_expr=[constraint], senses=["G"], rhs=[float(QUANTITY_PER_TYPE_PER_DESTINATION)])

# Each tanker is assigned to only one destination
for tanker_type in tankers_barrels:
    for tanker in tankers_barrels[tanker_type]:
        vars_and_coeffs = [(create_var_name(tanker_type, tanker, destination), 1.0)
                           for destination in destinations]
        constraint = SparsePair(ind=[var for var, coeff in vars_and_coeffs], 
                                val=[coeff for var, coeff in vars_and_coeffs])
        model.linear_constraints.add(lin_expr=[constraint], senses=["E"], rhs=[1])

# ...

# Solve the model
try:
    model.solve()
except CplexError as e:
    print(e)

# Output the solution
solution = model.solution
if solution.is_primal_feasible():
    print("Solution status = ", solution.get_status())
    print("Total cost = ", solution.get_objective_value())
    for tanker_type in tankers_barrels:
        for tanker in tankers_barrels[tanker_type]:
            for destination in destinations:
                var_name = create_var_name(tanker_type, tanker, destination)
                try:
                    if solution.get_values(var_name) > 0.5:  # Selected tanker
                        print(f"From {tanker_type}, Tanker {tanker} to {destination}")
                except CplexSolverError as e:
                    print(f"Error accessing variable '{var_name}': {e}")
else:
    print("No solution available")
