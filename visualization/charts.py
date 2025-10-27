"""Generación de gráficos comparativos de compresión."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def saveResults(dfSorted, outdir="resultados_compresion"):
    """Guarda tabla de resultados en CSV."""
    outdir = Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    csvPath = outdir / "tabla_resultados.csv"
    dfSorted.to_csv(csvPath, index=False)
    print(f"\n💾 CSV guardado en: {csvPath}")
    
    return outdir


def _createHorizontalComparison(origU8, waveImgs, waveRows):
    """Crea comparación horizontal: Original | Wavelet1 | Wavelet2 | Wavelet3."""
    a = Image.fromarray(origU8)
    waves = [Image.fromarray(w) for w in waveImgs]

    targetH = 400
    allImgs = [a] + waves
    resized = []
    for im in allImgs:
        scale = targetH / im.height
        newW = int(im.width * scale)
        resized.append(im.resize((newW, targetH), Image.BICUBIC))

    titleH = 50
    capH = 70
    pad = 10
    fontTitle = ImageFont.load_default(20)
    fontCaption = ImageFont.load_default(20)

    totalW = sum([im.width for im in resized]) + pad * (len(resized) - 1)
    totalH = titleH + targetH + capH

    canvas = Image.new("RGB", (totalW, totalH), (0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    x = 0
    titles = ["Original"] + [r["Method"] for r in waveRows]
    captions = [""] + [
        f"Size: {r['Size_KB']:.1f} KB | PSNR: {r['PSNR_dB']:.2f} dB | SSIM: {r['SSIM']:.3f}"
        for r in waveRows
    ]

    for im, title, cap in zip(resized, titles, captions):
        w = im.width

        draw.rectangle([x, 0, x + w, titleH], fill=(15, 15, 15))
        tb = draw.textbbox((0, 0), title, font=fontTitle)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        draw.text((x + (w - tw)//2, (titleH - th)//2), title, fill=(255, 255, 255), font=fontTitle)

        canvas.paste(im, (x, titleH))

        draw.rectangle([x, titleH + targetH, x + w, totalH], fill=(15, 15, 15))
        if cap:
            cb = draw.textbbox((0, 0), cap, font=fontCaption)
            cw, ch = cb[2] - cb[0], cb[3] - cb[1]
            draw.text((x + (w - cw)//2, titleH + targetH + (capH - ch)//2),
                      cap, fill=(255, 255, 255), font=fontCaption)

        x += w + pad

    return canvas


def _createSideBySide(aU8, bU8, captionText, bestMethodName):
    """Crea comparación lado a lado: Original vs Mejor método."""
    a = Image.fromarray(aU8)
    b = Image.fromarray(bU8)

    if max(a.size + b.size) > 1200:
        a.thumbnail((600, 600))
        b.thumbnail((600, 600))

    titleHeight = 60
    captionHeight = 75
    w = a.width + b.width
    h = max(a.height, b.height)

    canvas = Image.new("RGB", (w, h + titleHeight + captionHeight), (0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    topY = titleHeight
    bottomY = topY + h

    canvas.paste(a, (0, topY))
    canvas.paste(b, (a.width, topY))

    rightX0 = a.width
    rightX1 = a.width + b.width
    rightY0 = bottomY
    rightY1 = bottomY + captionHeight
    draw.rectangle([rightX0, rightY0, rightX1, rightY1], fill=(15, 15, 15))

    fontTitle = ImageFont.load_default(30)
    fontCaption = ImageFont.load_default(30)

    titleL = "Original"
    bboxL = draw.textbbox((0, 0), titleL, font=fontTitle)
    textWL, textHL = bboxL[2] - bboxL[0], bboxL[3] - bboxL[1]
    textXL = (a.width - textWL) // 2
    draw.text((textXL, (titleHeight - textHL)//2), titleL, fill=(255, 255, 255), font=fontTitle)

    titleR = bestMethodName
    bboxR = draw.textbbox((0, 0), titleR, font=fontTitle)
    textWR, textHR = bboxR[2] - bboxR[0], bboxR[3] - bboxR[1]
    textXR = a.width + (b.width - textWR) // 2
    draw.text((textXR, (titleHeight - textHR)//2), titleR, fill=(255, 255, 255), font=fontTitle)

    bboxC = draw.textbbox((0, 0), captionText, font=fontCaption)
    textWC, textHC = bboxC[2] - bboxC[0], bboxC[3] - bboxC[1]
    textXC = rightX0 + (b.width - textWC) // 2
    textYC = bottomY + (captionHeight - textHC) // 2 - 2
    draw.text((textXC, textYC), captionText, fill=(255, 255, 255), font=fontCaption)

    return canvas


def _findRow(dfSorted, methodSubstr):
    """Encuentra fila en DataFrame que contiene substring en columna Method."""
    mask = dfSorted["Method"].str.contains(methodSubstr, case=False, na=False)
    return dfSorted[mask].iloc[0]


def createVisualizations(imgU8, dfSorted, recons, outdir):
    """Genera todas las visualizaciones comparativas y las guarda."""
    print("\n🎨 Generando visualizaciones...")
    
    rowHaar = _findRow(dfSorted, "haar")
    rowDb2 = _findRow(dfSorted, "db2")
    rowSym4 = _findRow(dfSorted, "sym4")

    imgsWave = [
        recons[rowHaar["Method"]], 
        recons[rowDb2["Method"]], 
        recons[rowSym4["Method"]]
    ]
    rowsWave = [rowHaar, rowDb2, rowSym4]

    canvasAll = _createHorizontalComparison(imgU8, imgsWave, rowsWave)
    waveletPath = outdir / "comparacion_wavelets.png"
    canvasAll.save(waveletPath)
    print(f"  ✓ Comparación wavelets guardada: {waveletPath}")

    rankPsnr = dfSorted["PSNR_dB"].rank(ascending=False)
    rankSsim = dfSorted["SSIM"].rank(ascending=False)
    score = (rankPsnr + rankSsim) / 2.0
    bestIdx = int(score.idxmin())

    bestRow = dfSorted.loc[bestIdx]
    bestName = bestRow["Method"]

    print(f"\n🏆 Mejor método (ranking PSNR+SSIM): {bestName}")
    
    captionText = (
        f"{bestRow['Method']} | "
        f"Size: {bestRow['Size_KB']:.1f} KB | "
        f"PSNR: {bestRow['PSNR_dB']:.2f} dB | "
        f"SSIM: {bestRow['SSIM']:.3f}"
    )

    bestImg = recons[bestName]

    canvas = _createSideBySide(imgU8, bestImg, captionText, bestRow["Method"])
    bestPath = outdir / "mejor_metodo_comparacion.png"
    canvas.save(bestPath)
    print(f"  ✓ Mejor método guardado: {bestPath}")
    
    origPath = outdir / "original.png"
    Image.fromarray(imgU8).save(origPath)
    print(f"  ✓ Original guardado: {origPath}")
    
    return bestName, bestRow

