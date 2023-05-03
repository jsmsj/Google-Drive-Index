from urllib import parse

token = 'xxxxxxx' # discord bot token
client_secret = 'secret' #client-secret from discord dev page
client_id = 'client_id' # from discord dev page
redirect_url = 'http://127.0.0.1:5000/authorise'
oauth_url = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={parse.quote(redirect_url)}&response_type=code&scope=identify%20guilds'

guild_id = 123456789123456789 

drives={
    'drive1':'googledrive1id',
    'drive2':'googledrive2id'
}

client_email = 'mfc-abrakadabra@proj.iam.gserviceaccount.com'
token_uri = 'https://oauth2.googleapis.com/token'
private_key = '-----BEGIN PRIVATE KEY-----\nsaspriv\n-----END PRIVATE KEY-----\n'
