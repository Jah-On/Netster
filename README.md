# Netster
A tool to track the performance of your network

I made this repo for my capstone PLTW Engineering course to collect data on network performance degradation due to inadequate cooling systems found in consumer routers, modems, APs, swtiches, etc.

If you would like to help with data collection, share personal testimonials about your equipment overheating and underperforming, your janky solutions to fix it, ideas our team should consider, or anything related to the stated issue, please open a new issue or comment on an existing one! 

This lib requires the speedtest-cli library, which can be installed with
```python3 -m pip install speedtest-cli```

If you also want the GUI, you need DearPyGUI. Note this is temporarily the release candidate for v1.0.0. ```python3 -m pip install dearpygui==1.0.0rc2```

To run the data collection script, run ```python3 PLTW_EDD_Data_Collection.py```

If you want to add more addresses (Default site is just CloudFlare's DNS website), like google.com, add each IP/hostname after the .py with spaces separating each. 

E.g. ```python3 PLTW_EDD_Data_Collection.py google.com example.com```


**Note: The IP/Hostname must have an open port on port 80.**

The console commands so far are ```quit``` to exit the program and ```pr``` to process the log file into CSV files.

To run the GUI, use ```gui```.

For some graphs, the number of ping address must be the same for all days. 

More stuff to come...
