# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Anthony Lem
# Collaborators (discussion):
# Time:

import pylab
import re #Provides full support for Perl-like regular expressions in Python

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',') #strip removes all whitespace at the start and end
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')]) #The index method returns the index in header where 'DATE' occurs
#re.match(pattern, string) is a method and it checks to see if the string is in the pattern. In this case, \d represents a decimal digit. It returns a match object.
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available" #Raises ArgumentExpression if it fails and terminates the program
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x) #Calculate stdDev of pop/sqrt(n) = SE
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for d in degs:
        fit = pylab.polyfit(x, y, d)
        models += [fit]
    return models

#print(generate_models(pylab.array([1961, 1962, 1963]), pylab.array([-4.4, -5.5, -6.6]), [1, 2]))
#print(generate_models(pylab.array(range(50)), pylab.array(range(0,100,2)),[1,2,20]))
      
def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    return 1 - sum((y - estimated)**2)/sum((y - pylab.mean(y))**2)

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        predictions = pylab.polyval(model, x)
        pylab.figure()
        pylab.plot(x, y, 'bo')
        pylab.plot(x, predictions, 'r')
        pylab.xlabel('Years')
        pylab.ylabel('Temperature (degrees C)')
        if len(model) == 2:
            pylab.title('Plot of Actual Temperatures Each Year Versus Predicted Values ' + 'Degree of Model: ' + str(len(model)-1) + ' R2 = ' + str(r_squared(y, predictions)))
        else:
            pylab.title('Plot of Actual Temperatures Each Year Versus Predicted Values ' + 'Degree of Model: ' + str(len(model)-1))
    pylab.show()
    return None

#models = generate_models(pylab.array(range(50)), pylab.array(range(0,100,2)),[1,2,20])
#evaluate_models_on_training(pylab.array(range(50)), pylab.array(range(0,100,2)),models)

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    average_temperature = []
    temp = 0
    for year in years:
        for city in multi_cities:
            temp += (climate.get_yearly_temp(city, year)).mean()
        temp = temp/len(multi_cities)
        average_temperature += [temp]
        temp = 0
    return pylab.array(average_temperature)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    average = []
    for i in range(len(y)):
        avg = 0
        counter = 0
        for e in range(window_length):
            if (i-e) >= 0:
                avg += y[i-e]
                counter += 1
            else:
                pass
        avg = avg/counter
        average += [avg]
    return pylab.array(average)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    result = 0
    for i in range(len(y)):
        result += (y[i] - estimated[i])**2
    result /= len(y)
    return result**0.5

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    std_devs = []
    for year in years:
        yearly_temps = []
        for month in range(1,13):
            for day in range(1,32):
                avg_temp = 0
                viable = False
                for city in multi_cities:
                    try:
                        avg_temp += climate.get_daily_temp(city, month, day, year)
                        viable = True
                    except:
                        pass
                if viable:
                    avg_temp /= len(multi_cities)
                    yearly_temps += [avg_temp]
        std_devs += [pylab.std(yearly_temps)]
    return pylab.array(std_devs)
    """for year in years:
        temperatures = []
        for city in multi_cities:
            temperatures += [gen_cities_avg(climate, [city], [year])]
        std_devs += [pylab.std(temperatures)]
    return pylab.array(std_devs)
    """    
def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        predictions = pylab.polyval(model, x)
        pylab.figure()
        pylab.plot(x, y, 'bo')
        pylab.plot(x, predictions, 'r')
        pylab.xlabel('Years')
        pylab.ylabel('Temperature (degrees C)')
        pylab.title('Plot of Actual Temperatures Each Year Versus Predicted Values; ' + 'Degree of Model: ' + str(len(model)-1) + '; RMSE = ' + str(rmse(y, predictions)))
    pylab.show()
    return None


if __name__ == '__main__':

    # Part A.4
    climate = Climate('data.csv')
    test_interval = pylab.array(TRAINING_INTERVAL)
    prediction_interval = pylab.array(TESTING_INTERVAL)
    test_data = []
    for year in TRAINING_INTERVAL:
        test_data += [climate.get_daily_temp('NEW YORK', 1, 10, year)]
    test_data = pylab.array(test_data)
    models = generate_models(test_interval, test_data, [1])
    evaluate_models_on_training(test_interval, test_data, models)
    print(se_over_slope(test_interval, test_data, pylab.polyval(models[0], test_interval), models[0]))

    test_data2 = []
    for year in TRAINING_INTERVAL:
        yearly_temp = climate.get_yearly_temp('NEW YORK', year)
        average_temp = sum(yearly_temp)/len(yearly_temp)
        test_data2 += [average_temp]
    test_data2 = pylab.array(test_data2)
    models = generate_models(test_interval, test_data2, [1])
    evaluate_models_on_training(test_interval, test_data2, models)
    print(se_over_slope(test_interval, test_data2, pylab.polyval(models[0], test_interval), models[0]))
    
    # Part B
    test_data_B = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    models = generate_models(test_interval, test_data_B, [1])
    evaluate_models_on_training(test_interval, test_data_B, models)
    print(se_over_slope(test_interval, test_data_B, pylab.polyval(models[0], test_interval), models[0]))
    
    # Part C
    test_data_C = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    average = moving_average(test_data_C, 5)
    models = generate_models(test_interval, average, [1])
    evaluate_models_on_training(test_interval, average, models)
    
    # Part D.2
    training_data = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
    average = moving_average(training_data, 5)
    models = generate_models(test_interval, average, [1, 2, 20])
    evaluate_models_on_training(test_interval, average, models)

    testing_data = gen_cities_avg(climate, CITIES, TESTING_INTERVAL)
    testing_average = moving_average(testing_data, 5)
    evaluate_models_on_testing(prediction_interval, testing_average, models)
    
    # Part E
    std_devs = gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
    average = moving_average(std_devs, 5)
    models = generate_models(test_interval, average, [1])
    evaluate_models_on_training(test_interval, average, models)
