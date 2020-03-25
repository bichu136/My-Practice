function setup(){

  createCanvas(300,300)
  angleMode(DEGREES)
  directions = ["up","down","left","right"]
  width = 10;
  height= 10;
  grids = []
  current=[15,15];
  backtrack = []
  writer = createWriter('maze.txt')

  for (var i = 0; i < 30; i++) {
    grids.push([])
    for (var j = 0; j < 30; j++) {
      grids[i].push(new Grid())
    }
  }
  grids[current[0]][current[1]].visited = true
  backtrack.push(current)
}
function drawMaze(){
  for (var i = 0; i < 30; i++) {
     for (var j = 0; j < 30; j++) {
      if(grids[i][j].visited){
        noStroke()
        fill(0,0,255)
        rect(i*height,j*width,height,width)
      }
      if(grids[i][j].walls["left"]){
        stroke(255,0,0)
        line (i*height,j*width,(i+1)*height,j*width)
      }
      if(grids[i][j].walls["right"]){
        stroke(255,0,0)
        line ((i+1)*height,(j+1)*width,(i+1)*height,j*width)
      }
      if(grids[i][j].walls["down"]){
        stroke(255,0,0)
        line ((i+1)*height,(j+1)*width,i*height,(j+1)*width)
      }
      if(grids[i][j].walls["up"]){
        stroke(255,0,0)
        line (i*height,(j+1)*width,i*height,j*width)
      }

    }
  }
}
function check_colision(checkgrid){
  if(checkgrid[0]<0 ||checkgrid[0]>=30){
    return true;
  }
  if(checkgrid[1]<0 ||checkgrid[1]>=30){
    return true;
  }
  return grids[checkgrid[0]][checkgrid[1]].visited;
}
function can_go(checkgrid){
  up = [checkgrid[0]-1,checkgrid[1]]
  down = [checkgrid[0]+1,checkgrid[1]]
  left = [checkgrid[0],checkgrid[1]-1]
  right = [checkgrid[0],checkgrid[1]+1]
  direction_can = []
  if (check_colision(up)==false)
  {
     direction_can.push("up")
  }
  if (check_colision(down)==false)
  {
     direction_can.push("down")
  }
  if (check_colision(left)==false)
  {
     direction_can.push("left")
  }
  if (check_colision(right)==false)
  {
     direction_can.push("right")
  }
  return direction_can
}
function goto(checkgrid,goto){
      next = [checkgrid[0],checkgrid[1]]
      switch(goto){
        case "up":
          next[0]-=1
          break;
        case "down":
          next[0]+=1
          break;
        case "left":
            next[1]-=1
          break;
        case "right":
          next[1]+=1
          break;
      }
  return next;
}
function reverseDir(dir){
  switch(dir){
    case "up":
      return "down";
      break;
    case "down":
      return "up"
      break;
    case "left":
        return "right"
      break;
    case "right":
      return "left"
      break;
  }
}
function draw(){
  background(0)
  drawMaze();
  current = backtrack.pop()
  directon_can = can_go(current)
  if (directon_can.length>0){
    backtrack.push(current)
    dir = random(direction_can)
    next = goto(current,dir)
    next_dir = reverseDir(dir)
    grids[next[0]][next[1]].walls[next_dir]= false
    grids[current[0]][current[1]].walls[dir] = false
    grids[next[0]][next[1]].visited = true
    backtrack.push(next)
  }
  frameRate(60);
  if (backtrack.length==0){
    noLoop()
    let writer = createWriter('maze.txt')
    writer.write([30,30])
    writer.write('\n')
    for(var i = 0;i<30;i++){
      for (var j = 0; j < 30; j++) {
        writer.write([grids[i][j].walls["left"],grids[i][j].walls["right"],grids[i][j].walls["up"],grids[i][j].walls["down"]])
        writer.write('\n')
      }
    }
    writer.close()
  }

}
