# Elastic Search 
- below is the command to run docker compose file 
```
docker-compose up -d
```
- Access Elasticsearch at: http://localhost:9200
- Kibana: http://localhost:5601
- URL To access Kibana Dev tool console: http://localhost:5601/app/dev_tools#/console

- Elastic search contains index, documets, mapping which contains field and value 
- Below steps that needs to follow create index and then add document in to it

- 📁 Step 1: Create Index with Settings and Mappings
```text
PUT /books
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "title":        { "type": "text" },
      "author":       { "type": "keyword" },
      "description":  { "type": "text" },
      "price":        { "type": "float" },
      "publish_date": { "type": "date" },
      "categories":   { "type": "keyword" },
      "reviews": {
        "type": "nested",
        "properties": {
          "user":    { "type": "keyword" },
          "rating":  { "type": "integer" },
          "comment": { "type": "text" }
        }
      }
    }
  }
}
```
- 📝 Step 2: Insert a Document
```text
POST /books/_doc
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "description": "A novel about the American Dream in the Jazz Age",
  "price": 9.99,
  "publish_date": "1925-04-10",
  "categories": ["Classic", "Fiction"],
  "reviews": [
    {
      "user": "reader1",
      "rating": 5,
      "comment": "A masterpiece!"
    },
    {
      "user": "reader2",
      "rating": 4,
      "comment": "Beautifully written, but a bit sad."
    }
  ]
}
```
- 🔍 Step 3: Search the Index
```text
GET /books/_search
```
- To see all documents or test specific queries:
```text
GET /books/_search
{
  "query": {
    "match": {
      "categories": "Fiction"
    }
  }
}
```
- 🧪 Step 4: Verify Index and Mapping
```text
GET /books/_mapping
```
- View Indexed Documents
```text
GET /books/_search?pretty
```