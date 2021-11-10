# CRCrypto

This repo has been updated to work with `Python v3.8` and up.

### How To Run
1. Install `virtualenv`:
```
$ pip3 install virtualenv
```

2. Open a terminal in the project root directory and run:
```
$ virtualenv env
```

3. Then run the command:
```
$ source env/bin/activate 
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Start the web server:
```
$ (env) python3 app.py
```

This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(debug=True, port=<desired port>)
```

6. Terminate the web server:
```
control c
```
5. deactivate the virtual enviorment:
```
$ (env) $ deactivate
```