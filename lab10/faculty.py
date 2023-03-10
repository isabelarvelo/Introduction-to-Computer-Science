# STUDENTS: Fill in code for all procedures marked pass.
# Implement new doc tests to ensure functionality.

import csv
"""
This collection of utilities is useful for manipulating faculty.csv,
a Williams College faculty database stored in CSV format.

The fields of this database are:
  0: Instructor's name.  e.g. "Daniel P. Aalberts"
  1: Instructor's department. e.g. "Physics"
  2: Instructor's title. e.g. "Kennedy P. Richardson '71 Professor of Physics"
  3 onward: Instructor's degrees: year, degree, granting institution.
     e.g. "1994, Ph.D., Massachusetts Institute of Technology"

Each Degrees are constructed from the strings that describe them (as above).
They contain the following properties:
  d.year: 1994 (an int)
  d.kind: 'Ph.D.' (a string)
  d.institution: 'Massachusetts Institute of Technology"
Degrees have exactly on of the following predicates True:
  d.isbac(): a bool, True when degree is at bachelor level
  d.ismas(): a bool, True when degree is at master level
  d.isdoc(): a bool, True when degree is at doctorate level

Each Instructor describes the faculty member and is constructed based
on a name, department, title, and a list of Degrees:
  i.name: "Daniel P. Aalberts"
  i.title: "Kennedy P. Richardson '71 Professor of Physics"
  i.department: "Physics"
  i.degrees: a list of Degrees
"""

# Add functions to __all__ you want included when you 'from faculty import *'
__all__ = [ 'Degree', 'Instructor', 'readDB', 'uniqCount' ]

class Degree(object):
    """This class describes a degree.  It includes the institution,
    the degree kind, and the year the degree was granted."""

    __slots__ = ['_year', '_kind', '_inst']

    def __init__(self,info):
        """Construct a Degree from a string of the form
            '2020, Ph.D., Cornell University'
        >>> d = Degree('2020, Ph.D., Cornell University')
        >>> d.year
        2020
        >>> d.kind
        'Ph.D.'
        >>> d.institution
        'Cornell University'

        >>> b = Degree("2007, M.A., McGill University")
        >>> b.kind == 'M.A.'
        True
        >>> b._year = 2010
        >>> b.year
        2010

        """
        info = info.split(",")

        #year should be an integer
        self._year = int(info[0])
        #clean data by removing leading and lagging spaces
        self._kind = info[1].strip()
        self._inst = info[2].strip()

    @property
    def year(self):
        """The year the degree was granted (an int)."""
        return self._year

    @property
    def kind(self):
        """The kind of the degree (e.g. "M.S.")."""
        return self._kind

    @property
    def institution(self):
        """The granting institution."""
        return self._inst

    def isbac(self):
        """Returns True exactly when this a bachelor's degree."""
        return self._kind.startswith('B.') or self._kind.endswith('B.')

    def ismas(self):
        """Returns True exactly when this a master's degree."""
        return not (self.isbac() or self.isdoc())

    def isdoc(self):
        """Returns True exactly when this a doctorate."""
        return self._kind.startswith('D') or self._kind.endswith('D.')

    def __eq__(self, other):
        """Returns True if self and other are equal."""
        return (self._year == other._year and self._kind == other._kind and
                self._inst == other._inst)

    def __str__(self):
        """Returns a string representation of a degree."""
        return '{}, {}, {}'.format(self._year, self._kind, self._inst)

    def __repr__(self):
        """Returns a formal representation of a degree."""
        return 'Degree("{}, {}, {}")'.format(self._year, self._kind, self._inst)

class Instructor(object):
    """This class describes an instructor.  An instructor includes a
    name, a home department, a title, and a list of Degrees."""

    __slots__ = ['_name', '_dept', '_title', '_degs']

    def __init__(self, name, dept, title, degrees):
        """Construct an instructor from a name, a home department, a
        title, and a list of Degrees.

        >>> d1 = Degree("1989, B.S., Massachusetts Institute of Technology")
        >>> d2 = Degree("1994, Ph.D., Massachusetts Institute of Technology")
        >>> i = Instructor("Daniel P. Aalberts", "Physics", "Kennedy P. Richardson '71 Professor of Physics", [d1,d2] )
        >>> i.name
        'Daniel P. Aalberts'
        >>> i.dept
        'Physics'
        >>> i.title
        "Kennedy P. Richardson '71 Professor of Physics"
        >>> isinstance(i.degrees[0], Degree)
        True
        """
        self._name = name.strip()
        self._dept = dept.strip()
        self._title = title.strip()
        #want to read in degrees as a list
        self._degs = list(degrees)

    @property
    def name(self):
        """The instructor's name."""
        return self._name

    @property
    def dept(self):
        """The instructor's home department."""
        return self._dept

    @property
    def title(self):
        """The instructor's title."""
        return self._title

    @property
    def degrees(self):
        """A list of the instructor's Degrees."""
        return list(self._degs)

    def __eq__(self,other):
        """True if self and other are the same instructor."""
        return self._name == other._name and self._dept == other._dept

    def __str__(self):
        """A string representation of the Instructor."""
        degs = ','.join(['"'+str(deg)+'"' for deg in self._degs])
        return '"{}","{}","{}",{}'.format(self._name, self._dept, self._title, degs)

    def __repr__(self):
        """The formal representation of the Instructor."""
        return "Instructor({!r}, {!r}, {!r}, {!r})".format(self._name,self._dept,self._title,self._degs)

def readDB(filename="faculty.csv"):
    """Reads data from a CSV database (in Dean of Faculty-specified format)
    and returns a list of member descriptions.
    """
    #initialize result that will be a list on instructor objects with objects inside
    result = []
    with open(filename,'r') as f:
        csvf = csv.reader(f)
        for row in csvf:
            #intialize list of degrees for each faculty
            degs = []
            for degree in list(row[3:]):
                #need to create list of degree objects
                degs.append(Degree(degree))
            info = Instructor(row[0],row[1],row[2], degs)
            result.append(info)
    return result


def uniqCount(itemList):
    """Removes duplicate non-None values.
    Each result entry is a list containing the original value
    and its count.

    >>> uniqCount([1,1,2,-3,-3,-3,1,2])
    [[1, 2], [2, 1], [-3, 3], [1, 1], [2, 1]]

    >>> uniqCount([1,1,1,2,2,-3,-3,-3,])
    [[1, 3], [2, 2], [-3, 3]]

    >>> uniqCount (['Amy', 'Amy', 'Bob', 'Bob', 'Bob', 'Calvin'])
    [['Amy', 2], ['Bob', 3], ['Calvin', 1]]

    >>> uniqCount ([])
    []

    >>> uniqCount ([5])
    [[5, 1]]
    """

    results = []
    lastValue = None

    for i in range(len(itemList)):
        #comparing adjacent values because this function assumes lists are sorted
        #compare each item to the one before it
        if itemList[i] == lastValue:
            #increment count for the value if you see it again
            results[-1][1] += 1
        else:
            results.append([itemList[i], 1 ])
        lastValue = itemList[i]

    return results


def test():
    from doctest import testmod
    testmod()

if __name__ == '__main__':
    test()
