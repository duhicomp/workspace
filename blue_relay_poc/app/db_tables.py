
from app import app, db

with app.app_context():
    print db.reflect()
    # print db.metadata.schema
    # print db.metadata.tables
    ResDesc = db.metadata.tables['res_desc']
    # print dir(ResTyp)
    # res_select = ResTyp.select().where(ResTyp.columns.ID == 0)
    # print dir(res_select)
    # result = db.session.execute(res_select)
    # for row in result:
    #     print row

    #print dir(db.session)
    #print dir(db.metadata)