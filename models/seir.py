class SEIR:
    DEFAULTS = {
        "S": 1_000_000,
        "E": 1,
        "I": 1,
        "R": 0,
        "beta": 0.429,
        "sigma": 0.192,
        "gamma": 0.143,
        "r0": 3,
        "days": 365
    }
    COMPARTMENTS = ["Susceptíveis", "Expostos", "Infectados", "Recuperados"]

    def __init__(self):
        pass

    def get_default(self, key):
        return self.DEFAULTS[key]
    
    def get_compartments(self):
        return self.COMPARTMENTS

    def odes(self, initialValues, time, transfer_rates):
        S, E, I, R = initialValues
        beta, sigma, gamma = transfer_rates
        N = S + E + I + R

        dSdt = -beta * I * (S / N)
        dEdt = beta * I * (S / N) - (sigma * E)
        dIdt = sigma * E - (gamma * I)
        dRdt = gamma * I

        return [dSdt, dEdt, dIdt, dRdt]