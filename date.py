from datetime import datetime

## %Y: Year
##  %B: Month as Text
## %m: Month as a number
## %d: Date

date = '2017-01-28'
print(date)

database_date = datetime.strptime(date, '%Y-%m-%d') #- strptime: String Parse Time (Parse the date as a string)
print(database_date)

final_database_date = datetime.strftime(database_date, '%Y%m%d') #- strftime: String Format Time
print(final_database_date)

pretty_date = datetime.strftime(database_date, '%B %d, %Y')
print(pretty_date)