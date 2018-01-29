import json
import re
import editdistance as ed

# declare global variables
masechtos = []
shas_path = ""
curr_masechta = 0
between_dots = []
mishnah_set = []
processed_data = ["", [], []]  # all_gemara_text, between_dots, mishnah_set
times_found = 0

def main():
    setup_globals()
    analyze_all()

def analyze_all():
    global masechtos
    global shas_path
    global processed_data
    global between_dots
    global mishnah_set
    for i in range(len(masechtos)):
        masechta = masechtos[i]
        print("Analyzing Masechta " + masechta)
        # response_data = get_gemara(masechta,amudim)
        # print("First string of Masechta: " + response_data["he"][0][0])
        with open(shas_path + "preprocessed\\" + masechta + ".txt", "r") as infile:
            processed_data = json.load(infile)
        between_dots = processed_data[1]
        mishnah_set = processed_data[2]
        analyze_masechta(i)
        # with open(shas_path + "preprocessed\\" + masechta + ".txt", "w") as outfile:
        #    json.dump(processed_data, outfile)

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

def analyze_masechta(index):
    global masechtos
    global between_dots
    global mishnah_set
    global processed_data
    global times_found
    print("Masechta " + masechtos[index] + " has %d 'between_dots' segments." % len(between_dots))
    print("Its mishnayos are at indices: ", end="")
    for m in range(len(mishnah_set)):
        print("%d " % mishnah_set[m], end="")
    print("")
    repeats_in_masechta = False;
    for mish in range(len(mishnah_set)-1):
        mish_index = mishnah_set[mish];
        # print("Checking " + masechtos[index] + " mishnah # %d" % mish)
        repeat = False
        for sug in range(mish_index + 1, mishnah_set[mish+1]):
            to_check = between_dots[sug]
            if len(to_check) < 50:
                for again in range (sug + 1, mishnah_set[mish+1]):
                    if again != sug:
                        against = between_dots[again]
                        if len(against) < 50:
                            comp = compare_sugs(to_check,against)
                            if comp:
                                print("index %d (" % sug + to_check + ") ", end="")
                                print("matches %d (" % again + against + ")")
                                times_found = times_found + 1
                                # citeArray.push(logString);
                                # console.log(logString);
                                repeats_in_masechta = True
    if times_found == 0:
        print("No matches yet")
    if index == len(masechtos)-1:
        print("Total found: %d!" % times_found)
        # print("Report: " + citeArray.join(". NEXT: "))

def compare_sugs(to_check, against):
    strip_non_hebrew(to_check)
    strip_non_hebrew(against)
    match = False
    if close_enough(to_check,against):
        match = True
    if close_enough(to_check + " וכו'",against):
        match = True
    if close_enough(to_check,against + " וכו'"):
        match = True
    return match

def strip_non_hebrew(to_strip):
    to_strip = re.sub(r"[^א-ת ]", "", to_strip)
    return to_strip

def close_enough(a,b):
    ce = False
    # if levenshteinDistance(a,b) <=3:
    if ed.eval(a, b) <= 3:
    # if a == b:
        ce = True
    return ce

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

if __name__ == "__main__":
    main()
