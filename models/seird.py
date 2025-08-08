class SEIRD:
    DEFAULTS = {
        "S": 1_000_000,
        "E": 1,
        "I": 1,
        "R": 0,
        "D": 0,
        "beta": 0.4332,
        "sigma": 0.192,
        "gamma": 0.143,
        "mu": 0.0014,
        "r0": 3,
        "days": 365
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
        dEdt = beta * I * (S / N) - (sigma * E)
        dIdt = (sigma * E) - (gamma * I) - (mu * I)
        dRdt = gamma * I
        dDdt = mu * I

        return [dSdt, dEdt, dIdt, dRdt, dDdt]
