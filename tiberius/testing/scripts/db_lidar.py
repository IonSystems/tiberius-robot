from tiberius.database_wrapper.polyhedra_database import PolyhedraDatabase
from tiberius.database.query import get_latest
from tiberius.database.tables import LidarTable

pd = PolyhedraDatabase("test_gps_fetcher")
print get_latest(pd, LidarTable)
