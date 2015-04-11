{
    'name': 'odoowarehouse',
    'version': '1.0',
    'summary': 'odoowarehouse',
    'description': """ this is my module for warehouse """,
    'author': 'fatma',
    'website': 'http://www.odooproject.com',
    'depends': ['base', 'hr'],
    'data': [
        'odoowarehouse_view.xml', 'security/odoowarehouse_security.xml', 'security/ir.model.access.csv']
}
