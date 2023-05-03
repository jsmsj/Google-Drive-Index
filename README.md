# Google Drive Index (View-Only)

### Features:
1. Add multiple drives
2. Search for a file/folder across all those drives.
3. Discord Authorization (User visiting the index will have to login with discord, and if the user is in a specific guild then only they can access the index.)

### Setup:
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Make a new application
![](https://i.imgur.com/gOUonXq.png)
3. Go to Oauth2 -> General, copy the client id and client secret, add http://127.0.0.1:5000/authorise to redirect url, you can add https:www.yoursitewherethiswillbehosted.com/authorise too.
![](https://i.imgur.com/MKYKJqY.png)
4. Go to Bot and build a bot, keep the token safe.
![](https://i.imgur.com/idpgGpy.png)
5. Now open [config.py](./config.py) and add the above copied values.
6. Add the guild id to config.py in which the user mus be to access the index
7. Add the shared drive names and id to the config.py
8. Lastly add a service account mail, token_uri, and private key to the config. Make sure that the particular service account can access all the drives you want the index to display.
9. Run `pip install -r requirements.txt`
10. Run main.py
11. Index will be at [127.0.0.1:5000](https://127.0.0.1:5000)


### How it looks:

Before Logging in:
![](https://i.imgur.com/zA6Mlri.png)

After Logging in:
![](https://i.imgur.com/L7asroO.png)

### Note:
The code can be improved a lot, and load times can be made faster, but out of scope for now.