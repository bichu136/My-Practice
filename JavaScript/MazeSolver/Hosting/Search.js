function GreedySearch()
{
  if(current.x == goal.x && current.y == goal.y){
    console.log("DONE")
    noLoop()
  }
  if (open.length <=0){
    return
  }
  current = open.pop()
  if (grids[current.x][current.y].visited)
  {
    return
  }
  let currentDistance = abs(goal.x - current.x)+abs(goal.y-current.y)
  let upDistance   = -1
  let downDistance = -1
  let leftDistance = -1
  let rightDistance = -1
  let t = []
  let nextgrids = []
  if (grids[current.x][current.y].walls["up"] ==false){
    t = goto(current,"up")
    upDistance = abs(goal.x - t.y)+abs(goal.x-t.y)
    if(grids[t.x][t.y].visited == false)
      nextgrids.push({pos:t,d:upDistance})
  }
  if (grids[current.x][current.y].walls["down"] ==false){
    t = goto(current,"down")
    downDistance = abs(goal.x - t.x)+abs(goal.y-t.y)
    if(grids[t.x][t.y].visited == false)
      nextgrids.push({pos:t,d:downDistance})
  }
  if (grids[current.x][current.y].walls["left"] ==false){
    t = goto(current,"left")
    leftDistance = abs(goal.x - t.x)+abs(goal.y-t.y)
    if(grids[t.x][t.y].visited == false)
      nextgrids.push({pos:t,d:leftDistance})
  }
  if (grids[current.x][current.y].walls["right"] ==false){
    t = goto(current,"right")
    rightDistance = abs(goal[0] - t[0])+abs(goal[1]-t[1])
    if(grids[t.x][t.y].visited == false)
      nextgrids.push({pos:t,d:rightDistance})
  }
  nextgrids.sort(function(a,b){return b.d-a.d})// if  return <0 then a first return >0 then b first
  grids[current.x][current.y].visited = true
  while(nextgrids.length>1)
  {
    open.push(nextgrids.shift().pos)
  }
  open.push(current)
  if(nextgrids.length == 1)
    open.push(nextgrids.shift().pos)
}
function DFSSearch()
{

}
