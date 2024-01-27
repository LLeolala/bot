import numpy as np
import cv2
import math


# 載入文字檢測模型
net = cv2.dnn.readNet("frozen_east_text_detection.pb")


# 讀取圖片
image_path = "../../../Coding by Leo/test_picture/test (20).jpg"  # 請將路徑換成你的圖片路徑
output_path = "../../../Coding by Leo/test_picture/test (100).jpg"  # 請將路徑換成你想要保存的路徑

image = cv2.imread(image_path)
height, width = image.shape[:2]

# 進行文字檢測
blob = cv2.dnn.blobFromImage(image, 1.0, (width, height), (123.68, 116.78, 103.94), True, False)
net.setInput(blob)
(scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"])

# 定義 confidences 變數
confidences = []

# 透過 non-maximum suppression 來過濾掉重疊的框
rectangles = []
for i in range(len(scores)):
    score = scores[i]
    geo = geometry[i]
    (numRows, numCols) = score.shape[2:4]
    for y in range(0, numRows):
        scoresData = score[0, 0, y]
        xData0 = geo[0, 0, y]
        xData1 = geo[0, 1, y]
        xData2 = geo[0, 2, y]
        xData3 = geo[0, 3, y]
        anglesData = geo[0, 4, y]

        for x in range(0, numCols):
            if scoresData[x] < 0.5:
                continue

            offsetX = x * 4.0
            offsetY = y * 4.0
            angle = anglesData[x]
            cosA = math.cos(angle)
            sinA = math.sin(angle)
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            offset = ([offsetX + cosA * xData1[x] + sinA * xData2[x], offsetY - sinA * xData1[x] + cosA * xData2[x]])

            p1 = (-sinA * h + offset[0], -cosA * h + offset[1])
            p3 = (-cosA * w + offset[0],  sinA * w + offset[1])
            center = (0.5*(p1[0]+p3[0]), 0.5*(p1[1]+p3[1]))
            rectangles.append((center, (w,h), -1*angle*180.0/math.pi))
            confidences.append(float(scoresData[x]))

# 顯示處理後的圖片
for rect, confidence in zip(rectangles, confidences):
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
    cv2.putText(image, f'{confidence:.2f}', (box[0][0], box[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

# 將處理後的圖片保存到指定路徑
cv2.imwrite(output_path, image)

cv2.imshow("Detected Text", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
