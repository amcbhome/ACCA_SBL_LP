import pulp

def solve_sbl_dispatch(depot1_req, depot2_req, depot3_req):
    """
    Solves the SBL Minimization problem based on variable depot requirements.
    
    Parameters:
    depot1_req (float): Demand/dispatch volume for Equality Constraint 1 (originally 2,500)
    depot2_req (float): Demand/dispatch volume for Equality Constraint 2 (originally 3,100)
    depot3_req (float): Demand/dispatch volume for Equality Constraint 3 (originally 1,250)
    """
    [span_16](start_span)model = pulp.LpProblem("Minimize_Z", pulp.LpMinimize)[span_16](end_span)
    
    # 9 decision variables representing routes
    [span_17](start_span)X = {i: pulp.LpVariable(f\"X{i}\", lowBound=0, cat='Continuous') for i in range(1, 10)}[span_17](end_span)
    
    # Cost/Weight multipliers
    [span_18](start_span)Y = {[span_18](end_span)
        [span_19](start_span)1: 22, 2: 33, 3: 40,[span_19](end_span)
        [span_20](start_span)4: 27, 5: 30, 6: 22,[span_20](end_span)
        [span_21](start_span)7: 36, 8: 20, 9: 25[span_21](end_span)
    [span_22](start_span)}
    z = 5[span_22](end_span)
    
    # Objective function
    [span_23](start_span)model += pulp.lpSum(X[i] * Y[i] * z for i in range(1, 10)), "Objective_Function"[span_23](end_span)
    
    # Supply constraints mapped to dynamic inputs
    [span_24](start_span)model += X[1] + X[2] + X[3] == depot1_req, "Equality_Constraint_1"[span_24](end_span)
    [span_25](start_span)model += X[4] + X[5] + X[6] == depot2_req, "Equality_Constraint_2"[span_25](end_span)
    [span_26](start_span)model += X[7] + X[8] + X[9] == depot3_req, "Equality_Constraint_3"[span_26](end_span)
    
    # Destination capacity constraints (remain fixed at their upper bounds)
    [span_27](start_span)model += X[1] + X[4] + X[7] <= 2000, "Inequality_Constraint_1"[span_27](end_span)
    [span_28](start_span)model += X[2] + X[5] + X[8] <= 3000, "Inequality_Constraint_2"[span_28](end_span)
    [span_29](start_span)model += X[3] + X[6] + X[9] <= 2000, "Inequality_Constraint_3"[span_29](end_span)
    
    [span_30](start_span)status = model.solve()[span_30](end_span)
    [span_31](start_span)status_str = pulp.LpStatus[status][span_31](end_span)
    
    return {
        [span_32](start_span)"status": status_str,[span_32](end_span)
        [span_33](start_span)"variables": {f"X{i}": X[i].varValue for i in range(1, 10)},[span_33](end_span)
        [span_34](start_span)"min_z": pulp.value(model.objective) if status_str == "Optimal" else 0.0[span_34](end_span)
    }
