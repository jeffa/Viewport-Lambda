import json
from window.viewport import viewport

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    # handle both REST-API v1 and HTTP-API v2 shapes
    method = (
        event.get("httpMethod")
        or event.get("requestContext", {}).get("http", {}).get("method")
        or "GET"
    )

    # Common CORS headers
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }

    # short-circuit OPTIONS preflight
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({"message": "OK"})
        }

    # Check if the request method is POST
    if method != 'POST':
        return {
            "statusCode": 405,
            "headers": cors_headers,
            "body": json.dumps({"error": "Method not allowed. Only POST requests are accepted."})
        }

    try:
        logger.info("API was called.")
        #logger.info("Incoming event: %s", json.dumps(event))

        # pull out the JSON string
        raw_body = event.get("body")
        if raw_body is None and "body-json" in event:
            raw_body = json.dumps(event["body-json"])

        if raw_body is None:
            return {
            "statusCode": 400,
            "headers": cors_headers,
            "body": json.dumps({ "error": "no body found" })
            }

        raw_body = event.get("body") or ""
        outer = json.loads(raw_body)

        # if API Gateway wrapped it under "body", unwrap again
        if isinstance(outer, dict) and "body" in outer and isinstance(outer["body"], str):
            body = json.loads(outer["body"])
        else:
            body = outer

        # Extract coordinates, world_bounds, and view_bounds from the JSON object
        coordinates = body.get('coordinates', [])
        world_bounds = tuple(body.get('world_bounds', [0, 1, 0, 1]))
        view_bounds = tuple(body.get('view_bounds', [100, 0, 0, 100]))

        # Create viewport object
        vp = viewport(world_bounds=world_bounds, view_bounds=view_bounds)

        # Transform the coordinates
        transformed_points = []

        for pair in coordinates:
            if len(pair) != 2:
                raise ValueError("Each coordinate pair must contain exactly two values (x, y).")
            x, y = pair
            tx = vp.Dx(float(x))
            ty = vp.Dy(float(y))
            transformed_points.append([tx, ty])

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({"coordinates": transformed_points})
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": cors_headers,
            "body": json.dumps({"error": "Invalid JSON format."})
        }
    except ValueError as ve:
        return {
            "statusCode": 400,
            "headers": cors_headers,
            "body": json.dumps({"error": str(ve)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": str(e)})
        }
