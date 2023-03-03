## How to develop a api in this backend

### 1. Create a new service

create a new file in `web_components` folder, then `from . import *` and write a class which extends `Component` class.

for example
```python
from . import *


class YourApiName(Component):
    def __init__(self, env: Environment):
        super().__init__(env, '/YourApiPath', 'YourApiName', ['GET'])
        self.env = env

    # when frontend request this api, this function will be called
    def view(self):
        # you can get the request args by request.args.get('argName')
        arg1 = request.args.get('arg1')
        # you can reutrn a dict, it will be converted to json automatically
        return {'status': 'ok', 'arg1': arg1}

```

### 2. Register the service

add the service to `web_components/__init__.py` file

```python
from .YourApiFileName import YourApiName
```

and add YourApiName into a list called "init_web_components" in `server_initializer.py` file


## How to debug

### 1. Install the requirements

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
python run.py
```
