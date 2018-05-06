import requests

index = 'data'

object_example = {
    'favicon': 'some.url/favicon.ico',
    'domain': 'domain.com',
    'resource': 'some/interesting/url.html',
    'text': 'By default, internal versioning is used that starts at 1 '
            'and increments with each update, deletes included. '
            'Optionally, the version number can be supplemented '
            'with an external value (for example, '
            'if maintained in a database). '
            'To enable this functionality, '
            'version_type should be set to external. '
            'The value provided must be a numeric, long '
            'value greater or equal to 0, and less than '
            'around 9.2e+18. When using the external version type, '
            'instead of checking for a matching version number, '
            'the system checks to see if the version number '
            'passed to the index request is greater than the '
            'version of the currently stored document. '
            'If true, the document will be indexed and the new version number used. '
            'If the value provided is less than or equal to the stored document’s '
            'version number, a version conflict will occur and the'
            ' index operation will fail.',
    'title': 'some title',
    'readmore': None,
    'protocol': 'https'
}
url = 'http://localhost:9200'
r = requests.get(url)
if r.status_code != 200:
    exit()
r = requests.delete(url + index)
r = requests.put(url + index, json={
    "settings": {
        "number_of_shards": 1
    },
    "mappings": {
        "doc": {
            "properties": {
                "favicon": {"type": "text"},
                "domain": {"type": "text"},
                "resource": {"type": "text"},
                "text": {"type": "text"},
                "title": {"type": "text"},
                "readmore": {"type": "text"},
                "protocol": {"type": "text"}
            }
        }
    }
})
count = 1000
i = 1
while i < count + 1:
    r = requests.post(url='http://localhost:9200/' + index + '/doc', json=object_example)
    print("Indexing" + str(i) + "\n")
    i = i + 1
