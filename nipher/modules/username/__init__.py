import requests

SITES={
"GitHub":"https://github.com/{}",
"Reddit":"https://www.reddit.com/user/{}",
"GitLab":"https://gitlab.com/{}",
"Pinterest":"https://www.pinterest.com/{}/",
"Medium":"https://medium.com/@{}",
"Keybase":"https://keybase.io/{}"
}

def run(target):
    username=target.strip().lstrip("@")
    found=[]
    for name,url in SITES.items():
        try:
            r=requests.get(url.format(username),timeout=8,allow_redirects=True,
                           headers={"User-Agent":"NIPHER/0.1"})
            found.append({
                "site":name,
                "url":r.url,
                "status":r.status_code,
                "exists":r.status_code==200
            })
        except Exception as e:
            found.append({"site":name,"error":str(e)})
    return {"module":"username","target":username,"results":found}
