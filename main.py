import pandas as pd
import numpy as np
import joblib
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI , HTTPException
from custom_function import create_total_late



# Effort 
def agent_efforts(I):
    return 10* (1-np.exp(-I/400))

# probability 
def agent_probability(E):
    return 0.20 * (1 - np.exp(-E/5))

# profit
def total_profit(premimum , agent_prob , client_prob , I):
    return (premimum*(agent_prob + client_prob) - I)



class RenewalInsentive(BaseModel):
    data : List[List]

app = FastAPI()

@app.post('/predict')
def insurance_insentive(request : RenewalInsentive):
    try:
        data = request.data
        data = pd.DataFrame(data ,columns = ['perc_premium_paid_by_cash_credit', 'age_in_days', 'Income',
        'Count_3-6_months_late', 'Count_6-12_months_late',
        'Count_more_than_12_months_late', 'application_underwriting_score',
        'no_of_premiums_paid', 'sourcing_channel', 'residence_area_type',
        'premium'])
        

        
        model = joblib.load("insurance_project.pkl")
        client_prob = model.predict_proba(data)[:,1]
        result = dict()
        incentives = [500, 1000, 1500, 2000]
        for i in range(len(data)):
            premium = data['premium'].iloc[i]
            cp = client_prob[i]
            max_profit = float("-inf")
            max_incentive = None
            l = []
            for j in incentives:

                Eff = agent_efforts(j)
                agent_proba = agent_probability(Eff)
                profit =  total_profit(premium , agent_proba , cp, j )
                l.append(profit)

            max_profit, idx= max(l),np.argmax(l)
            max_incentive = incentives[idx]
            result[i] = {'profit':max_profit , 'incentive':max_incentive}
        return result
    except Exception as e:
        raise HTTPException(status_code = 500 , detail = str(e))

            