import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# from Ipython.display import display, HTML
from IPython.display import display, HTML

class DataLoader:
    """Class to Load data"""
    def __init__(self):      
        pass

    def read_data(self, file_path):
        _, file_ext = os.path.splitext(file_path)
        """
        Load data from a CSV, TSV, JSON or Excel file
        """
        if file_ext == '.csv':
            return pd.read_csv(file_path, index_col=None)
        
        elif file_ext == '.tsv':
            return pd.read_csv(file_path, sep='\t')

        elif file_ext == '.json':
            return pd.read_json(file_path)

        elif file_ext in ['.xls', '.xlsx']:
            return pd.read_excel(file_path)

        else:
            raise ValueError(f"Unsupported file format:")
       
class DataInfo:
    """Class to get dataset information """
    def __init__(self):      
        pass

    def info(self, df): 
        """
        Displaying Relevant Information on the the Dataset Provided
        """    
        # Counting no of rows and columns
        print('=='*20 + f'\nShape of the dataset : {df.shape} \n' + '=='*20 + '\n')
        
        # Extracting column names
        column_name =  df.columns 
        print('=='*20 + f'\nColumn Names\n' + '=='*20 +  f'\n{column_name} \n ')

        # Checking if 'Timestamp' column exists and displaying date range
        if 'Date and Time' in df.columns:
            print("=="*20 + "\nRange of the Dataset (Date and Time)\n" + "=="*20)
            # Converting Timestamp column to datetime if not already
            df['Date and Time'] = pd.to_datetime(df['Date and Time'], errors='coerce')
            print("Start Date:", df['Date and Time'].min())
            print("End Date:  ", df['Date and Time'].max())
        print('\n')

        # List of all numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        print('=='*20 + f'\nNumerical Columns\n' + '=='*20)
        print(numerical_cols, end="\n\n")
        
        # List of all categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        print('=='*20 + f'\nCategorical Columns\n' + '=='*20)
        print(categorical_cols, end="\n\n")
            
        # Data type info
        print('=='*20 + f'\nData Summary\n' + '=='*20 )
        data_summary = df.info() 
        print('=='*20 +'\n')

        # Descriptive statistics
        describe =  df.describe() 
        print('=='*20 + f'\nDescriptive Statistics\n' + '=='*20  )
        display(describe)
        
        #Display the dataset
        print('=='*20 + f'\nDataset Overview\n'+ '=='*20 )
        return display(HTML(df.head().to_html()))
    
class EDA:
    """Class to Perform various checks on the dataset"""
    def __init__(self, df):
        self.df =df
        self.categorical_columns = [] 
        self.numerical_columns =[]
        self._identify_columns()

    def _identify_columns(self):
        """
        Identify numerical and categorical columns.
        """
        for col in self.df.columns:
            if self.df[col].dtype == object:
                self.categorical_columns.append(col)
            else:
                self.numerical_columns.append(col)

    

    def check_outliers_and_plot(self):
        """
        Detect outliers in numerical columns using the IQR method and plot boxplots.
        """
        

        outlier_columns = []

        for column in self.numerical_columns:
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Find outliers
            outlier_indices = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)].index.tolist()

            if outlier_indices: 
                outlier_columns.append(column)

        print("***********************************************")
        print("Columns Containing Outliers Include:", outlier_columns)
        print("***********************************************")

        if outlier_columns:
            # Plot boxplots for columns with outliers
            num_rows = (len(outlier_columns) + 2) // 2
            num_cols = min(len(outlier_columns), 2)
            fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(20, 20))

            # Ensure axes is always iterable
            if len(outlier_columns) == 1:
                axes = [axes]  # Make axes a list to allow consistent indexing
            else:
                axes = axes.flatten() if num_rows > 1 else axes

            for i, column in enumerate(outlier_columns):
                sns.boxplot(x=self.df[column], ax=axes[i])
                axes[i].set_xlabel(column)
                axes[i].set_ylabel('Values')
                axes[i].set_title(f'{column}')
                axes[i].tick_params(axis='x', rotation=45)

            # Remove any unused subplots
            if len(outlier_columns) < len(axes):
                for j in range(len(outlier_columns), len(axes)):
                    fig.delaxes(axes[j])

            # Adjust layout to prevent overlapping
            plt.tight_layout()
            plt.show()
        else:
            print("NO OUTLIERS FOUND")