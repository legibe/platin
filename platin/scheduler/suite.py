import os
import sys
try:
    import ecflow 
except ImportError as e:
    print '---------------------------------------------------------------------------------------'
    print '"ecflow" must be installed on the system. It is not an automatic dependency for platin'
    print '---------------------------------------------------------------------------------------'
    exit()
from collections import OrderedDict
from ..core.config import Config
from ..core.date import Day, Date
from ..core.config import Config
from ..core.factory import createFactory
from platinflow import PlatinFlow

class Suite(PlatinFlow):

    # default duration for each loop type (about 25 years)
    loop_increment = {
        'daily': 1,
        'weekly': 7,
    }
    # 25 years
    duration = 365 * 25
    families = OrderedDict()

    #---------------------------------------------------------------------
    # returns a factory instance in which the caller can register
    # a class to create families.
    #---------------------------------------------------------------------
    @classmethod
    def createFamilyLoop(self,name,loop_type,python_scripts,start_date=None,duration=None):
        if name in self.families:
            raise ValueError('Family %s alredy exists' % (name))
        d = dict(
            loop_type = loop_type,
            python_scripts = python_scripts,
            start_date = start_date,
            duration = duration
        )
        self.families[name] = d
        return createFactory(name) 
        

    def __init__(self,configFile = None, action = None):
        self._pwd = os.path.dirname(__file__)
        if configFile is None:
            configFile = os.path.join(self._pwd,'config.yaml')
        self._config = Config.read(configFile)
        self._defs = ecflow.Defs()
        self._suite= self._defs.add_suite(self._config['preferences']['suite_name'])
        super(Suite,self).__init__(self._suite)


    def make_path(self,prefix,path):
        if path[0] != '/':
            path = os.path.join(prefix,path)
        return path

    def __call__(self,replace_path):
        suite = self._suite
        paths = self._config['path']
        prefix = paths['prefix']
        clock = ecflow.Clock(False)
        suite.add_clock(clock)
        suite.add_variable("ECF_JOB_CMD","/bin/bash %ECF_JOB% 1> %ECF_JOBOUT% 2>&1")
        suite.add_variable("ECF_HOME",self.make_path(prefix,paths['server']))
        suite.add_variable("ECF_FILES", self.make_path(prefix,paths['tasks']))
        if paths['include'] is None:
            suite.add_variable("ECF_INCLUDE", os.path.join(self._pwd,'include'))
        else:
            suite.add_variable("ECF_INCLUDE", self.make_path(prefix,paths['include']))
        suite.add_variable("ECF_BIN", os.path.join(self._pwd,'bin'))
        suite.add_variable("PYTHON_EXEC", self._config['preferences']['python_runtime'])
        suite.add_variable("TMPDIR", self.make_path(prefix,paths['tmpdir']))
        suite.add_variable("ECF_TRIES", self._config['preferences']['tries'])
        suite.add_variable("DELTA", 0)
        suite.add_variable("CONFIG_DIR",self.make_path(prefix,self._config['path']['config']))

        # admin emails related variables
        suite.add_variable("SCHEDULER_PATH",self._pwd)
        suite.add_variable("SCHEDULER_EMAIL",self._config['preferences']['email']['from'])
        suite.add_variable("SCHEDULER_ADMIN",','.join(self._config['preferences']['email']['to']))


        # for customer emails
        suite.add_variable("EMAIL_STATUS",'1')

        # where tasks are supposed to save data
        suite.add_variable("DATA_STORE",self.make_path(prefix,paths['datastore']))

        for family,info in self.families.items():
            with suite.add_family(family) as current:
                if info['start_date'] is None:
                    startdate = Day(Date())
                else:
                    startdate = Day(info['start_date'])
                duration = self.duration
                if info['duration'] is not None:
                    duration = info['duration']
                enddate = startdate + duration

                # adjust environment
                current.add_variable("PYTHON_SCRIPTS", info['python_scripts'])
                current.add_repeat(ecflow.RepeatDate("YMD", int(startdate.format('%Y%m%d')),int(enddate.format('%Y%m%d')),self.loop_increment[info['loop_type']]))

                # if it exists, createFactory just returns the factory
                factory = createFactory(family)
                families = factory.registered()
                for family in families:
                    factory.create(family)(PlatinFlow(current))

                restart = current.add_task('restart')
                restart.add_time('23:59')

        cleanup = suite.add_task('cleanup')
        cleanup.add_time('23:59')

        client = ecflow.Client(self._config['preferences']['host'],
                               self._config['preferences']['port'])
        if replace_path is None:
            replace_path = '/' + self._config['preferences']['suite_name']
        client.replace(replace_path,self._defs)
