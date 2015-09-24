#!/usr/bin/env python
from flask.ext.script import Manager
from app import app
manager = Manager(app)
manager.run()
#app.run(debug=True)
