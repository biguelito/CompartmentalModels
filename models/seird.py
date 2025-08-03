class SEIRD:
    DEFAULTS = {
        "S": 1_000_000,
        "E": 1,
        "I": 1,
        "R": 0,
        "D": 0,
        "sigma": 1/3,
        "gamma": 1/2,
        "mu": 0.3,
        "r0": 4.0,
        "days": 100
    }

    COMPARTMENTS = ["Susceptíveis", "Expostos", "Infectados", "Recuperados", "Mortos"]

    def get_default(self, key):
        return self.DEFAULTS[key]
    
    def get_compartments(self):
        return self.COMPARTMENTS

    def odes(self, initialValues, time, transfer_rates):
        S, E, I, R, D = initialValues
        beta, sigma, gamma, mu = transfer_rates
        N = S + E + I + R + D

        dSdt = -beta * I * (S / N)
        dEdt = beta * I * (S / N) - sigma * E
        dIdt = sigma * E - gamma * I - mu * I
        dRdt = gamma * I
        dDdt = mu * I

        return [dSdt, dEdt, dIdt, dRdt, dDdt]
