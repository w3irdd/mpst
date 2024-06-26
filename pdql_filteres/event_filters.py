fortinet_attacks = {
    "aggregateBy": [],
    "aliases": None,
    "distributeBy": [],
    "groupBy": [],
    "orderBy": [
        {
            "field": "time",
            "sortOrder": "descending"
        }
    ],
    "select": [
            "time",
            "event_src.host",
            "src.ip",
            "src.geo.country",
            "dst.host",
            "dst.ip",
            "dst.port",
            "object.state",
            "object.type",
            "text",
            "uuid"
    ],
    "top": None,
    "where": "(event_src.vendor = \"fortinet\") AND (msgid = \"0419016384\")"
}
