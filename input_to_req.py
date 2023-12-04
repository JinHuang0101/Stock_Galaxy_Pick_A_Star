# dictionary that maps select box value to API reqeust name 
selectToAPI = {'10-K Assets': "Assets", 
               '10-K Revenues': "RevenueFromContractWithCustomerExcludingAssessedTax",
               "10-K Gross Profit": "GrossProfit",
               "10-K Costs": "CostOfGoodsAndServicesSold",
               "10-K Operating Expenses": "OperatingExpenses",
               "10-K Operating Income Loss": "OperatingIncomeLoss",
               "10-K Net Income Loss": "NetIncomeLoss",
               "10-K Earnings Per Share Basic": "EarningsPerShareBasic",
               "10-K Depreciation": "Depreciation",
               "10-K Earnings Per Share Diluted": "EarningsPerShareDiluted",
               "10-K Cash": "Cash"
               }

# dictionary that tracks unavailable data in each category in real time 
new_no_data_dict = {}