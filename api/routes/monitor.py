"""User routes."""

from flask_restful import Resource
from api.routes.helper import create_blueprint, create_restful_api


class MonitorAPI(Resource):
    """API to monitor and track server health."""

    def get(self):
        """Check server is running."""
        return "😈"


monitor_blueprint = create_blueprint("monitor", __name__, no_prefix=True)
monitor_api = create_restful_api(monitor_blueprint)

# Register routes
monitor_api.add_resource(MonitorAPI, "/")
