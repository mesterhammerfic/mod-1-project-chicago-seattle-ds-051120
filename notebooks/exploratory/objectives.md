Data Overview:

# 1. What data does each table contain?

- ### ct_puma_xwalk ###
    -https://www.census.gov/programs-surveys/geography/technical-documentation/records-layout/2010-tract-to-puma-record-layout.html
    - Maps Census Tract Codes > PUMA codes.
    

- ### puma_names_2010 ###
    - Contains location information (state, geoid) for each PUMA name.
    
    
- ### pums_2017 ###


- ### wa_geo_xwalk ###
    - Contains information data on areas in Washington, Oregon, Idaho including longitude and latitude info.
    
    
- ### wa_jobs_2017 ###

---

# 2. Which tables (and what columns) correspond to which questions? 

- ### Map of which parts of king county are considered south king county. ###


    - puma_names_2010
    - ct_puma_xwalk
    - wa_geo_xwalk
    
    - ct_puma_name >(via puma name or id)> ct_puma_xwalk >(via tract name or id)> wa_geo_xwalk


- ### Update on number of OY youth in South King Country. ###
    - OY are people ages 16 to 24 who are neither *currently* in school nor working


- ### Updated Opportunity Youth Status by Age from road map report. ###
    - https://roadmapproject.org/wp-content/uploads/2018/09/Opportunity-Youth-2016-Data-Brief-v2.pdf


- ### A visualization that reports a trend between 2016 data and current data. ###


---


## Today's goals: ##

#### 1. Get everyone updated from the main repo ####
    - start branches
    - start notebooks
    
##### 2. Explore pums_2017 #####
    - what is contained in the columns
    - what sample of the population does it represent
        - Create 3 visualizations that represent the typical characteristics of the whole sample
#### 3. Start cloropleth ####
    - Find out what parts are considered South King County
    - How to make a clorpleth
    - Create a sample (even if it doesn't have the correct locations highlighted)