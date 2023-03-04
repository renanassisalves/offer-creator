import configparser

config = configparser.ConfigParser()
config.read("config.ini")

removerResultados = config['Geral']['remover_resultados']
removerImagensPromo = config['Geral']['remover_imagens_promo']
telegram_api_id = config['Telegram']['telegram_api_id']
telegram_api_hash = config['Telegram']['telegram_api_hash']
telegram_phone = config['Telegram']['telegram_phone']
telegram_username = config['Telegram']['telegram_username']
loginInstagram = config['Instagram']['instagram_login']
senhaInstagram = config['Instagram']['instagram_senha']
consumerKeyTwitter = config['Twitter']['twitter_consumer_key']
consumerKeySecretTwitter = config['Twitter']['twitter_consumer_secret_key']
accessTokenTwitter = config['Twitter']['twitter_access_token']
accessTokenSecretTwitter = config['Twitter']['twitter_access_token_secret']
cuttlyApiKey = config['Cuttly']['cuttly_api_key']
diretorioVideo = config['Youtube']['youtube_diretorio_video']