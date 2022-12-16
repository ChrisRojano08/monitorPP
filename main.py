import sys
import os
import shutil
import datetime
import psutil
import time
from prettytable import PrettyTable

numI = 0
while True:
    process_table = PrettyTable(['PID', 'PNAME', 'STATUS',
                                'CPU', 'NUM THREADS', 'MEMORY(MB)'])

    try:
        proc = []
        for pid in psutil.pids()[-200:]:
            try:
                p = psutil.Process(pid)
                p.cpu_percent()
                proc.append(p)
            except Exception as e:
                pass

        top = {}
        time.sleep(0.1)
        for p in proc:
            top[p] = p.cpu_percent() / psutil.cpu_count()

        top_list = sorted(top.items(), key=lambda x: x[1])
        top10 = top_list[-15:]
        top10.reverse()

        for p, cpu_percent in top10:
            try:
                with p.oneshot():
                    process_table.add_row([
                        str(p.pid),
                            p.name(),
                            p.status(),
                            f'{cpu_percent:.2f}' + "%",
                            p.num_threads(),
                            f'{p.memory_info().rss / 1e6:.3f}'
                        ])

            except Exception as e:
                pass
    except Exception as e:
        pass

    if sys.platform.startswith('linux'):
        rootDir = r'/'
    elif sys.platform.startswith('win'):
        rootDir = r'C:'

    fullPath = os.path.join(rootDir, "softitlan", "log", "cuponealo")

    if numI < 200:
        ind = 0
        while ind < 5:
            if not (os.path.isdir(os.path.join(rootDir, "softitlan"))):
                os.mkdir(os.path.join(rootDir, "softitlan"))
            elif not (os.path.isdir(os.path.join(rootDir, "softitlan", "log"))):
                os.mkdir(os.path.join(rootDir, "softitlan", "log"))
            elif not (os.path.isdir(fullPath)):
                os.mkdir(fullPath)
            elif not (os.path.isfile(os.path.join(fullPath, "processLog.log"))):
                f = open(os.path.join(fullPath, "processLog.log"), "w")
                ind = 5
            else:
                f = open(os.path.join(fullPath, "processLog.log"), "a")
                ind = 5

        f.write('\n')
        f.write(str(process_table))
        f.write('\n')
        numI = numI+1

        f.close()
    else:
        e = datetime.datetime.now()
        newFile = os.path.join(fullPath, str("processLog "+str(e.strftime("%Y-%m-%d %H-%M-%S"))+".log"))
        shutil.copyfile(os.path.join(fullPath, "processLog.log"), newFile)

        open(os.path.join(fullPath, "processLog.log"), "w").close()
        numI=0
    time.sleep(10)
