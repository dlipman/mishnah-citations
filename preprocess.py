import json
import re

# declare global variables
masechtos = []
shas_path = ""
curr_masechta = 0
original_outer_array = [[]]
processed_data = ["", [], []]  # all_gemara_text, between_dots, mishnah_set

def main():
    setup_globals()
    preprocess_all()
    # preprocess_tester()

def preprocess_tester():
    global masechtos
    global shas_path
    global original_outer_array
    global processed_data
    for i in range(len(masechtos)):
        masechta = masechtos[i]
        print("Pre-process testing Masechta " + masechta)
        # response_data = get_gemara(masechta,amudim)
        # print("First string of Masechta: " + response_data["he"][0][0])
        if i == len(masechtos) - 14:
            with open(shas_path + masechta + ".txt", "r") as infile:
                original_outer_array = json.load(infile)
            process_masechta(i)
        # with open(shas_path + "preprocessed\\" + masechta + ".txt", "w") as outfile:
        #    json.dump(processed_data, outfile)

def get_perakim(all_gemara_text):
    # print("Testing masechta " + masechta)
    between_perakim = all_gemara_text.split('הדרן עלך')
    perakim = []
    for i in range(len(between_perakim)):
        perek = between_perakim[i]
        if i < (len(between_perakim)-1):
            start = perek.index('מתני')
            perakim.append(perek[start:])
    return perakim

def preprocess_all():
    global masechtos
    global shas_path
    global original_outer_array
    global processed_data
    for i in range(len(masechtos)):
        masechta = masechtos[i]
        print("Pre-processing Masechta " + masechta)
        # response_data = get_gemara(masechta,amudim)
        # print("First string of Masechta: " + response_data["he"][0][0])
        with open(shas_path + masechta + ".txt", "r") as infile:
            original_outer_array = json.load(infile)
        process_masechta(i)
        with open(shas_path + "preprocessed\\" + masechta + ".txt", "w") as outfile:
            json.dump(processed_data, outfile)

def setup_globals():
    global masechtos
    global shas_path
    masechtos = ['Berachot', 'shabbos', 'eiruvin', 'pesachim',
                 'sukkah', 'yoma', 'Rosh_Hashanah', 'beitzah',
                 'taanit', 'megillah', 'Moed_Katan', 'chagigah', 'yevamot',
                 'ketubot', 'nedarim', 'nazir', 'sotah', 'gittin', 'Kiddushin',
                 'Bava_Kamma', 'Bava_Metzia', 'Bava_Batra', 'sanhedrin', 'makkot',
                 'shevuot', 'Avodah_Zarah', 'horayot', 'zevachim', 'menachot',
                 'Chullin', 'bechorot', 'Arakhin', 'temurah', 'meilah', 'Keritot',
                 'tamid', 'niddah']
    shas_path = "c:\\users\\lipman\\documents\\shas\\"

def process_masechta(index):
    global masechtos
    global original_outer_array
    global processed_data
    # step 1: obtain 'all_gemara_text'
    all_gemara_text = ""
    for i in range(len(original_outer_array)):
        for j in range(len(original_outer_array[i])):
            all_gemara_text = all_gemara_text+' '+original_outer_array[i][j]
    all_gemara_text = all_gemara_text.replace("<strong>","")
    all_gemara_text = all_gemara_text.replace("<big>","")
    all_gemara_text = all_gemara_text.replace("<br>","")
    all_gemara_text = all_gemara_text.replace("</strong>","")
    all_gemara_text = all_gemara_text.replace("</big>","")
    all_gemara_text = all_gemara_text.replace("</br>","")
    all_gemara_text = all_gemara_text.replace(",","")
    processed_data[0] = all_gemara_text
    # step 2: obtain 'between_dots' array
    perakim = get_perakim(all_gemara_text)
    between_dots = []
    for perek in perakim:
        print(perek)
        betweeen_dots_of_perek = perek.split(':')
        for segment in betweeen_dots_of_perek:
            # print(segment)
            if segment != " ":
                between_dots.append(segment)
    processed_data[1] = between_dots
    # step 3: obtain 'mishnah_set' array
    mishnah_set = get_mishnah_set(between_dots)
    processed_data[2] = mishnah_set

def get_mishnah_set(between_dots):
    mishnah_set = []
    next_mishnah = 0
    for i in range(len(between_dots)-1):
        # print('"'+between_dots[i]+'"')
        curr_words = my_parse(between_dots[i])
        curr_first_word = first_real_word_in_array(curr_words)
        next_words = my_parse(between_dots[i + 1])
        next_first_word = first_real_word_in_array(next_words)
        if (curr_first_word == 'מתני׳') and (next_first_word == 'גמ׳'):
            mishnah_set.append(i)
    return mishnah_set

def first_real_word_in_array(arr):
    realword = False
    j = 0
    while realword == False:
        if j==len(arr):
            break;
        first = arr[j]
        if re.match('[א-ת]',first):
            realword = True
        else:
            j = j + 1
    return first;

def my_parse(my_str):
    parsed = my_str.split(' ')
    return parsed


if __name__ == "__main__":
    main()
