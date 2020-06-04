class Grid{
  name = "Grid"
  constructor(wallarray){
    this.walls = {"up": wallarray[0],
                  "down": wallarray[1],
                  "left":wallarray[2],
                  "right":wallarray[3]}
    this.visited = false;
  }

}
