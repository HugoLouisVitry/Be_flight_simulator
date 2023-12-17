import math
# Attention il faut mettre l'altitude positif pour le dernier waypoint
# Liste des waypoints sous le format Nom,Distance,Cap (Site pour avoir ces information : www.iflightplanner.com/)
raw_waypoints = [("SFO",0,0,"flyover")]

if __name__ == "__main__":
    x = ''
    while True:
        print("Entrez un waypoint au format nom/distance/cap/type (en Nm et deg et flyby/over) (ou q pour quitter)")
        x = input()
        if x == 'q':
            break
        nom, dist, cap, type = x.split("/")
        raw_waypoints.append((nom,float(dist),float(cap),type))
    
    f = open("flightplan.csv","w")

    old_pos_x = 0
    old_pos_y = 0
    for i in range(0,len(raw_waypoints)-1):
        next_pos_x = old_pos_x + math.cos(math.radians(raw_waypoints[i+1][2])) * raw_waypoints[i+1][1] * 1852
        next_pos_y = old_pos_y + math.sin(math.radians(raw_waypoints[i+1][2])) * raw_waypoints[i+1][1] * 1852
        f.write(f"{raw_waypoints[i+1][0]},{int(next_pos_x)},{int(next_pos_y)},-1,{raw_waypoints[i+1][3]}\n")
        old_pos_x, old_pos_y = next_pos_x, next_pos_y
    
    f.close()