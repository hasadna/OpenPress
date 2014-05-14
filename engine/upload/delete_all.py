import pysolr

def main():
    # Setup a Solr instance. The timeout is optional.
    solr = pysolr.Solr('http://localhost:8983/solr/', timeout=10)
    solr.delete(q='*:*')

if __name__ == "__main__":
    main()
