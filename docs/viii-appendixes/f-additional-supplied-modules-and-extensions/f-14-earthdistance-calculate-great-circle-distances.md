---
title: "F.14. earthdistance — calculate great-circle distances"
id: earthdistance
---

## earthdistance calculate great-circle distances

The `earthdistance` module provides two different approaches to calculating great circle distances on the surface of the Earth.
The one described first depends on the `cube` module.
The second one is based on the built-in `point` data type, using longitude and latitude for the coordinates.

In this module, the Earth is assumed to be perfectly spherical. (If that\'s too inaccurate for you, you might want to look at the [PostGIS](https://postgis.net/) project.)

The `cube` module must be installed before `earthdistance` can be installed (although you can use the `CASCADE` option of `CREATE EXTENSION` to install both in one command).

:::{.callout type="caution"}
It is strongly recommended that `earthdistance` and `cube` be installed in the same schema, and that that schema be one for which CREATE privilege has not been and will not be granted to any untrusted users. Otherwise there are installation-time security hazards if `earthdistance`\'s schema contains objects defined by a hostile user. Furthermore, when using `earthdistance`\'s functions after installation, the entire search path should contain only trusted schemas.
:::

### Cube-Based Earth Distances

Data is stored in cubes that are points (both corners are the same) using 3 coordinates representing the x, y, and z distance from the center of the Earth.
A domain `earth` over type `cube` is provided, which includes constraint checks that the value meets these restrictions and is reasonably close to the actual surface of the Earth.

The radius of the Earth is obtained from the `earth()` function.
It is given in meters.
But by changing this one function you can change the module to use some other units, or to use a different value of the radius that you feel is more appropriate.

This package has applications to astronomical databases as well.
Astronomers will probably want to change `earth()` to return a radius of `180/pi()` so that distances are in degrees.

Functions are provided to support input in latitude and longitude (in degrees), to support output of latitude and longitude, to calculate the great circle distance between two points and to easily specify a bounding box usable for index searches.

The provided functions are shown in [Cube-Based Earthdistance Functions](#earthdistance-cube-functions).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Function

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `earth` () float8

   Returns the assumed radius of the Earth.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `sec_to_gc` ( `float8` ) float8

   Converts the normal straight line (secant) distance between two points on the surface of the Earth to the great circle distance between them.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `gc_to_sec` ( `float8` ) float8

   Converts the great circle distance between two points on the surface of the Earth to the normal straight line (secant) distance between them.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `ll_to_earth` ( `float8`, `float8` ) earth

   Returns the location of a point on the surface of the Earth given its latitude (argument 1) and longitude (argument 2) in degrees.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `latitude` ( `earth` ) float8

   Returns the latitude in degrees of a point on the surface of the Earth.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `longitude` ( `earth` ) float8

   Returns the longitude in degrees of a point on the surface of the Earth.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `earth_distance` ( `earth`, `earth` ) float8

   Returns the great circle distance between two points on the surface of the Earth.
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `earth_box` ( `earth`, `float8` ) cube

   Returns a box suitable for an indexed search using the `cube` `@>` operator for points within a given great circle distance of a location. Some points in this box are further than the specified great circle distance from the location, so a second check using `earth_distance` should be included in the query.
  :::{/cell}
  :::{/row}
:::{/table}

: Cube-Based Earthdistance Functions

### Point-Based Earth Distances

The second part of the module relies on representing Earth locations as values of type `point`, in which the first component is taken to represent longitude in degrees, and the second component is taken to represent latitude in degrees. Points are taken as (longitude, latitude) and not vice versa because longitude is closer to the intuitive idea of x-axis and latitude to y-axis.

A single operator is provided, shown in [Point-Based Earthdistance Operators](#earthdistance-point-operators).

:::{.table}
  :::{.row header="true"}
  :::{.cell}
   Operator

   Description
  :::{/cell}
  :::{/row}
  :::{.row}
  :::{.cell}
   `point` `<@>` `point` float8

   Computes the distance in statute miles between two points on the Earth\'s surface.
  :::{/cell}
  :::{/row}
:::{/table}

: Point-Based Earthdistance Operators

Note that unlike the `cube`-based part of the module, units are hardwired here: changing the `earth()` function will not affect the results of this operator.

One disadvantage of the longitude/latitude representation is that you need to be careful about the edge conditions near the poles and near +/- 180 degrees of longitude. The `cube`-based representation avoids these discontinuities.
