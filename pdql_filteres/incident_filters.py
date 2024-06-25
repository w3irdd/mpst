base_filter = {
    "select": [
      "key",
      "name",
      "category",
      "type",
      "status",
      "created",
      "description"
    ],
    "where": "",
    "orderby": [
      {
        "field": "created",
        "sortOrder": "descending"
      },
      {
        "field": "status",
        "sortOrder": "ascending"
      },
      {
        "field": "severity",
        "sortOrder": "descending"
      }
    ]
}
