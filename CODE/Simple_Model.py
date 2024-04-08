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
    # ... other products
}
capacities = {
    "Greece": 400000,
    "Poland": 540000,
    # ... other refineries
}
demands = {
    "Gasoline-87": {"Greece": 35000, "Poland": 22000},
    # ... other products and regions
}

# Additional data for transportation
tanker_rates = {
    'LR1': {'Gudrun': 30000, 'Trinity': 32000},
    'LR2': {'Garonne': 41000, 'Torm Rhone': 44000},
}
port_charges = {
    'Ceyhan': {'LR1': 124000, 'LR2': 135000},
    # ... other ports
}
fuel_costs = {
    'LR1': 3000, # Cost per hour
    'LR2': 3250,
}
# Times in days from port to refinery
shipping_times = {
    'Ceyhan': {'Greece': 2, 'Spain': 8, 'UK': 12},
    # ... other ports
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

# Add transportation cost with detailed calculations
transportation_cost = mdl.sum(
    (tanker_rates['LR2'][tanker] + port_charges[port]['LR2'] + fuel_costs['LR2'] * shipping_hours[port][ref]) * crude_shipping_vars[crude, ref]
    for crude, port in costs["crude"].items() for ref, tanker in tanker_rates['LR2'].items()
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