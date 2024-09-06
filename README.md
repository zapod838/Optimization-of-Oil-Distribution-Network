# Optimization of Oil Distribution Network

This repository contains the source code and documentation for the "Optimization of Oil Distribution Network" project conducted as part of the EC6055: Prescriptive Analytics Group Project at MSc in Business Analytics. The project focuses on streamlining purchasing, production, and transportation activities for ABSA Oil refineries across Europe using advanced optimization models.

## Project Overview

The goal of this project was to enhance operational efficiencies within ABSA Oil's distribution network. We developed several models to optimize different aspects of the supply chain, from raw material procurement to product delivery, ensuring cost-effectiveness and demand fulfillment.

![Supply-chain-issues-in-petroleum-industry](https://github.com/user-attachments/assets/77639830-dd78-43dd-ac08-ff5f6e7d945a)


## Project Approach

The flowchart represents the iterative process involved in optimizing the oil distribution network for ABSA Oil refineries. This process can be broken down into the following key steps:

![Flowchart_updated](https://github.com/user-attachments/assets/7550079b-2d58-4af1-b3af-e8f4563ffdd0)


1. **Dataset Preparation**: The process begins by leveraging a dataset comprising various variables such as purchasing variables (`purchase_vars`), production variables (`production_vars`), and crude shipping variables (`crude_shipping_vars`). These variables serve as the foundation for defining the decision variables used in optimization models.

2. **Defining Decision Variables**: The next step is defining decision variables, which are the variables we control in order to optimize the supply chain. These decision variables are based on the dataset and are crucial in formulating the optimization model. They represent choices that need to be optimized, such as how much crude oil to purchase, how to allocate production capacity, and how to schedule transportation.

3. **Evaluate the Objective Function and Constraints**: After defining the decision variables, we evaluate them in relation to the objective function and constraints. This involves using optimization techniques (e.g., linear programming) to calculate cost-efficiency, profitability, and constraint satisfaction. Constraints might include refinery capacities, shipping limits, demand fulfillment, and other logistical considerations.

4. **Optimality Check**: Once the evaluation is complete, the process checks if the solution is optimal. If the current decision variables satisfy all constraints and optimize the objective function (e.g., minimizing cost or maximizing profit), the process concludes.

5. **Updating Decision Variables**: If optimality is not achieved, the decision variables are updated based on the feedback from the previous evaluation. This iterative loop continues until the solution is optimal, ensuring that the most efficient operational plan is identified.

The flowchart provides a clear representation of this optimization cycle, ensuring that the process is efficient and systematic.

## Technologies Used

- **Python**: Main programming language used for scripting and model development.
- **IBM Decision Optimization CPLEX**: Used for solving linear and integer optimization problems.
- **docplex library**: A Python library for modeling optimization problems, interfacing with CPLEX solvers.

## Repository Structure

- `src/`: Contains all the Python scripts used for model building and optimization.
- `data/`: Includes sample datasets used for modeling (Note: due to confidentiality, actual data might be omitted or anonymized).
- `docs/`: Documentation related to project setup, configuration, and detailed explanation of the methodology.
- `models/`: Stores serialized versions of trained models and optimization solutions.

## Models

1. **Maximizing Profit Model**: Optimizes production and procurement choices to maximize profitability while adhering to demand constraints.
2. **Minimizing Shipping Cost Model**: Focuses on scheduling and routing optimizations to minimize transportation costs.
3. **Profit Analysis Model**: Provides insights into potential profitability and operational cost reductions based on the optimized models.

## Setup and Installation

To set up this project locally:

```bash
git clone https://github.com/zapod838/optimization-oil-distribution.git
cd optimization-oil-distribution
pip install -r requirements.txt
```

## Usage

To run the optimization models:

```bash
python src/maximize_profit.py
python src/minimize_shipping_costs.py
```

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your proposed changes. Ensure to follow the existing code style and add unit tests for any new or changed functionality.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Team members: Eoin Holly, Karan Shankar, Manish Kamble, Rashmi Singh, Sanyam Singh Chauhan, Shabbir Yusufbhai Motorwala
- Instructors and course coordinators of EC6055: Prescriptive Analytics.
