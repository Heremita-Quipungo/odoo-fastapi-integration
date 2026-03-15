import xmlrpc.client

ODOO_URL = "http://localhost:8070"
DB = "sale_quotation1"
USERNAME = "admin"
PASSWORD = "admin"  # ou API KEY

common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(DB, USERNAME, PASSWORD, {})

models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")


def create_sale_order(partner_id: int, lines: list):
    return models.execute_kw(
        DB, uid, PASSWORD,
        'sale.order',
        'create',
        [{
            'partner_id': partner_id,
            'order_line': [
                (0, 0, {
                    'product_id': line['product_id'],
                    'product_uom_qty': line['qty'],
                    'price_unit': line['price']
                }) for line in lines
            ]
        }]
    )


def list_sales(limit=30):
    return models.execute_kw(
        DB, uid, PASSWORD,
        'sale.order',
        'search_read',
        [[]],
        {
            'fields': ['name', 'amount_total', 'state'],
            'limit': limit
        }
    )
