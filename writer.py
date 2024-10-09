import pyautogui as pg
import time

class Writer:
    "用于在屏幕上用鼠标书写大小于和数字 每个占 40x100 px"
    # 难点：控制手机屏幕时的延迟问题

    original: tuple = (0, 0) # 画布的坐标点
    current_pos: tuple # 当前绘制到的点
    valid = '0123456789.<>'
    interval = 0
    move_interval = 0.11
    hsize = 50 # 横大小（宽度）
    vsize = 80 # 纵大小（高度）
    padding = 10 # 字距 

    def __init__(self, pos: tuple):
        pg.PAUSE = 0
        self.original = pos
        self.current_pos = pos

    def drawline(self, start_pos, end_pos, release=True):
        pg.moveTo(start_pos)
        pg.mouseDown()
        pg.dragTo(end_pos, duration=self.move_interval)
        time.sleep(self.interval)
        if release:
            pg.mouseUp()

    def drawlines(self, points):
        for i in range(len(points) - 1):
            self.drawline(points[i], points[i + 1], release=False)
        pg.mouseUp()

    def write0(self, x, y, w, h):
        self.drawlines([
            (x, y),
            (x + w, y),
            (x + w, y + h),
            (x, y + h),
            (x - 15, y),
        ])

    def write1(self, x, y, w, h):
        self.drawlines([
            (x + w / 2, y),
            (x + w / 2, y + h),
        ])

    def write2(self, x, y, w, h):
        self.drawlines([
            (x, y),
            (x + w, y),
            (x, y + h),
            (x + w + 15, y + h),
        ])

    def write3(self, x, y, w, h):
        self.drawlines([
            (x, y),
            (x + w, y),
            (x + w / 2, y + h / 2),
            (x + w, y + h),
            (x - 15, y + h),
        ])

    def write4(self, x, y, w, h):
        self.drawlines([
            (x, y),
            (x, y + h / 2),
            (x + w, y + h / 2),
            (x + w / 2, y),
            (x + w / 2, y + h + 15),
        ])

    def write5(self, x, y, w, h):
        self.drawlines([
            (x + w, y),
            (x, y),
            (x, y + h / 2),
            (x + w, y + h / 2),
            (x + w / 2, y + h + 15),
        ])

    def write6(self, x, y, w, h):
        self.drawlines([
            (x + w / 2, y),
            (x, y + h / 2),
            (x, y + h),
            (x + w, y + h),
            (x + w, y + h / 2),
            (x, y + h / 2),
        ])

    def write7(self, x, y, w, h):
        self.drawlines([
            (x, y),
            (x + w, y),
            (x + w / 2, y + h),
        ])

    def write8(self, x, y, w, h):
        self.drawlines([
            (x, y),
            (x + w, y),
            (x, y + h),
            (x + w, y + h),
            (x - w / 3, y - h / 3),
        ])

    def write9(self, x, y, w, h):
        self.drawlines([
            (x + w / 2, y + h / 2),
            (x, y),
            (x + w, y),
            (x, y + h),
        ])

    def writeDot(self, x, y, w, h):
        self.drawlines([
            (x + w / 2, y + h - 10),
            (x + w / 2, y + h),
        ])

    def writeLt(self, x, y, w, h):
        self.drawlines([
            (x + w, y + h / 4),
            (x, y + h / 2),
            (x + w, y + h * 3 / 4),
        ])

    def writeGt(self, x, y, w, h):
        self.drawlines([
            (x, y + h / 4),
            (x + w, y + h / 2),
            (x, y + h * 3 / 4),
        ])

    def writeEq(self, x, y, w, h):
        self.drawlines([
            (x, y + h / 4),
            (x + w, y + h / 4),
        ])
        self.drawlines([
            (x, y + h * 3 / 4),
            (x + w, y + h * 3/ 4),
        ])

    def writeChar(self, c):
        x = self.current_pos[0]
        y = self.current_pos[1]
        w = self.hsize
        h = self.vsize
        pad = self.padding

        match c:
            case '0':
                self.write0(x, y, w, h)
            case '1':
                self.write1(x, y, w, h)
            case '2':
                self.write2(x, y, w, h)
            case '3':
                self.write3(x, y, w, h)
            case '4':
                self.write4(x, y, w, h)
            case '5':
                self.write5(x, y, w, h)
            case '6':
                self.write6(x, y, w, h)
            case '7':
                self.write7(x, y, w, h)
            case '8':
                self.write8(x, y, w, h)
            case '9':
                self.write9(x, y, w, h)
            case '.':
                self.writeDot(x, y, w, h)
            case '>':
                self.writeGt(x, y, w, h)
            case '<':
                self.writeLt(x, y, w, h)
            case '=':
                self.writeEq(x, y, w, h)

        if c == '.' or c == '1':
            self.current_pos = (x + w, y)
        else:
            self.current_pos = (x + w + pad * 2, y)

    # 从original处开始书写
    def writeString(self, msg):
        for c in msg:
            self.writeChar(c)

    def flush(self):
        self.current_pos = self.original
