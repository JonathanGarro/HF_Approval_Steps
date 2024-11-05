import streamlit as st
import pandas as pd

# Load data
file_path = 'path_to_file/Requests with Approval History.xlsx'
data = pd.read_excel(file_path, sheet_name='Summary', skiprows=5)

# Clean and rename columns
data.columns = ['Index', 'Program', 'GO Approval', 'Legal Approval', 
				'Legal Approval Post-GO', 'OE Approval', 
				'PD Approval', 'PO Approval', 'Grand Total']
data = data.dropna(subset=['Program']).reset_index(drop=True)

# Streamlit app
st.title("Approval Process Summary Dashboard")

# Sidebar filters
programs = st.sidebar.multiselect("Select Program", options=data['Program'].unique(), default=data['Program'].unique())
approval_steps = st.sidebar.multiselect(
	"Select Approval Step",
	options=['GO Approval', 'Legal Approval', 'Legal Approval Post-GO', 'OE Approval', 'PD Approval', 'PO Approval'],
	default=['GO Approval', 'Legal Approval', 'OE Approval', 'PD Approval', 'PO Approval']
)

# Filter data
filtered_data = data[(data['Program'].isin(programs))][['Program'] + approval_steps + ['Grand Total']]

# Display filtered data
st.dataframe(filtered_data)

# Display bar chart of elapsed hours by selected steps
for step in approval_steps:
	st.bar_chart(filtered_data.groupby('Program')[step].sum())

st.write("Grand Total of Elapsed Hours by Program")
st.bar_chart(filtered_data.groupby('Program')['Grand Total'].sum())