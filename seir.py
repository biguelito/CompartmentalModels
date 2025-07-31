from CompartmentalModelSolver import CompartmentalModelSolver

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

    initial_conditions = [initS, initE, initI, initR]
    transfer_rate = [beta, sigma, gamma]
    solver = CompartmentalModelSolver(initial_conditions, transfer_rate, days)
    solver.solve()
    solver.save("matplotlib")