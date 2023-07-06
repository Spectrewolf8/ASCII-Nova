import base64
import sys
import compress_json
from RendererAndPlayer import RenderScreen


def renderAudio(asciiVideoDict):
    # f = open("temp/" + "BadAppleForPython2.mp4_audio_encoded" + '.txt', 'rb')
    b = base64.b64decode(asciiVideoDict['base64Audio'])
    # f.close()

    try:
        file = open("../temp/" + asciiVideoDict['filename'] + '_audio_decoded.mp3', 'wb')
        file.write(b)
        file.close()
    except Exception as e:
        print(e)
        sys.exit(0)


fontColorHex = "#FFFFFF"
fontSize = 8
lineHeight = 1.0
showFpsSwitch = True
ascii_render_fontName = "../fonts/courier.ttf"


def playAsciiVideo(gzippedJsonfile_path):
    asciiVideoDict = compress_json.load(gzippedJsonfile_path)  # loads json as a dictionary

    renderAudio(asciiVideoDict)
    RenderScreen.renderFramesOnScreen(asciiVideoDict, fontColorHex=fontColorHex, fontSize=fontSize,
                                      lineheight=lineHeight,
                                      showFpsSwitch=True,
                                      ascii_render_font_name=ascii_render_fontName)
