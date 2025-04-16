#!/usr/bin/env python
# coding: utf-8

# In[7]:


import sqlite3
import csv

# Connect to SQLite
conn = sqlite3.connect('student_performance.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender TEXT,
    math_score INTEGER,
    reading_score INTEGER,
    writing_score INTEGER
)
''')

# Read and insert data
try:
    with open('StudentsPerformance.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            gender = row['gender']
            math = int(row['math score'])
            reading = int(row['reading score'])
            writing = int(row['writing score'])
            cursor.execute('''
                INSERT INTO performance (gender, math_score, reading_score, writing_score)
                VALUES (?, ?, ?, ?)''', (gender, math, reading, writing))
    conn.commit()
    print("Data inserted successfully.\n")

    # Open output file
    with open('summary.txt', 'w', encoding='utf-8') as out:

        # 🔍 Query 1: Top 5 Math Scores
        out.write("🔹 Top 5 Math Scores:\n")
        cursor.execute('''
            SELECT gender, math_score
            FROM performance
            ORDER BY math_score DESC
            LIMIT 5;
        ''')
        for row in cursor.fetchall():
            out.write(f"{row}\n")

        # 🔍 Query 2: Average Scores by Gender
        out.write("\n🔹 Average Scores by Gender:\n")
        cursor.execute('''
            SELECT gender,
                   ROUND(AVG(math_score), 2) AS avg_math,
                   ROUND(AVG(reading_score), 2) AS avg_reading,
                   ROUND(AVG(writing_score), 2) AS avg_writing
            FROM performance
            GROUP BY gender;
        ''')
        for row in cursor.fetchall():
            out.write(f"{row}\n")

        # 🔍 Query 3: Pass/Fail (Math)
        out.write("\n🔹 Pass/Fail (First 10 by Math Score):\n")
        cursor.execute('''
            SELECT gender, math_score,
                CASE
                    WHEN math_score >= 70 THEN 'Pass'
                    ELSE 'Fail'
                END AS math_status
            FROM performance
            LIMIT 10;
        ''')
        for row in cursor.fetchall():
            out.write(f"{row}\n")

    print("Results saved to summary.txt ✅")

except Exception as e:
    print("Error:", e)
finally:
    conn.close()


# In[8]:


pip install matplotlib seaborn


# In[9]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Reconnect to DB
conn = sqlite3.connect('student_performance.db')

# 1️⃣ Top 5 Math Scores
df_top5 = pd.read_sql_query('''
    SELECT gender, math_score
    FROM performance
    ORDER BY math_score DESC
    LIMIT 5;
''', conn)

plt.figure(figsize=(6,4))
sns.barplot(data=df_top5, x='gender', y='math_score')
plt.title("Top 5 Math Scores")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("top_5_math_scores.png")
plt.show()

# 2️⃣ Average Scores by Gender
df_avg = pd.read_sql_query('''
    SELECT gender,
           AVG(math_score) AS avg_math,
           AVG(reading_score) AS avg_reading,
           AVG(writing_score) AS avg_writing
    FROM performance
    GROUP BY gender;
''', conn)

df_avg_melt = df_avg.melt(id_vars='gender', var_name='Subject', value_name='Average Score')

plt.figure(figsize=(8,5))
sns.barplot(data=df_avg_melt, x='gender', y='Average Score', hue='Subject')
plt.title("Average Scores by Gender")
plt.tight_layout()
plt.savefig("avg_scores_by_gender.png")
plt.show()

# 3️⃣ Pass/Fail Distribution (Math ≥ 70)
df_pass = pd.read_sql_query('''
    SELECT
        CASE
            WHEN math_score >= 70 THEN 'Pass'
            ELSE 'Fail'
        END AS status
    FROM performance;
''', conn)

plt.figure(figsize=(5,5))
df_pass['status'].value_counts().plot.pie(autopct='%1.1f%%', startangle=140, colors=['#66bb6a', '#ef5350'])
plt.title("Math Pass/Fail Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("pass_fail_pie.png")
plt.show()

conn.close()


# In[ ]:




