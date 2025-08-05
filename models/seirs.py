class SEIRS:
    DEFAULTS = {
        "S": 1_000_000,
        "E": 1,
        "I": 1,
        "R": 0,
        "sigma": 0.33,
        "gamma": 0.5,
        "alfa": 0.33,
        "beta": 4.0 * 0.5, 
        "r0": 4.0,
        "days": 100
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
        beta, sigma, gamma, alfa = transfer_rates
        N = S + E + I + R

        dSdt = -beta * I * (S / N) + (alfa * R)
        dEdt = beta * I * (S / N) - (sigma * E)
        dIdt = sigma * E - (gamma * I)
        dRdt = gamma * I - (alfa * R)

        return [dSdt, dEdt, dIdt, dRdt]