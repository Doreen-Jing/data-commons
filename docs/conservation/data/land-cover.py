import datacommons_pandas as dc
import pandas as pd
import os

# Retrieve all counties in Georgia (state code: 13)
georgia_counties_info = dc.get_places_in(['geoId/13'], 'County')

# Extract the DCIDs of the counties
georgia_counties_dcids = georgia_counties_info['geoId/13']

# Fetch LandCoverFraction_Forest data for each county in Georgia
forest_cover_data = {}
for county_dcid in georgia_counties_dcids:
    # Fetching only the needed information (forest cover values for each year)
    forest_data = dc.get_stat_all([county_dcid], ["LandCoverFraction_Forest"])
    if forest_data:
        forest_cover_data[county_dcid] = {
            "Location": county_dcid,
            **{year: series['val'][year] for series in forest_data[county_dcid]['LandCoverFraction_Forest']['sourceSeries'] for year in series['val']}
        }

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(forest_cover_data, orient='index')

# Save the DataFrame to a CSV file
forest_cover_path = os.path.join(os.getcwd(), 'forest_cover.csv')
df.to_csv(forest_cover_path, index=False)
