class ALU:
    def __init__(self):
        self.result = 0

    def execute(self, acc_a, acc_b, su):
        if su == 0:
            # Suma
            self.result = (acc_a + acc_b) & 0xFF 
        else:
            # Resta
            self.result = (acc_a - acc_b) & 0xFF
            
        return self.result