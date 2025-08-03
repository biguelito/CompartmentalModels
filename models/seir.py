def odes(initialValues, time, transfer_rates):
    S, E, I, R = initialValues
    beta, sigma, gamma = transfer_rates
    N = S + E + I + R

    dSdt = -beta * I * (S / N)
    dEdt = beta * I * (S / N) - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I

    return [dSdt, dEdt, dIdt, dRdt]