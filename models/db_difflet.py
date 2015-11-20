# -*- coding: utf-8 -*-

db.define_table('category', Field('name'))
#                , auth.signature)

db.define_table('entity'
               ,Field('category', 'reference category')
               ,Field('name'))
#               ,auth.signature)

db.define_table('diff_point'
               ,Field('name'))
#               ,auth.signature)

db.define_table('listing'
               ,Field('entity', 'reference entity')
               ,Field('diff_point', 'reference diff_point')
               ,Field('summary', 'text'))
#               ,auth.signature)

db.define_table('recent_searches'
                ,Field('entity1')
                ,Field('entity2'))

# db.define_table('difflet'
#                ,Field('entity1', 'reference entity')
#                ,Field('entity2', 'reference entity')
#                ,Field('score', default=0))
# # db.define_table('vote'
#                ,Field('difflet', 'reference difflet')
#                ,Field('score', 'integer', default=0)
#                ,auth.signature)
