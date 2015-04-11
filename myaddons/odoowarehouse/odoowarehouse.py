#! /usr/bin/env python
# encoding:UTF-8
from openerp.osv import orm, fields


class myhr_employees(orm.Model):
    gender = [('m', 'Male'), ('f', 'Female')]
    _name = 'myhr.employee'
    _columns = {
        'name': fields.char(string="الاسم", size=50, required=True),
        'tel': fields.char(string="رقم التليفون", size=30),
        'picture': fields.binary(string="الصوره الشخصيه "),
        'age': fields.integer(string="العمر", size=2),
        'salary': fields.float(string="المرتب", size=8),
        'gender': fields.selection(gender, string="النوع"),
        'user_login': fields.many2one("res.users", "User Login"),
        'warehouse_id': fields.many2one('odoowarehouse.warehouse', 'Warehouse'),

    }
    _rec_name = 'name'
    ################################################


class odoowarehouse_warehouse(orm.Model):
    _name = 'odoowarehouse.warehouse'
    _columns = {

        'name': fields.char(string='الاسم', required=True, size=30),
        'address': fields.char(string='المكان', size=30),
        'keeper_ids': fields.one2many('myhr.employee', 'warehouse_id', string="المسئولين"),
    }

    ################################################


class odoowarehouse_category(orm.Model):
    _name = 'odoowarehouse.category'
    _columns = {
        'name': fields.char(string='الاسم ', size=50),
        'catcode': fields.integer(string='الكود', size=2),
        'subcategory_ids': fields.one2many('odoowarehouse.subcategory', 'cat_id', 'الفئه الفرعيه '),
    }

    ################################################


class odoowarehouse_subcategory(orm.Model):
    _name = 'odoowarehouse.subcategory'
    _columns = {
        'name': fields.char(string='الاسم ', size=50),
        'subcatcode': fields.integer(string='الكود', size=2),
        'cat_id': fields.many2one('odoowarehouse.category', 'الفئه'),

    }
    ################################################


class odoowarehouse_sub_subcategory(orm.Model):
    _name = 'odoowarehouse.sub.subcategory'
    _columns = {
        'name': fields.char(string='الاسم', size=50),
        'sub_subcatcode': fields.integer(string='الكود', size=2),
        'cat_id': fields.many2one('odoowarehouse.category', 'الفئه'),
        'subcat_id': fields.many2one('odoowarehouse.subcategory', 'الفئه الفرعيه ')
    }
    ################################################


class odoowarehouse_addproduct(orm.Model):
    def _concat_code(self, cr, uid, ids, name, arg, context=None):
        result = {}
        ids = self.search(cr, uid, [])
        products = self.browse(cr, uid, ids, context)
        for product in products:
            result[product.id] = str(product.cat_id.catcode) +str(
                product.subcat_id.subcatcode) +str(product.subsubcat_id.sub_subcatcode) +str(
                product.Proid)
        return result

    case = [
        ('new', 'جديد'),
        ('damage', 'هالك'),
        ('used', 'مستخدم')
    ]
    _name = 'odoowarehouse.addproduct'
    _columns = {
        'Pname': fields.char(string='الاسم', size=50),
        'Photo': fields.binary(string='صوره المنتج'),
        'Price': fields.integer(string='السعر', size=50),
        'Pmax': fields.integer(string='اكبر كميه ', size=50),
        'Pmin': fields.integer(string='اقل كميه', size=50),
        'Proid': fields.integer(string='رقم المنتج', size=2),
        'warehouse_id': fields.many2one('odoowarehouse.warehouse', 'المخزن'),
        'cat_id': fields.many2one('odoowarehouse.category', 'الفئه'),
        'subcat_id': fields.many2one('odoowarehouse.subcategory', 'الفئه الفرعيه'),
        'subsubcat_id': fields.many2one('odoowarehouse.sub.subcategory', 'القسم'),
        'Procode': fields.function(_concat_code, string='Reference', method=True, type='char', store=True),
        'case': fields.selection(case, string='الحاله'),
        'State': fields.selection([
                                      ('new', 'New'),
                                      ('received_by_keeper', 'Received_By_Keeper'),
                                      ('waiting_for_check', 'waiting_for_check'),
                                      ('accepted', 'Accepted'),
                                      ('confirm_by_keeper', 'Confirm_By_Keeper'),
                                      ('confirm_by_manger', 'Confirm_By_manger'),
                                      ('entered_the_stock', 'Entered_The_Stock'),
                                  ], string='المرحله', readonly=True),
    }

    def product_new(self, cr, uid, ids):
        self.write(cr, uid, ids, {'State': 'new'})
        return True

    def product_received(self, cr, uid, ids):
        self.write(cr, uid, ids, {'State': 'received_by_keeper'})
        return True

    def product_waiting(self, cr, uid, ids):
        self.write(cr, uid, ids, {'State': 'waiting_for_check'})
        return True

    def product_accepted(self, cr, uid, ids):
        self.write(cr, uid, ids, {'State': 'accepted'})
        return True

    def product_confirm_keeper(self, cr, uid, ids):
        self.write(cr, uid, ids, {'State': 'confirm_by_keeper'})
        return True

    def product_confirm_manger(self, cr, uid, ids):
        self.write(cr, uid, ids, {'State': 'confirm_by_manger'})
        return True

    def product_entered(self, cr, uid, ids):
        self.write(cr, uid, ids, {'State': 'entered_the_stock'})
        return True

        ################################################

class odoowarehouse_search(orm.Model):
    _name = 'odoowarehouse.search'
    _columns = {
        'search': fields.char(string='البحث عن', size=100),
        'select': fields.selection([('Pname', 'Pname'),
                                    ('Procode', 'Procode')], string='البحث باستخدام', size=100),
        'result': fields.text(string='نتيجه البحث', size=100),
    }
    def find_product(self, cr, uid, ids, search , select , context=None):
        record = self.pool.get('odoowarehouse.addproduct').search(cr, uid, [(select,'=',search)], context=context)
        record=self.pool.get('odoowarehouse.addproduct').read(cr, uid,record , context=context)
        if record:
            found = {'result':'Name:'+str(record[0]['Pname'].encode('utf8'))+" "+'-Price:'+str(record[0]['Price'])+" "+'-Case:'+str(record[0]['case'])+" "+
                               '-Code:'+str(record[0]['Procode'])}
        else:
            found={'result':''}
        return {'value':found}
