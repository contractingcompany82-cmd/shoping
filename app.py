import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Al-Khaleej Manpower ERP", layout="wide", page_icon="✈️")

# --- SESSION STATE INITIALIZATION (Simulating Database) ---
if 'candidates' not in st.session_state:
    # Sample Data
    data = {
        'ID': [101, 102, 103],
        'Name': ['Rahul Kumar', 'Mohammad Ali', 'John Doe'],
        'Passport_No': ['P123456', 'P987654', 'P456789'],
        'Passport_Expiry': [datetime(2028, 5, 20), datetime(2024, 1, 15), datetime(2026, 8, 10)],
        'Iqama_No': ['2456789012', '2345678901', 'None'],
        'Iqama_Expiry': [datetime(2025, 12, 1), datetime(2024, 2, 28), None],
        'Visa_Status': ['Stamped', 'MOFA Ready', 'Medical Pending'],
        'Country': ['Saudi Arabia', 'UAE', 'Qatar'],
        'Agent_Name': ['Agent A', 'Agent B', 'Agent A'],
        'Agent_Commission': [1500, 2000, 1200]
    }
    st.session_state['candidates'] = pd.DataFrame(data)

if 'attendance' not in st.session_state:
    st.session_state['attendance'] = pd.DataFrame(columns=['Date', 'ID', 'Name', 'Status'])

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏗️ Manpower ERP")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Visa Processing", "Passport & Iqama", "Agent Commission", "Payroll & HR"])

# --- MODULE 1: DASHBOARD ---
if menu == "Dashboard":
    st.title("📊 ERP Dashboard")
    
    df = st.session_state['candidates']
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Candidates", len(df))
    col2.metric("Saudi Visas", len(df[df['Country'] == 'Saudi Arabia']))
    col3.metric("Medical Pending", len(df[df['Visa_Status'] == 'Medical Pending']))
    col4.metric("Total Commission Due", f"${df['Agent_Commission'].sum():,}")

    st.markdown("---")
    
    # Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Visa Status Distribution")
        st.bar_chart(df['Visa_Status'].value_counts())
    
    with c2:
        st.subheader("Candidates by Country")
        st.bar_chart(df['Country'].value_counts())

# --- MODULE 2: VISA PROCESSING (Medical, MOFA, Wakalah) ---
elif menu == "Visa Processing":
    st.title("✈️ Visa Processing Workflow")
    
    tab1, tab2 = st.tabs(["Add New Candidate", "Update Status"])
    
    with tab1:
        with st.form("new_candidate"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Candidate Name")
            pp_no = c2.text_input("Passport Number")
            country = c1.selectbox("Target Country", ["Saudi Arabia", "UAE", "Qatar", "Kuwait"])
            agent = c2.text_input("Recruiting Agent Name")
            commission = c1.number_input("Agent Commission ($)", min_value=0)
            
            submitted = st.form_submit_button("Register Candidate")
            if submitted:
                new_data = {
                    'ID': random.randint(1000, 9999),
                    'Name': name,
                    'Passport_No': pp_no,
                    'Passport_Expiry': datetime.now() + timedelta(days=365*5), # Default 5 years
                    'Iqama_No': "Pending",
                    'Iqama_Expiry': None,
                    'Visa_Status': "Document Collection",
                    'Country': country,
                    'Agent_Name': agent,
                    'Agent_Commission': commission
                }
                st.session_state['candidates'] = pd.concat([st.session_state['candidates'], pd.DataFrame([new_data])], ignore_index=True)
                st.success("Candidate Added Successfully!")

    with tab2:
        st.subheader("Update Visa Stages")
        df = st.session_state['candidates']
        
        # Select Candidate
        candidate_id = st.selectbox("Select Candidate ID", df['ID'].unique())
        current_status = df.loc[df['ID'] == candidate_id, 'Visa_Status'].values[0]
        st.info(f"Current Status: **{current_status}**")
        
        # Workflow Actions
        new_status = st.selectbox("Update Status To:", 
                                  ["Document Collection", "Medical Pending", "Medical Fit", "MOFA Ready", "Wakalah Done", "Visa Stamped", "Deployed"])
        
        if st.button("Update Status"):
            st.session_state['candidates'].loc[st.session_state['candidates']['ID'] == candidate_id, 'Visa_Status'] = new_status
            st.success(f"Status updated to {new_status}")
            st.rerun()

# --- MODULE 3: PASSPORT & IQAMA MANAGEMENT ---
elif menu == "Passport & Iqama":
    st.title("🛂 Passport & Iqama Expiry Tracker")
    
    df = st.session_state['candidates']
    
    # Filter for expiring documents (Next 6 months)
    today = datetime.now()
    expiry_threshold = today + timedelta(days=180)
    
    st.subheader("⚠️ Critical Alerts (Expiring Soon)")
    
    # Logic to find expiring passports
    # Ensuring datetime type
    df['Passport_Expiry'] = pd.to_datetime(df['Passport_Expiry'])
    expiring_pp = df[(df['Passport_Expiry'] < expiry_threshold) & (df['Passport_Expiry'] > today)]
    
    if not expiring_pp.empty:
        st.error(f"Attention: {len(expiring_pp)} Passports expiring within 6 months!")
        st.dataframe(expiring_pp[['Name', 'Passport_No', 'Passport_Expiry']])
    else:
        st.success("No Passports expiring soon.")
        
    st.markdown("---")
    st.subheader("📂 Full Database")
    st.dataframe(df)

# --- MODULE 4: AGENT COMMISSION ---
elif menu == "Agent Commission":
    st.title("💰 Agent Accounts")
    
    df = st.session_state['candidates']
    
    # Group by Agent
    agent_summary = df.groupby('Agent_Name')['Agent_Commission'].sum().reset_index()
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("Commission Summary")
        st.dataframe(agent_summary)
        
    with c2:
        st.subheader("Detailed Breakdown")
        selected_agent = st.selectbox("Select Agent", df['Agent_Name'].unique())
        filtered_data = df[df['Agent_Name'] == selected_agent]
        st.table(filtered_data[['Name', 'Country', 'Visa_Status', 'Agent_Commission']])
        
        total = filtered_data['Agent_Commission'].sum()
        st.markdown(f"### Total Payable: **${total}**")

# --- MODULE 5: PAYROLL & HR ---
elif menu == "Payroll & HR":
    st.title("👷 Salary & Attendance")
    
    tab1, tab2 = st.tabs(["Mark Attendance", "Salary Slip"])
    
    with tab1:
        st.subheader("Daily Attendance")
        date = st.date_input("Date", datetime.now())
        
        with st.form("attendance_form"):
            df = st.session_state['candidates']
            # Creating a checkbox for every employee
            attendance_data = {}
            for index, row in df.iterrows():
                attendance_data[row['ID']] = st.checkbox(f"{row['Name']} (ID: {row['ID']})", value=True)
            
            submit_att = st.form_submit_button("Save Attendance")
            
            if submit_att:
                for emp_id, is_present in attendance_data.items():
                    status = "Present" if is_present else "Absent"
                    name = df.loc[df['ID'] == emp_id, 'Name'].values[0]
                    new_record = {'Date': date, 'ID': emp_id, 'Name': name, 'Status': status}
                    st.session_state['attendance'] = pd.concat([st.session_state['attendance'], pd.DataFrame([new_record])], ignore_index=True)
                st.success("Attendance Marked!")
    
    with tab2:
        st.subheader("Generate Salary Slip")
        emp_id = st.selectbox("Select Employee", st.session_state['candidates']['ID'].unique())
        basic_salary = st.number_input("Basic Salary (SAR/AED)", value=2500)
        
        if st.button("Calculate Salary"):
            # Count present days
            att_df = st.session_state['attendance']
            if not att_df.empty:
                present_days = len(att_df[(att_df['ID'] == emp_id) & (att_df['Status'] == 'Present')])
            else:
                present_days = 0
            
            # Simple Calculation (Assuming 30 days month)
            daily_wage = basic_salary / 30
            final_salary = daily_wage * present_days
            
            st.markdown("---")
            st.markdown(f"### 🧾 Salary Slip")
            st.markdown(f"**Employee:** {st.session_state['candidates'].loc[st.session_state['candidates']['ID'] == emp_id, 'Name'].values[0]}")
            st.markdown(f"**Days Present:** {present_days}")
            st.markdown(f"**Net Salary:** {final_salary:.2f} SAR")
