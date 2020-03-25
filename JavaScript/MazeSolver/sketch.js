let i= 0
let j =0
function setup(){

  createCanvas(300,300)
  angleMode(DEGREES)
  directions = ["up","down","left","right"]
  width = 10;
  height= 10;
  grids = []
  current=[15,15];
  backtrack = []
  for (var i = 0; i < 30; i++) {
    grids.push([])
    for (var j = 0; j < 30; j++) {
      grids[i].push(new Grid(maze[i*30+j]))
    }
  }
  background(0)
}
function drawGrid(i,j){
  if(grids[i][j].visited){
    noStroke()
    fill(0,0,255)
    rect(i*height,j*width,height,width)
  }
  if(grids[i][j].walls["up"]){
    stroke(255,0,0)
    line (i*width,j*height,(i+1)*width,j*height)
  }
  if(grids[i][j].walls["right"]){
    stroke(255,0,0)
    line ((i+1)*width,(j+1)*height,(i+1)*width,j*height)
  }
  if(grids[i][j].walls["down"]){
    stroke(255,0,0)
    line ((i+1)*width,(j+1)*height,i*width,(j+1)*height)
  }
  if(grids[i][j].walls["left"]){
    stroke(255,0,0)
    line (i*width,(j+1)*height,i*width,j*height)
  }

}
function drawMaze(){
  for (var i = 0; i < 30; i++) {
     for (var j = 0; j < 30; j++) {
      drawGrid(i,j)
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

  //console.log(i,j,[grids[i][j].walls["up"],grids[i][j].walls["down"],grids[i][j].walls["left"],grids[i][j].walls["right"]])
  drawMaze()
  frameRate(60);
  // j+=1
  // if (j == 30){
  //   i+=1
  //   j = 0
  //   if(i == 29){
  //     noLoop()
  //   }
  // }
}
