from nlp_tools.tools import GramTools
import csv

def get_csv_content(csvfile, column_name):
    with open(csvfile, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        contents = [row[column_name] for row in reader]
        contents = '\n'.join(contents)
    return contents

csvfile     = './speakingmax_en_review.csv'
column_name = 'comment'

contents = get_csv_content(csvfile, column_name)
g = GramTools(contents, remove_symbles='')
uni_gram = g.get_n_gram_freq(1)
bi_gram = g.get_n_gram_freq(2)
tri_gram = g.get_n_gram_freq(3)
four_gram= g.get_n_gram_freq(4)
five_gram= g.get_n_gram_freq(5)
g.save('D:/teacherCho/speakingmax_en_1gram.txt', uni_gram)
g.save('D:/teacherCho/speakingmax_en_2gram.txt', bi_gram)
g.save('D:/teacherCho/speakingmax_en_3gram.txt', tri_gram)
g.save('D:/teacherCho/speakingmax_en_4gram.txt', four_gram)
g.save('D:/teacherCho/speakingmax_en_5gram.txt', five_gram)