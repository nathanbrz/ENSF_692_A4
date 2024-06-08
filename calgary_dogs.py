# calgary_dogs.py
# AUTHOR NAME
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.
import numpy as np
import pandas as pd

class Breed_stats:

    @staticmethod
    def breed_year_top(breed, df):
        # Top Years
        years_on_top = []
        
        df = DataFrame_creation("CalgaryDogBreeds.xlsx")

        for value in df.index.get_level_values('Year').unique():
            idx = pd.IndexSlice
            year_level = df.loc[idx[value],:]
            if breed in year_level.index.get_level_values('Breed'):
                years_on_top.append(value)

        return years_on_top
    @staticmethod
    def breed_total_reg(breed, df):
        idx = pd.IndexSlice

        df = df.loc[idx[:, :, breed], :]

        sum_of_total = np.nansum(df['Total'])

        return sum_of_total
    
    @staticmethod
    def breed_percentage_years(breed, df):
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
        idx = pd.IndexSlice
        df_count = np.nansum(df['Total'])

        breed_df = df.loc[idx[:, :, breed], :]
        breed_count = np.nansum(breed_df['Total'])

        percentage_for_breed = breed_count / df_count

        return percentage_for_breed
    
    @staticmethod
    def breed_popular_months(breed, df):
        idx = pd.IndexSlice

        df = df.loc[idx[:, :, breed], :]
        month_counts = df.groupby(level= 'Month').count()
        max_value_count = month_counts['Total'].max()
        top_months = month_counts[month_counts['Total'] == max_value_count]
        top_months = top_months.index.get_level_values('Month')

        return top_months
    
    @staticmethod
    def print_all_stats(df, user_input):
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
    df = pd.read_excel(dataframe)
    df.set_index(['Year', 'Month', 'Breed'], inplace=True)
    return df

def user_entry_handdler(df):
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
