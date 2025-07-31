class CompartmentalModel:
    initialValues = None
    transfer_rates = None
    days = None

    def __init__(self, initialValues, transfer_rates, days):
        self.initialValues = initialValues
        self.transfer_rates = transfer_rates
        self.days = days

    def get_odes(self, initialValues, time, transfer_rates):
        S, E, I, R = initialValues
        beta, sigma, gamma = transfer_rates
        N = S + E + I + R

        dSdt = -beta*I*(S/N)
        dEdt = beta*I*(S/N) - (sigma*E)
        dIdt = (sigma*E) - (gamma*I)
        dRdt = gamma*I
        
        model = [
            dSdt, 
            dEdt, 
            dIdt, 
            dRdt
        ]
        return model
        
