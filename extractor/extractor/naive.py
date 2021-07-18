import os
import database.msql
import media.editor
import control.xvidgen
import algorithm.shotcut.shotcut
import algorithm.common.sig
import algorithm.danmu.sentiments
import algorithm.danmu.density
import scipy.signal
import numpy as np
import math
import ffmpeg
import json
import sys
from matplotlib import pyplot as plt

from cv2 import data
sys.path.append("..")
# from matplotlib import pyplot as plt


def solve(bvid):
    print("extractor.naive: Hello ", bvid)
    duration = int(math.ceil(
        float(ffmpeg.probe("../../data/media/%s.mp4" % bvid)["format"]["duration"])))
    frame_rate = 24
    frame_total = int(math.ceil(duration*frame_rate))

    # file_danmu = open("../../data/danmu/%s.danmu.json"%bvid,"r",encoding="utf-8")
    # danmu_list = json.load(file_danmu)
    # file_danmu.close()

    # shotcut_list = algorithm.shotcut.shotcut.shotcut("../../data/media/%s.mp4"%bvid)

    print("extractor.naive: Read danmu and shotcut from database... ", bvid)
    cid = database.msql.query(
        "biliextract", "select cid from Vinfo where bvid='%s'" % bvid)[0][0]
    danmu_list = database.msql.query(
        "biliextract", "select * from Danmu where cid='%s'" % cid, isDict=True)
    shotcut_list = database.msql.query(
        "biliextract", "select * from shotcut where bvid='%s'" % bvid, isDict=True)

    print("extractor.naive: Analysing...")

    density_s = algorithm.danmu.density.calcDanmuDensity(
        danmu_list, duration, Delta=7)
    density_l = algorithm.danmu.density.calcDanmuDensity(
        danmu_list, duration, Delta=25)
    density_p = [density_s[i]/(density_l[i]+1) for i in range(duration)]
    sentiments = algorithm.danmu.sentiments.calcDanmuSentiments(
        danmu_list, duration)
    tans = [density_p[i] * math.sqrt(density_s[i]) *
            (0.5+math.sqrt(sentiments[i])) for i in range(duration)]
    ans = []
    for i in tans:
        ans += [i]*24
    ans = ans[0:frame_total]
    ans = scipy.signal.savgol_filter(ans, 119, 3)

    plt.plot(ans)

    for shotcut in shotcut_list:
        if shotcut["transition"] == "cut":
            fid = shotcut["cut_frame"]
            if fid < frame_total:
                ans[fid] = 0
            if fid > 0:
                ans[fid-1] = 0
        else:
            fid_l = shotcut["start_frame"]
            fid_r = shotcut["end_frame"]
            for i in range(fid_l-1, fid_r+1):
                if i >= 0 and i < frame_total:
                    ans[i] = 0

    thres = algorithm.common.sig.getPropotionPoint(ans, 0.15)
    bans = [(ans[i] > thres) for i in range(frame_total)]

    plt.plot(bans)
    plt.show()

    res = algorithm.common.sig.makeRanges(bans, 24, 360)

    print("extractor.naive: writing...")
    for i in res:
        xvid = control.xvidgen.generateId()
        xvobj = {"id": xvid, "bvid": bvid,
                 "frame_begin": i[0], "frame_end": i[1], "src_type": 0, "clip_type": 0}
        media.editor.edit([{"filename": "../../data/media/%s.mp4" % bvid, "start": xvobj["frame_begin"]/frame_rate,
                          "duration":(xvobj["frame_end"]-xvobj["frame_begin"])/frame_rate}], "../../data/output/%s.mp4" % xvid, quiet=True)
        os.system("ffmpeg -i ../../data/output/%s.mp4 -r 24 -ss 00:00:00 -vframes 1 ../../data/poster/%s.jpg  -hide_banner -loglevel error" % (xvid, xvid))
        database.msql.query("biliextract", "INSERT INTO extraction (id, bvid, frame_begin, frame_end, src_type, clip_type) VALUES ('%s','%s',%d,%d,%d,%d);" % (
            xvobj["id"], xvobj["bvid"], xvobj["frame_begin"], xvobj["frame_end"], xvobj["src_type"], xvobj["clip_type"]))

    print("extractor.naive: OK!")


if __name__ == "__main__":
    solve("BV1Uv411v7mM")
