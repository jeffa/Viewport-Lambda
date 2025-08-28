import json
from window.viewport import viewport

def lambda_handler(event, context):

    # Common CORS headers
    cors_headers = {
        "Access-Control-Allow-Origin":  "*",
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
    }
    
    #TODO: do not use GET -- pass JSON as POST
    # Extract the query string parameter
    query_string_parameters = event.get('queryStringParameters', {})
    coordinates = query_string_parameters.get('coordinates', '')

    # Parse the coordinates, expecting a format like "x1,y1;x2,y2;...;xn,yn"
    if not coordinates:
        return {
            "statusCode": 400,
            "headers": cors_headers,
            "body": json.dumps({"error": "No coordinates provided"})
        }

    coordinate_pairs = coordinates.split(';')

    try:
        # Create viewport object
        world_bounds = (0, 1, 0, 1)
        view_bounds = (-1, 1, -1, 1)
        vp = viewport(world_bounds=world_bounds, view_bounds=view_bounds)

        # Transform the coordinates
        transformed_points = []

        for pair in coordinate_pairs:
            x_str, y_str = pair.split(',')
            x, y = float(x_str), float(y_str)
            transformed_x = vp.Dx(x)
            transformed_y = vp.Dy(y)
            transformed_points.append(f"{transformed_x},{transformed_y}")

        # Return transformed coordinates as a delimited string
        transformed_coordinates = ';'.join(transformed_points)

        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps({"transformed_coordinates": transformed_coordinates})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": str(e)})
        }


