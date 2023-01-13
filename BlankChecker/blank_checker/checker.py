import cv2
import numpy as np
import math


def getting_file(file_name: str):
    return cv2.imread(file_name)


def getting_boxes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 50, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    centers = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        min_area = 2000
        max_area = 15000
        x1, y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and area > min_area and area < max_area:
            x, y, w, h = cv2.boundingRect(cnt)
            ratio = float(w) / h
            if ratio >= 0.8 and ratio <= 1.2:
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append([cX, cY])
    if len(centers) == 3:
        return centers
    else:
        print('С изображением что-то не так!')
        exit(0)


def getting_distances(boxes):
    boxesWithDistances = []
    for box in range(3):
        dstn = []
        for other_box in range(3):
            dstn.append(
                int(math.hypot(abs(boxes[other_box][0] - boxes[box][0]), abs(boxes[other_box][1] - boxes[box][1]))))
        boxesWithDistances.append([boxes[box], dstn])
    return boxesWithDistances


def getting_rates(boxes):
    main_box = boxes[0]
    right_box = boxes[1]
    bottom_box = boxes[2]
    ratioX = abs(main_box[0][0] - right_box[0][0]) / 1070
    ratioY = abs(main_box[0][1] - bottom_box[0][1]) / 1584
    return ratioX, ratioY


def check_orient(boxes):
    first_box = sorted(boxes, key=lambda box: math.hypot(box[0][0], box[0][1]))[0]
    main_box = boxes[0]
    if first_box != main_box:
        print('Правильно соорентируйте фотографию!')
        exit(0)


def check_line(image, firstChB, count, inter, stX, stY, rX, rY, addition):
    result = ''
    for checkbox in range(count):
        pixel = image[int(stY + firstChB[1] * rY), int(stX + (firstChB[0] + inter * checkbox) * rX)]
        # cv2.circle(image, (int(stX + (firstChB[0] + inter * checkbox)* rX), int(stY + firstChB[1] * rY)), 7, (255, 255, 255), -1)
        # cv2.imshow('test', image)
        # cv2.waitKey(0)
        if pixel < 100:
            result += str(checkbox + addition)
    return result


def getting_data(file_name):
    image = getting_file(file_name)
    centers = getting_boxes(image)
    distances = getting_distances(centers)
    distances = sorted(distances, key=lambda box: sum(box[1]))
    first_box = sorted(distances, key=lambda box: math.hypot(box[0][0], box[0][1]))[0]
    main_box = distances[0]
    check_orient(distances)
    rateX, rateY = getting_rates(distances)
    startX, startY = main_box[0]

    results = {}

    name = image[int(startY + 135 * rateY):int(startY + 215 * rateY), int(startX):int(startX + 615 * rateX)]
    results['name'] = name
    img = cv2.GaussianBlur(image, (17, 17), 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('blur.jpg', img)
    # cv2.waitKey(0)

    grade = check_line(img, [167, 255], 7, 58, startX, startY, rateX, rateY, 5)
    results['grade'] = grade
    if len(grade) > 1:
        print('Отмечено несколько классов одновременно')
    # print(grade)

    letter = check_line(img, [167, 315], 8, 58, startX, startY, rateX, rateY, 1)
    results['letter'] = letter
    if len(letter) > 1:
        print('Отмечено несколько букв одновременно')
    # print(letter)

    var = check_line(img, [167, 378], 8, 58, startX, startY, rateX, rateY, 1)
    results['var'] = var
    if len(var) > 1:
        print('Отмечено несколько вариантов одновременно')
    # print(var)

    answers = []
    for block in range(4):
        fChB = [116 if block % 2 == 0 else 668, 522 if block < 2 else 1000]
        for answer in range(9):
            normal = check_line(img, [fChB[0], fChB[1] + 41 * answer], 5, 35, startX, startY, rateX, rateY, 1)
            correction = check_line(img, [fChB[0] + 204, fChB[1] + 41 * answer], 5, 35, startX, startY, rateX, rateY, 1)
            if correction == '':
                answers.append(normal)
            else:
                answers.append(correction)
    results['answers'] = answers

    return results


def verification_works(work, pattern):
    work['max_score'] = pattern['count_questions']
    pattern = pattern[work['var']]
    work['score'] = 0
    for num, answer in enumerate(pattern):
        if answer == work['answers'][num]:
            work['score'] += 1
    work['result'] = f'{work["score"]}/{work["max_score"]} '
    work['per_complition'] = f'{int(work["score"] / work["max_score"] * 100)} %'
    return work


def main():
    pattern = {
        'count_questions': 18,
        '1': ['3', '5', '5', '3', '2', '4', '3', '1', '3', '2', '5', '2', '3', '5', '1', '2', '1', '3'],
        '2': ['2', '4', '3', '2', '2', '3', '3', '2', '4', '1', '4', '3', '4', '1', '3', '5', '2', '4'],
        '3': ['5', '4', '4', '4', '2', '3', '1', '1', '5', '2', '1', '5', '3', '4', '2', '3', '4', '4'],
        '4': ['2', '5', '1', '3', '4', '2', '3', '4', '3', '3', '3', '4', '1', '5', '5', '4', '1', '5'],
    }
    files = ['pp1.jpg']
    for number, file in enumerate(files):
        work = getting_data(file)
        work = verification_works(work, pattern)
        print(f'Работа {number + 1} - Выполнена на {work["per_complition"]} - {work["result"]}')


if __name__ == '__main__':
    main()