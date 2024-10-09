from ocr import Ocr
import time

def main():
    o = Ocr((40, 240, 380, 340), (40, 530, 380, 800))
    while True:
        print("按回车继续... 按Ctrl+C退出...")
        input()
        for i in range(1):
            try:
                o.solve()
            except Exception as e:
                print(e)
            time.sleep(0.4)
    #o.w.writeString('157')

if __name__ == "__main__":
    main()
