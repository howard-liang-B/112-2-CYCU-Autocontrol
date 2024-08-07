import cv2
import pytesseract
import re
import easyocr

def find_plate_contour(org_img, canny_img):
    contours, hierarchy = cv2.findContours(canny_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    crop_img = org_img.copy()
    for item in contours:
        rect = cv2.boundingRect(item)
        x = rect[0]
        y = rect[1]
        weight = rect[2]
        height = rect[3]
        if weight / height > 4:
            crop_img = org_img[y:y+height, x:x+weight] # 第 6. 切割
            cv2.rectangle(org_img, (x, y), (x+weight, y+height), (0, 0, 255), 3)
            break
    return org_img, crop_img, x, y

def find_plate_contour_2(text):
    for data in text:
        if data[2] > 0.7:
            return data

# 1. 讀取圖片，並且轉成使用灰階讀取
img_path = r"plates\test\images\-2024-02-20-3-35-34_png.rf.7207fad0a58ca511421fa799fe88caa7.jpg"
plate_img = cv2.imread(img_path)
gray_plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

# 2. 降躁處理(以下使用三種方法)
blur_plate_img = cv2.GaussianBlur(gray_plate_img, (19, 19), 0) # {高斯濾波}，這裡的區域必須是奇數
# blur_plate_img = cv2.blur(plate_img, (10, 10)) # {平均模糊}，(10, 10) 代表平均的區域
# blur_plate_img = cv2.medianBlur(plate_img, 25) # {中值模糊}

# 3. 邊緣檢測
canny_plate_img = cv2.Canny(blur_plate_img, 50, 150) # 數字範圍都是 0 ~ 255

# 4. 找出車牌輪廓、5. 切割車牌出來
plate_img, crop_img, x, y =  find_plate_contour(plate_img, canny_plate_img)

# 6. 對切割出來的照片進行辨識
############################## 使用 pytesseract #####################################
# text = pytesseract.image_to_string(crop_img, config='--psm 11')
# text = re.sub(r'[^\w\d]', '', text)
# print("## plate number:", text)

# # 7. 顯示車牌號碼在原圖
# cv2.putText(plate_img, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)


# cv2.imshow("plate", plate_img)
# # cv2.imshow("blur plate", blur_plate_img)
# # cv2.imshow("canny plate", canny_plate_img)
# # cv2.imshow("crop plate", crop_img)
# cv2.waitKey()
# cv2.destroyAllWindows()

############################## 使用 easyocr #####################################
reader = easyocr.Reader(['en'], gpu = True) 
text = reader.readtext(crop_img)
print("## ", text)
'''
text print 出來長這樣:
[([[191, 168], [462, 168], [462, 249], [191, 249]], '0 9 &', 0.014731698078101775), 
([[0, 216], [640, 216], [640, 470], [0, 470]], '9R8027', 0.756721173876858)]
'''

data = find_plate_contour_2(text)
[left_top, right_top, right_down, left_down] = data[0]
cv2.putText(plate_img, data[1], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

cv2.imshow("plate", plate_img)
cv2.imshow("crop plate", plate_img[left_top[1]:left_down[1], left_top[0]: right_top[0]])
cv2.waitKey()
cv2.destroyAllWindows()


###################################################################