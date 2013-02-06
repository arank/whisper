import audioop
import wave
import numpy as np
import scipy
import random
import string
from models import sound
from scikits.audiolab import Format, Sndfile


def convert(filename):
    f = Sndfile(filename, 'r')
    fs = f.samplerate
    nc = f.channels
    enc = f.encoding

    data = f.read_frames(f.nframes)

    new_name = 'newfile.wav'
    format = Format('wav')
    f = Sndfile(new_name, 'w', format, 1, fs)
    f.write_frames(data)
    f.close()

    return new_name

def generate(filename, target, base):
    format = Format('wav')

    #total blocks
    blocks = 90

    #clustering
    min_length = 4
    max_length = 9

    #Block Size (in s)
    blocksize = .033

    #sample rate
    fs = 48000

    #starting pause
    pauseblocks = 20

    #init incrementing vars
    block = 0
    count=0
    code = ''

    data = np.zeros( ( (blocks+pauseblocks) * blocksize * fs) )

    while block < blocks:

        start =  block * blocksize * fs

        #number of blocks

        if (block + max_length) >= blocks:
            numblocks = blocks - block
        else:
            numblocks = random.randint(min_length, max_length)

        #Duration of sound
        T = blocksize*numblocks

        #keep count of total blocks
        block += numblocks

        #frequency
        if count % 2 == 0:
            f = target
            code += str(numblocks)+','
        else:
            f = base
            code += str(numblocks)+','

        # Create tone
        x = scipy.cos((2*scipy.pi*f/fs)*scipy.arange(fs*T))

        for i, value in enumerate(x):
            if (start + i) < len(data):
                data [start + i] = value

        #increment count
        count+=1
        # print T, " ", count, " ", data


    # Create a Sndfile instance for writing wav files @ 48000 Hz
    f = Sndfile(filename, 'w', format, 1, 48000)
    f.write_frames(data)
    f.close()
    return code;

def get_data(filename):
    f = Sndfile(filename, 'r')
    return f.read_frames(f.nframes)

#frequency detection by justin peel on so
#http://stackoverflow.com/questions/2648151/python-frequency-detection
def find_freq(filename, target, tolerance):
    #chunk = 1584
    chunk = 1584
    count = 0
    countsound = 0
    countpause = 0
    issound = False
    ispause = False
    code = ''

    # open up a wave
    wf = wave.open(filename, 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(chunk)

    data = wf.readframes(chunk)
    #data = get_data(filename)

    # read some data5
    if wf.getnchannels() == 2:
        data = audioop.tomono(data, swidth, .5, .5)



    # play stream and find the frequency of each chunk
    while len(data) == chunk*swidth:
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh"%(len(data)/(swidth)),\
            data))*window

        # Take the fft and square each value
        fftData=abs(np.fft.rfft(indata))**2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*RATE/chunk
            print count , "The freq is %f Hz." % (thefreq)
            if thefreq > target-tolerance and thefreq < target+tolerance*2:
                countsound+=1
                issound = True
                if ispause == True:
                    code += ( str(countpause))+','
                    countpause = 0
                    ispause = False
            else:
                countpause+=1
                ispause = True
                if issound == True:
                    code += (str(countsound))+','
                    countsound = 0
                    issound = False

        else:
            thefreq = which*RATE/chunk
            print count , "The freq is %f Hz." % (thefreq)
            if thefreq > target-tolerance and thefreq < target+tolerance*2:
                countsound+=1
                issound = True
                if ispause == True:
                    code += ( str(countpause))+','
                    countpause = 0
                    ispause = False
            else:
                countpause+=1
                ispause = True
                if issound == True:
                    code += ( str(countsound))+','
                    countsound = 0
                    issound = False


        count+=1
        # read some more data
        data = wf.readframes(chunk)
        # read some data5
        if wf.getnchannels() == 2:
            data = audioop.tomono(data, swidth, .5, .5)
    if len(code) % 2 == 0:
        code += str(countsound)+','
    else:
        code += str(countpause)+','
    return code


def check_if_same(code):
    numbers = string.split(code, ',')

    numbers = numbers[:-1]
    for s in sound.objects.all():
        matched = 0
        little = string.replace(s.data, ',' , '')

        print "little: ", little

        l_index = 0

        end = 0 + len(little)
        if end > len(numbers):
            end = len(numbers)


        for i in range(0, end ):
            print 'little[l_index] ', int(little[l_index])
            print 'numbers[i] ', int(numbers[i])
            diff = int(little[l_index]) - int(numbers[i])
            if diff < 2:
                matched += 1

            l_index += 1

        if float(matched) / len(little) > .85:
            print "matched: ", matched, s.last_name
            return False

    return True

def match(longcode):
    numbers = string.split(longcode, ',')
    if len(numbers) < 5:
        return 'err'
    print numbers
    start = []
    for i, n in enumerate(numbers):
        try:
            if int(n) > 15:
                start.append(i)
        except ValueError:
            pass

    print "start: ", start


    for s in sound.objects.all():
        matched = 0
        little = string.replace(s.data, ',' , '')

        print "little: ", little

        l_index = 0

        end = start[0]+1 + len(little)
        if end > len(numbers):
            end = len(numbers)


        print start[0]+1, " ", start[0] + len(little)
        for i in range(start[0]+1, end ):

            #print 'little[l_index] ', int(little[l_index])
            #print 'numbers[i] ', int(numbers[i])
            try:
                diff = int(little[l_index]) - int(numbers[i])
            except ValueError:
                diff = 5
            if diff < 2:
                matched += 1

            l_index += 1

        if float(matched) / len(little) > .8:
            print "matched: ", matched, s.last_name
            return s.last_name




    return 'err'