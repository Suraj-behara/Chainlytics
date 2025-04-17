# Simplified Sales Data Analysis Script for Retail_Data_Transactions.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Step 1: Load Data
df = pd.read_csv("Retail_Data_Transactions.csv")
print("Original Data:")
print(df.head())

# Step 2: Clean and Prepare Data
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['trans_date'] = pd.to_datetime(df['trans_date'], format="%d-%b-%y")
df['Month'] = df['trans_date'].dt.to_period('M').astype(str)
df['Year'] = df['trans_date'].dt.year

# Step 3: Load into SQLite Database
conn = sqlite3.connect("retail_sales_simple.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)

# Step 4: Run SQL Queries
query1 = "SELECT Year, COUNT(*) as Total_Transactions, SUM(tran_amount) as Total_Amount FROM transactions GROUP BY Year ORDER BY Year"
query2 = "SELECT Month, SUM(tran_amount) as Monthly_Sales FROM transactions GROUP BY Month ORDER BY Month"

yearly_summary = pd.read_sql_query(query1, conn)
monthly_sales = pd.read_sql_query(query2, conn)
monthly_sales['Month'] = pd.to_datetime(monthly_sales['Month'].astype(str))

print("\nYearly Summary:")
print(yearly_summary)

# Step 5: Visualize Monthly Sales
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales['Month'].values, monthly_sales['Monthly_Sales'].values, marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales Amount")
plt.grid(True)
plt.tight_layout()
plt.savefig("monthly_sales_trend_simple.png")
plt.show()

# Step 6: Export to Excel
with pd.ExcelWriter("simplified_sales_report.xlsx") as writer:
    df.to_excel(writer, sheet_name="Cleaned Transactions", index=False)
    yearly_summary.to_excel(writer, sheet_name="Yearly Summary", index=False)
    monthly_sales.to_excel(writer, sheet_name="Monthly Sales", index=False)

print("\nSimplified project execution completed. Reports saved.")