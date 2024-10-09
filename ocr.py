from PIL import Image, ImageGrab
import numpy as np
import cv2
import pytesseract
import sympy
import pyautogui as pg
#import cnocr

from writer import Writer

class Ocr:
    qbox: tuple
    cbox: tuple
    w: Writer

    def __init__(self, question_box, canvas_box):
        self.qbox = question_box
        self.cbox = canvas_box
        self.w = Writer((canvas_box[0], canvas_box[1]))
        #self.ocr = cnocr.CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')

    # 若无黑色需要更新
    def needUpdate(self):
        im = ImageGrab.grab(self.cbox)
        return not np.any(np.array(im) < 0x50)

    def calcQuestion(self):
        im = np.array(ImageGrab.grab(self.qbox))
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
        #Image.fromarray(thresh).show()
        text = pytesseract.image_to_string(thresh, config='--psm 6')
        #result = self.ocr.ocr(im)
        #jprint(result)
        #if int(result[0]['text']) < int(result[2]['text']):
        #    return '<'
        #else:
        #    return '>'
        '''放弃了！垃圾OCR
        比一辈子大小去得了
        text = ''.join([x['text'] for x in result])
        '''
        text = text.split('\n')[0]
        '''
        # reader = easyocr.Reader(['en'])
        # results = reader.readtext(thresh)
        # text=''.join([result[1] for result in results])
        text = text.replace('x', '*')
        text = text.replace(' 7', '?') # 莫名其妙的
        text = text.replace('2.', '?') # 更莫名其妙的，毁灭吧
        text = text.replace('?', 'x')
        '''
        print(f'识别结果：{text}')
        if '=' in text:
            x = sympy.symbols('x')
            sp = text.split('=')
            eq = sympy.Eq(eval(sp[0]), eval(sp[1]))
            return str(sympy.solve(eq, x)[0])
        else:
            sp = text.split(' ')
            left = eval(sp[0])
            right = eval(sp[len(sp)-1])
            if left < right:
                return "<"
            else:
                return ">"

    def solve(self):
        pos = pg.position()
        sol = self.calcQuestion()
        self.w.writeString(sol)
        self.w.flush()
        pg.moveTo(pos)
        pg.click()

