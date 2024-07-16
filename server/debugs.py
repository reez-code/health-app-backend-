
#!/usr/bin/env python3

from server.apps import app
from server.modelss import db,Admin,Patient

if __name__ == '__main__':
    with app.app_context():
        import ipdb; ipdb.set_trace()