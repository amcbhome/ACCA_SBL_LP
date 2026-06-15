import streamlit as st
from model import solve_sbl_dispatch

st.set_page_config(page_title="SBL Dispatch Optimizer", layout="wide")

st.title("🚛 SBL Logistics & Dispatch Optimizer")
st.markdown("Input required dispatch targets across the distribution nodes to optimize system costs.")

st.sidebar.header("Depot Requirements (User Input)")
d1 = st.sidebar.number_input("Depot 1 Required Volume:", min_value=0.0, value=2500.0, step=50.0)
d2 = st.sidebar.number_input("Depot 2 Required Volume:", min_value=0.0, value=3100.0, step=50.0)
d3 = st.sidebar.number_input("Depot 3 Required Volume:", min_value=0.0, value=1250.0, step=50.0)

if st.sidebar.button("Run Dispatch Optimization"):
    results = solve_sbl_dispatch(d1, d2, d3)
    
    if results["status"] == "Optimal":
        st.success(f"System Status: Optimized successfully.")
        st.metric(label="Minimum Total Cost (Z)", value=f"£{results['min_z']:,.2f}")
        
        st.subheader("Optimal Dispatch Routing Assignments")
        
        # Display the allocations in a clean 3x3 layout
        vars_dict = results["variables"]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("**Depot 1 Routes**")
            st.write(f"Route X1: {vars_dict['X1']:,.1f} units")
            st.write(f"Route X2: {vars_dict['X2']:,.1f} units")
            st.write(f"Route X3: {vars_dict['X3']:,.1f} units")
            
        with col2:
            st.info("**Depot 2 Routes**")
            st.write(f"Route X4: {vars_dict['X4']:,.1f} units")
            st.write(f"Route X5: {vars_dict['X5']:,.1f} units")
            st.write(f"Route X6: {vars_dict['X6']:,.1f} units")
            
        with col3:
            st.info("**Depot 3 Routes**")
            st.write(f"Route X7: {vars_dict['X7']:,.1f} units")
            st.write(f"Route X8: {vars_dict['X8']:,.1f} units")
            st.write(f"Route X9: {vars_dict['X9']:,.1f} units")
    else:
        st.error(f"Optimization failed. The distribution constraint criteria cannot be met. (Status: {results['status']})")
