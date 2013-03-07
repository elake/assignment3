#include <Arduino.h>
#include <Adafruit_ST7735.h>
#include <SD.h>
#include <mem_syms.h>

#include "map.h"
#include "serial_handling.h"
#include "path.h"

#define DEBUG_PATH6

/* path routine error code
   0 no error
   1 
*/
int16_t path_errno;

extern Adafruit_ST7735 tft;

// read a path from the serial port and return the length of the
// path and a pointer to the array of coordinates.  That array should
// be freed later.

// Returns 1 if the call was successful, 0 if not.

uint8_t read_path(uint16_t *length_p, coord_t *path_p[]) {
    // the line to be read, and it size
    const uint8_t line_size = 40;
    char line[line_size];
    uint16_t bytes_read;

    // the field extracted
    const uint8_t field_size = 20;
    char field[field_size];
    uint16_t field_index;
    int32_t field_value;

    *length_p = 0;
    *path_p = 0;

    // reset the error code
    path_errno = 0;

    while ( ! Serial.available() )  { };

    uint16_t max_path_size = (AVAIL_MEM - 256) / sizeof(coord_t);

    #ifdef DEBUG_PATH
    //Serial.print("Max path length ");
    //Serial.println(max_path_size);
    #endif

    bytes_read = serial_readline(line, line_size);

    // read the number of points, first field
    field_index = 0;   
    field_index = 
        string_read_field(line, field_index, field, field_size, " ");
    field_value = string_get_int(field);

    #ifdef DEBUG_PATH
        Serial.print("Path length ");
        Serial.print(field_value);
        Serial.println();
    #endif

    // do a consistency check
    if ( field_value < 0  || max_path_size < field_value ) {
        path_errno = 1;
        return 0;
        }
    uint8_t tmp_length = field_value;
    *length_p = tmp_length;

    // allocate the storage, see if we got it.
    coord_t *tmp_path = (coord_t *) malloc( tmp_length * sizeof(coord_t));
    if ( !tmp_path ) { 
        path_errno = 2;
        return 0; 
        }

    *path_p = tmp_path;

    while ( tmp_length > 0 ) {
        bytes_read = serial_readline(line, line_size);

        // read the number of points, first field
        field_index = 0;   

        field_index = 
            string_read_field(line, field_index, field, field_size, " ");
        tmp_path->lat = string_get_int(field);

        field_index = 
            string_read_field(line, field_index, field, field_size, " ");
        tmp_path->lon = string_get_int(field);

        tmp_length--;
        tmp_path++;
        }

    return 1;
    }

uint8_t is_coord_visible(coord_t point) {
    // figure out the x and y positions on the current map of the 
    // given point
    uint16_t point_map_y = latitude_to_y(current_map_num, point.lat);
    uint16_t point_map_x = longitude_to_x(current_map_num, point.lon);

    uint8_t r = 
        screen_map_x < point_map_x &&
        point_map_x < screen_map_x + display_window_width &&
        screen_map_y < point_map_y &&
        point_map_y < screen_map_y + display_window_height; 

    return r;
    }

void draw_path(uint16_t length, coord_t path[], char map_num) {
  coord_t line_from;
  coord_t line_to;

  int16_t x0;
  int16_t y0;

  int16_t x1;
  int16_t y1;
  
  for (int i = 0; i < length - 1; i++) {
    line_from = path[i];
    line_to = path[i+1];
   
    x0 = longitude_to_x(map_num, line_from.lon) - screen_map_x;
    y0 = latitude_to_y(map_num, line_from.lat) - screen_map_y;

    x1 = longitude_to_x(map_num, line_to.lon) - screen_map_x;
    y1 = latitude_to_y(map_num, line_to.lat) - screen_map_y;

    if (box_contains(x0, y0) && box_contains(x1, y1)) {
      draw_line(x0, y0, x1, y1);
    }
    else {
      clip_draw(x0, y0, x1, y1);
    }
  }
    // if current and prev points are visible then draw a line
    // tft.drawLine(prev_x, prev_y, cur_x, cur_y, BLUE);
}

int box_contains(int16_t x0, int16_t y0)
{
  // globals: display_window_height, display_window_width, msg_window_height
  return (x0 >= 0 && x0 <= 120) && 
    (y0 >= 0 && y0 <= (148));
}

const int xmin = 0;
const int xmax = 128;
const int ymin = 0;
const int ymax = 148;

typedef int OutCode;

const int INSIDE = 0; // 0000
const int LEFT = 1;   // 0001
const int RIGHT = 2;  // 0010
const int BOTTOM = 4; // 0100
const int TOP = 8;    // 1000
 
// Compute the bit code for a point (x, y) using the clip rectangle
// bounded diagonally by (xmin, ymin), and (xmax, ymax)
 
// ASSUME THAT xmax, xmin, ymax and ymin are global constants.
 
OutCode ComputeOutCode(double x, double y)
{
        OutCode code;
 
        code = INSIDE;          // initialised as being inside of clip window
 
        if (x < xmin)           // to the left of clip window
                code |= LEFT;
        else if (x > xmax)      // to the right of clip window
                code |= RIGHT;
        if (y < ymin)           // below the clip window
                code |= BOTTOM;
        else if (y > ymax)      // above the clip window
                code |= TOP;
 
        return code;
}
 
// Cohen–Sutherland clipping algorithm clips a line from
// P0 = (x0, y0) to P1 = (x1, y1) against a rectangle with 
// diagonal from (xmin, ymin) to (xmax, ymax).
void clip_draw(double x0, double y0, double x1, double y1)
{
      
  OutCode outcode0 = ComputeOutCode(x0, y0);
  OutCode outcode1 = ComputeOutCode(x1, y1);
  bool accept = false;
 
  while (true) {
    if (!(outcode0 | outcode1)) { // Bitwise
      accept = true;
      break;
    } 
    else if (outcode0 & outcode1) { // Bit
      if (0) {
	tft.fillRect(0, 75, 25, 125, GREEN);
      }
      break;
      
    } else {
      // failed both tests, so calcula
      // from an outside point to an i
      double x, y;
 
      // At least one endpoint is outs
      OutCode outcodeOut = outcode0 ? outcode0 : outcode1;
 
      // Now find the intersection point;
      // use formulas y = y0 + slope *
      if (outcodeOut & TOP) {         
	x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0);
	y = ymax;
      } 
      else if (outcodeOut & BOTTOM) {
	x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0);
	y = ymin;
      }
      else if (outcodeOut & RIGHT) { 
	y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0);
	x = xmax;
      }
      else if (outcodeOut & LEFT) {  
	y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0);
	x = xmin;
      }
 
      // Now we move outside point to i
      // and get ready for next pass.
      if (outcodeOut == outcode0) {
	x0 = x;
	y0 = y;
	outcode0 = ComputeOutCode(x0, y0);
      }
      else {
	x1 = x;
	y1 = y;
	outcode1 = ComputeOutCode(x1, y1);
      }
    }
  }
  if (accept) {
    // Following functions are left for implem
    // their platform (OpenGL/graphics.h etc.)
    draw_line(x0, y0, x1, y1);
  }
}
