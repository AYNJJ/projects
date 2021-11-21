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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
    
    if city not in ['chicago','new york city','washington']:
        while city not in ['chicago','new york city','washington']:
            city = input('Wrong city, please enter the city again choosing between Chicago, New York City and Washington.\n').lower()
    # TO DO: get user input for month (all, january, february, ... , june)
    filter = input("Would you to filter the data by month, day, both or not at all? Type \"none\" for no time filter.\n")
    
    if filter not in ['none', 'day', 'month', 'both']:
        while filter not in ['none', 'day', 'month', 'both']:
            filter = input("Wrong filter input, please enter what you'd like to filter on again choosing between, month, day, both or none.\n").lower()
    if filter in ['month','both']:
        month = input("Which month? January, February, March, April, May or June?\n").lower()
        while month not in ['january', 'february', 'march', 'april', 'may','june']:
            month = input("Wrong month, please enter a month from January to June.\n").lower()
    else:
        month = 'all'
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if filter in ['day','both']:
        day = input("Which day? Please type your respone in days (e.g Friday)\n").lower()
        while day not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            day = input("Wrong day, please enter a day from Monday to Sunday.\n").lower()
    else:
        day = 'all'

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month']== month]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    count_month = df.groupby(['month'])['month'].count()
    max_count_month = count_month.max()
    popular_month = count_month.idxmax()
    print('Most popular month: ',popular_month, 'Count:',max_count_month)

    # TO DO: display the most common day of week
    count_day = df.groupby(['day_of_week'])['day_of_week'].count()
    max_count_day = count_day.max()
    popular_day = count_day.idxmax()
    print('Most popular day: ',popular_day, 'Count:',max_count_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    count_hour = df.groupby(['hour'])['hour'].count()
    max_count_hour = count_hour.max()
    popular_hour = count_hour.idxmax()
    print('Most popular hour: ',popular_hour, 'Count:',max_count_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    count_start_station = df.groupby(['Start Station'])['Start Station'].count()
    max_count_start_station = count_start_station.max()
    popular_start_station = count_start_station.idxmax()
    print('Most popular start station: ', popular_start_station, 'Count: ', max_count_start_station)

    # TO DO: display most commonly used end station
    count_end_station = df.groupby(['End Station'])['End Station'].count()
    max_count_end_station = count_end_station.max()
    popular_end_station = count_end_station.idxmax()
    print('Most popular end station: ', popular_end_station, 'Count: ', max_count_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_station_combination = df[['Start Station', 'End Station']].mode().loc[0]
    print('Most popular start and end station combination:', popular_station_combination[0], ' to ', popular_station_combination[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].count()
    print('Total travel time for this period: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time for this period: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Usert types:', user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Gender and count:', gender_count)
    else:
        print('No Gender data available')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df['Birth Year'].fillna(0).astype(int)
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest birth year:', earliest_birth_year)
        
        most_recent_birth_year = df['Birth Year'].max()
        print('Most recent birth year:', most_recent_birth_year)

        most_common_birth_year = df['Birth Year'].mean()
        print('Most comon birth year:', most_common_birth_year)
    else:
        print('No Birth Year data available')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Displays raw data in increments of five lines per users response."""
    print(df.head())
    i = 0
    while True:
        raw_data = input('\nWould you like to view next five rows of data? Enter yes or no.\n').lower()
        if raw_data != 'yes':
            break
        i+= 5
        
        if i >= len(df):
            break
        else:
            print(df.iloc[i:i+5])
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            raw_data = input('\nWould you like to view first five row of raw data? Enter yes or no.\n')
            if raw_data.lower() != 'yes':
                break
            show_raw_data(df)
            break
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()