# coding: utf8


db.define_table(
    'borrow',

    Field('bike_id', db.bike),
    Field('borrower_id', db.auth_user),
    
    Field('from','date'),
    Field('to','date'), # inclusive
    
    Field('state', 'string'), # 'request', 'accepted', 'confirmed', 'cancled', 'stolen'
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    
    format = '%(bike_id)s -> %(borrower_id)s',
    singular = 'Borrow',
    plural = 'Borrows',
)

db.define_table( # Never editable! Newest log state must equal borrow state!
    'borrow_log',

    Field('borrow_id', db.borrow),
    Field('initiator_id', db.auth_user), # None => system
    
    Field('state', 'string'), # 'request', 'accepted', 'confirmed', 'cancled', 'stolen'
    
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    
    format = '%(borrow_id)s: %(initiator_id)s -> %(state)s',
    singular = 'BorrowLog',
    plural = 'BorrowLogs',
)
