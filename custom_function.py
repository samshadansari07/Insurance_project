def create_total_late(a):
    a=a.copy()
    a["Total_late"] = a['Count_3-6_months_late'] + a['Count_6-12_months_late'] +a['Count_more_than_12_months_late']
    a.drop(columns = ['Count_3-6_months_late','Count_6-12_months_late','Count_more_than_12_months_late'], inplace =True)
    return a