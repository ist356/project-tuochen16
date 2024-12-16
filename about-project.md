# About My Project

Student Name:  Tuo Chen 
Student Email:  tuchen@syr.edu 

### What it does
This project conducts an  data analysis on Superstore sales data, a fictional dataset that mimics the operations of a real-world retail company. The analysis aims to uncover valuable insights related to sales trends, customer behavior, and profitability to support data-driven decision-making. Specifically, it addresses:

1. **Product Categories**: Identifying the most and least profitable product categories to optimize inventory and marketing strategies.
2. **Geographical Insights**: Understanding regional sales dynamics to target marketing efforts and allocate resources effectively.
3. **Seasonal Trends**: Analyzing seasonal spikes in sales to enhance stock and promotional strategies during peak periods.

Key insights include:
- Top-performing products are phones, chairs, and storage products.
- Underperforming categories include copiers, furnishings, and fasteners.
- Seasonal trends show sales peaks during holidays and back-to-school seasons.

The project also provides actionable recommendations to improve sales and profitability across regions and categories.

### How you run my project
1. Clone or download the project repository.
2. Install the required Python libraries from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the Kaggle dataset `ishanshrivastava28/superstore-sales` using the script `get_dataset_xlsx.py`. Ensure you have Kaggle API credentials set up.
4. Run the `retail_analysis.py` file using the Streamlit framework:
   ```bash
   streamlit run code/retail_analysis.py
   ```
5. Interact with the visualizations and insights provided in the Streamlit dashboard.
6. Run all test code 
   ```bash
   pytest tests/test_processing_util.py
   ```

### Other things you need to know
- The dataset (`Superstore.xlsx`) should be placed in the `cache` folder.
- This project uses Streamlit for interactive visualization and analysis.
- Key Python libraries used include in `requirements.txt` file.
- Insights and recommendations are based on data analysis from the years 2011 to 2014.
