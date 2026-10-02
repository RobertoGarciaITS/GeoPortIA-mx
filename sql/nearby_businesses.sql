SELECT business_id, name, economic_activity, employee_range, latitude, longitude
FROM `${PROJECT_ID}.${DATASET}.businesses`
WHERE ST_DWITHIN(geography, ST_GEOGPOINT(@lng, @lat), @radius_m)
ORDER BY business_id;
