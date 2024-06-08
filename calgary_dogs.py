'''
Dogs of Calgary Data Analysis

AUTHOR: Nathan De Oliveira
DATE: 2024-06-08
VERSION: 1.0

This module provides a terminal-based application for computing and printing statistics based on given input.
It allows users to input a specific dog breed and generates various statistics.

The data is read from an Excel file with a multi-index structure, and the module utilizes pandas and numpy for 
data manipulation and analysis.
'''
import numpy as np
import pandas as pd

class Breed_stats:
    """
    A class to perform various statistical analyses on dog breed data with static methods. Has no instance varirables.
    """

    @staticmethod
    def breed_year_top(breed, df):
        """
        Determine the years in which a particular breed was registered.

        Args:
            breed (str): The breed of dog to analyze.
            df (pd.DataFrame): The DataFrame containing breed registration with hierarchical indexes year, month, breed.

        Returns:
            list: A list of years in which the breed was registered.
        """
        years_on_top = []
        
        for value in df.index.get_level_values('Year').unique():
            idx = pd.IndexSlice
            year_level = df.loc[idx[value],:]
            if breed in year_level.index.get_level_values('Breed'):
                years_on_top.append(value)

        return years_on_top
    @staticmethod
    def breed_total_reg(breed, df):
        """
        Calculate the total number of registrations for a particular breed.

        Args:
            breed (str): The breed of dog to analyze.
            df (pd.DataFrame): The DataFrame containing breed registration with hierarchical indexes year, month, breed.

        Returns:
            int: The total number of registrations for the breed.
        """
        idx = pd.IndexSlice

        df = df.loc[idx[:, :, breed], :]

        sum_of_total = np.nansum(df['Total'])

        return sum_of_total
    
    @staticmethod
    def breed_percentage_years(breed, df):
        """
        Calculate the percentage of a breed's registration out of the total percentage for each year.

        Args:
            breed (str): The breed of dog to analyze.
            df (pd.DataFrame): The DataFrame containing breed registration with hierarchical indexes year, month, breed.

        Returns:
            list: A list of percentages representing the breed's registration out of the total percentage for each year.
        """
        idx = pd.IndexSlice
        percentage_per_year = []
        df_breed = df.loc[idx[:, :, breed], :] #get the years the breed was shown in and display the percentage for those
        for value in df.index.get_level_values('Year').unique():
            year_df = df.loc[idx[value], :]
            year_sum = np.nansum(year_df['Total'])

            if value in df_breed.index.get_level_values('Year').unique():

                breed_df = df.loc[idx[value, :, breed], :]
                breed_sum = np.nansum(breed_df['Total'])

                percentage_for_breed = breed_sum / year_sum

                percentage_per_year.append(percentage_for_breed)
        
        return percentage_per_year
    
    @staticmethod
    def breed_percentage_all_years(breed, df):
        """
        Calculates and print the percentage of selected breed registrations out of the total three-year percentage.

        Args:
            breed (str): The breed of dog to analyze.
            df (pd.DataFrame): The DataFrame containing breed registration with hierarchical indexes year, month, breed.

        Returns:
            float: The percentage of the breed's registration across all years.
        """
        idx = pd.IndexSlice
        df_count = np.nansum(df['Total'])

        breed_df = df.loc[idx[:, :, breed], :]
        breed_count = np.nansum(breed_df['Total'])

        percentage_for_breed = breed_count / df_count

        return percentage_for_breed
    
    @staticmethod
    def breed_popular_months(breed, df):
        """
        Finds the months that were most popular for the selected breed registrations.

        Args:
            breed (str): The breed of dog to analyze.
            df (pd.DataFrame): The DataFrame containing breed registration with hierarchical indexes year, month, breed.

        Returns:
            list: A list of the most popular months for the breed's registration (months that tie in max count in the list).
        """
        idx = pd.IndexSlice

        df = df.loc[idx[:, :, breed], :]
        month_counts = df.groupby(level= 'Month').count()
        max_value_count = month_counts['Total'].max()
        top_months = month_counts[month_counts['Total'] == max_value_count]
        top_months = top_months.index.get_level_values('Month')

        return top_months
    
    @staticmethod
    def print_all_stats(df, user_input):
        """
        Print all the statistics in this class for a given breed.

        Args:
            df (pd.DataFrame): The DataFrame containing breed registration with hierarchical indexes year, month, breed.
            user_input (str): The breed of dog to analyze.
        """
        # Top years for that breed
        breed_years = Breed_stats.breed_year_top(user_input, df)
        print(f"The {user_input} was found in the top breeds for years: {', '.join(str(i) for i in breed_years)}")

        # Total registered for that breed
        breed_total = Breed_stats.breed_total_reg(user_input, df)
        print(f"There have been {breed_total} {user_input} dogs registered total.")

        # Percentage of breed in each year
        breed_percentage = Breed_stats.breed_percentage_years(user_input, df)
        for i, year in enumerate(breed_years):
            print(f"The {user_input} was {breed_percentage[i]:0%} of top breeds in {breed_years[i]}.")

        # Percentage of breed in all years
        breed_percentage_all = Breed_stats.breed_percentage_all_years(user_input, df)
        print(f"The {user_input} was {breed_percentage_all:0%} of top breeds across all years.")

        # Popular months for that breed
        breed_months = Breed_stats.breed_popular_months(user_input, df)
        print(f"The most popular month(s) for {user_input} dogs: {', '.join(str(i) for i in breed_months)}")
    

    

def DataFrame_creation (dataframe):
    """
    Create a DataFrame from an Excel file and sets the multi-index correctly.

    Args:
        dataframe (str): The path to the Excel file.

    Returns:
        pd.DataFrame: The created DataFrame with multi-index.
    """
    df = pd.read_excel(dataframe)
    df.set_index(['Year', 'Month', 'Breed'], inplace=True)
    return df

def user_entry_handdler(df):
    """
    Handle user input for breed entry and print statistics.

    Args:
        df (pd.DataFrame): The DataFrame containing breed registration with hierarchical indexes year, month, breed.
    """
    while True:
        user_input = input("Please enter a dog breed: ")
        user_input = user_input.upper()

        try:
            if user_input in df.index.get_level_values("Breed"):
                Breed_stats.print_all_stats(df, user_input)
                break
            else:
                raise ValueError("Dog breed not found in the data. Please try again.")

        except ValueError as e:
            print(e)
            continue


def main():

    # Import data here
    df = DataFrame_creation("CalgaryDogBreeds.xlsx")

    print("ENSF 692 Dogs of Calgary")

    # User input stage
    # Data anaylsis stage
    user_entry_handdler(df)

if __name__ == '__main__':
    main()
