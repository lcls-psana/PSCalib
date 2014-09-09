#ifndef PSCALIB_GEOMETRYACCESS_H
#define PSCALIB_GEOMETRYACCESS_H

//--------------------------------------------------------------------------
// File and Version Information:
// 	$Id$
//
// Description:
//	Class GeometryAccess.
//
//------------------------------------------------------------------------

//-----------------
// C/C++ Headers --
//-----------------
#include <string>
#include <vector>
#include <map>
#include <boost/shared_ptr.hpp>

//----------------------
// Base Class Headers --
//----------------------

//-------------------------------
// Collaborating Class Headers --
//-------------------------------
#include "PSCalib/GeometryObject.h"

#include "ndarray/ndarray.h" // for img_from_pixel_arrays(...)

//------------------------------------
// Collaborating Class Declarations --
//------------------------------------

//		---------------------
// 		-- Class Interface --
//		---------------------

namespace PSCalib {

/// @addtogroup PSCalib

/**
 *  @ingroup PSCalib
 *
 *  @brief Class supports universal detector geometry description.
 *
 *  This software was developed for the LCLS project.  If you use all or 
 *  part of it, please give an appropriate acknowledgment.
 *
 *  @version $Id$
 *
 *  @see GeometryObject, CalibFileFinder, PSCalib/test/ex_geometry_access.cpp
 *
 *  @anchor interface
 *  @par<interface> Interface Description
 * 
 *  @li  Include
 *  @code
 *  #include "PSCalib/GeometryAccess.h"
 *  #include "ndarray/ndarray.h" // need it if image is returned
 *  @endcode
 *
 *  @li Instatiation
 *  \n
 *  Code below instateates GeometryAccess object using path to the calibration "geometry" file and verbosity control bit-word:
 *  @code
 *  std::string path = /reg/d/psdm/<INS>/<experiment>/calib/<calib-type>/<det-src>/geometry/0-end.data"
 *  unsigned print_bits = 0377; // or = 0 (by default) - to suppress printout from this object. 
 *  PSCalib::GeometryAccess geometry(path, print_bits);
 *  @endcode
 *  To find path automatically use CalibFileFinder.
 *
 *  @li Access methods
 *  @code
 *    // Access and print coordinate arrays:
 *        const double* X;
 *        const double* Y;
 *        const double* Z;
 *        unsigned   size;
 *        geometry.get_pixel_coords(X,Y,Z,size);
 *        cout << "size=" << size << '\n' << std::fixed << std::setprecision(1);  
 *        cout << "X: "; for(unsigned i=0; i<10; ++i) cout << std::setw(10) << X[i] << ", "; cout << "...\n"; 
 *        // or get coordinate arrays for specified geometry object:
 *        geometry.get_pixel_coords(X,Y,Z,size, "QUAD:V1", 1);
 *        // then use X, Y, Z, size
 *    
 *    // Access pixel areas:
 *        const double* A;
 *        unsigned   size;
 *        geometry.get_pixel_areas(A,size);
 * 
 *    // Access pixel size for entire detector:
 *        double pix_scale_size = geometry.get_pixel_scale_size ();
 *        // or for specified geometry object, for example one quad of CSPAD
 *        double pix_scale_size = geometry.get_pixel_scale_size("QUAD:V1", 1);
 *    
 *    // Access pixel indexes for image:
 *        const unsigned * iX;                                                                             
 *        const unsigned * iY;                                                                             
 *        unsigned   isize;                                                                                
 *        // optional parameters for specified geometry  
 *        const std::string ioname = "QUAD:V1";                                                            
 *        const unsigned ioindex = 1;                                                                      
 *        const double pix_scale_size_um = 109.92;                                                         
 *        const int xy0_off_pix[] = {200,200};
 *        
 *        // this call returns index arrays iX, iY of size=isize for QUAD with offset 
 *        geometry.get_pixel_coord_indexes(iX, iY, isize, ioname, ioindex, pix_scale_size_um, xy0_off_pix);
 *        
 *        // this call returns index arrays for entire detector with auto generated minimal offset
 *        geometry.get_pixel_coord_indexes(iX, iY, isize);
 *        // then use iX, iY, isize, for example make image as follows.   
 *
 *    // Make image from index, iX, iY, and intensity, W, arrays
 *        ndarray<PSCalib::GeometryAccess::image_t, 2> img = 
 *                PSCalib::GeometryAccess::img_from_pixel_arrays(iX, iY, 0, isize);
 *    
 *    // Access and print comments from the calibration "geometry" file:
 *        std::map<std::string, std::string>& dict = geometry.get_dict_of_comments ();
 *        cout << "dict['HDR'] = " << dict["HDR"] << '\n';
 *  @endcode
 * 
 *  @li Print methods
 *  @code
 *    geometry.print_pixel_coords();
 *    geometry.print_pixel_coords("QUAD:V1", 1);
 *    geometry.print_list_of_geos();
 *    geometry.print_list_of_geos_children();
 *    geometry.print_comments_from_dict();
 *
 *    // or print info about specified geometry objects (see class GeometryObject):
 *    geometry.get_geo("QUAD:V1", 1)->print_geo();
 *    geometry.get_top_geo()->print_geo_children();
 *  @endcode
 *
 *  @author Mikhail S. Dubrovin
 */


class GeometryAccess  {

//typedef boost::shared_ptr<GeometryObject> shpGO;
/** Use the same declaration of the shared pointer to geometry object like in the class GeometryObject*/
typedef PSCalib::GeometryObject::shpGO shpGO;

public:

  typedef double image_t;

  /**
   *  @brief Class constructor accepts path to the calibration "geometry" file and verbosity control bit-word 
   *  
   *  @param[in] path  path to the calibration "geometry" file
   *  @param[in] pbits verbosity control bit-word; 
   *  \n         =0  print nothing, 
   *  \n         +1  info about loaded file, 
   *  \n         +2  list of geometry objects, 
   *  \n         +8  list of geometry objects with childrens, 
   *  \n         +16 info about setting relations between geometry objects, 
   *  \n         +32 info about pixel coordinate reconstruction
   */ 
  GeometryAccess (const std::string& path, unsigned pbits=0) ;

  // Destructor
  virtual ~GeometryAccess () ;

  /// Returns shared pointer to the geometry object specified by name and index 
  shpGO get_geo(const std::string& oname, const unsigned& oindex);

  /// Returns shared pointer to the top geometry object, for exampme CSPAD
  shpGO get_top_geo();

  /// Returns pixel coordinate arrays X, Y, Z, of size for specified geometry object 
  /**
   *  @param[out] X - pointer to x pixel coordinate array
   *  @param[out] Y - pointer to y pixel coordinate array
   *  @param[out] Z - pointer to z pixel coordinate array
   *  @param[out] size - size of the pixel coordinate array (number of pixels)
   *  @param[in]  oname - object name
   *  @param[in]  oindex - object index
   */
  void  get_pixel_coords(const double*& X, 
                         const double*& Y, 
                         const double*& Z, 
                         unsigned& size,
			 const std::string& oname = std::string(), 
			 const unsigned& oindex = 0);

  /// Returns pixel areas array A, of size for specified geometry object 
  /**
   *  @param[out] A - pointer to pixel areas array
   *  @param[out] size - size of the pixel array (number of pixels)
   *  @param[in]  oname - object name
   *  @param[in]  oindex - object index
   */
  void  get_pixel_areas (const double*& A, 
                         unsigned& size,
			 const std::string& oname = std::string(), 
			 const unsigned& oindex = 0);

  /// Returns pixel scale size for specified geometry object through its children segment
  /**
   *  @param[in]  oname - object name
   *  @param[in]  oindex - object index
   */
  double get_pixel_scale_size(const std::string& oname = std::string(), 
                              const unsigned& oindex = 0);

  /// Returns dictionary of comments
  std::map<std::string, std::string>& get_dict_of_comments() {return m_dict_of_comments;}

  /// Prints the list of geometry objects
  void print_list_of_geos();

  /// Prints the list of geometry objects with children
  void print_list_of_geos_children();

  /// Prints comments loaded from input file and kept in the dictionary  
  void print_comments_from_dict();

  /// Prints beginning of pixel coordinate arrays for specified geometry object (top object by default)
  void print_pixel_coords( const std::string& oname= std::string(), 
			   const unsigned& oindex = 0);

  /// Returns pixel coordinate index arrays iX, iY of size for specified geometry object 
 /**
   *  @param[out] iX - pointer to x pixel index coordinate array
   *  @param[out] iY - pointer to y pixel index coordinate array
   *  @param[out] size - size of the pixel coordinate array (number of pixels)
   *  @param[in]  oname - object name (deafault - top object)
   *  @param[in]  oindex - object index (default = 0)
   *  @param[in]  pix_scale_size_um - ex.: 109.92 (default - search for the first segment pixel size)
   *  @param[in]  xy0_off_pix - array containing X and Y coordinates of the offset (default - use xmin, ymin)
   */
  void get_pixel_coord_indexes( const unsigned *& iX, 
                                const unsigned *& iY, 
				unsigned& size,
                                const std::string& oname = std::string(), 
				const unsigned& oindex = 0, 
                                const double& pix_scale_size_um = 0, 
                                const int* xy0_off_pix = 0 );

  /// Returns image as ndarray<image_t, 2> object
 /**
   *  @param[in] iX - pointer to x pixel index coordinate array
   *  @param[in] iY - pointer to y pixel index coordinate array
   *  @param[in]  W - pointer to the intensity (weights) array (default - set 1 for each pixel) 
   *  @param[in] size - size of the pixel coordinate array (number of pixels)
   */
  static ndarray<image_t, 2>
  img_from_pixel_arrays(const unsigned*& iX, 
                        const unsigned*& iY, 
                        const double*    W = 0,
                        const unsigned&  size = 0);

protected:

private:

  /// path to the calibration "geometry" file
  std::string m_path;

  /// print bits
  unsigned m_pbits;

  /// pointer to x pixel coordinate index array
  unsigned* p_iX;

  /// pointer to x pixel coordinate index array
  unsigned* p_iY;
 
  /// vector/list of shared pointers to geometry objects
  std::vector<shpGO> v_list_of_geos;

  /// map/dictionary of comments from calibration "geometry" file 
  std::map<std::string, std::string> m_dict_of_comments;

  /// Loads calibration file
  void load_pars_from_file();

  /// Adds comment to the dictionary
  void add_comment_to_dict(const std::string& line);

  /// Parses input data line, creates and returns geometry object
  shpGO parse_line(const std::string& line);

  /// Returns shp to the parent of geobj. If parent is not found adds geobj as a top parent and returns 0.
  shpGO find_parent(const shpGO& geobj);

  /// Set relations between geometry objects in the list_of_geos
  void set_relations();

  /// Returns class name for MsgLogger
  static const std::string name() {return "PSCalib";}

  // Copy constructor and assignment are disabled by default
  GeometryAccess ( const GeometryAccess& ) ;
  GeometryAccess& operator = ( const GeometryAccess& ) ;

};

} // namespace PSCalib

#endif // PSCALIB_GEOMETRYACCESS_H
