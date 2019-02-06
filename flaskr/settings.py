from google.cloud import datastore

class Settings():

  @staticmethod
  def get(name):
    kind = 'Settings'
    NOT_SET_VALUE = "NOT SET"

    ds = datastore.Client()
    task_key = ds.key(kind, name)
    retval = ds.get(task_key)

    if not retval:
      task = datastore.Entity(key=task_key)
      task['value'] = NOT_SET_VALUE
      ds.put(task)
      return NOT_SET_VALUE
    if retval['value'] == NOT_SET_VALUE:
      raise Exception(('Setting %s not found in the database. A placeholder ' +
        'record has been created. Go to the Developers Console for your app ' +
        'in App Engine, look up the Settings record with name=%s and enter ' +
        'its value in that record\'s value field.') % (name, name))
    return retval['value']
