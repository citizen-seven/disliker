import vk_api
import time, sys
import webbrowser, getpass


print("Please, enter your vk login:")
login = input()
password = getpass.getpass("Enter your password (hidden):")

if (not len(login) or not len(password)):
    print("One of the fields is empty")
    sys.exit(1)

def captcha_handler(captcha):
    url = captcha.get_url()
    print(url)
    webbrowser.open(url, new = 2)
    key = input("Enter captcha code: ").strip()
    return captcha.try_again(key)

user = vk_api.VkApi(login, password,
        captcha_handler = captcha_handler)
try:
    user.auth()
except vk_api.exceptions.BadPassword:
    print("Username or password is incorrect!")
    sys.exit(1)

owner = []
item = []

photos = user.method('fave.getPhotos',{'count': 700})
owner = [item['owner_id'] for item in photos['items']]
item = [item['id'] for item in photos['items']]
len_photo = len(owner)
print("Total number of likes:", len_photo)
for i in range(len_photo):
    try:
        user.method('likes.delete',{'type': 'photo', 'owner_id': owner[i], 'item_id': item[i]})
    except vk_api.exceptions.ApiError:
        print('skipping like')
    time.sleep(0.6)
    print(i+1, "/", len_photo)
