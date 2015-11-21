# -*- coding: utf-8 -*-
UPLOAD_PATH="./applications/diffLet/uploads"
def getEntityIdByName(name):
    return (db(db.entity.name==name).select())[0]['id']

def addDiffPoint():
    new_diff_point = request.vars.new_dp;
    presentAlready = db(db.diff_point.name==new_diff_point).select()
    if len(presentAlready) == 0:
        nid=db.diff_point.insert(name=new_diff_point)
    else:
        nid = presentAlready[0]['id']

    e1id = getEntityIdByName(request.vars.e1);
    e2id = getEntityIdByName(request.vars.e2);

    e1_dp_summary = request.vars.new_e1_dp;
    e2_dp_summary = request.vars.new_e2_dp;

    db.listing.insert(entity=e1id, diff_point = nid, summary = e1_dp_summary )
    db.listing.insert(entity=e2id, diff_point = nid, summary = e2_dp_summary )

    session.flash = 'New differentiating point added!'
    redirect(URL('default' , 'difflet', vars={'e1' : request.vars.e1, 'e2': request.vars.e2 }))
    return locals()


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    redirect(URL('default', 'search'))
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def saveSearch(e1, e2):
    last5=db(db.recent_searches).select(orderby=~db.recent_searches.id , limitby=(0,5))
    for row in last5:
        if row['entity1'] == e1 and row['entity2'] == e2 or row['entity1'] == e2 and row['entity2'] == e1:
            return
    db.recent_searches.insert(entity1=e1, entity2=e2)
    return

def difflet():
    e1 = request.vars['e1']
    e2 = request.vars['e2']
    saveSearch(e1, e2)
    e1id=(db(db.entity.name==e1).select())[0]['id']
    e2id=(db(db.entity.name==e2).select())[0]['id']

    e1rows = db(db.listing.entity==e1id).select(join = db.diff_point.on(db.listing.diff_point == db.diff_point.id))
    e2rows = db(db.listing.entity==e2id).select(join = db.diff_point.on(db.listing.diff_point == db.diff_point.id))

    e1_dp_id = []
    for i in range(0, len(e1rows)):
        e1_dp_id.append(e1rows[i]['diff_point.id'] )
    e2_dp_id = []
    for i in range(0, len(e2rows)):
        e2_dp_id.append(e2rows[i]['diff_point.id'] )

    # {  diff_point : (e1, e2)}
    common=[]
    for i in e1_dp_id:
        if i in e2_dp_id:
            common.append(i)

    output={}

    for r in e1rows:
        if r['diff_point.id'] in common:
            output[r['diff_point.name']] = (r['listing.summary'] , '')

    for r in e2rows:
        if r['diff_point.id'] in common:
            old_tuple = output[r['diff_point.name']]
            output[r['diff_point.name']] =  ( old_tuple[0],  r['listing.summary'])

    return locals()

def search():
    if auth.user is not None:
        print auth.user.id
    else:
        print 'No user logged in'
    last5=db(db.recent_searches).select(orderby=~db.recent_searches.id , limitby=(0,5))
    recent_searches = [ (row['entity1'], row['entity2'])  for row in last5 ]
    categories = db(db.category).select()
    entities =  { }
    for c in categories:
        es = db(db.entity.category == c['id']).select(db.entity.name)
        entities[c['name']] = []
        for e in es:
            entities[c['name']].append(e['name'])
    return locals()

def processCsv(folder, csvf):
    print folder, csvf
    print type(folder),type(csvf)
    import csv
    filename = folder + '/' + csvf
    print filename
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        entities=[]
        for entity in header[1:]:
            entities.append(getEntityIdByName(entity))
        for row in reader:
            dp = row[0]
            presentAlready = db(db.diff_point.name==dp).select()
            if len(presentAlready) == 0:
                nid=db.diff_point.insert(name=dp)
            else:
                nid = presentAlready[0]['id']
            for i in range(1, len(row)):
                db.listing.insert(entity=entities[i-1], diff_point=nid, summary = row[i])
            print row

def csv_upload():
    form = SQLFORM.factory(Field('csv_file', 'upload', uploadfolder=UPLOAD_PATH, requires = [ IS_NOT_EMPTY(), IS_UPLOAD_FILENAME(extension='csv')] ) )
    if form.process().accepted:
        print form.vars.csv_file
        print type(form.vars.csv_file)
        response.flash = "File Uploaded!"
        processCsv(UPLOAD_PATH, form.vars.csv_file)
        # redirect(URL('default', 'search'))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)


def about():
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def difflet_template():
    #redirect(URL('static', 'difflet_template.html'))
    return locals()

def popup_form():
    return locals()
