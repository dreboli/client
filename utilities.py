from datetime import datetime
from PIL import Image
import cStringIO
import base64
import re
import json
import random
import string

class Listing(object):
    # Listing class
    def __init__(self):
        self.id = str(random.SystemRandom().randint(10000000000,9999999999999))
        self.title = ''
        self.description = ''
        self.unitprice = ''
        self.currency_code = ''
        self.categories = ''
        self.is_public = True
        
class full_name(object):
    def __init__(self,display_name,pgpkey_id):
        self.display_name = display_name
        self.pgpkey_id = pgpkey_id

class queue_task(object):   # Tasks passed from the front end to the main thread for processing
    def __init__ (self, id, command, data):
        self.id = id
        self.command = command
        self.data = data

def current_time():
    utc_datetime = datetime.utcnow()
    return utc_datetime.strftime("%Y-%m-%d %H:%M")+":00" # always zero seconds to reduce impact of clock time skew leakage

def encode_image(buf,size):
    im = Image.open(cStringIO.StringIO(buf))
    im.thumbnail(size, Image.ANTIALIAS)
    image_buffer = cStringIO.StringIO()
    im.save(image_buffer, "PNG")
    image_buffer.getvalue()
    b64_image = base64.b64encode(image_buffer.getvalue())
    return b64_image

def got_pgpkey(orm, key_id):
    if key_id == '': return True
    session = orm.DBSession()
    key_present = session.query(orm.cachePGPKeys).filter_by(key_id=key_id).first()
    if key_present: return True
    else: return False

def parse_user_name(name):
    if not name:
        return None
    key_only = re.compile('^[0-9a-fA-F]{16}$')
    if key_only.match(name):
        pgp_keyid=name
        fullname = full_name
        fullname.display_name=''
        fullname.pgpkey_id=name
        return fullname
    elif re.match('.*\([0-9a-fA-F]{16}\)(?!.*\([0-9a-fA-F]{16}\))$',name):
        display_name = name[0:str(name).rindex('(')].strip()
        pgp_keyid = name[str(name).rindex('(')+1:len(name)-1]
        fullname = full_name
        fullname.display_name=display_name
        fullname.pgpkey_id=pgp_keyid
        return fullname
    else:
        print "Unable to extract display name/key if from recipient"
        return None
   # display_name =
