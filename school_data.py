# school_data.py
# AUTHOR: Bo Zheng Ma
#
# A terminal-based application for computing and printing statistics based on given input.
# The application loads school enrollment data from a CSV file and calculates statistics for a specific school.

import numpy as np
import pandas as pd
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022


def load_school_data(filename='Assignment3Data.csv'):
    """ 
    Load the CSV data into a structured NumPy array. 
    :param filename: the name of the CSV file.
    :return: the data, school codes, and school names.
    """
    df = pd.read_csv(filename)
    school_codes = sorted(df['School Code'].unique()) # Get the unique school codes
    school_names = df[['School Code', 'School Name']].drop_duplicates().set_index('School Code').to_dict()['School Name'] # Create a dictionary of school codes and names
    years = sorted(df['School Year'].unique()) # Get the unique school years, in ascending order
    
    
    data = np.empty((len(years), len(school_codes), 3), dtype=np.float32) # Create a 3D array to store the data
    data.fill(np.nan) # Initialize data array with NaNs to fill the missing data
    
    # Fill the data array with the enrollment data
    for i, year in enumerate(years):
        for j, code in enumerate(school_codes):
            yearly_data = df[(df['School Year'] == year) & (df['School Code'] == code)] # Get the data for the specific year and school code
            if not yearly_data.empty:
                data[i, j, :] = yearly_data[['Grade 10', 'Grade 11', 'Grade 12']].values[0]  # Fill the data array with the data for a specific school in a specific year.

    return data, school_codes, school_names

def print_school_statistics(data, school_idx, school_name, school_code):
    """ 
    Calculate and print the statistics for a specific school using its index. 
    :param data: the school data.
    :param school_idx: the index of the school.
    :param school_name: the name of the school.
    :param school_code: the code of the school.
    """
    school_data = data[:, school_idx, :] # Data for the specific school
    mean_enrollments = np.nanmean(school_data, axis=0) # Mean enrollment for each grade, nan ignores missing data
    max_enrollment = np.nanmax(school_data) # Highest enrollment in any grade
    min_enrollment = np.nanmin(school_data) # Lowest enrollment in any grade
    total_enrollment_per_year = np.nansum(school_data, axis=1) # Total enrollment for each year
    total_ten_year = np.nansum(total_enrollment_per_year) # Total enrollment over 10 years
    mean_yearly = np.nanmean(total_enrollment_per_year) # Mean total yearly enrollment over 10 years

    # Enrollment over 500
    large_classes = school_data[school_data > 500]
    median_large_classes = np.median(large_classes) if large_classes.size > 0 else None

    # Print the school statistics
    print(f"\nSchool Name: {school_name}, School Code: {school_code}")
    print(f"Mean Enrollment for Grade 10: {int(mean_enrollments[0])}")
    print(f"Mean Enrollment for Grade 11: {int(mean_enrollments[1])}")
    print(f"Mean Enrollment for Grade 12: {int(mean_enrollments[2])}")
    print(f"Highest Enrollment for a single Grade: {int(max_enrollment)}")
    print(f"Lowest Enrollment for a single Grade: {int(min_enrollment)}")
    for i, year in enumerate(range(2013, 2023)): # Print the total enrollment for each year
        print(f"  Total enrollment for {year}: {int(total_enrollment_per_year[i])}")
    print(f"Total Ten Year Enrollment: {int(total_ten_year)}")
    print(f"Mean Total Yearly Enrollment Over 10 Years: {int(mean_yearly)}")
    if median_large_classes is not None: # Print the median value for enrollments over 500
        print(f"For all enrollments over 500, the median value was: {int(median_large_classes)}")
    else: # If there are no enrollments over 500, print a message
        print("No enrollments over 500")

def print_general_statistics(data):
    """
    Calculate and print general statistics for all schools.
    :param data: the school's entire data.
    """
    mean_2013 = np.nanmean(data[0, :, :])  # Mean over all grades and schools for 2013
    mean_2022 = np.nanmean(data[-1, :, :])  # Mean over all grades and schools for 2022
    
    # Calculate the total graduating class for 2022 across all schools (Grade 12)
    total_grads_2022 = np.nansum(data[-1, :, 2])
    
    # Find the highest and lowest enrollments in any grade over the entire dataset
    max_enrollment = np.nanmax(data)
    min_enrollment = np.nanmin(data)

    # Print the general statistics
    print("Mean Enrollment in 2013:", mean_2013.astype(int))
    print("Mean Enrollment in 2022:", mean_2022.astype(int))
    print(f"Total Graduating Class of 2022: {int(total_grads_2022)}")
    print(f"Highest Enrollment for a Single Grade: {int(max_enrollment)}")
    print(f"Lowest Enrollment for a Single Grade: {int(min_enrollment)}")


def main():
    years = np.array([year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022])
    reshaped_years = [year.reshape(20, 3) for year in years]
    arr = np.array(reshaped_years)

    # Part 1
    print("ENSF 692 School Enrollment Statistics")
    print("Shape of full data array: ", arr.shape)
    print("Dimensions of full data array: ", arr.ndim)
    
    data, school_codes, school_names = load_school_data()
    school_input = input("Please enter the high school name or school code: ")
    try: 
        if school_input.isdigit(): # Check if the input is a school code
            school_input = int(school_input)
            if school_input in school_codes:
                school_idx = school_codes.index(school_input)
                school_name = school_names[school_input]
            else:
                raise ValueError("School code not found.")
        else: # Check if the input is a school name
            if school_input in school_names.values():
                school_code = list(school_names.keys())[list(school_names.values()).index(school_input)]
                school_idx = school_codes.index(school_code)
                school_name = school_input
                # print("!!!found " + school_code)
            else:
                raise ValueError("School name not found.")
        # Part 2
        print("\n***Requested School Statistics***\n")
        print_school_statistics(data, school_idx, school_name, school_code)
        # Part 3
        print("\n***General Statistics for All Schools***\n")
        print_general_statistics(data)
    except ValueError as e:
        print(e)
        
if __name__ == '__main__':
    main()

