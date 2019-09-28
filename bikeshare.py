import pandas as pd

def main():
    '''This function calculates:
        1- Popular times of travel (month, day of week, hour)
        2- Trip duration (total travel time, average travel time)
        3- Popular stations and trip (most common start station, most common end station, most common trip from start to end)
        4- User info (counts of each user type, counts of each gender, earliest, most recent, and most common year of birth ).'''

    
    '''Selecting and filtering inputs and reading data'''
    user_input = ''
    cities = {'1': 'chicago.csv', '2':'new_york_city.csv','3':'washington.csv'}
      
    while user_input not in ['1','2','3','4']:   
        user_input = input('please select which city you want to run the statistics on:\n\
        (type the number of the city)\n\
        \n1 for Chicago\n\
2 for NewYork city\n\
3 for Washington\n\
4 to exit\n')
        if user_input in ['1','2','3']:
            break
        elif  user_input == '4':
            return user_input
        while user_input not in ['1','2','3','4']:
            user_input = input('you did not enter a right input.\nPlease enter \n1 for Chicago\n\
2 for NewYork City\n\
3 for Washington: \n')
        
    data = pd.read_csv(cities[user_input])
    
    def common_time(data):
        '''Common time: getting the most common month, day, hour in which most rentals happened.
           Inputs:
               data: the city the user selected.'''
        
        
        month_dic = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May',
                     6:'June', 7:'July', 8:'August', 9:'Septemper',
                     10:'October', 11:'November', 12:'December'}
        
        dow_dic = {0:'Monday', 1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
        
        hour_dic = {13:'1 Pm', 14:'2 Pm',15:'3 Pm',16:'4 Pm',17:'5 Pm',18:'6 Pm',
                    19:'7 Pm',20:'8 Pm',21:'9 Pm',22:'10 Pm',23:'11 Pm'}
        
        '''Adding the month, day of week, and hour in a seperate series.'''
        
        data['Start Time'] = pd.to_datetime(data['Start Time'])
        time_ser = pd.DataFrame(data['Start Time'])
        time_ser['travel time']= data['Trip Duration']
        time_ser['month'] = data['Start Time'].dt.month
        time_ser['day of week'] = data['Start Time'].dt.weekday
        time_ser['hour'] = data['Start Time'].dt.hour
        
        '''Grouping by month, day of week, and hour in seperate serieses.'''
        
        month = time_ser.groupby(['month']).size()
        month.rename(index=month_dic, inplace = True)
        month_result = 'The common month in which most bike rentals happened in 2017 is: {} \nand the total rentals in this month is {}\n\n'.format(month.idxmax(), month.max()) #get the value of the row of the max column value
        
        day_of_week = time_ser.groupby(['day of week']).size()
        day_of_week.rename(index=dow_dic, inplace = True)
        dow_result = 'The common day of week in which most bike rentals happened during 2017 is: {} \nand the total rentals in this day is {}\n\n'.format(day_of_week.idxmax(), day_of_week.max())
        
        hour = time_ser.groupby(['hour']).size()
        hour.rename(index=hour_dic, inplace = True)
        hour_result ='The common hour in which most bike rentals happened during 2017 is: {} \nand the total rentals during this hour is {}\n\n'.format(hour.idxmax(), hour.max())
        
        print('\nAnalysis finished!\n\nthe results are:\n{}{}{}'.format(month_result, dow_result, hour_result))
    
        def travel_time(data):
            '''Calculate the total and mean travel time.
               Inputs:
                   data: the city the user selected'''
            
            dur_sum = data['travel time'].sum()
            mean = data['travel time'].mean()
            return 'The total travel time during 2017 is {} seconds.\nThe average travel time during 2017 is {} seconds'.format(dur_sum,mean)
        
        print(travel_time(time_ser))
    
    
    def common_station_trip(data):
        '''Showing the most common start station, end station, and combination of start and end stations for travels.
           Inputs:
               data: the city the user selected'''
        
        start_stat = pd.DataFrame(data['Start Station'])
        start_stat['End Station'] = data['End Station']
        comm_start = start_stat.groupby(['Start Station']).size()
        comm_end = start_stat.groupby(['End Station']).size()
        comm_start_end = start_stat.groupby(['Start Station', 'End Station']).size()
        
        print ('\nThe most common Start Station during 2017 is {} with {} travels.\n\
The most common End Station during 2017 is {} with {} travels.'.format(comm_start.idxmax(), comm_start.max(), comm_end.idxmax(), comm_end.max()))
        print('The most common combination of start and end station during 2017 is {} with number of travels of {}'.format(comm_start_end.idxmax(), comm_start_end.max()))    
    
    def cst_types_gender(data,user_input):
        '''cst_types_gender calculates the number of each customer type, earliest, recent, and most common birth year.
           Inputs:
               data: the data selected by the user
               user_input: the number corresponding to the data'''
        
        user_info = pd.DataFrame(data['User Type'])
        counts = user_info.groupby(['User Type']).size()
        
        print('\nThis city has {} customer types.'.format(len(counts.index)))
        for i in counts.index:
            print('There are {} as customer type "{}"'.format(counts[i], i))
        
        if user_input != '3':
            gender_type = pd.DataFrame(data['Gender'])
            gender_type = gender_type.groupby(['Gender']).size()
            
            print('\nThere are {} who did not enter their Gender type'.format(len(data['Gender'])- gender_type.sum()))
            for i in gender_type.index:
                print('There are {} persons as {}'.format(gender_type[i], i))
            
            birth_year = pd.DataFrame(data['Birth Year'])
            birth_year_group = birth_year.groupby(['Birth Year']).size()
            byear_NAN_values = '\nThere are {} persons who did not enter their birth year'.format(len(data['Birth Year'])- birth_year_group.sum())
            common_year = 'The most common year of birth is {} with {} persons'.format(int(birth_year_group.idxmax()), birth_year_group.max())
            oldest_youngest = 'The earliest Birth Year is {}, while the most recent Birth year is {}'.format(int(birth_year['Birth Year'].min()), int(birth_year['Birth Year'].max()))
            
            return  byear_NAN_values, common_year, oldest_youngest
    
    common_time(data)
    common_station_trip(data)
    
    if user_input != '3':
        for i in cst_types_gender(data,user_input):
            print(i)
    else:
        cst_types_gender(data,user_input)
    
    def show_5lines(data):
        '''Showing 5 lines of raw data at a time on user request.
           Inputs:
                data: the city the user selected'''
        
        show_5 = input('Do you want to see the raw data?\n\n\
    type:\n\
    1 for yes\n\
    2 for no\n')
        n=0
        
        while show_5 == '1':
            print(data.loc[n:n+4, :])
            n+=5
            show_5 = input('continue?\n\n\
    type:\n\
    1 for yes\n\
    2 for no\n')
            while show_5 not in ['1','2']:
                show_5 = input('you did not enter a right number.\n\
    please type:\n\
    1 for yes\n\
    2 for no\n')
                if show_5 in ['1','2']:
                    break
    show_5lines(data)
    
user_input = main()

while True:
    '''Re-running the analysis or exit on user request.'''
    
    if user_input == '4':
        break
    retry = input('Do you want to rerun the analysis on different city?\n\
type:\n\n\
1 for yes\n\
2 to exit\n')
    if retry == '1':
        user_input = main()
    elif retry == '2':
        break
    else:
        print('You did not enter a correct choice')
        