import os
import re
import xlrd
import pandas as pd

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
    

def main():
    src_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'export2022826.xls')
    moni = MoneyO("yago")
    
    moni.add_data(src_file)
    print(moni.get_data())
    moni.save()

if __name__ == "__main__":
    main()