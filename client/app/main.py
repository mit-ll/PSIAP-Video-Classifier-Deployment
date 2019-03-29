import os
import sys
import logging
from skimage.transform import resize
from scipy import misc
import matplotlib.pyplot as plt
import requests

os.environ['NO_PROXY'] = 'tf-server'

PRINT_LOG = True

DN_MODEL='day-night'
IVA_DAY='iva-day'
IVA_NIGHT='iva-night'

# other analytics
IVA_DAY_JB = 'iva-day-jb'
IVA_DAY_COMBO = 'iva-day-combo'
IVA_NIGHT_JB = 'iva-night-jb'
IVA_NIGHT_COMBO = 'iva-night-combo'

logformatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
def setup_logger(name, log_file, formatter=logformatter, level=logging.INFO):
    """Function to setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

timelogger = setup_logger('tmp', 'tmp.log')
LOG = setup_logger('tmplog', 'tmplog.log')

def info(val):
    LOG.info(val)
    if PRINT_LOG:
        print(val)

def debug(val):
    LOG.debug(val)

def warn(val):
    LOG.warn(val)
    if PRINT_LOG:
        print(val)

def error(val):
    LOG.error(val)
    if PRINT_LOG:
        print(val)

def query(image_data, model_name):
    '''
    submits image_data to the model_name model hosted at tf_server
    '''

    predict_request = {"instances" : [{"input_data": image_data.tolist()}]}

    # server_url = 'http://localhost:8501/v1/models/{model_name}:predict'.format(model_name=model_name)
    server_url = 'http://tf-server:8501/v1/models/{model_name}:predict'.format(model_name=model_name)
    response = requests.post(server_url, json=predict_request)
    response.raise_for_status()

    return response.json()

def parse_prediction_result(res):
    list = res['predictions']
    if list[0][1] == 1.0: # day or in-vehicle
        return True
    else:
        return False

def process_images(input, reportpath, pattern = None):
    iva_output = []
    plt_vals = []
    num_t = 0
    num_f = 0
    framecount = 0

    timelogger.info('Frame,Model,IVA_Value')

    files = os.listdir(input)
    for f in files:
        info('Processing File: {0}'.format(f))

        img = misc.imread(input+"/"+f)
        img = resize(img,(128, 72, 3))

        # query tensorflow server
        res = query(img, DN_MODEL)
        debug('Is_day response: {0}'.format(res))

        is_day = parse_prediction_result(res)
        debug('is_day result: {0}'.format(is_day))

        is_invehicle = False
        if is_day == True:
            res = query(img, IVA_DAY)
            is_invehicle = parse_prediction_result(res)
        else:
            res = query(img, IVA_NIGHT)
            is_invehicle = parse_prediction_result(res)

        if is_invehicle == True:
            num_t += 1
            dataval = 1
        else:
            num_f += 1
            dataval = 0

        plt_vals.append(dataval)

        info('IVA: Frame {0} = {1}.  Is_Day: {2}'.format(framecount, is_invehicle, is_day))
        timelogger.info('{0},{1}'.format(framecount, dataval))
        iva_output.append(is_invehicle)
        framecount += 1


    debug('Num in-vehicle: {0}'.format(num_t))
    debug('Num not in-vehicle: {0}'.format(num_f))
    info('IVA frame output: {0}'.format(iva_output))

    plt.plot(plt_vals)
    plt.title('IVA Report')
    plt.ylabel('In-Vehicle(1) or Not(0)')
    plt.xlabel('Frame #')
    plt.xlim([0, framecount+1])
    plt.ylim([-0.2, 1.2]) # space at top/bottom of y axis

    filepath = '{0}figure_plot.png'.format(reportpath)
    plt.savefig(filepath)
    plt.clf()

def main(path, reportpath):
    # setup process logger
    global LOG
    logfile = '{0}iva-processor.log'.format(reportpath)
    LOG = setup_logger('log', logfile)
    # logging.basicConfig(filename=logfile, format='%(asctime)s: %(message)s', level=logging.INFO)
    info('Extracting videos in path: {0}'.format(path))

    # setup data logger
    global timelogger
    tlogfile = '{0}iva-data.log'.format(reportpath)
    timelogger = setup_logger('data_logger', tlogfile, formatter=logging.Formatter('%(message)s'))

    process_images(path, reportpath)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        error('Invalid argument options.  Must pass directory path of images and path for reports')

