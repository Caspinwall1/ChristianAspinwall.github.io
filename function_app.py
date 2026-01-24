import os
import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="visitcounter", methods=["GET"])
def visitcounter(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Visitor counter function triggered.")

    try:
        endpoint = os.environ["COSMOS_ENDPOINT"]
        key = os.environ["COSMOS_KEY"]

        client = CosmosClient(endpoint, credential=key)
        database = client.get_database_client("ResumeDB")
        container = database.get_container_client("VisitorCounter")

        item = container.read_item(item="counter", partition_key="resume")
        item["count"] += 1
        container.replace_item(item=item["id"], body=item)

        return func.HttpResponse(
            json.dumps({"count": item["count"]}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500
        )