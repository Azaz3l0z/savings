import pandas as pd
import matplotlib.pyplot as plt
from money_manager import MoneyManager

def main():
    file = "export2022114.xls"
    
    mm = MoneyManager("yago")
    mm.add_data(file)
    mm.set_date("2022-10-01")
    
    fig, axs = plt.subplots(1, 2)
    grouped_unordered(mm.group_expenses(ignore_income=True), axs[0])
    gastos_vs_ingresos(mm.get_data(), axs[1])
    plt.show()
    
def grouped_unordered(data: dict, axes):
    other = pd.DataFrame(data["Other"]).sort_values(by="amount")

    for key in data:
        data[key] = sum([x["amount"] for x in data[key]])/100

    # Remove empty elements
    data = {key: value for key, value in data.items() if value}
    axes.barh(list(data.keys()), data.values())

def gastos_vs_ingresos(data: pd.DataFrame, axes):
    pos = sum([i for i in data["amount"] if i > 0])
    neg = sum([i for i in data["amount"] if i < 0])
    total = pos - neg
    sizes = [abs(x/total) for x in [pos, neg]]
    
    # Plotting
    labels = "Ingresos", "Gastos"
    explode = (0, 0.1)
    axes.pie(sizes, labels=labels, explode=explode, shadow=True,
             autopct=lambda p: '{:.2f}€'.format(p * abs(total)/10000))
    
    
if __name__ == "__main__":
    main()