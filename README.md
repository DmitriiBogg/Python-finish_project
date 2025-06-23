Baseball Stats Dashboard (2000–2025)

This project focuses on collecting, processing, and visualizing historical baseball data from the Major League Baseball History website (baseball-almanac.com) for the years 2000 to 2025.
Main Project Components:

1. Web Scraping:
   Using Selenium, the script scrapes data on top players, teams, and statistics from the site.
2. Data Cleaning & Structuring:
   The collected data is cleaned and saved as CSV files, then imported into a SQLite database.
3. Database Querying:
   A simple CLI interface allows for executing SQL queries, including table joins.
4. Interactive Dashboard:
   Built with Streamlit, the dashboard presents clear and dynamic visualizations using Altair and Pandas.

Install dependencies:
pip install -r requirements.txt
To recreate the database:
python src/db_import.py
Run the dashboard:
streamlit run dashboard.py
