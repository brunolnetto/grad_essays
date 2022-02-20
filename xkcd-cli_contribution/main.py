import requests
import sys
import numpy as np

from scipy.stats import linregress
from sklearn import linear_model, datasets

import matplotlib.pyplot as plt
from alive_progress import alive_bar

if __name__ == '__main__':    
    '''
    intercept=260.2147
    slope=0.06698

    day=10
    month_=5
    year=2013

    d0 = date(2006, 1, 1)
    d1 = date(year, month_, day)

    delta = d1 - d0
    dt=delta.days

    index=int(slope*dt+intercept)

    comic_url=comic_url_str.format(index)
    r = requests.get(comic_url).json()

    d0 = date(year, month_, day)
    d1 = date(int(r["year"]), int(r["month"]), int(r["day"]))
    delta = d1 - d0
    dt_sign=int(delta.days/np.abs(delta.days))
    
    is_found=False

    while(not is_found or stop_search):
        try:
            comic_url=comic_url_str.format(index)
            r = requests.get(comic_url).json()

            d0 = date(year, month_, day)
            d1 = date(int(r["year"]), int(r["month"]), int(r["day"]))
            delta = d1 - d0
            curr_dt_sign=int(delta.days/np.abs(delta.days))

            is_found=delta.days==0
            stop_search = (curr_dt_sign) or \
                       (int(r["year"])==year and 
                        int(r["month"])==month_ and 
                        int(r["day"])== day)
            
            index=index+1
            
            print(r["year"]+'/'+r["month"]+'/'+r["day"])
            
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            print("Next entry.")
    
    if(is_found):
        print('Desired comic index:')
        print(index)

    if(stop_search):
        comic_url=comic_url_str.format(index)
        r = requests.get(comic_url).json()
        print('Nearest comic:')
        print(r)
    '''

    r = requests.get('https://xkcd.com/info.0.json').json()
    
    num_comics = r['num']
    comic_dates=[]
    
    comic_url_str='https://xkcd.com/{}/info.0.json'

    days=[]
    comic_numbers=[]
    prev_day=-1

    num_max=75
    #num_max=num_comics
    with alive_bar(num_max) as bar:
        for i in range(num_max):
            comic_url=comic_url_str.format(i+1)
            
            try:
                r = requests.get(comic_url).json()
                
                if(i==0 or len(np.unique(days))==1):
                    prev_day=int(r['day'])

                    days.append(int(r['day']))
                    comic_numbers.append(int(r['num']))
                
                else:
                    sum_elem= 0 if prev_day==int(r['day']) else days[-1]
                    
                    days.append(int(r['day'])+sum_elem)
                    comic_numbers.append(int(r['num']))

                    ransac = linear_model.RANSACRegressor()
                    
                    X = np.concatenate([
                        np.array(days).reshape(-1, 1), 
                        np.ones(len(days)).reshape(-1, 1)
                        ], axis=1)
                    y=np.array(comic_numbers)
                    
                    ransac.fit(X, y)
                    
                    print("Estimated coefficients (RANSAC):")
                    print(ransac.estimator_.coef_)
                    
                    prev_day=int(r['day'])

                comic_dates.append((r['num'], r['day'], r['month'], r['year']))
            
            except:
                print("Oops!", sys.exc_info()[0], "occurred at comic ", i, ".")
                print("Next entry.")

            bar()

inlier_mask = ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)

days_len=len(days)

dx=np.floor((max(days)-min(days))/days_len-1)
line_X = np.array(list(zip(np.arange(min(days), max(days), dx), np.ones(days_len))))

line_y_ransac = ransac.predict(line_X)

print(X)
print(y)

plt.plot(
    line_X,
    line_y_ransac,
    color="cornflowerblue",
    label="RANSAC regressor",
)

plt.show