import asyncio
import datetime
import numpy as np
import aiohttp
import pandas as pd

links = ["https://api.apify.com/v2/key-value-stores/yaPbKe9e5Et61bl7W/records/LATEST?disableRedirect=true", "https://api.apify.com/v2/datasets/suHgi59tSfu02VsRO/items?limit=15&desc=true", "https://api.apify.com/v2/datasets/suHgi59tSfu02VsRO/items?limit=31&desc=true"] # Latest, 2 weeks, 1 Month
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for l in links:
            task = asyncio.ensure_future(get_data(l, session))
            tasks.append(task)
        data = await asyncio.gather(*tasks)
    return data

async def get_data(link, session):
    async with session.get(link) as response:
        result_data = await response.json()
        return result_data

data = asyncio.get_event_loop().run_until_complete(main())

### Latest Item ###
result = data[0]
result['updatedActive'] = result['inCommunityFacilites'] + result['stableHospitalized'] + result['criticalHospitalized']
result["updatedInfected"] = result['deceased'] + result['updatedActive'] + result['discharged']
date = result['lastUpdatedAtApify']
newdate = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z")    
result['lastUpdatedAtApify'] = str(newdate)

def map_func(dictionary):
        dictionary["date"] = str(datetime.datetime.strptime(dictionary['lastUpdatedAtApify'], "%Y-%m-%dT%H:%M:%S.000Z").date())
        dictionary['dateTime'] = datetime.datetime.strptime(dictionary['lastUpdatedAtApify'], "%Y-%m-%dT%H:%M:%S.000Z")
        return dictionary

def formatResult(newresult):
    newresult.reverse()
    newresult = list(map(map_func, newresult))
    for d in newresult:
        d['updatedActive'] = int(d['inCommunityFacilites'] + d['stableHospitalized'] + d['criticalHospitalized'])
        d["updatedInfected"] = int(d['deceased'] + d['updatedActive'] + d['discharged'])

    # This code chunk formats data by only allowing 1 entry per date
    mapOutDates = list(set(list(map(lambda x: x['date'], newresult))))
    mapOutDates.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"))
    formattedDates = []
    for date in mapOutDates:
        filtered_data = list(filter(lambda x: x['date'] == date, newresult))
        if len(filtered_data) > 1:
            mapOutDatesFromFiltered = list(map(lambda x: x['dateTime'], filtered_data))
            latestDate = max(mapOutDatesFromFiltered)
            filtered = list(filter(lambda x: x['dateTime'] == latestDate, filtered_data))
            formattedDates.append(filtered[0])
        else:
            formattedDates.append(filtered_data[0])

    infections = list(np.diff(list(map(lambda x: x['updatedInfected'], formattedDates))))
    infections.insert(0,0)
    counter = 0
    for d in formattedDates:
        d["communityCases"] = int(infections[counter])
        counter += 1

    return formattedDates

def comparePast2Days(data):
    result = {}
    newdata = data.copy()
    newdata.reverse()
    newdata = newdata[:2]
    for row in newdata[0].keys():
        datapacket = list(map(lambda x: x[row], newdata))
        if type(datapacket[0]) == int:
            result[row] = datapacket[0] - datapacket[1]

    return result

twoWeeks = formatResult(data[1])

oneMonth = formatResult(data[2])
latestStatsComparison = comparePast2Days(twoWeeks)