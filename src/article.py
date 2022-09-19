

class Article():

    def __init__(self, article_id, source, publication_date, section, headline, abstract, body):
        self.article_id = article_id
        self.source = source
        self.publication_date = publication_date
        self.section = section
        self.headline = headline
        self.abstract = abstract
        self.body = body
    
    def generate_metadata_table(self):
        pass
    
    def generate_headline_table(self):
        pass

    def generate_abstract_table(self):
        pass

    def generate_body_table(self):
        pass