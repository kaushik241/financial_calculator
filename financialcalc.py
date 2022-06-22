import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Financial Planning Calculator")

st.title("Financial Planning Calculator XC")

st.header("Parameters")

current_year = st.number_input("Current Year: ", min_value=2022, format='%d')
number_of_working_years = st.number_input("Number of Working Years: ", min_value=0, format='%d')
number_of_year_post_retirement = st.number_input("Number Post Retirement Years: ", min_value=0, format='%d')
monthly_cash_requirement = st.number_input("Monthly Cash Requirement: ", min_value=0.0, format='%f')
inflation_rate = st.number_input("Inflation Rate: ", min_value=0.0, format='%f')
yearly_hike = st.number_input("Yearly Hike in SIP: ", min_value=0.0, format='%f')
investment = st.number_input("Investment(SIP_per_month): ", min_value=0.0, format='%f')
growth_rate = st.number_input("Expected Growth Rate: ", min_value=0.0, format='%f')


year_of_retirement = current_year + number_of_working_years
final_year = year_of_retirement + number_of_year_post_retirement - 1
yearly_cash_requirement = monthly_cash_requirement*12

df = pd.DataFrame(columns = ['year_of_retirement','year','years_away','corpus_required_today'],index=range(number_of_year_post_retirement))

for i in range(1,number_of_year_post_retirement+1):
    df['year_of_retirement'].iloc[i-1] = i
    df['year'].iloc[i-1] = year_of_retirement + i - 1
    df['years_away'].iloc[i-1] = number_of_working_years + i - 1
df['corpus_required_today'] = yearly_cash_requirement

df['future_value'] = df['years_away'].apply(lambda a : round(yearly_cash_requirement*((1 + inflation_rate)**a),2))

df2 = pd.DataFrame(columns = ['SI_no', 'months_remaining', 'months','investment','future_value'], index = range(number_of_working_years*12))

for i in range(len(df2)):
    df2['SI_no'].iloc[i] = i+1
    df2['months_remaining'].iloc[i] = len(df2) - i
    df2['months'].iloc[i] = ((df2['SI_no'].iloc[i] - 1) % 12) + 1
    df2['investment'].iloc[i] = investment
    if (i!=0 and df2['months'].iloc[i] == 1):
        investment = investment + investment*yearly_hike    

df2['future_value'] = df2['investment'] * ((1 + growth_rate)**(df2['months_remaining']/12))

st.header('First dataframe to calculate needed investment value')
st.dataframe(df)
st.line_chart(df['future_value'])



st.header('Second dataframe to calculate accumulated wealth at the year of retirement')
st.dataframe(df2)
st.line_chart(df2['future_value'])

st.write(f"Your accumulated wealth will be at {year_of_retirement} will be {sum(df2['future_value'])}")
st.write(f"You must have {sum(df['future_value'])} at {year_of_retirement} to retire healthy")
st.write(f"Your difference with target is: {sum(df2['future_value'])-sum(df['future_value'])}")

if (sum(df2['future_value'])-sum(df['future_value']) > 0):
    st.write('You can retire without any worry and your current investment plan.')
else:
    st.write('You have to invest more.')
