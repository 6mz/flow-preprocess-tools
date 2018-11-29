# -*- coding: utf-8 -*-

from simple2d import draw_rect_and_save

if '__main__' == __name__:
    for i in range(0,100):
        gtflow=draw_rect_and_save(i,root = './data/TESTsimple2d/rect_v2')


#    #绘制直线
#    draw.line((20, 20, 150, 150), 'cyan')
#    #绘制弧
#    draw.arc((100, 200, 300, 400), 0, 180, 'yellow')
#    draw.arc((100, 200, 300, 400), -90, 0, 'green')
# 
#    #绘制弦
#    draw.chord((350, 50, 500, 200), 0, 120, 'khaki', 'orange')
# 
#    #绘制圆饼图
#    draw.pieslice((350, 50, 500, 200), -150, -30, 'pink', 'crimson')
#    
#    #绘制椭圆
#    draw.ellipse((350, 300, 500, 400), 'yellowgreen', 'wheat')
#    #外切矩形为正方形时椭圆即为圆
#    draw.ellipse((550, 50, 600, 100), 'seagreen', 'skyblue') 
# 
#    #绘制多边形
#    draw.polygon((150, 180, 200, 180, 250, 120, 230, 90, 130, 100), 'olive', 'hotpink')
# 
#    #绘制文本
#    font = ImageFont.truetype("consola.ttf", 40, encoding="unic")#设置字体
#    draw.text((100, 50), u'Hello World', 'fuchsia', font)