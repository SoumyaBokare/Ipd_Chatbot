// Raspberry Pi 4 Case with 3.5" LCD Display - Modified Version
// All measurements in mm

// Parameters
wall_thickness = 2.5;
corner_radius = 3;
tolerance = 0.8; // Increased for easier fit - 1.6mm total clearance

// Raspberry Pi 4 dimensions
rpi_length = 85;
rpi_width = 56;
rpi_height = 18; // Height with GPIO header
board_thickness = 1.5;

// Display dimensions (3.5" LCD on GPIO)
display_length = 85;
display_width = 56;
display_height = 8; // Display assembly height above RPi
screen_length = 73; // Visible screen area
screen_width = 49;
screen_offset_x = 6; // Screen position offset from edge
screen_offset_y = 3.5;

// Total case dimensions - INCREASED length and breadth
case_length = 120; // 12cm (increased from ~91mm)
case_width = 80;   // 8cm (increased from ~62mm)
case_height = rpi_height + display_height + wall_thickness + 2;

// Keep RPi positioning fixed (not centered) - maintain original spacing
center_offset_x = 0; // Keep RPi at original position from left edge
center_offset_y = 0; // Keep RPi at original position from front edge

// Port cutout positions (from RPi edge)
// USB and Ethernet side (width side)
usb_port_y = 9;
usb_port_width = 15;
usb_port_height = 16;
usb_spacing = 19;

ethernet_y = 47;
ethernet_width = 16;
ethernet_height = 14;

// Power and HDMI side (length side)
usbc_x = 11;
usbc_width = 9;
usbc_height = 4;

hdmi0_x = 26;
hdmi1_x = 40;
hdmi_width = 7.5;
hdmi_height = 6;

audio_x = 54;
audio_diameter = 6;

// SD card side
sd_y = 20;
sd_width = 14;
sd_height = 2;
sd_protrusion = 2;

// Mounting holes
mounting_hole_diameter = 2.75;
mounting_hole_positions = [
    [3.5, 3.5],
    [61.5, 3.5],
    [3.5, 52.5],
    [61.5, 52.5]
];

// Main case module
module case_bottom() {
    difference() {
        // Main body with rounded corners
        translate([corner_radius, corner_radius, 0])
            minkowski() {
                cube([case_length - 2*corner_radius, 
                      case_width - 2*corner_radius, 
                      case_height/2]);
                cylinder(r=corner_radius, h=case_height/2, $fn=30);
            }
        
        // Hollow interior - EXPANDED to use available space in larger case
        translate([wall_thickness + tolerance + center_offset_x, 
                   wall_thickness + tolerance + center_offset_y, 
                   wall_thickness])
            cube([case_length - 2*wall_thickness - 2*tolerance, 
                  case_width - 2*wall_thickness - 2*tolerance, 
                  case_height]);
        
        // Display window cutout - CENTERED
        translate([wall_thickness + tolerance + center_offset_x + screen_offset_x,
                   wall_thickness + tolerance + center_offset_y + screen_offset_y,
                   case_height - 1])
            cube([screen_length, screen_width, 2]);
        
        // USB ports (2x USB 2.0) - ADJUSTED for centered RPi
        for(i = [0:1]) {
            translate([-1,
                       wall_thickness + tolerance + center_offset_y + usb_port_y + i * usb_spacing,
                       wall_thickness + 2])
                cube([wall_thickness + center_offset_x + 2, usb_port_width, usb_port_height]);
        }
        
        // USB 3.0 ports (2x) - ADJUSTED for centered RPi
        for(i = [0:1]) {
            translate([-1,
                       wall_thickness + tolerance + center_offset_y + usb_port_y + 20 + i * usb_spacing,
                       wall_thickness + 2])
                cube([wall_thickness + center_offset_x + 2, usb_port_width, usb_port_height]);
        }
        
        // Ethernet port - ADJUSTED for centered RPi
        translate([-1,
                   wall_thickness + tolerance + center_offset_y + ethernet_y,
                   wall_thickness + 2])
            cube([wall_thickness + center_offset_x + 2, ethernet_width, ethernet_height]);
        
        // USB-C power port - ADJUSTED for centered RPi
        translate([wall_thickness + tolerance + center_offset_x + usbc_x,
                   -1,
                   wall_thickness + 2])
            cube([usbc_width, wall_thickness + center_offset_y + 2, usbc_height]);
        
        // HDMI ports - ADJUSTED for centered RPi
        for(x_pos = [hdmi0_x, hdmi1_x]) {
            translate([wall_thickness + tolerance + center_offset_x + x_pos,
                       -1,
                       wall_thickness + 2])
                cube([hdmi_width, wall_thickness + center_offset_y + 2, hdmi_height]);
        }
        
        // Audio jack - ADJUSTED for centered RPi
        translate([wall_thickness + tolerance + center_offset_x + audio_x,
                   -1,
                   wall_thickness + 7])
            rotate([-90, 0, 0])
                cylinder(d=audio_diameter, h=wall_thickness + center_offset_y + 2, $fn=30);
        
        // SD card slot - ADJUSTED for centered RPi
        translate([wall_thickness + tolerance + center_offset_x + sd_y,
                   case_width - wall_thickness - 1,
                   wall_thickness + 1])
            cube([sd_width, wall_thickness + sd_protrusion + 1, sd_height]);
        
        // Ventilation holes on back (opposite display side) - ADJUSTED for 12x8cm
        vent_rows = 6; // Adjusted for 8cm width
        vent_cols = 10; // Adjusted for 12cm length
        vent_hole_d = 3;
        vent_spacing_x = 10;
        vent_spacing_y = 8;
        vent_start_x = 15;
        vent_start_y = 10;
        
        for(row = [0:vent_rows-1]) {
            for(col = [0:vent_cols-1]) {
                translate([wall_thickness + tolerance + vent_start_x + col * vent_spacing_x,
                           case_width - wall_thickness - 1,
                           wall_thickness + vent_start_y + row * vent_spacing_y])
                    rotate([90, 0, 0])
                        cylinder(d=vent_hole_d, h=wall_thickness + 2, $fn=20);
            }
        }
        
        // Side ventilation slots - ADJUSTED for 8cm width
        side_vent_rows = 4; // Adjusted for 8cm width
        side_vent_height = 2;
        side_vent_width = 15;
        for(row = [0:side_vent_rows-1]) {
            translate([case_length - wall_thickness - 1,
                       wall_thickness + 10 + row * 15,
                       wall_thickness + 5 + row * 4])
                cube([wall_thickness + 2, side_vent_width, side_vent_height]);
        }
        
        // Additional ventilation on the bottom for better cooling - ADJUSTED for 12x8cm
        bottom_vent_rows = 4; // Adjusted for 8cm width
        bottom_vent_cols = 8;  // Adjusted for 12cm length
        for(row = [0:bottom_vent_rows-1]) {
            for(col = [0:bottom_vent_cols-1]) {
                translate([wall_thickness + 10 + col * 12,
                           wall_thickness + 10 + row * 15,
                           -0.5])
                    cylinder(d=4, h=wall_thickness + 1, $fn=20);
            }
        }
    }
    
    // Support posts for mounting holes - ADJUSTED for centered RPi
    for(pos = mounting_hole_positions) {
        translate([wall_thickness + tolerance + center_offset_x + pos[0],
                   wall_thickness + tolerance + center_offset_y + pos[1],
                   wall_thickness])
            difference() {
                cylinder(d=6, h=3, $fn=30);
                translate([0, 0, -0.5])
                    cylinder(d=mounting_hole_diameter, h=4, $fn=20);
            }
    }
    
    // Corner reinforcement posts for the larger case
    corner_post_positions = [
        [5, 5],
        [case_length - 5, 5],
        [5, case_width - 5],
        [case_length - 5, case_width - 5]
    ];
    
    for(pos = corner_post_positions) {
        translate([pos[0], pos[1], wall_thickness])
            cylinder(d=8, h=2, $fn=30);
    }
}

// Optional: Case lid/top (uncomment to generate)
/*
module case_top() {
    difference() {
        // Main lid body
        translate([corner_radius, corner_radius, 0])
            minkowski() {
                cube([case_length - 2*corner_radius, 
                      case_width - 2*corner_radius, 
                      wall_thickness/2]);
                cylinder(r=corner_radius, h=wall_thickness/2, $fn=30);
            }
        
        // Display window cutout in lid
        translate([wall_thickness + tolerance + center_offset_x + screen_offset_x - 2,
                   wall_thickness + tolerance + center_offset_y + screen_offset_y - 2,
                   -0.5])
            cube([screen_length + 4, screen_width + 4, wall_thickness + 1]);
    }
}
*/

// Render the case
case_bottom();

// Uncomment to render the top lid
// translate([0, case_width + 10, 0]) case_top();

echo("=== Modified Case Dimensions ===");
echo(str("Length: ", case_length, "mm (", case_length/10, "cm)"));
echo(str("Width: ", case_width, "mm (", case_width/10, "cm)"));
echo(str("Height: ", case_height, "mm (", case_height/10, "cm)"));
echo(str("Wall thickness: ", wall_thickness, "mm"));
echo("=== Print Settings Recommendation ===");
echo("Layer height: 0.2mm");
echo("Infill: 15-20%");
echo("Supports: No (designed support-free)");
echo("Print orientation: Bottom face down");