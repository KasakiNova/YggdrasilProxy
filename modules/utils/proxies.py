import modules.globalVariables as gVar

class Proxies:
    def __init__(self):
        local_proxies = {}
        proxy_settings = gVar.cfgContext['Proxy']
        if proxy_settings['enable']:
            # If enable auth
            if proxy_settings['enable_auth']:
                protocol = proxy_settings['address'].split("://")[0]
                link = proxy_settings['address'].split("://")[1]
                local_proxies = {
                    "http": f"{protocol}://{proxy_settings['username']}:{proxy_settings['password']}@{link}",
                    "https": f"{protocol}://{proxy_settings['username']}:{proxy_settings['password']}@{link}",
                }
            # no auth
            else:
                local_proxies = {"http": f"{proxy_settings['address']}", "https": f"{proxy_settings['address']}"}
        gVar.proxies = local_proxies