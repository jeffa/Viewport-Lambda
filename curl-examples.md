Below are a few usage examples of querying the AWS Lambda function from the Linux command line using `curl`.
These examples demonstrate how to send a JSON payload via a POST request to the API.

### POST Request with Required Valid Data
```bash
curl -X POST https://your-api-endpoint.amazonaws.com/dev/transform \
-H "Content-Type: application/json" \
-d '{
    "coordinates": [[1, 2], [3, 4], [5, 6]],
}'
```

### POST Request with Optional Valid Data
```bash
curl -X POST https://your-api-endpoint.amazonaws.com/dev/transform \
-H "Content-Type: application/json" \
-d '{
    "coordinates": [[1, 2], [3, 4], [5, 6]],
    "world_bounds": [0, 1, 0, 1],       # quadrant 1 only
    "view_bounds": [500, 0, 0, 250]     # scale x and y and invert y
}'
```

### POST Request with Different Coordinate Values
```bash
curl -X POST https://your-api-endpoint.amazonaws.com/dev/transform \
-H "Content-Type: application/json" \
-d '{ "coordinates": [[10, 20], [30, 40]] }'
```

### POST Request with Invalid Coordinate Pair
```bash
curl -X POST https://your-api-endpoint.amazonaws.com/dev/transform \
-H "Content-Type: application/json" \
-d '{ "coordinates": [[10, 20], [30]] }'
```

### POST Request with Invalid JSON Format
```bash
curl -X POST https://your-api-endpoint.amazonaws.com/dev/transform \
-H "Content-Type: application/json" \
-d '{
    "coordinates": [[10, 20}, [30, 40]],    # Invalid bracket here
    "world_bounds": [-1, 1, -1, 1]          # all four quadrants
    "view_bounds": [500, 0, 0, 250]
}'
```

### Getting Method Not Allowed Error
```bash
curl -X GET https://your-api-endpoint.amazonaws.com/dev/transform \
-H "Content-Type: application/json"
```
