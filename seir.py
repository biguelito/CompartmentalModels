from CompartmentalModelSolver import CompartmentalModelSolver

def seir_odes(initialValues, time, transfer_rates):
    S, E, I, R = initialValues
    beta, sigma, gamma = transfer_rates
    N = S + E + I + R

    dSdt = -beta * I * (S / N)
    dEdt = beta * I * (S / N) - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I

    return [dSdt, dEdt, dIdt, dRdt]

if __name__ == "__main__":
    initS = 1000000
    initE = 1
    initI = 1
    initR = 0
    sigma = 1/3
    gamma = 1/2
    R0 = 4
    beta = R0 * gamma
    days = 100
    GRAPH_LIB = "matplotlib"

    initial_conditions = [initS, initE, initI, initR]
    transfer_rate = [beta, sigma, gamma]
    solver = CompartmentalModelSolver(seir_odes, initial_conditions, transfer_rate, days)
    solver.solve()
    solver.save(GRAPH_LIB)