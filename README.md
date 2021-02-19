# Data-File-imputation
# The code is designed for energy website at Georgia Tech. Other source may need a little modification based on the style. 
# FillUnvTime will take one or multiple Excel files as input, and output one file with all the info from input. The code remove delete dupllicated rows, fill/delete empty space, and add an empty row with correct time interval if missing info is detected. It also adds statstical properties as extra columns in the end (i.e. the sum of each row)
# FillUnvTime will merge multiple tables from different files into one file. It will automatically check the time interval of each energy consumption, and return any error deteced. 
# DeleteEST will change all the date and time into '%Y-%m-%d %H:%M' formate. It will also detect and fix error caused by Daylight saving time. 
