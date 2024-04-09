from docplex.mp.model import Model

# Initialize the CPLEX model
mdl = Model("ABSA_Oil")

# Example data structures (Fill these with your actual data)
costs = {
    "processing": 19,
    "crude": {"Azeri BTC": 57, "Poseidon Streams": 48, "Laguna": 35, "Snøhvit Condensate": 71},
    # Removed old transport costs since we will use detailed tanker rates and other costs
}

prices = {
    "Gasoline-87": 90.45,
    "Gasoline-89": 93.66,
    "Gasoline-92": 95.50,
    "Jet fuel": 61.25,
    "Diesel fuel": 101.64,
    "Heating oil": 66.36
    }

capacities = {
    "Greece": 400000,
    "Poland": 540000,
    "Spain": 625000, 
    "UK": 735000
    
    }

demands = {
    "Gasoline-87": {"Greece": 35000, "Poland": 22000, "Spain": 76000, "UK": 98000},
    "Gasoline-89": {"Greece": 45000, "Poland": 38000, "Spain": 103000, "UK": 52000},
    "Gasoline-92": {"Greece": 50000, "Poland": 60000, "Spain": 83000, "UK": 223000},
    "Jet fuel": {"Greece": 20000, "Poland": 25000, "Spain": 47000, "UK": 127000},
    "Diesel fuel": {"Greece": 75000, "Poland": 35000, "Spain": 125000, "UK": 87000},
    "Heating oil": {"Greece": 25000, "Poland": 205000, "Spain": 30000, "UK": 13000}
}


# Additional data for transportation
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


# Convert shipping times to hours for fuel cost calculation
shipping_hours = {port: {ref: days * 24 for ref, days in ref_times.items()} for port, ref_times in shipping_times.items()}

# Decision variables
purchase_vars = mdl.continuous_var_dict(costs["crude"].keys(), name="purchase")
production_vars = mdl.continuous_var_matrix(prices.keys(), capacities.keys(), name="produce")
# Updated transportation decision variables for crude oil using detailed tanker rates and other costs
crude_shipping_vars = mdl.continuous_var_matrix(costs["crude"].keys(), capacities.keys(), name="ship_crude")

# Objective function: Maximize profit
revenue = mdl.sum(prices[prod] * production_vars[prod, ref] for prod in prices for ref in capacities)
crude_cost = mdl.sum(costs["crude"][crude] * purchase_vars[crude] for crude in costs["crude"])
production_cost = mdl.sum(costs["processing"] * production_vars[prod, ref] for prod in prices for ref in capacities)

# Hypothetical mapping from crude oil types to ports
crude_to_port = {
    "Azeri BTC": "Ceyhan",
    "Poseidon Streams": "Houma",
    "Laguna": "Puerto Miranda",
    "Snøhvit Condensate": "Melkoya"
}

# Then, in your transportation cost calculation:
transportation_cost = mdl.sum(
    (tanker_rates[tanker_class][tanker] + port_charges[crude_to_port[crude]][tanker_class] + fuel_costs[tanker_class] * shipping_hours[crude_to_port[crude]][ref]) * crude_shipping_vars[crude, ref]
    for crude in costs["crude"].keys()
    for ref in capacities.keys()
    for tanker_class in tanker_rates.keys()
    for tanker in tanker_rates[tanker_class].keys()
)





mdl.maximize(revenue - crude_cost - production_cost - transportation_cost)

# Constraints
# Capacity, demand, and crude shipping constraints from your original code
for ref in capacities:
    mdl.add_constraint(mdl.sum(production_vars[prod, ref] for prod in prices) <= capacities[ref], ctname="capacity_%s" % ref)

# Demand satisfaction constraints
for prod in prices:
    for region in demands.get(prod, {}):
        mdl.add_constraint(mdl.sum(production_vars[prod, ref] for ref in capacities) >= demands[prod][region], ctname="demand_%s_%s" % (prod, region))

# Crude oil transportation constraints (transported crude does not exceed purchased crude)
for crude in costs["crude"]:
    mdl.add_constraint(mdl.sum(crude_shipping_vars[crude, ref] for ref in capacities) <= purchase_vars[crude], ctname="transport_%s" % crude)


# Solve the model
solution = mdl.solve()

# Print the solution
if solution:
    print("The objective value (Profit) is: ", mdl.objective_value)
    for crude in costs["crude"]:
        print("Purchase", purchase_vars[crude].solution_value, "barrels of crude oil", crude)
    for crude in costs["crude"]:
        for ref in capacities:
            print("Transport", crude_shipping_vars[crude, ref].solution_value, "barrels of", crude, "to refinery", ref)
    for prod in prices:
        for ref in capacities:
            print("Produce", production_vars[prod, ref].solution_value, "barrels of", prod, "at refinery", ref)
else:
    print("No solution found")