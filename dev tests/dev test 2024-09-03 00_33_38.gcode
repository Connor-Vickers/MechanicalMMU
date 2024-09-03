;Dev test generated on 2024-09-03 00:33:38 by conno;
;
;
;
;from prusa default startup
M862.3 P "MINI" ; printer model check
G90 ; use absolute coordinates
M83 ; extruder relative mode
M204 T1250 ; set travel acceleration
G28 ; home all without mesh bed level
;end prusa default startup
;
G1 X119.00 F500;go to center
G1 Z43.60;engage with pusher
;start interpolate 1 revolutions of a XZ circle with 20 points centered at X119 Z65.6
G1 X125.80 Z44.68
G1 X131.93 Z47.80
G1 X136.80 Z52.67
G1 X139.92 Z58.80
G1 X141.00 Z65.60
G1 X139.92 Z72.40
G1 X136.80 Z78.53
G1 X131.93 Z83.40
G1 X125.80 Z86.52
G1 X119.00 Z87.60
G1 X112.20 Z86.52
G1 X106.07 Z83.40
G1 X101.20 Z78.53
G1 X98.08 Z72.40
G1 X97.00 Z65.60
G1 X98.08 Z58.80
G1 X101.20 Z52.67
G1 X106.07 Z47.80
G1 X112.20 Z44.68
G1 X119.00 Z43.60
;end interpolate 1 revolutions of a XZ circle with 20 points centered at X119 Z65.6
G1 Z30.60;go back down to clearance z
