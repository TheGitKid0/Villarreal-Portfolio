from os.path import basename, exists
import matplotlib.pyplot as plt

"""Function to download correct file"""
def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve
        local, _ = urlretrieve(url, filename)
        print('Downloaded ' + local)
download('https://github.com/AllenDowney/ModSimPy/raw/master/modsim.py')

from pandas import read_html
from modsim import *


"""Function representing quadratic model for population growth """
def growth_func_quad(t, pop, system):
    return system.alpha * pop + system.beta * pop**2

"""Function that will run our simulation using growth function"""
def run_simulation1(system, growth_func):
    results = TimeSeries()
    results[system.t_0] = system.p_0
    
    for t in range(system.t_0, system.t_end):
        # add our 'snap date' when year is 2025
        if t == 2025:
            results[t] = results[t] / 2
             

        growth = growth_func(t, results[t], system)
        results[t+1] = results[t] + growth
        # expanded model to account for old age loss of population
        #results[t+1] = results[t+1] * 0.85 
        
    return results


# get table information 
filename = 'https://en.wikipedia.org/wiki/Estimates_of_historical_world_population'
tables = read_html(filename,
                   header=0,
                   index_col=0,
                   decimal='M')


# our table which displays data from 1950-2016
table2 = tables[2]
table2.columns = ['census', 'prb', 'un', 'maddison', 
                  'hyde', 'tanton', 'biraben', 'mj', 
                  'thomlinson', 'durand', 'clark']

census = table2.census / 1e9 # 1e9 --> 1 billion 


# parameter data
t_0 = census.index[50] # data starting at year 2000'
p_0 = census[t_0]

# define our system 
system = System(t_0 = t_0,
                p_0 = p_0,
                alpha = 25 / 1000,
                beta = -1.8 / 1000,
                t_end = 2100)                                

# get results
results = run_simulation1(system, growth_func_quad)


def run_simulation2(system, growth_func):
    results2 = TimeSeries()
    results2[system.t_0] = system.p_0
    
    for t in range(system.t_0, system.t_end):
        # add our 'snap date' when year is 2025
        if t == 2025:
            results2[t] = results2[t] / 2 
            
        if t == 2030:
            results2[t] = results2[t] + results2[2025] 

        growth = growth_func(t, results2[t], system)
        results2[t+1] = results2[t] + growth
        
    return results2

# simulation 2 where people return after 5 years 
results2 = run_simulation2(system, growth_func_quad) 

yearly_sacrifices = .0853 # 85 million people will be sacrificed a year

def run_simulation3(system, growth_func):
    results = TimeSeries()
    results[system.t_0] = system.p_0

    for t in range(system.t_0, system.t_end):
        growth = growth_func(t, results[t], system)
        results[t] = results[t] - yearly_sacrifices
        results[t+1] = results[t] + growth

        # account for annual sacrifices 
        #results[t] = results[t] * yearly_sacrifices
        
    return results

results3 = run_simulation3(system, growth_func_quad)
print(results3)
