"""catalog __init__ — expose all three course specs."""
from seed.catalogs.english import ENGLISH_COURSE_SPEC
from seed.catalogs.spanish import SPANISH_COURSE_SPEC
from seed.catalogs.french import FRENCH_COURSE_SPEC

ALL_COURSE_SPECS = [ENGLISH_COURSE_SPEC, SPANISH_COURSE_SPEC, FRENCH_COURSE_SPEC]
