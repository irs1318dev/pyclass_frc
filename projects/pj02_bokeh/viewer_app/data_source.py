"""Gets data for viewer classes.
Meghana Annamaneni 2/17/2020
Revised by Stacy Irwin 2/17/2020

Contents
--------
    DataSource: A class that can extract scouting data from either the
        scouting system's SQL database, or from a Python pickle file.

All classes that create plots or tables for the viewer_app should use
DataSource to connect to the scouting SQL database or to a Python pickle
data file. In general, a DataSource will be passed to the plotting
class's constructor as an argument.
"""
import pickle

import pandas as pd


class DataSource:
    """Provides DataFrames for plotting to viewer_app classes.

    If no arguments are passed to the constructor, DataSource will retrieve
    data directly from the scouting database. Other options are to pass
    a file name or both an event name and the season.
        Constructor Arguments:
            fname: Optional, str. If specified, data will be loaded from a
                Python pickle file. fname must be a path or filename that
                can be used with the Python `open()` built-in function. If
                omitted, DataSource will load scouting data from the
                scouting database.
            event: Optional, str. A string used to identify the competition.
                Usually the FIRST API event code. If not specified,
                DataSource will connect directly to the scouting system SQL
                database.
            season: Optional, str. A string identifying the four-digit year
                for the specific game being scouted. E.g., '2020' refers to
                *Infinite Recharge* and `2019` refers to *Deep Space*.

        Attributes:
            measures: Pandas DataFrame containing detailed scouting data for
                each team and match.
            schedule: Pandas DataFrame containing the match schedule
            teams: Pandas DataFrame with list of teams participating in
                    competition
            event: str, FIRST API event code for event
            season: str, 4-digit year denoting the season
            fname: str, name of file from which data was loaded, or None if
                data loaded directly from scouting database.
            from_sql: bool, True if loaded from database, False otherwise

        Methods:
            refresh(): Reload scouting data from the source, either a file
                or the scouting database.
            write_file(): Write the scouting data to a Python pickle file.
    """
    def __init__(self, sql=False, fname=None, event=None, season=None):
        """Initializes a DataSource object."""
        self.measures = None
        self.enum_measures = None
        self.schedule = None
        self.teams = None
        self.status = None
        self.event = event
        self.season = season
        self.fname = fname
        self.from_sql = False
        self.enum_tasks = None

        if self.fname is not None:
            self._load_from_file()
        else:
            # Import non-viewer_app modules only if loading from SQL
            #   Allows viewer_app to be run as a standalone application
            #   without the rest of the server files.
            import server.model.connection
            import server.model.event
            global smc, sme
            smc = server.model.connection
            sme = server.model.event

            self.from_sql = True
            self._load_from_sql()

    def _load_from_file(self):
        """Loads data from a Python pickle file."""
        with open(self.fname, 'rb') as data_file:
            data = pickle.load(data_file)
        self.measures = data['measures']
        self.enum_measures = data['enum_measures']
        self.schedule = data['schedule']
        self.teams = data['teams']
        self.event = data['event']
        self.season = data['season']
        self.status = data['status']
        self.enum_tasks = list(pd.unique(self.enum_measures.task))

    def _load_from_sql(self):
        """Connects to the scouting database and creates DataFrames."""
        if self.event is not None and self.season is not None:
            sme.EventDal.set_current_event(self.event, self.season)

        # Load measures data
        conn = smc.pool.getconn()
        sql = "SELECT * FROM vw_measures;"
        measures = pd.read_sql(sql, conn)
        self.measures = measures.dropna(subset=['task']).copy()

        # Preprocess enumerated values
        self.enum_measures = self._enum_preprocess()

        # Get teams and event data
        sql = """
        SELECT * FROM vw_schedule;"""
        self.schedule = pd.read_sql(sql, conn)

        evt = sme.EventDal.get_current_event()
        evt_id = evt[0]
        self.event = evt[1]
        self.season = evt[2]
        sql = """
        SELECT * FROM teams
            WHERE teams.name IN
                (SELECT team FROM schedules WHERE event_id = %s) AND
                name <> 'na';"""
        self.teams = pd.read_sql(sql, conn, params=[str(evt_id)])
        self._add_num_matches()

        sql = """
        SELECT * FROM vw_status_date;"""
        self.status = pd.read_sql(sql, conn)

        enum_tasks = pd.unique(self.enum_measures.task)
        enum_tasks.sort()
        self.enum_tasks = list(enum_tasks)

        # generate pickle file to clients that don't have sql
        self.write_file(fname='vif.pickle')

        # Return connection to pool.
        smc.pool.putconn(conn)

    def refresh(self, fname=None):
        """Refreshes data by reconnecting to the database or to a file.

        Args:
            fname: A Python style filename or path. fname must work with
                Python's built-in open() function.
        """
        if fname is not None:
            self.fname = fname
        if self.from_sql:
            self._load_from_sql()
        else:
            self._load_from_file()

    def write_file(self, fname=None):
        """Writes all data to a Python pickle file.

        Args:
            fname: A Python style filename or path. fname must work with
                Python's built-in open() function.
        """
        data = {'measures': self.measures, 'enum_measures': self.enum_measures,
                'schedule': self.schedule,
                'teams': self.teams, 'event': self.event,
                'season': self.season, 'status': self.status}

        with open(fname, 'wb') as data_file:
            pickle.dump(data, data_file)

    def _enum_preprocess(self):
        """Modifies enumerated tasks to simplify plotting.

        1. For all enumerated tasks in the measures table, modifies
        value of task measures.task to {task_name}_{enum_value}.
        2. Places a 1 integer in the measures.successes column.

        Returns:
            Pandas dataframe
        """
        measures = self.measures.copy()
        measures.loc[
            measures.measuretype == 'enum',
            'task'] = (measures.task + '_' + measures.capability)
        measures.loc[measures.measuretype == 'enum', 'successes'] = 1
        return measures.dropna(subset=['task']).copy()

    def _add_num_matches(self):
        """Inserts a num_matches columns in the teams dataframe.
        """
        max_match = self.measures.sort_values('match',
                                              ascending=False).iat[0, 4]
        completed_matches = self.schedule[
            self.schedule.match <= max_match][['match', 'team']]
        match_counts = completed_matches.groupby('team').count()
        match_counts.rename({'match': 'matches_played'}, axis=1, inplace=True)
        self.teams = pd.merge(self.teams, match_counts, left_on='name',
                              right_on='team', how='left').copy()
        return self.teams
