import os
import sys


# functions
####################################################################################################

def convert_codecs(videos):
    i = 0
    sizes = ['720', '480', '360x240', '160x120']
    for video in videos:
        # vp8
        order = 'ffmpeg -i ' + video + ' -c:v libvpx -b:v 1M -c:a libvorbis material/vp8_' + sizes[i] + '.webm'
        os.system(order)
        # vp9
        order = 'ffmpeg -i ' + video + ' -c:v libvpx-vp9 -b:v 2M material/vp9_' + sizes[i] + '.webm'
        os.system(order)
        # h265
        order = 'ffmpeg -i ' + video + ' -c:v libx265 -crf 28 -preset fast -c:a aac -b:a 128k material/h265_' + sizes[
            i] + '.mp4'
        os.system(order)
        # av1
        order = 'ffmpeg -i ' + video + ' -c:v libaom-av1 -crf 30 -b:v 2000k -strict experimental material/av1_' + sizes[
            i] + '.mkv'
        os.system(order)
        i += 1


####################################################################################################

cont = 'n'

while (cont == 'n'):
    option = option = input(
        '\nChoose an exercise:\n1. Convert videos to vp8, vp9, h265 and av1.\n2. Create mosaic of videos.\n3. Live '
        'streaming.\n\n')

    if option == '1':
        # exercise 1
        # input videos of all sizes
        videos = ['material/720p.mp4', 'material/480p.mp4', 'material/360x240.mp4', 'material/160x120.mp4']

        # for each size video convert from h264 to the corresponding codecs
        convert_codecs(videos)
    elif option == '2':
        # exercise 2 (done only with the 720p quality videos)
        order = 'ffmpeg -i material/vp8_720.webm -i material/vp9_720.webm -i material/h265_720.mp4 -i ' \
                'material/av1_720.mkv' \
                ' -filter_complex "nullsrc=size=1280x720 [base];' \
                ' [0:v] setpts=PTS-STARTPTS, scale=640x360 [upperleft];' \
                ' [1:v] setpts=PTS-STARTPTS, scale=640x360 [upperright];' \
                ' [2:v] setpts=PTS-STARTPTS, scale=640x360 [lowerleft];' \
                ' [3:v] setpts=PTS-STARTPTS, scale=640x360 [lowerright];' \
                ' [base][upperleft] overlay=shortest=1 [tmp1];' \
                ' [tmp1][upperright] overlay=shortest=1:x=640 [tmp2];' \
                ' [tmp2][lowerleft] overlay=shortest=1:y=360 [tmp3];' \
                ' [tmp3][lowerright] overlay=shortest=1:x=640:y=360"' \
                ' -c:v libx264 material/mosaic_vp8_vp9_h265_av1.mp4'

        os.system(order)
    elif option == '3':
        # exercise 3
        print('\nTo activate the streaming open a new terminal and enter: "python3 activate_streaming.py"\n\n')
        # send the video to local IP
        order = 'ffmpeg -re -i material/bbb_original.mp4 -v 0 -vcodec mpeg4 -f mpegts udp://127.0.0.1:23000'
        os.system(order)
        # to activate the streaming open a new terminal and enter into the command line "python3 activate_streaming.py"

    cont = input('Close program?[y/n] ')
