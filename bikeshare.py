import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    ######### TO DO: get user input for city (chicago, new york city, washington) #########
    while True:
        try:
            city = input("Would you like to see data for Chicago, New York City or Washington?").strip().lower()
            if city in ["chicago", "new york city", "washington"]:
                break
            else:
                print("That is not a valid city. Please select one option out of Chicago, New York City or Washington.")
        except:
            print("That is not a valid city. Please select one option out of Chicago, New York City or Washington.")
            
    ######### TO DO: get user input for month (all, january, february, ... , june) #########
    # I think that asking the user about filtering on month and day in independent questions makes it easier for user to clearly understand all the options. 
    # This way they can separately decide what time frame they want to select or if they want to look at all time
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        try:
            month = input("Which month would you like to see data for? All (If your answer is: All, it means no month based filtering), January, February, March, April, May or June?").strip().lower()
            if month in months:
                break
            else:
                print("That is not a valid month. Please select one option out of All, January, February, March, April, May or June.")
        except:
            print("That is not a valid month. Please select one option out of All, January, February, March, April, May or June.")

    ######### TO DO: get user input for day of week (all, monday, tuesday, ... sunday) #########
    # As mentioned above, I think that asking the user about filtering on month and day in independent questions makes it easier for user to clearly understand all the options. 
    # This way they can separately decide what time frame they want to select or if they want to look at all time
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        try:
            day = input("Which day would you like to see data for? All (If your answer is: All, it means no day based filtering), Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?").strip().lower()
            if day in days:
                break
            else:
                print("That is not a valid day. Please select one option out of All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.")
        except:
            print("That is not a valid day. Please select one option out of All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime. Link: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns. Link: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DatetimeIndex.strftime.html?highlight=strftime
    df['month'] = df['Start Time'].dt.month
    df['month name'] = df['Start Time'].dt.strftime('%B')
    df['day of week'] = df['Start Time'].dt.weekday_name

    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        month_filter_num = 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    else:
        month_filter_num = 0
        
    # filter by day of week if applicable
    if day != 'all':
        day_filter_num = 1
        # filter by day of week to create the new dataframe
        df = df[df['day of week'] == day.title()]
    else:
        day_filter_num = 0
        
    df['City'] = city
    df['month_filter'] = month_filter_num
    df['day_filter'] = day_filter_num
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    ######### TO DO: display the most common month #########
    # find the most common month
    if df['month_filter'].iloc[0] == 0: # Checking if month filter has been applied. If month filter has been applied, there is no reason to calculate most common month
        calc_most_common_value(df['month name'])
    
    ######### TO DO: display the most common day of week #########
    # find the most common day
    if df['day_filter'].iloc[0] == 0: # Checking if day filter has been applied. If day filter has been applied, there is no reason to calculate most common day of week
        calc_most_common_value(df['day of week'])
    

    ######### TO DO: display the most common start hour #########
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most common hour
    calc_most_common_value(df['hour'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    ######### TO DO: display most commonly used start station #########                                
    # Most Common Start Station
    calc_most_common_value(df['Start Station'])
    
    ######### TO DO: display most commonly used end station #########
    # Most Common End Station
    calc_most_common_value(df['End Station'])

    ######### TO DO: display most frequent combination of start station and end station trip #########    
    # Combine columns Start Station and End Station. Link for this information: https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-dataframe-in-pandas-python
    df['Combination Start Station And End Station'] = 'Start Station: ' + df['Start Station'] + ' -> ' + 'End Station: ' + df['End Station']
    # Most Common Combination Start Station and End Station
    calc_most_common_value(df['Combination Start Station And End Station']) 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    ######### TO DO: display total travel time #########
    ttl_trvl_time = df['Trip Duration'].sum()
    print("{} seconds is the total travel duration".format(ttl_trvl_time)) 
    
    ######### TO DO: display mean travel time #########
    mean_trvl_time = df['Trip Duration'].mean()
    print("{} seconds is the mean travel duration".format(mean_trvl_time))     

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Suppress in print -> Name: User Type, dtype: int64. 
    # Link for this information: https://stackoverflow.com/questions/24295451/suppress-descriptive-output-when-printing-pandas-dataframe
    pd.Series.__unicode__ = pd.Series.to_string 
    ######### TO DO: Display counts of user types #########
    calc_count_column(df['User Type'])
    print('') # Adding a blank line to make output display better
    
    ######### TO DO: Display counts of gender #########
    if 'Gender' in df: # Checking if Gender is a column in df. Washington city does not contain this information.
        calc_count_column(df['Gender'])
    else:
        print('{} does not contain Gender information'.format(df['City'].iloc[0].title()))
    print('') # Adding a blank line to make output display better
    
    ######### TO DO: Display earliest, most recent, and most common year of birth #########
    if 'Birth Year' in df: # Checking if Birth Year is a column in df. Washington city does not contain this information.
        # Minimum birth year is the earliest year of birth
        earliest_by = df['Birth Year'].min()
        print("{} is the earliest birth year for users".format(earliest_by))   
    
        # Maximum birth year is the most recent year of birth
        mst_recent_by = df['Birth Year'].max()
        print("{} is the most recent birth year for users".format(mst_recent_by))      
    
        # Calculate Most Common Birth year
        calc_most_common_value(df['Birth Year']) 
    else:
        print('{} does not contain Birth Year information'.format(df['City'].iloc[0].title()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function to calculate count of different values in a column
def calc_count_column(df_column):
    # Calculate value counts for each value in df_column
    count_column = df_column.value_counts()
    # Use name of column in the output. This way same output format can be used for several columns
    column_name = df_column.name.lower()
    print('Counts for different {}:'.format(column_name))
    print(count_column)

# Function to calculate most common value in a column and print the value along with the number of times the value occurs
def calc_most_common_value(df_column):
    # Calculate most common value and count for most common value
    mostcomm = df_column.value_counts().idxmax()
    mostcomm_num = df_column.value_counts().max()
    # Use name of column in the output. This way same output format can be used for several columns
    column_name = df_column.name.lower()
    print("{} is the most common {} and its count is {}".format(mostcomm, column_name, mostcomm_num))
 

def disp_raw_data(df):
    while True:
        should_display = input('\nWould you like to display raw data? Enter yes or no.\n')
        if should_display.lower() == 'no':
            break
        elif should_display.lower() == 'yes':
            while True:
                try:
                    num_lines_display = int(input('How many lines do you want displayed at a time? Enter an integer.\n'))
                    print(df.head(num_lines_display))
                    break
                except:
                    print('Wrong Input. Enter an integer.\n')
            break
        else:
            print('Wrong Input. Enter yes or no.\n')

            
def additional_stats(df):
    if 'Birth Year' in df:
        print('\nAverage Trip Duration per Birth Year')
        print(df.groupby(['Birth Year'])['Trip Duration'].mean())
        print('')
    if 'Gender' in df:
        print('\nAverage Trip Duration per Gender')
        print(df.groupby(['Gender'])['Trip Duration'].mean())
        print('')
    print('\nAverage Trip Duration per Month')
    print(df.groupby(['month name'])['Trip Duration'].mean())
    print('')
    print('\nAverage Trip Duration per Day of week')
    print(df.groupby(['day of week'])['Trip Duration'].mean())
    print('')
    if 'Birth Year' in df:
        print("\nDescriptive statistics for 'Trip Duration', 'Birth Year':")
        print(df[['Trip Duration', 'Birth Year']].describe()) #https://stackoverflow.com/questions/11285613/selecting-columns-in-a-pandas-dataframe
        print('')
        print("\nCorrelation between 'Trip Duration', 'Birth Year':")
        print(df[['Trip Duration', 'Birth Year']].corr())
    else:
        print("\nDescriptive statistics for 'Trip Duration':")
        print(df[['Trip Duration']].describe()) #https://stackoverflow.com/questions/11285613/selecting-columns-in-a-pandas-dataframe
        print('')        


            
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        disp_raw_data(df)
        calc_addnl_stats = input('\nWould you like to get additional statistics on data? Enter yes or no.\n')
        if calc_addnl_stats.lower() == 'yes':
            additional_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            break
        elif restart.lower() != 'yes' and restart.lower() != 'no':
            print('Wrong Input. We will not restart.\n')
            break

if __name__ == "__main__":
	main()
