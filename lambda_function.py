import json
from window.viewport import viewport

def lambda_handler(event, context):

    # Common CORS headers
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }

    # Check if the request method is POST
    if event['httpMethod'] != 'POST':
        return {
            "statusCode": 405,
            "headers": cors_headers,
            "body": json.dumps({"error": "Method not allowed. Only POST requests are accepted."})
        }

    try:
        # Parse JSON body
        body = json.loads(event['body'])

        # Extract coordinates, world_bounds, and view_bounds from the JSON object
        coordinates = body.get('coordinates', [])
        world_bounds = tuple(body.get('world_bounds', [0, 1, 0, 1]))
        view_bounds = tuple(body.get('view_bounds', [-1, 1, -1, 1]))

        # Create viewport object
        vp = viewport(world_bounds=world_bounds, view_bounds=view_bounds)

        # Transform the coordinates
        transformed_points = []

        for pair in coordinates:
            if len(pair) != 2:
                raise ValueError("Each coordinate pair must contain exactly two values (x, y).")
            x, y = pair
            transformed_x = vp.Dx(float(x))
            transformed_y = vp.Dy(float(y))
            transformed_points.append(f"{transformed_x},{transformed_y}")

        # Return transformed coordinates as a delimited string
        transformed_coordinates = ';'.join(transformed_points)

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({"transformed_coordinates": transformed_coordinates})
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
