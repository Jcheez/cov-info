import asyncio
import datetime
import numpy as np
import aiohttp


links = ["https://api.apify.com/v2/key-value-stores/yaPbKe9e5Et61bl7W/records/LATEST?disableRedirect=true", "https://api.apify.com/v2/datasets/suHgi59tSfu02VsRO/items?limit=16&desc=true"]
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

### Historical Items ###
newresult = data[1]
newresult.reverse()
def map_func(dictionary):
    dictionary["date"] = str(datetime.datetime.strptime(dictionary['lastUpdatedAtApify'], "%Y-%m-%dT%H:%M:%S.000Z").date())
    return dictionary
newresult = list(map(map_func, newresult))
for d in newresult:
    d['updatedActive'] = d['inCommunityFacilites'] + d['stableHospitalized'] + d['criticalHospitalized']
    d["updatedInfected"] = d['deceased'] + d['updatedActive'] + d['discharged']
infections = list(np.diff(list(map(lambda x: x['updatedInfected'], newresult))))
infections.insert(0,0)
counter = 0
for d in newresult:
    d["communityCases"] = infections[counter]
    counter += 1