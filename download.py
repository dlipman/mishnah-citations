# import urllib.parse
import requests
import json

#declare global variables
masechtos = []
last_amudim = []
shas_path = ""
curr_masechta = 0

def main():
    setup_globals()
    download_all()

def download_all():
    global masechtos
    global last_amudim
    global shas_path
    for i in range(len(masechtos)):
        masechta = masechtos[i]
        print("Downloading Masechta " + masechta)
        amudim = '2a-' + last_amudim[i]
        if masechta == 'tamid':
            amudim = "25b-" + last_amudim[i]
        response_data = get_gemara(masechta,amudim)
        print("First string of Masechta: " + response_data["he"][0][0])
        with open(shas_path + masechta + ".txt", "w") as outfile:
            json.dump(response_data["he"], outfile)


def setup_globals():
    global masechtos
    global last_amudim
    global shas_path
    masechtos = ['Berachot', 'shabbos', 'eiruvin', 'pesachim',
                 'sukkah', 'yoma', 'Rosh_Hashanah', 'beitzah',
                 'taanit', 'megillah', 'Moed_Katan', 'chagigah', 'yevamot',
                 'ketubot', 'nedarim', 'nazir', 'sotah', 'gittin', 'Kiddushin',
                 'Bava_Kamma', 'Bava_Metzia', 'Bava_Batra', 'sanhedrin', 'makkot',
                 'shevuot', 'Avodah_Zarah', 'horayot', 'zevachim', 'menachot',
                 'Chullin', 'bechorot', 'Arakhin', 'temurah', 'meilah', 'Keritot',
                 'tamid', 'niddah']
    last_amudim = ['64a', '157b', '105a', '121b', '56b', '88a', '35a',
                  '40b', '31a', '32a', '29a', '27a',
                  '122b', '112b', '91b', '66b', '49b', '90b', '82b',
                  '119b', '119a', '176b', '113b', '24b', '49b', '76b', '14a',
                  '120b', '110a', '142a', '61a', '34a', '34a', '22a', '28b', '33b', '73a']
    shas_path = "c:\\users\\lipman\\documents\\shas\\"

def get_gemara(masechta,amudim):
    main_api = "https://sefaria.org/api/texts/"
    # address = "97653"
    # url = main_api + urllib.parse.urlencode({'address': address})
    url = main_api + masechta + "." + amudim
    response_data = requests.get(url)
    cutoff = 100
    if len(response_data.text) < cutoff:
        cutoff = len(response_data.text)
    trunc = response_data.text[:cutoff]
    print("response_data (truncated) is: " + trunc)
    if "503 Service Unavailable" in response_data.text:
        print("API failed! Retrying...")
        json_data = get_gemara(masechta,amudim)
    elif "error" in trunc:
        json_data = {"he":[[""]]}
    else:
        json_data = response_data.json()
    # json_data = requests.get(url)
    return json_data

def test_read():
    path = "c:\\users\\lipman\\documents\\shas\\"
    with open(path+"Berachot.txt", "r") as infile:
        a = json.load(infile)
    return a

def old_main():
    mydata = get_gemara("Berachot","2a-64a")
    print("First string of Masechta: " + mydata["he"][0][0])
    path = "c:\\users\\lipman\\documents\\shas\\"
    with open(path+"Berachot.txt","w") as outfile:
        json.dump(mydata["he"],outfile)
    test_input = test_read()
    print("And after write and read: " + test_input[0][0])


if __name__ == "__main__":
    main()
