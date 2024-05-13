# Optimization of Oil Distribution Network

This repository contains the source code and documentation for the "Optimization of Oil Distribution Network" project conducted as part of the EC6055: Prescriptive Analytics Group Project at MSc in Business Analytics. The project focuses on streamlining purchasing, production, and transportation activities for ABSA Oil refineries across Europe using advanced optimization models.

## Project Overview

The goal of this project was to enhance operational efficiencies within ABSA Oil's distribution network. We developed several models to optimize different aspects of the supply chain, from raw material procurement to product delivery, ensuring cost-effectiveness and demand fulfillment.

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
git clone https://github.com/yourusername/optimization-oil-distribution.git
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
