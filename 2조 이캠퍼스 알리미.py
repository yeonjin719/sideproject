from importlib.abc import ResourceLoader
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import selenium
import requests
import copy

#파이썬 3.9 버전 지원
#pip install (selenium, html_table_parser, requests) 으로 설치
#Chrome 버전에 맞추어 Chrome webdriver 설치 후 크롬 웹드라이버 설치 위치로 코드 수정

sub_nums = []
assign_num = 0
assignment = []

def assign_searching(sub_num):
        element = []
        url="https://ecampus.smu.ac.kr/mod/assign/index.php?id="+str(sub_nums[k])
        driver.get(url)
        try:
                find_main = driver.find_element(By.ID,"region-main")
                tbody = find_main.find_element(By.TAG_NAME, "tbody")
                tr = len(tbody.find_elements(By.TAG_NAME, "tr"))
                for b in range(tr):
                    try:
                        for l in range(4):
                                if driver.find_element(By.XPATH, "//*[@id=\"region-main\"]/div/table/tbody/tr["+str(b+1)+"]/td["+str(l+1)+"]").text == '':
                                        continue
                                else:
                                        element.append(driver.find_element(By.XPATH, "//*[@id=\"region-main\"]/div/table/tbody/tr["+str(b+1)+"]/td["+str(l+1)+"]").text)
                        find_name = driver.find_element(By.CLASS_NAME, "page-content-navigation")
                        title = find_name.find_element(By.CLASS_NAME, 'breadcrumb').text
                        element.append(title)
                        assignment.append(copy.deepcopy(element))
                        element.clear()
                    except:
                        pass
        except:
                pass

        return assignment

def find_subject_num(driver):
        try:
                find_sub_div = driver.find_element(By.CLASS_NAME,"course_lists")
                find_sub_class = find_sub_div.find_elements(By.TAG_NAME,"li")
                for li in find_sub_class:
                        aTag = li.find_element(By.TAG_NAME,"a")
                        href = aTag.get_attribute('href')
                        sub_num = str(href).strip("https://ecampus.smu.ac.kr/course/viw.php?id=")
                        sub_nums.append(sub_num)
                print("로그인 성공")
        except:
                print("로그인 실패")
                print("아이디 혹은 비밀번호가 틀렸거나 스톤패스 인증이 되지 않았습니다.")
                print("다시 실행해 주세요")

def ecampus_login(id, pw):
    driver.find_element(By.NAME, 'username').send_keys(id)    
    elem_pw = driver.find_element(By.NAME, 'password')
    elem_pw.send_keys(pw)
    elem_pw.submit()

driver=webdriver.Chrome(executable_path="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/116.0.5845.96/mac-x64/chrome-mac-x64.zip/Users/kimyeonjin/Downloads/chrome-mac-x64/Google_Chrome_for_Testing") #각자 크롬 웹드라이버 다운로드 위치에 맞게 바꿔주기
driver.set_window_size(414,800)
driver.get('https://ecampus.smu.ac.kr/login.php?')
req = requests.get('https://ecampus.smu.ac.kr/login.php?')

id = input("아이디를 입력하세요: ")
pw = input("패스워드를 입력하세요: ")

ecampus_login(id, pw)

url = 'https://ecampus.smu.ac.kr'
find_subject_num(driver)

for k in range(len(sub_nums)):
        assign_searching(sub_nums[k])

 
num = 0
print("미완료된 과제 목록은 다음과 같습니다.")
print()
for d in range(len(assignment)):
        if assignment[d][-2] == '제출 완료':
                continue
        else:
                print(re.sub('[(0-9)\(a-zA-Z)\[\]\서울\-\학년도\학기\ ]','',assignment[d][-1]), end = ': ')
                for v in range(len(assignment[d])-1):
                        print(assignment[d][v], end = '')
                        if v == len(assignment[d])-2:
                                pass
                        else:
                                print(",", end = ' ')
                print()
                num += 1
print()
print("미완료된 과제는",str(num)+"개 입니다.")