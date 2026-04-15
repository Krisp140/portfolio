import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const BIKEWATCH_DIR = join(import.meta.dirname, '..', '..', 'bikewatch');
const OUTPUT_DIR = join(import.meta.dirname, '..', 'static', 'bikewatch');

mkdirSync(OUTPUT_DIR, { recursive: true });

// Step 1: Fetch station locations from BlueBikes GBFS
console.log('Fetching station locations from GBFS...');
const gbfsRes = await fetch('https://gbfs.bluebikes.com/gbfs/en/station_information.json');
const gbfsData = await gbfsRes.json();
const stationsRaw = gbfsData.data.stations;

const stationMap = new Map();
for (const s of stationsRaw) {
  stationMap.set(s.station_id, {
    station_id: s.station_id,
    name: s.name,
    lat: s.lat,
    lon: s.lon,
  });
}
console.log(`  Found ${stationMap.size} stations`);

// Step 2: Aggregate trips
console.log('Reading trip data...');
const csvPath = join(BIKEWATCH_DIR, 'bluebikes-traffic-2024-03.csv');
const csvText = readFileSync(csvPath, 'utf-8');
const lines = csvText.trim().split('\n');
const headers = lines[0].split(',');

const startIdIdx = headers.indexOf('start_station_id');
const endIdIdx = headers.indexOf('end_station_id');
const startedAtIdx = headers.indexOf('started_at');
const endedAtIdx = headers.indexOf('ended_at');

// departures[station_id][hour] and arrivals[station_id][hour]
const departures = {};
const arrivals = {};

for (let i = 1; i < lines.length; i++) {
  const cols = lines[i].split(',');
  const startId = cols[startIdIdx];
  const endId = cols[endIdIdx];
  const startedAt = cols[startedAtIdx];
  const endedAt = cols[endedAtIdx];

  if (startId && startedAt) {
    const depHour = new Date(startedAt).getHours();
    if (!departures[startId]) departures[startId] = new Array(24).fill(0);
    departures[startId][depHour]++;
  }

  if (endId && endedAt) {
    const arrHour = new Date(endedAt).getHours();
    if (!arrivals[endId]) arrivals[endId] = new Array(24).fill(0);
    arrivals[endId][arrHour]++;
  }
}

console.log('  Aggregated trips');

// Step 3: Build output — stations.csv and hourly_demand.json
const allStationIds = new Set([
  ...Object.keys(departures),
  ...Object.keys(arrivals),
]);

const stationRows = [];
const hourlyDemand = {};

for (const id of allStationIds) {
  const station = stationMap.get(id);
  if (!station) continue; // skip stations not in GBFS

  const depArr = departures[id] || new Array(24).fill(0);
  const arrArr = arrivals[id] || new Array(24).fill(0);

  const totalDepartures = depArr.reduce((a, b) => a + b, 0);
  const totalArrivals = arrArr.reduce((a, b) => a + b, 0);

  stationRows.push({
    station_id: id,
    name: station.name,
    lat: station.lat,
    lng: station.lon,
    totalArrivals,
    totalDepartures,
  });

  const hourly = [];
  for (let h = 0; h < 24; h++) {
    hourly.push({ hour: h, arrivals: arrArr[h], departures: depArr[h] });
  }
  hourlyDemand[id] = { hourly };
}

// Write stations.csv
const csvHeader = 'station_id,name,lat,lng,totalArrivals,totalDepartures';
const csvRows = stationRows.map(
  (r) =>
    `${r.station_id},"${r.name.replace(/"/g, '""')}",${r.lat},${r.lng},${r.totalArrivals},${r.totalDepartures}`
);
writeFileSync(join(OUTPUT_DIR, 'stations.csv'), [csvHeader, ...csvRows].join('\n'));
console.log(`  Wrote stations.csv (${stationRows.length} stations)`);

// Write hourly_demand.json
writeFileSync(join(OUTPUT_DIR, 'hourly_demand.json'), JSON.stringify(hourlyDemand));
console.log('  Wrote hourly_demand.json');

// Step 4: Cambridge bike lanes
console.log('Downloading Cambridge bike lanes...');
const cambridgeRes = await fetch(
  'https://raw.githubusercontent.com/cambridgegis/cambridgegis_data/main/Recreation/Bike_Facilities/RECREATION_BikeFacilities.geojson'
);
const cambridgeGeoJSON = await cambridgeRes.text();
writeFileSync(join(OUTPUT_DIR, 'cambridge_bike_lanes.geojson'), cambridgeGeoJSON);
console.log('  Wrote cambridge_bike_lanes.geojson');

// Copy Boston bike lanes
console.log('Copying Boston bike lanes...');
const bostonGeoJSON = readFileSync(
  join(BIKEWATCH_DIR, 'Existing_Bike_Network_2022.geojson'),
  'utf-8'
);
writeFileSync(join(OUTPUT_DIR, 'boston_bike_lanes.geojson'), bostonGeoJSON);
console.log('  Wrote boston_bike_lanes.geojson');

console.log('Done!');
