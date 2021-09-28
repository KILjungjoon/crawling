from nlp_tools.tools import GooglePlay

driver_path = './chromedriver.exe'

gp             = GooglePlay(driver_path)
gp.url         = 'https://play.google.com/store/apps/details?id=air.com.speakingmax&hl=ko&showAllReviews=true'
gp.result_file = './speakingmax_en_review.csv'
gp.scroll_cnt  = 100
gp.headers     = {'accept-language': 'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7'}
gp.run_script()
