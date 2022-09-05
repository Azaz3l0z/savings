import os
import re
import xlrd
import pandas as pd

from copy import deepcopy
from functools import reduce
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

categories = {
    "food": [
        "Lupa",
        "Mercadona",
        "Mcdonald",
        "Bazar"
    ],
    "transfers": [
        "Bizum"
    ],
    "credit_card": [
        "Contactless"
    ],
    "parking": [
        "Parking"
    ],
    "suscriptions": [
        "HBO Max"
    ]
}


class MoneyO(object):
    """_summary_
    Class to manage, save and load bank information in a .csv format
    """
    # Default save folder
    __default_save_folder: str = './lol'
    
    def __init__(self, user: str) -> None:
        """_summary_
        Initializes the class with a given user and loads a saved file
        with the name of said user

        Args:
            user (str): Name of the user
        """
        self.user = user
        self.__save_folder = os.path.abspath(self.__default_save_folder)
        self.__save_file = os.path.join(self.__save_folder, self.user + '.csv')
    
        self.df = {
            "date": [],
            "description": [],
            "amount": []
        }
        
        self.df = pd.DataFrame(self.df)
        
        self.__load_save()
        
    def save(self) -> None:
        """_summary_
        Saves current dataframe in a file with the username as the save file
        """
        if not os.path.isdir(self.__save_folder):
            os.makedirs(self.__save_folder)    
        
        self.df.to_csv(self.__save_file, index=False)
               
    def get_data(self) -> pd.DataFrame:
        """
        Returns the current dataframe
        
        Returns:
            pd.DataFrame: Current data of the class in a dataframe format
        """
        self.df = self.df.sort_values(by=["date"])
        
        if self.df['date'].dtype != 'datetime64[ns]':
            self.df['date'] =  pd.to_datetime(self.df['date'], format='%Y-%m-%d')
        
        return self.df

    def add_data(self, src_file: str) -> None:
        """
        Adds new data via an excel / csv file to the current
        dataframe

        Args:
            src_file (str): File to add the data from
        """
        # Read Frame
        df = self.__read_excel(src_file)
            
        # Find out which bank we are working with
        banks = {
            "0049": {
                "name": "Santander",
                "row": 8,
                "col": "B:D"
            }
        }
        
        IBAN = self.__get_IBAN(df)
        bank = IBAN[4:8]
        df = self.__read_excel(src_file, banks[bank]["row"] - 1, banks[bank]["col"])
        
        for old, new in zip(df, self.df):
            df = df.rename(columns={old: new})
                
        self.df = pd.concat([self.df, df], ignore_index=True)
        self.df["date"] = pd.to_datetime(self.df["date"])
        
        self.df = self.df.drop_duplicates()
        
    def __load_save(self) -> None:
        """
        Loads an existing frame from a save
        """
        if os.path.isfile(self.__save_file):
            df = pd.read_csv(self.__save_file)
            self.df = pd.concat([self.df, df])
        
    def __get_IBAN(self, df: pd.DataFrame) -> str:
        """
        Finds the IBAN present in the excel

        Args:
            df (pd.DataFrame): Dataframe to search the IBAN in

        Returns:
            str: IBAN
        """
        for j in range(len(df[df.keys()[0]])):
            for i in df:
                cell = df[i][j]
                if isinstance(cell, str):
                    match = re.match(r'[a-zA-Z]{2}\d{22}', cell)

                    if match:
                        return match.group(0)
        
        return None
    
    def __read_excel(self, file: str, header: int = 0, 
                     cols: str = "") -> pd.DataFrame:
        """
        Reads an excel file

        Args:
            file (str): File path
            header (int, optional): Line in which the header of the frame 
                                    is located. Defaults to 0.
            cols (str, optional): Columns to read. Defaults to "".

        Returns:
            pd.DataFrame: _description_
        """
        if cols == "":
            cols = pd.read_excel(file, nrows=1).columns

        if '.xls' == os.path.splitext(os.path.basename(file))[1]:
            wb = xlrd.open_workbook(file, logfile=open(os.devnull, 'w'))
            df = pd.read_excel(wb, engine='xlrd', header=header, usecols=cols)

        else:
            df = pd.read_excel(file, header=header, usecols=cols)
            
        return df
    
    @staticmethod
    def group_expenses(expenses: pd.DataFrame, category: str) -> dict:
        def dict_walker(_dict: dict, pre = None):
            pre = pre if pre else []
            
            if isinstance(_dict, dict):
                for key, value in _dict.items():
                    if isinstance(value, dict):
                        for d in dict_walker(value, pre + [key]):
                            yield d
                        
                    elif isinstance(value, list) or isinstance(value, tuple):
                        for i, v in enumerate(value):
                            for d in dict_walker(v, pre + [key, i]):
                                yield d
                        
                    else:
                        yield pre + [key, value]
                        
            else:
                yield pre + [_dict]

        # Gets a tree of paths of the dict and chooses the one that we need
        # It uses a generator for better performance
        for i in dict_walker(categories):
            if category in i:
                if category == i[-1]:
                    category = i[:-1]
                
                else:
                    idx = i.index(category)
                    category = i[:idx + 1]
                break

        # Now we create a copy of the categories to remove every key / value
        # that we don't need
        
        _dict = deepcopy(categories)

        for i in range(len(category)):
            sub_dict = reduce(lambda x, y: x[y], category[:i], _dict)
            if isinstance(sub_dict, dict):
                keys = list(sub_dict.keys())
                keys.remove(category[i])
                for key in keys:
                    sub_dict.pop(key)
                    
            elif isinstance(sub_dict, list) or isinstance(sub_dict, tuple):   
                items = sub_dict.copy()     
                items.pop(category[i])
                for item in items:
                    sub_dict.remove(item)
                    
        # Finally we perform a regular expression search using the terms
        for path in dict_walker(_dict):
            path, sub_string = path[:-1], path[-1]
            matches = []
            
            sub_dict = reduce(lambda x, y: x[y], path[:-1], _dict)

            for i, item in enumerate(expenses['description']):
                match = re.search(f'(?i){sub_string}', item)
                
                if match:
                    matches.append(i)

            sub_dict[sub_dict.index(sub_string)] = {sub_string: expenses.iloc[matches]}
            
        return _dict, dict_walker(_dict)


class Grapher(object):
    def __init__(self, figure: plt.figure, moneyManager: MoneyO) -> None:
        self.figure = figure
        self.moneyManager = moneyManager
        
        self.canvas = FigureCanvas(self.figure)
        
    def empty(self):
        self.figure.clf()
        return self.canvas
        
    def basic_plot(self, category: str):
        self.figure.clf()
        data = self.moneyManager.get_data()  
        organised = MoneyO.group_expenses(data, category)
        
        # Plot configuration
        ax = self.figure.add_subplot(111)
        ax.set_title(category.capitalize())
        ax.axline((0, 0), (1, 0), linewidth=1, color='k')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
        
        # Add actual plot
        _max, _min = data["date"][0], data["date"][0]
        for path in organised[1]:
            frame = reduce(lambda x, y: x[y], path[:-1], organised[0])
            x = frame["date"]
            y = frame["amount"]

            ax.plot(x, y, '.', label = path[-2])
            
            _max = max(x) if max(x) > _max else _max
            _min = min(x) if min(x) < _min else _min
            
        
        ax.set_xlim(_min - (_max - _min)*0.05, _max + (_max - _min)*0.05)               
        ax.legend(loc='lower right', fontsize='x-large')
        
        self.canvas.draw()
        
        return self.canvas

    def pie_plot(self, category: str):
        self.figure.clf()
        money_limit = 0.04
        
        data = self.moneyManager.get_data()  
        organised = MoneyO.group_expenses(data, category)
        
        pie_dict = {}
        
        for path in organised[1]:   
            pie_dict[path[-2]] = len(path[-1].index)
        
        pie_dict = {item: value / sum(pie_dict.values()) 
                       for item, value in pie_dict.items()}
        
        pie_dict['Other'] = 0
        for value in pie_dict.values():
            if value < money_limit:
                pie_dict['Other'] += value
        
        pie_dict = {key: value for key, value in pie_dict.items() if value > money_limit}
                
        ax = self.figure.add_subplot(111)
        ax.set_title(category.capitalize())
        ax.pie(pie_dict.values(), labels = pie_dict.keys(), autopct='%1.1f%%')
        
        self.canvas.draw()
        
        return self.canvas


def main():
    pass

    
if __name__ == "__main__":
    main()