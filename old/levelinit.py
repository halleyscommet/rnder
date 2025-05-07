from typedefs import Vec2

def Init(cam, polys):
    cam.camAngle = 0.42
    cam.camPos.x = 451.96
    cam.camPos.y = 209.24

    polys[0].vert[:5] = [
        Vec2(141.00, 84.00),
        Vec2(496.00, 81.00),
        Vec2(553.00, 136.00),
        Vec2(135.00, 132.00),
        Vec2(141.00, 84.00)
    ]
    polys[0].height = 50000
    polys[0].vertCnt = 5

    polys[1].vert[:5] = [
        Vec2(133.00, 441.00),
        Vec2(576.00, 438.00),
        Vec2(519.00, 493.00),
        Vec2(123.00, 497.00),
        Vec2(133.00, 441.00)
    ]
    polys[1].height = 50000
    polys[1].vertCnt = 5

    polys[2].vert[:7] = [
        Vec2(691.00, 165.00),
        Vec2(736.00, 183.00),
        Vec2(737.00, 229.00),
        Vec2(697.00, 247.00),
        Vec2(656.00, 222.00),
        Vec2(653.00, 183.00),
        Vec2(691.00, 165.00)
    ]
    polys[2].height = 10000
    polys[2].vertCnt = 7

    polys[3].vert[:7] = [
        Vec2(698.00, 330.00),
        Vec2(741.00, 350.00),
        Vec2(740.00, 392.00),
        Vec2(699.00, 414.00),
        Vec2(654.00, 384.00),
        Vec2(652.00, 348.00),
        Vec2(698.00, 330.00)
    ]
    polys[3].height = 10000
    polys[3].vertCnt = 7

    polys[4].vert[:6] = [
        Vec2(419.00, 311.00),
        Vec2(461.00, 311.00),
        Vec2(404.00, 397.00),
        Vec2(346.00, 395.00),
        Vec2(348.00, 337.00),
        Vec2(419.00, 311.00)
    ]
    polys[4].height = 50000
    polys[4].vertCnt = 6

    polys[5].vert[:5] = [
        Vec2(897.00, 98.00),
        Vec2(1079.00, 294.00),
        Vec2(1028.00, 297.00),
        Vec2(851.00, 96.00),
        Vec2(897.00, 98.00)
    ]
    polys[5].height = 10000
    polys[5].vertCnt = 5

    polys[6].vert[:5] = [
        Vec2(1025.00, 294.00),
        Vec2(1080.00, 292.00),
        Vec2(1149.00, 485.00),
        Vec2(1072.00, 485.00),
        Vec2(1025.00, 294.00)
    ]
    polys[6].height = 1000
    polys[6].vertCnt = 5

    polys[7].vert[:5] = [
        Vec2(1070.00, 483.00),
        Vec2(1148.00, 484.00),
        Vec2(913.00, 717.00),
        Vec2(847.00, 718.00),
        Vec2(1070.00, 483.00)
    ]
    polys[7].height = 1000
    polys[7].vertCnt = 5

    polys[8].vert[:4] = [
        Vec2(690.00, 658.00),
        Vec2(807.00, 789.00),
        Vec2(564.00, 789.00),
        Vec2(690.00, 658.00)
    ]
    polys[8].height = 10000
    polys[8].vertCnt = 4

    polys[9].vert[:7] = [
        Vec2(1306.00, 598.00),
        Vec2(1366.00, 624.00),
        Vec2(1369.00, 678.00),
        Vec2(1306.00, 713.00),
        Vec2(1245.00, 673.00),
        Vec2(1242.00, 623.00),
        Vec2(1306.00, 598.00)
    ]
    polys[9].height = 50000
    polys[9].vertCnt = 7