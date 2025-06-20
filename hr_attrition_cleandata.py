# Load the HR attrition dataset and display basic info and first few rows
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV
df_attrition = pd.read_csv('hr_attrition_data.csv')

# Basic shape and first 5 rows
print(df_attrition.shape)
print(df_attrition.head())

# Overall attrition rate
attrition_rate = df_attrition['Attrition'].value_counts(normalize=True) * 100
print(attrition_rate)

# Department-wise attrition counts and percentage
dept_attrition = df_attrition.groupby(['Department','Attrition']).size().unstack(fill_value=0)
# Calculate percentage leaving
dept_attrition['Attrition_%'] = dept_attrition['Yes'] / (dept_attrition['Yes'] + dept_attrition['No']) * 100
print(dept_attrition)

# Salary bands using quartiles
df_attrition['SalaryBand'] = pd.qcut(df_attrition['MonthlyIncome'], 4, labels=['Low','Mid-Low','Mid-High','High'])
salary_attrition = df_attrition.groupby(['SalaryBand','Attrition']).size().unstack(fill_value=0)
salary_attrition['Attrition_%'] = salary_attrition['Yes'] / (salary_attrition['Yes'] + salary_attrition['No']) * 100
print(salary_attrition)

# Plot department-wise attrition percentage
plt.figure(figsize=(6,4))
order = dept_attrition.sort_values('Attrition_%', ascending=False).index
sns.barplot(x=dept_attrition.loc[order,'Attrition_%'], y=order, color='salmon')
plt.xlabel('Attrition (%)')
plt.ylabel('Department')
plt.title('Department-wise Attrition Rate')
plt.tight_layout()
plt.show()

# Create a compact "dashboard" style figure (2x2) with key attrition visuals
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare metrics
overall_attrition_pct = (df_attrition['Attrition'] == 'Yes').mean() * 100

# Re-use already computed tables
dept_attr = df_attrition.groupby(['Department','Attrition']).size().unstack(fill_value=0)
dept_attr['Attrition_%'] = dept_attr['Yes'] / dept_attr.sum(axis=1) * 100

dept_order = dept_attr.sort_values('Attrition_%', ascending=False).index

salary_attr = df_attrition.groupby(['SalaryBand','Attrition']).size().unstack(fill_value=0)
salary_attr['Attrition_%'] = salary_attr['Yes'] / salary_attr.sum(axis=1) * 100

promo_attr = df_attrition.groupby(['PromoBand','Attrition']).size().unstack(fill_value=0)
promo_attr['Attrition_%'] = promo_attr['Yes'] / promo_attr.sum(axis=1) * 100

# Build figure
plt.figure(figsize=(12,8))

# KPI text box
ax0 = plt.subplot2grid((2,2), (0,0))
ax0.text(0.5,0.5, str(round(overall_attrition_pct,1)) + '%', fontsize=48, ha='center', va='center', color='crimson', weight='bold')
ax0.text(0.5,0.15, 'Overall Attrition Rate', fontsize=14, ha='center', va='center')
ax0.axis('off')

# Department bar
ax1 = plt.subplot2grid((2,2), (0,1))
sns.barplot(x=dept_attr.loc[dept_order,'Attrition_%'], y=dept_order, ax=ax1, palette='viridis')
ax1.set_xlabel('Attrition (%)')
ax1.set_ylabel('Department')
ax1.set_title('By Department')

# Salary band bar
ax2 = plt.subplot2grid((2,2), (1,0))
order_salary = ['Low','Mid-Low','Mid-High','High']
sns.barplot(x=salary_attr.loc[order_salary,'Attrition_%'], y=order_salary, ax=ax2, palette='magma')
ax2.set_xlabel('Attrition (%)')
ax2.set_ylabel('Salary Band')
ax2.set_title('By Salary Band')

# Promotion bar
ax3 = plt.subplot2grid((2,2), (1,1))
order_promo = ['0','1-2','3-4','5+']
sns.barplot(x=promo_attr.loc[order_promo,'Attrition_%'], y=order_promo, ax=ax3, palette='Blues')
ax3.set_xlabel('Attrition (%)')
ax3.set_ylabel('Years Since Last Promotion')
ax3.set_title('By Promotion Recency')

plt.suptitle('Employee Attrition Dashboard', fontsize=16, weight='bold')
plt.tight_layout(rect=[0,0,1,0.96])
plt.show()