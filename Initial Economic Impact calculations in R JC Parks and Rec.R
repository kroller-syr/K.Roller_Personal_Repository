a<-0.071278
b<-0.4074
# Need package "SciViews" for ln() function 
library(SciViews)
chang<-1.566+(0.53 * ln(a)) - (0.009 * b)
chang
# Code broken here, not sure why, Chang==1.42583
# This value calculated using JC pop not Washington County

chang_calc<-1.42583
# where a is the InPOP or natural log of regions population in millions
# where b is the POPDEN or population density in thousands of persons per square mile


#Then need to apply Stynes method for adjusting to capture rate
#Expected capture rate is 60-70% so the final demand multiplier is found 
# by creating a range we can then create a better estimate for demand in the region 

styne_lower<-(0.6)*chang_calc
styne_upper<-(0.7)*chang_calc

styne_lower
styne_upper

# JC population 71,278(2021)
# Washington County population estimate(2022): 136,172


# population density of washington county per square mile=0.4074(in thousands)
# so b should be ==0.4074
#making those changes

# Total accomodation and food service sales($1000)==352,776

#Required inputs:
# 1. Number of Tourist (Estimate or otherwise)
# In example given state that the usage of other cities survey data provides a reasonable estimate
# Regardless of how it is obtained must ensure there is a distinction between local and non-local groups
# 2. Average Spending Per Visitor 
# (Look back at previous value in other document)
# 3. Appropriate Multiplier (calculated above)
# 4. Capture rate (also calculated above)

# Applying the method to JC using data used in study for columbus
# Means using Gibson et. al(2012) Small scale event sport tourism: A case study of sustainable tourism
# Study addresses direct spending at events 
# Three adult and three youth tournaments 
# This particular study is inclusive of both youth and adult programs, need to verify this is appropriate 
# Also utilizes Crompton and Lees's (2000) The Eonomic impact of 30 sports tournaments, festivals, and spectator events in seven US cities 
# Non local percentages used in this study are used as estimates 

# Looking only soccer games impact 
# Overnight total: $649.87 (Assumes average of 3 night stay)
# Day total: $206.45
# Other sports can be added in to the total as needed like softball/baseball etc
# % nonlocal Overnight: 89.48%
# % nonlocal day: 89.48%
# Total # of participants: 1050
# Adjusted total for nonlocals only: 939.54

# Before making any calculations of total spending need to take daily and overnight averges
# and then recalculate the actual cost with cost of living adjustments between Gaineville, FL and JC, TN

# The study this is based on uses a Living wage calc from MIT
# Formed a proportion on the after tax required living wage for a household with 2 adults and 2 children 
# Adjust estimated expenditures by this proportion 

# We can then calculate the DIRECT VISITOR SPENDING 
# We then use party event duration(3 days here) * the # of non locals
# This gives a value of 2,818 * avg of $206/day
# This gives us an economic impact of $580,508/year

# BUT, we then need to apply the multiplier and capture affect found from before 

#so

soccer<-580508
lower_bound<-soccer*styne_lower
upper_bound<-soccer*styne_upper

lower_bound
upper_bound 

## To consider additional sports will need to adjust number of attendees (non local)
## and consider any additional differences in spending per group
## Once those are calculated they would be summed and then subjected to the same treatment 

## BUT, now we can make a conclusion about the impact with the made assumptions
## That is, on average we could expect between $496,623 and $579,394
## of total economic impact which would reflect net cash flow 

## All sourced from "Inexpensively Estimating Economic Impact of Sports Tourism in Small American Cities"
## Posted on D2L
