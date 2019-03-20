import requests,re,os,csv,bs4,time

def get_message(N):
    """
    Climbing Rent Information from anjuke
    N is the pages
    """
    list_sum_message=[]          #return message
    headers={
    "User-Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    for i in range(1,N+1):        
        res=requests.get("https://nc.zu.anjuke.com/fangyuan/p"+str(i)+"/",headers=headers)
        res.raise_for_status()
        browser=bs4.BeautifulSoup(res.text,"lxml")
        info_lis=browser.find_all("div",attrs={"class":"zu-info"})
        list_message=[]         #each message
        for info_one in info_lis:
            try:
                for area in area_lis:
                    if area in info_one.address.text:
                        area_belong=area
                dict_message={"title":info_one.a["title"],
                              "address":info_one.address.text.replace(" ","").replace("\n"," ").replace("\xa0\xa0"," "),
                              "address_belong":area_belong,
                              "price":info_one.next_sibling.next_sibling.p.text.replace("元/月",""),
                              "range":info_one.p.text.replace(" ","").replace("\n"," "),
                              "href":info_one.a["href"]
                              }
                list_message.append(dict_message)
            except:
                continue
        list_sum_message.append(list_message)
        time.sleep(0.1)
        print(list_sum_message)
    return list_sum_message
def save_message(list_message,file_name,N):
    """Save the results crawled from the settlers as CSV files
       list_message is the crawling results list [[],[]]
       N is the numbers of page
    """
    with open(file_name,"w",encoding="utf8") as f:
        fildname=["title","address","address_belong","price","range","href"]
        write=csv.DictWriter(f,fieldnames=fildname)
        write.writeheader()#write fildname
        for i in range(N):
             write.writerows(list_message[i])
folder_name=input("Please enter the path to save the file (double \ ) :\n")
os.chdir(folder_name)
area_lis=["青山湖","新建","东湖","西湖","南昌县","红谷滩","高新区","青云谱","经开区","湾里","进贤","安义"]

N=int(input("please entering you want to climb pages: \n"))
file_name=input("please enter filename with suffix name: \n")
list_message=get_message(N)
save_message(list_message,file_name,N)