let i= 0
let j =0

function setup(){

  createCanvas(500,500)
  angleMode(DEGREES)
  directions = ["up","down","left","right"]
  width = 10;
  height= 10;
  grids = []
  backtrack = []
  for (var i = 0; i < 30; i++) {
    grids.push([])
    for (var j = 0; j < 30; j++) {
      grids[i].push(new Grid(maze[i*30+j]))
    }
  }
  background(0)

}



function findingAlgo()
{
  GreedySearch()
  //AstarSearch()
}
function mouseClicked()
{
  if(finding){
    return
  }
   mX = parseInt(mouseX)
   mY = parseInt(mouseY)
   i = floor(mX/width)
   j = floor(mY/height)
   if (haveCurrent)
  {
    if (haveGoal)
    {
        haveCurrent = false
        haveGoal = false
    }
      goal = {x:i,y:j}
      haveGoal = true
      finding = true

  }
  else
  {
      current = {x:i,y:j}
      open.push(current)
      haveCurrent = true
  }
}

function drawGrid(i,j){

  if(grids[i][j].visited){
    noStroke()
    fill(0,0,255)
    rect(i*height,j*width,height,width)
  }
  a = {x:i,y:j}
  console.log("open:",open)
  if (open.includes(a))
  {
    noStroke()
    fill(0,125,0)
    rect(i*height,j*width,height,width)
  }
  if(grids[i][j].walls["up"]){
    stroke(255,150,125)
    line (i*width,j*height,(i+1)*width,j*height)
  }
  if(grids[i][j].walls["right"]){
    stroke(255,150,125)
    line ((i+1)*width,(j+1)*height,(i+1)*width,j*height)
  }
  if(grids[i][j].walls["down"]){
    stroke(255,150,125)
    line ((i+1)*width,(j+1)*height,i*width,(j+1)*height)
  }
  if(grids[i][j].walls["left"]){
    stroke(255,150,125)
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
  if(checkgrid.x<0 ||checkgrid.x>=30){
    return true;
  }
  if(checkgrid.y<0 ||checkgrid.y>=30){
    return true;
  }
  return grids[checkgrid.x][checkgrid.y].visited;
}
function can_go(checkgrid){
  up = {x:checkgrid.x-1,y:checkgrid.y}
  down = {x:checkgrid.x+1,y:checkgrid.y}
  left = {x:checkgrid.x,y:checkgrid.y-1}
  right = {x:checkgrid.x,y:checkgrid.y+1}
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
      next = {x:checkgrid.x,y:checkgrid.y}
      switch(goto){
        case "up":
          next.y-=1
          break;
        case "down":
          next.y+=1
          break;
        case "left":
            next.x-=1
          break;
        case "right":
          next.x+=1
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
function drawGoal()
{
  if (haveGoal)
  {
    noStroke()
    fill(255,255,0)
    ellipse((goal.x*width+(width/2)),(goal.y*height+(height/2)),width-4,height-4)
  }

}
function drawCurrent()
{
  if (haveCurrent)
  {
    noStroke()
    fill(255,0,0)
    ellipse((current.x*width+width/2),(current.y*height+(height/2)),width-4,height-4)
  }
}
function draw()
{
  fill(0)
  rect(0,0,300,300)
  drawMaze()
  drawGoal()
  drawCurrent()
  if (finding)
  {
    findingAlgo()
  }
  //if (haveGoal)
  //{
  //    ChangeCurrent()
  //}
  frameRate(60);

}
