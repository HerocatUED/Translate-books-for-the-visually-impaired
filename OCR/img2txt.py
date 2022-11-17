from PPOCR_api import PPOCR
import tbpu

# 初始化识别器对象，传入 PaddleOCR_json.exe 的路径
ocr = PPOCR(
    r'D:\course\Grade-two\CV\Translate-books-for-the-visually-impaired\OCR\PaddleOCR\PaddleOCR_json.exe')

testImg = r'D:\course\Grade-two\CV\Translate-books-for-the-visually-impaired\OCR\test.png'

# OCR识别图片，获取文本块
getObj = ocr.run(testImg)
ocr.stop()  # 结束引擎子进程
if not getObj["code"] == 100:
    print('识别失败！！')
    exit()
textBlocks = getObj["data"]  # 提取文本块数据

# 执行文本块后处理：合并自然段
# 传入OCR结果列表，返回新的文本块列表
textBlocksNew = tbpu.run_merge_line_h_m_paragraph(textBlocks)

txt = ""
for textBlock in textBlocksNew:
    txt = txt+textBlock["text"]+"\n"

print(txt)
