int types_of_crudeoils = ...;
int product_names = ...;
int num_of_refineries = ...;
int total_tanker_vessels = ...;
int total_tanker_vessels_ships = ...;
range crude_oils = 1..types_of_crudeoils;
range total_products = 1..product_names;
range total_refineries = 1..num_of_refineries;
float product_price[total_products] = ...;
float crude_oil_price[crude_oils] = ...;
float product_upper[total_products] = ...;
float product_lower[total_products] = ...;
float oil_api[crude_oils] = ...;
float oil_quota[crude_oils] = ...;
float product_demand_individual[total_refineries, total_products] = ...;
float total_product_demand[total_products] = ...;
float refinery_capacity[total_refineries] = ...;
range tanker_vessel = 1..total_tanker_vessels;
range tanker_vessel_ships = 1..total_tanker_vessels_ships;
float tanker_price[tanker_vessel, tanker_vessel_ships] = ...;
float tanker_dwt_barrels[tanker_vessel, tanker_vessel_ships] = ...;
float port_charges[crude_oils, tanker_vessel] = ...;
float trip_days[crude_oils, total_refineries] = ...;
float fuel_consumptions_perday[tanker_vessel] = ...;
// decision variables
dvar int+ G[crude_oils, total_products, total_refineries];
dvar int+ I[total_products];
dvar boolean H[tanker_vessel, tanker_vessel_ships, crude_oils, total_refineries];
dvar boolean J[tanker_vessel, crude_oils, total_refineries];
maximize
(sum (p in total_products) total_product_demand[p] * product_price[p]
)
+ (sum (p in total_products) 0.93 * product_price[p] * (I[p] -
total_product_demand[p]))
- (sum (o in crude_oils) (sum (p in total_products, r in total_refineries) G[o,
p, r]) * (crude_oil_price[o] + 19))
- (sum (v in tanker_vessel) (sum (s in tanker_vessel_ships) (sum (o in
crude_oils,
r in total_refineries) H[v, s, o, r] * trip_days[o,
r] *
tanker_price[v, s])))
- (sum (v in tanker_vessel) (sum (o in crude_oils,
refinery in total_refineries) J[v, o, refinery] * trip_days[o, refinery] *
fuel_consumptions_perday[v]))
- (sum (v in tanker_vessel) (sum (s in tanker_vessel_ships, o in crude_oils,
refinery in total_refineries) H[v, s, o, refinery] * port_charges[o,
v]));
subject to {
// Constraint1 - Crude Capacity
forall(oil in crude_oils)
sum (product in total_products, refinery in total_refineries)
G[oil][product][refinery] <= oil_quota[oil];
// Constraint 2 - API Lower Limit
forall(r in total_refineries)
forall(p in total_products)
(sum (o in crude_oils) G[o][p][r] * oil_api[o]) >= ((sum (o
in crude_oils) G[o][p][r]) * product_lower[p]);
// Constraint 3 - API Upper Limit
forall(r in total_refineries)
forall(p in total_products)
(sum (o in crude_oils) G[o][p][r] * oil_api[o]) <= ((sum (o
in crude_oils) G[o][p][r]) * product_upper[p]);
// Constraint 5 - Individual Product and Individual Refinery Demand Constraint
forall(r in total_refineries)
forall(p in total_products)
(sum (o in crude_oils) G[o][p][r]) >=
product_demand_individual[r, p];
// Constraint 6 - Individual Product Total Demand Constraint
forall(p in total_products)
(sum (o in crude_oils, r in total_refineries) G[o, p, r]) ==
I[p];
// Constraint 7 - Capacity of a Refinery Constraint
forall(r in total_refineries)
(sum (p in total_products, o in crude_oils) G[o][p][r]) <=
refinery_capacity[r];
// Constraint 8 - Production should be more than Demand
forall(p in total_products)
I[p] >= total_product_demand[p];
// Constraint 9 - Transportation Constraint
forall(o in crude_oils)
forall(r in total_refineries)
sum(v in tanker_vessel, s in tanker_vessel_ships) H[v, s, o,
r] * tanker_dwt_barrels[v, s] >= sum (p in total_products) G[o,
p, r];
// Constraint 10 - fuel consumptions constraint
forall(o in crude_oils)
forall(r in total_refineries)
sum(v in tanker_vessel) J[v, o, r] *
trip_days[o, r] * fuel_consumptions_perday[v] >= sum (p in
total_products) G[o,
p, r];
// Making Ships 5 to 8 in Vessel 3 and 4 as Zero
forall(v in 3..4)
forall(s in 5..8)
forall(o in crude_oils, r in total_refineries)
H[v, s, o, r] == 0;
// Constraint 11- Ships selection constraint
forall(v in tanker_vessel)
forall(s in tanker_vessel_ships)
sum(o in crude_oils, r in total_refineries) H[v, s, o, r] <=
1;
};
