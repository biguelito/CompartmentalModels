class CompartmentalModel:
    initialValues = None
    transfer_rates = None
    days = None

    def __init__(self, initialValues, transfer_rates, days):
        self.initialValues = initialValues
        self.transfer_rates = transfer_rates
        self.days = days

        return
