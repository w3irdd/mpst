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
            "status",
            "object.type",
            "text",
            "uuid"
    ],
    "top": None,
    "where": "(event_src.vendor = \"fortinet\") AND (msgid = \"0419016384\")"
}

vpn_connects = {
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
            "status",
            "object.type",
            "text"
    ],
    "top": None,
    "where": "(task_id = \"1a25286e-9600-0001-0000-000000000006\") AND (recv_ipv4 = \"10.100.3.26\") AND (msgid = \"722051\")"
}